from django.urls import path

from . import views

urlpatterns = [
	path('', views.prayerrequests, name = 'Prayers'),
	path('prayerrequest/', views.prayerrequest, name = 'Prayer Request'),
	path('prayer/<int:prayer_id>/', views.prayer, name = 'Prayer'),
	path('pray/<int:prayer_id>', views.pray, name = 'Prayers'),
	path('pray/<int:prayer_id>/<int:prayer_count>', views.prays, name = "Pray"),
	path('success/', views.success, name = 'Success'),
]
