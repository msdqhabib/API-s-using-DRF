from django.contrib import admin
from App.models import MyUser,CreateProject,Team,Tasks
from django.contrib.auth.admin import UserAdmin


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email","contactPerson","user_type",]
admin.site.register(MyUser,UserAdmin)


admin.site.register(CreateProject)
admin.site.register(Team)
admin.site.register(Tasks)


