import threading

request_local = threading.local()

def get_current_employee():
    request = getattr(request_local, 'request', None)
    if all([
        request,
        request.user.is_authenticated,
        hasattr(request.user, 'employee')
    ]):
        return request.user.employee
    return None

class CurrentEmployeeMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_local.request = request
        return self.get_response(request)

    def process_exception(self, request, exception):
        request_local.request = None

    def process_template_response(self, request, response):
        request_local.request = None
        return response