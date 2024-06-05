from django.contrib import admin
from .models import Dialog, Message

class DialogAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2')
    search_fields = ('user1__username', 'user2__username')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('dialog', 'sender', 'text', 'timestamp')
    search_fields = ('dialog__user1__username', 'dialog__user2__username', 'sender__username', 'text')
    list_filter = ('timestamp',)

admin.site.register(Dialog, DialogAdmin)
admin.site.register(Message, MessageAdmin)
