import http.client
import json
from typing import Optional


class Response:
    '''
    Формируется статус код, заголовки и тело ответа.
    '''

    def __init__(
        self,
        body: dict,
        status_code: int = 200,
        extra_headers: Optional[dict] = None,
    ) -> None:
        self.status_code: str = self._prepare_status_code(status_code)
        self.__body: dict = json.dumps(body).encode('utf-8')
        self.headers: dict = self._init_headers(self.body)
        if extra_headers:
            self.headers.update(extra_headers)

    @property
    def body(self) -> bytes:
        return self.__body

    @staticmethod
    def _prepare_status_code(status_code: int) -> str:
        '''
        Подготавливается статус код ответа.
        200 -> 200 OK
        '''
        return '%s %s' % (
            status_code, http.client.responses.get(status_code)
        )

    @staticmethod
    def _init_headers(body) -> dict:
        '''
        Инициализируются первоначальные заголовки, майм тип и длина тела.
        '''
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Content-Length': str(len(body))
        }
        return headers
