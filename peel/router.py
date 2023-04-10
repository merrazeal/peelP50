from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Router:
    '''
    Класс для хранения урла, доступных методов контроллера,
    самого контроллера и его аргументов.
    '''

    url: str
    methods: list
    controller: Callable
    view_args: Optional[dict] = None
