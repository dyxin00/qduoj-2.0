from django.shortcuts import render
from DjangoVerifyCode import Code

def sign_up(request):
    return render(request, "user/sign_up.html", {})

def sign_in(request):
    return render(request, "user/sign_in.html",{})

#http://www.oschina.net/p/django-verify-code
def get_code(request):
    code = Code(request)
    code.img_height = 46
    font_size = 35
    return code.display()

