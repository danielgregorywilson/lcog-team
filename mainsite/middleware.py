class CorsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # TODO: Allow this for develop mode, and switch on a setting
        
        # Needs to be commented out for production build
        # response["Access-Control-Allow-Origin"] = "http://localhost:8080"
        # response["Access-Control-Allow-Origin"] = "http://lcog-hr:8080"

        # Needs to be commented out for local development 
        response["Access-Control-Allow-Origin"] = "http://team.lcog.org.s3-website-us-west-2.amazonaws.com"
        
        # response["Access-Control-Allow-Origin"] = "*"
        
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        # response["Access-Control-Allow-Headers"] = "Accept, Accept-Encoding, Accept-Language, Access-Control-Request-Headers, Access-Control-Request-Method, Authorization, Connection, Content-Type, Host, Origin, Referer, Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site, User-Agent"
        response["Access-Control-Allow-Methods"] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
        return response
