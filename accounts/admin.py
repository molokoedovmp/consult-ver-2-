from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Определяем новый класс администратора для нашей модели пользователя
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'department', 'is_staff', 'is_active', 'date_joined', 'last_updated', 'image', 'description']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'department', 'image', 'description')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'first_name', 'last_name', 'department', 'image', 'description')}
        ),
    )
    search_fields = ['email', 'first_name', 'last_name', 'department']
    ordering = ['email']

admin.site.register(User, CustomUserAdmin)
