import functools
from re import Match, match
from typing import Callable, Iterable, List, Optional

from peel.exceptions import BaseEx, NotFound
from peel.middlewares import BaseMiddleware
from peel.request import Request
from peel.response import Response
from peel.router import Router


class PeelP50:
    '''
    WSGI приложение. Обрабатывается любым веб сервером, который
    работает по протоколу WSGI.
    '''

    def __init__(self, middlewares: List[BaseMiddleware]) -> None:
        '''
        При создании инстанса WSGI приложения контроллеры обяза-
        тельно должны быть рядом, чтобы сработали декораторы и в список
        добавились объекты Router.
        '''
        self.__routers: List[Router] = []
        self.__middlewares = middlewares

    def __call__(
        self,
        environ: dict,
        start_response: Callable
    ) -> Iterable[bytes]:
        '''
        На каждый HTTP запрос от клиента WSGI application сервер
        вызывает приложение(этот класс).
        1) Инициализируется новый объект запроса;
        2) У всех посредников вызывается метод process_request, чтобы
        гибко дополнительно обработать запрос;
        3) Выполняется маршрутизация, мы получаем объект роутера.
        4) У всех посредников вызывается метод process_router.
        5) Далее вызывается контроллер-свойство в объекте роутера,
        контроллер обязан возвращать объект Response;
        6) Вызывается process_response у всех посредников.
        7) Если все прошло без исключений, клиенту отправляются статус
        код и заголовки.
        8) Ну и наконец, из объекта Response извлекается свойство body,
        оно оборачивается в список и возвращается нашему Gunicorn серверу.
        '''
        request: Request = self._get_request(environ)
        try:
            self._activate_request_middlewares(request)
            router: Router = self._get_router(request.url)
            self._activate_router_middlewares(request, router)
            response: Response = self._get_response(request, router)
            self._activate_response_middlewares(request, response)
        except BaseEx as e:
            response: Response = Response(
                status_code=e.status_code,
                body=e.body
            )
        start_response(
            response.status_code,
            list(response.headers.items())
        )
        return [response.body]

    def add_router(
        self,
        url: str,
        methods: Optional[List['str']] = None
    ) -> Callable:
        '''
        Создается объект Router и через сеттер добавляется в список
        роутеров. Аргументы контроллера присваиваются при маршрутизации.
        '''
        allowed_methods: List['str'] = methods or ['GET']

        def wrapper(controller: Callable) -> Callable:
            router: Router = Router(url, allowed_methods, controller)
            self.routers = router  # type: ignore

            @functools.wraps(controller)
            def wrapped(*args, **kwargs) -> Response:
                return controller(*args, **kwargs)
            return wrapped
        return wrapper

    def _get_router(self, url) -> Router:
        '''
        Поиск роутера в списке роутеров по полю url, при нахождении -
        присваиваются аргументы и роутер возвращается.
        '''
        for router in self.routers:
            catched_router: Optional[Match[str]] = match(router.url, url)
            if catched_router:
                values: dict = catched_router.groupdict()
                self._add_values(router, values)
                return router
        raise NotFound

    @property
    def routers(self) -> List[Router]:
        return self.__routers

    @routers.setter
    def routers(self, value) -> None:
        if isinstance(value, Router):
            self.__routers.append(value)

    def _add_values(self, router: Router, values: dict) -> None:
        router.view_args = values

    def _get_request(self, environ: dict) -> Request:
        return Request(environ)

    def _get_response(
        self,
        request: Request,
        router: Router,
    ) -> Response:
        return router.controller(request, router.view_args)

    def _activate_request_middlewares(self, request: Request) -> None:
        '''
        Вызывается метод process_request у каждого мидлвар объекта.
        '''
        for m in self.middlewares:
            m.process_request(request)

    def _activate_router_middlewares(
        self,
        request: Request,
        router: Router
    ) -> None:
        '''
        Вызывается метод process_router у каждого мидлвар объекта.
        '''
        for m in self.middlewares:
            m.process_router(request, router)

    def _activate_response_middlewares(
        self,
        request: Request,
        response: Response
    ) -> None:
        '''
        Вызывается метод process_response у каждого мидлвар объекта.
        '''
        for m in self.middlewares:
            m.process_response(request, response)

    @property
    def middlewares(self) -> List[BaseMiddleware]:
        return self.__middlewares
