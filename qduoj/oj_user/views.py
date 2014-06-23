from django.shortcuts import render
from DjangoVerifyCode import Code

def sign_up(request):
    return render(request, "user/sign_up.html", {})

def sign_in(request):
    return render(request, "user/sign_in.html",{})

def get_code(request):
    code = Code(request)
    code.height = 46
    return code.display()

