from django.urls import path
from .views import StudentDashboardView, StudentCalendarView, StudentTeacherListView, StaffListView, user_detail, sign_up_for_event, user_events, cancel_event_signup, edit_profile, student_dashboard
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "student"

urlpatterns = [
    path("dashboard/", student_dashboard, name="student-dashboard"),
    path("calendar/", StudentCalendarView.as_view(), name="student-calendar"),
    path("stafflist/", StaffListView.as_view(), name="staff-list"),
    path('user/<int:id>/', user_detail, name='user_detail'),
    path('event/<int:event_id>/signup/', sign_up_for_event, name='event_sign_up'),
    path('my-events/', user_events, name='user_events'),
    path('event/<int:event_id>/cancel/', cancel_event_signup, name='cancel_event_signup'),
    path('profile/', edit_profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
