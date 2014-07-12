from django.contrib import admin
from solution.models import Solution, Compileinfo, Custominput, Runtimeinfo, Source_code, Sim

admin.site.register(Solution)
admin.site.register(Compileinfo)
admin.site.register(Custominput)
admin.site.register(Runtimeinfo)
admin.site.register(Source_code)
admin.site.register(Sim)
