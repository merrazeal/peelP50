from abc import ABC


class BaseEx(ABC, Exception):
    '''
    Базовый класс исключений сервера.
    '''

    status_code: int
    body: dict
    extra_headers: dict

    def __init__(self) -> None:
        super().__init__()


class NotFound(BaseEx):

    def __init__(self) -> None:
        self.status_code = 404
        self.body = {'ошибка': 'страница не найдена'}


class NotAllowed(BaseEx):

    def __init__(self) -> None:
        self.status_code = 405
        self.body = {'ошибка': 'метод не поддерживается'}


class Forbidden(BaseEx):

    def __init__(self) -> None:
        self.status_code = 403
        self.body = {'ошибка': 'отказано в доступе'}
