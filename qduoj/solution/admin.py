from django.contrib import admin
from solution.models import Solution, Compileinfo, Custominput, Runtimeinfo

admin.site.register(Solution)
admin.site.register(Compileinfo)
admin.site.register(Custominput)
admin.site.register(Runtimeinfo)
