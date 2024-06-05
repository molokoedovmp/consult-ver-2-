from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Dialog, Message
from accounts.models import User
from django.db.models import Q

@login_required
def chat_list(request):
    query = request.GET.get('q')
    if query:
        dialogs = Dialog.objects.filter(
            Q(user1=request.user) & (
                Q(user2__email__icontains=query) |
                Q(user2__first_name__icontains=query) |
                Q(user2__last_name__icontains=query)
            ) |
            Q(user2=request.user) & (
                Q(user1__email__icontains=query) |
                Q(user1__first_name__icontains=query) |
                Q(user1__last_name__icontains=(query))
            )
        ).distinct()
    else:
        dialogs = Dialog.objects.filter(Q(user1=request.user) | Q(user2=request.user)).distinct()
    
    template_name = 'calendarapp/chat/chat_list.html' if request.user.is_staff else 'studentapp/chat/chat_list.html'
    
    return render(request, template_name, {'dialogs': dialogs, 'query': query})

@login_required
def chat(request, email):
    chat_user = get_object_or_404(User, email=email)
    
    # Попробуйте получить диалог, независимо от порядка пользователей
    dialog = Dialog.objects.filter(
        (Q(user1=request.user) & Q(user2=chat_user)) | (Q(user1=chat_user) & Q(user2=request.user))
    ).first()
    
    # Если диалог не найден, создайте его
    if not dialog:
        dialog = Dialog.objects.create(user1=request.user, user2=chat_user)

    if request.method == 'POST':
        message = Message.objects.create(
            dialog=dialog,
            sender=request.user,
            text=request.POST.get('message')
        )
        message.save()

    messages = dialog.messages.all()
    template_name = 'calendarapp/chat/chat.html' if request.user.is_staff else 'studentapp/chat/chat.html'
    return render(request, template_name, {'dialog': dialog, 'messages': messages, 'chat_user': chat_user})
