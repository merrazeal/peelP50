from typing import List

from peel import middlewares
from peel.peel import PeelP50
from peel.request import Request
from peel.response import Response


MIDDLEWARE_CLASSES: List[middlewares.BaseMiddleware] = [
    middlewares.CheckRequestMethodMiddleware(),
]


app = PeelP50(middlewares=MIDDLEWARE_CLASSES)


@app.add_router(r'^/test/$')
@app.add_router(r'^/$')
def index(request: Request, values: dict) -> Response:
    return Response(
        {'method': request.method, 'user_agent': request.user_agent, }
    )


@app.add_router(r'^/multiply/(?P<value1>\d+)/(?P<value2>\d+)/$')
def multiply(request: Request, values: dict) -> Response:
    '''
    В адресной строке: /multiply/2/8/ -> 16.
    '''
    mul: int = int(values.get("value1")) * int(values.get("value2"))
    return Response({'произведение двух чисел': mul})


@app.add_router(r'^/not-allowed/$', methods=['123', '321'])
def not_allowed(request: Request, values: dict) -> Response:
    '''
    Проверка исключения method not allowed.
    '''
    return Response({})


@app.add_router(r'^/get-practice/$')
def get_practice(request: Request, values: dict) -> Response:
    '''
    Проверка гет параметров запроса.
    '''
    get: str = request.GET.get('get')[0]
    if not get:
        return Response({'error': 'используйте url/?get=value'})
    return Response({'get': get})
