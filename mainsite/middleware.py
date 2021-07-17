from django.conf import settings


class CorsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = settings.FRONTEND_DOMAIN
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        # response["Access-Control-Allow-Headers"] = "Accept, Accept-Encoding, Accept-Language, Access-Control-Request-Headers, Access-Control-Request-Method, Authorization, Connection, Content-Type, Host, Origin, Referer, Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site, User-Agent"
        response["Access-Control-Allow-Methods"] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
        return response
