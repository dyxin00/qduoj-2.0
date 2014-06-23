from random import choice

from django.shortcuts import render
from DjangoVerifyCode import Code

def sign_up(request):
    return render(request, "user/sign_up.html", {})

def sign_in(request):
    return render(request, "user/sign_in.html",{})

#http://www.oschina.net/p/django-verify-code/similar_projects?lang=26&sort=view
def get_code(request):
    code = Code(request)
    code.img_height = 46
    code.type = choice(['number', 'world'])
    return code.display()

