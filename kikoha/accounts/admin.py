from django.contrib import admin
from django.contrib.auth.models import Group

# Unregister Groups model which is not used
admin.site.unregister(Group)

# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import User

class UserAdmin(AuthUserAdmin):
    create_form_class = UserCreationForm
    update_form_class = UserChangeForm

admin.site.register(User, UserAdmin)
