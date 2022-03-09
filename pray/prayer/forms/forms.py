from django import forms
from ..models import Prayer

class Prayer(forms.ModelForm):
	class Meta:
		model = Prayer
		fields = '__all__'
	prayer_id = forms.CharField(required=True)
	prayer_request_date = forms.DateField(required=True)
	prayer_title = forms.CharField(required=True, max_length=100)
	prayer_description = forms.CharField(required=True, max_length=1000)
	prayer_count = forms.CharField(max_length=100,required=True)
class Pray(forms.Form):
	prayer_title = forms.CharField(max_length=100, required = True)
	prayer_description = forms.CharField(max_length = 1000, required = True, widget=forms.Textarea)
	prayer_count = forms.CharField(max_length=100, required = True)
class PrayerRequest(forms.Form):
	prayer_title = forms.CharField(max_length=100, required = True)
	prayer_description = forms.CharField(max_length = 1000, required = True, widget=forms.Textarea)
