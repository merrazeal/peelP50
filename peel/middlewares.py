from abc import ABC
from re import Match, search
from typing import Optional

from peel.exceptions import Forbidden, NotAllowed
from peel.request import Request
from peel.response import Response
from peel.router import Router


class BaseMiddleware(ABC):
    '''
    Базовый класс мидлваров - хуков для дополнительной обработки запросов,
    вьюх, ответов.
    '''

    def __init__(self) -> None:
        super().__init__()

    def process_request(self, request: Request) -> None:
        return

    def process_router(self, request: Request, router: Router) -> None:
        return

    def process_response(self, request: Request, response: Response) -> None:
        return


class CheckRequestMethodMiddleware(BaseMiddleware):
    '''
    Проверяется метод запрооса на допустимые в роутере.
    '''

    def process_router(self, request: Request, router: Router) -> None:
        request_method: str = request.method
        self.check_router_methods(router, request_method)

    @staticmethod
    def check_router_methods(router: Router, method: str) -> None:
        if method not in router.methods:
            raise NotAllowed


class BlockMozillaUserMiddleware(BaseMiddleware):
    '''
    Тестовый middleware, пользователям с веб браузером Mozilla Firefox
    доступ запрещен.
    '''

    def process_request(self, request: Request) -> None:
        web_browser: str = request.user_agent.lower()
        match: Optional[Match[str]] = search(r"mozilla", web_browser)
        if match:
            raise Forbidden
