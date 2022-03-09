from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import Prayer
from .forms import forms
from django.template import loader
import datetime



def prayerrequests(request):
	#Load completed and current as separate lists
	user_current_prayer_list = Prayer.objects.all().order_by('prayer_request_date')
	template = loader.get_template('prayerrequests.html')
	context = {
		'prayer_list' : user_current_prayer_list,
		'answered_prayer_list': user_answered_prayer_list
	}
	return HttpResponse(template.render(context,request))

def prayerrequest(request):
	if request.method == 'GET':
		form = forms.PrayerRequest()
		return render(request, 'form.html',{'form': form})
	elif request.method == 'POST':
		form = forms.PrayerRequest(request.POST)
		if form.isvalid()
			prayer_request_date = datetime.now()
			prayer_title = request.POST['prayer_title']
			prayer_description = request.POST['prayer_description']
			vals = {
				'prayer_title' = prayer_title
				'prayer_request_date' : prayer_request_date,
				'prayer_description' : prayer_description,
				'prayer_count' : '1'
			}
			try:
				form = forms.Prayer(initial=vals)
				form.save()
				return redirect('/')
			except Exception:
				print(str(Exception)
				form = forms.PrayerRequest()
				template = loader.get_template('form.html')
				context = {
					'form': form,
					'error' : str(Exception)
				}
		else:
			form = forms.PrayerRequest()
			context = {		
				'errorF' : True,
				'form' : form
			}
			template = loader.get_template('form.html')
	else:
		template = loader.get_template('error.html')
		context = {
			'errorP' : True,
			'protocol' : str(request.method)
		}
	return HttpResponse(template.render(context,request))

def prayer(request,prayer_id):
	#View an individual prayer to pray for it
	if request.method == 'GET':
		try:
			prayer = Prayer.objects.get(pk=prayer_id)
			form = forms.PrayerView()
			template = loader.get_template('form.html')
			context = {
				'prayer' : prayer,
				'form' : form
			}
		except Exception:
			template = loader.get_template('error.html')
			context = {
				'error' : str(Exception)
			}
	else:
		context = {
			'error' : '501 Invalid Request Protocol'
		}
		template = loader.get_template('error.html')
	return HttpResponse(template.render(context,request))

def pray(request, prayer_id):
	if request.method == 'GET':
		try:
			prayer = Prayer.objects.get(pk=prayer_id)
			form = forms.Pray()
			template = loader.get_template('form.html')
			context = {
				'prayer_title' : prayer.prayer_title,
				'prayer_description' : prayer.prayer_description,
				'prayer_count' : prayer.prayer_count,
				'form' : form
			}
		except Exception:
			form = forms.Pray()
			context = {
				'error' : str(Exception)
			}
			template = loader.get_template('error.html')
	elif request.method == 'POST':
		try:
			prayer = Prayer.objects.get(pk=prayer_id)
			form = forms.Pray(request.POST)
			if form.isvalid():
				#potentially reference other fields in prayer object to populate the rest of the form
				#increment prayer count
				count = form.request.POST['prayer_count']
				count = count + 1
				form = forms.Prayer()
				post = form.save(commit=False)
				post.prayer_id = prayer.prayer_id
				post.prayer_title = prayer.prayer_title
				post.prayer_description = prayer.prayer_description
				post.prayer_request_date = prayer.prayer_request_date
				post.prayer_count = count
				post.save()
				return redirect('/')
			else:
				context = {
					'error' : '501 Prayer Input Form Error' #501 prayer input form error
				}
				template = loader.get_template('error.html')
		except Exception:
			context = {
				'error' : str(Exception)
			}
			template = loader.get_template('error.html')
	else:
		context = {
			'error' : '501 Invalid Request Protocol' #protocol error
		}
		template = loader.get_template('error.html')
	return HttpResponse(template.render(context,request))
