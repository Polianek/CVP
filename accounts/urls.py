from django.urls import include, path, reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
from . import views

app_name = 'accounts'

urlpatterns=[
	path('signup/', views.signup, name='signup'),
	path('signup/done/', views.signupDone, name='signup_done'),
	path('login/', views.authentication, name='login'),
	path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
	path('activate/<uidb64>/<token>', views.activate, name='activate'),
	path('profile/', include([
		path('', views.profile , name='profile'),
		path('edit/', views.profile_edit, name='profile_edit'),
		path('userid=<id>', views.profileid, name='profileid'),
	])),
	path('password_change/', PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
	path('password_change/done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
	path('password_reset/', PasswordResetView.as_view(
										template_name='password_reset_form.html',
										email_template_name='registration/password_reset_html_email.html',
										success_url=reverse_lazy('accounts:password_reset_done')),
										name='password_reset'
										),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
										template_name='password_reset_confirm.html',
										success_url=reverse_lazy('accounts:password_reset_complete')),
										name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
	# path('users/', views.user_list, name='user_list'),
]
