from django.contrib import admin
from contest.models import Contest, Contest_problem, ContestPrivilege

admin.site.register(Contest)
admin.site.register(Contest_problem)
admin.site.register(ContestPrivilege)
