from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        public_paths = ["/", "/about/","/signup/"]

        if request.path_info in public_paths:
            return

        if request.path_info == "/login/":
            return

        info_dict = request.session.get("info")
        if info_dict:
            return
        
        return redirect('/login/')