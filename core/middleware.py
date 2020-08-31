from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

HTTPS_PAGES = [
    '/signin/', '/signup/', '/profile/', '/logout/', '/admin/', '/order/',
]


class HttpRedirectMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.build_absolute_uri()
        if request.scheme == 'http' and any(page in request.path for page in HTTPS_PAGES):
           new_path = path.replace("http", "https")
           return redirect(new_path, permanent=True)
        elif request.scheme == 'https' and not any(page in request.path for page in HTTPS_PAGES):
            new_path = path.replace("https", "http")
            return redirect(new_path, permanent=True)
        return None
