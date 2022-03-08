from django.urls import path

from . import views

urlpatterns = [
	#Login Page and Troubleshooting
	path('', views.login, name = 'Login'),
	path('help/', views.help, name = 'Login Help'),
	path('emailhelp/', views.emailhelp, name = 'Email Help'),
	path('passwordhelp/', views.passwordhelp, name = 'Password Help'),
	path('new/', views.new, name = 'New User'),
	#Individual User View URLs
	path('<int:user_id>/prayers/', views.prayerrequests, name = 'View Prayer Requests'),
	path('<int:user_id>/new/', views.prayerrequest, name='Submit Prayer Request'),
	path('<int:user_id>/edit/<int:prayer_id>', views.prayeredit, name='Edit Prayer Request'),
	path('<int:user_id>/security/', views.security, name = 'Security Settings'),
	path('success/', views.success, name="Prayer Received"),
	#Community URLs
	path('about/', views.about, name = 'About'),
	path('home/', views.home, name = 'Home'),
	path('latest/', views.latest, name = 'Latest Requests'),
	path('prayedfor/', views.mostprayedfor, name='Most Prayed For'),
	path('answered/', views.recentlyanswered, name='Answered Prayers'),
	path('<int:prayer_id>/', views.prayer, name='Prayer'),
	path('<int:prayer_id>/success/', views.praysuccess, name='Successful Prayer'),
	path('<int:user_id>/<int:prayer_id>/pray/', views.pray, name='Pray')
]
