from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from accounts.models import User
from calendarapp.models import Event, EventMember
from calendarapp.forms import EventForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from calendarapp.forms import UserProfileForm
from django.utils import timezone


class StudentDashboardView(LoginRequiredMixin, View):
    template_name = "studentapp/student.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
@login_required
def student_dashboard(request):
    # Получение данных о событиях, на которые записан студент
    user_events = EventMember.objects.filter(user=request.user).select_related('event')
    
    upcoming_events = [event_member.event for event_member in user_events.filter(event__start_time__gte=timezone.now()).order_by('event__start_time')]
    past_events = [event_member.event for event_member in user_events.filter(event__start_time__lt=timezone.now()).order_by('-event__start_time')]
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'studentapp/dashboard.html', context)

class StudentCalendarView(LoginRequiredMixin, View):
    template_name = "student/student_calendar.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class StudentTeacherListView(LoginRequiredMixin, View):
    template_name = "studentapp/teacher_list.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class StaffListView(ListView):
    model = User
    template_name = 'studentapp/teacher_list.html'
    context_object_name = 'staff_users'

    def get_queryset(self):
        return User.objects.filter(is_staff=True)

def user_detail(request, id):
    profile_user = get_object_or_404(User, id=id)
    events = Event.objects.filter(user=profile_user, start_time__gte=timezone.now()).order_by('start_time')
    event_list = []
    for event in events:
        event_list.append(
            {
                "id": event.id,
                "title": event.title,
                "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "description": event.description,
            }
        )
    context = {
        'profile_user': profile_user,
        'events': event_list,
    }
    return render(request, 'studentapp/user_detail.html', context)

@login_required
def sign_up_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    # Проверяем, не записан ли пользователь уже на это мероприятие
    if not EventMember.objects.filter(event=event, user=user).exists():
        EventMember.objects.create(event=event, user=user)
    
    return redirect('student:user_detail', id=user.id)

@login_required
def user_events(request):
    user = request.user
    events = EventMember.objects.filter(user=user).select_related('event')
    context = {
        'events': events,
    }
    return render(request, 'studentapp/user_events.html', context)

@login_required
def cancel_event_signup(request, event_id):
    event_member = get_object_or_404(EventMember, event_id=event_id, user=request.user)
    event_member.delete()
    return redirect(reverse('student:user_events'))

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('student:profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'studentapp/profile.html', {'form': form})
