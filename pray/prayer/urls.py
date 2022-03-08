from django.urls import path

from . import views

urlpatterns = [
	#Login Page and Troubleshooting
	path('', views.login, name = 'Login'),
	path('help/', views.help, name = 'Login Help'),
	path('password/', views.passwordhelp, name = 'Password Help'),
	path('new/', views.new, name = 'New User'),
	#Individual User View URLs
	path('<str:user>/prayers/', views.prayerrequests, name = 'View Prayer Requests'),
	path('<str:user>/new/', views.prayerrequest, name='Submit Prayer Request'),
	path('<str:user>/edit/<int:prayer_id>', views.prayeredit, name='Edit Prayer Request'),
	path('<str:user>/answered/<int:prayer_id>', views.answered, name='Prayer Answered'),
	path('<str:user>/security/', views.security, name = 'Security Settings'),
	path('success/', views.success, name="Prayer Received"),
	#Community URLs
	path('about/', views.about, name = 'About'),
	path('home/', views.home, name = 'Home'),
	path('latest/', views.latest, name = 'Latest Requests'),
	path('prayedfor/', views.mostprayedfor, name='Most Prayed For'),
	path('answered/', views.recentlyanswered, name='Answered Prayers'),
	path('<int:prayer_id>/', views.prayer, name='Prayer'),
	path('<int:prayer_id>/success/', views.praysuccess, name='Successful Prayer'),
	path('<str:user>/<int:prayer_id>/pray/', views.pray, name='Pray')
]
