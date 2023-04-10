from urllib.parse import parse_qs


class Request:
    '''
    Нужен для простой работы с HTTP запросами.
    '''

    def __init__(self, environ: dict) -> None:
        self.__environ = environ

    @property
    def GET(self) -> dict:
        '''
        Возвращаются параметры гет запроса в виде словаря.
        '''
        parsed_query = parse_qs(self.__environ.get('QUERY_STRING'))
        return parsed_query

    @property
    def method(self) -> str:
        return self.__environ.get('REQUEST_METHOD')  # type: ignore

    @property
    def user_agent(self) -> str:
        return self.__environ.get('HTTP_USER_AGENT')  # type: ignore

    @property
    def url(self) -> str:
        url = self.__environ.get('PATH_INFO')
        return self.get_correct_url(url)  # type: ignore

    @staticmethod
    def get_correct_url(url: str) -> str:
        if not url.endswith('/'):
            return url + '/'
        return url
