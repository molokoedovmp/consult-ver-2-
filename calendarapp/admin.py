from django.contrib import admin
from calendarapp.models import Event, EventMember

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'start_time', 'end_time']
    search_fields = ['title', 'user__email']
    list_filter = ['start_time', 'end_time']

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff

@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    list_display = ['event', 'user']
    search_fields = ['event__title', 'user__email']
    list_filter = ['event']

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff
