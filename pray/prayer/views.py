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
	}
	return HttpResponse(template.render(context,request))

def prayerrequest(request):
	if request.method == 'GET':
		form = forms.PrayerRequest()
		context = {
			'form': form,
			'reqGet': True
		}
		template = loader.get_template('requestform.html')
	elif request.method == 'POST':
		form = forms.PrayerRequest(request.POST)
		if form.is_valid():
			prd = datetime.datetime.now()
			pt = form.cleaned_data['prayer_title']
			pd = form.cleaned_data['prayer_description']
			pc = '1'
			try:
				p = Prayer(prayer_title=pt,prayer_request_date=prd,prayer_description=pd,prayer_count=pc)
				p.save()
				return redirect('/success/')
			except Exception as e:
				template = loader.get_template('error.html')
				context = {
					'error' : str(e)
				}
		else:
			context = {		
				'error' : 'Form Validation Error',
			}
			template = loader.get_template('error.html')
	else:
		template = loader.get_template('error.html')
		context = {
			'error' : '501 Invalid Request Protocol',
		}
	return HttpResponse(template.render(context,request))

def prayer(request,prayer_id):
	#View an individual prayer to pray for it
	if request.method == 'GET':
		try:
			prayer = Prayer.objects.get(pk=prayer_id)
			template = loader.get_template('prayer.html')
			context = {
				'prayer' : prayer
			}
		except Exception as e:
			template = loader.get_template('error.html')
			context = {
				'error' : str(e)
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
			template = loader.get_template('pray.html')
			context = {
				'prayer_id' : prayer_id,
				'prayer_title' : prayer.prayer_title,
				'prayer_description' : prayer.prayer_description,
				'prayer_count' : prayer.prayer_count
			}
		except Exception:
			form = forms.Pray()
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

def prays(request, prayer_id, prayer_count):
	if request.method == 'POST':
		try:
			prayer = Prayer.objects.get(pk=prayer_id)
			#potentially reference other fields in prayer object to populate the rest of the form
			#increment prayer count
			count = prayer_count
			count = count + 1
			prayer.prayer_count = count
			prayer.save()
			return redirect('/success/')
		except Exception as e:
			context = {
				'error' : str(e)
			}
			template = loader.get_template('error.html')
	else:
		context = {
			'error' : '501 Invalid Request Protocol' #protocol error
		}
		template = loader.get_template('error.html')
	return HttpResponse(template.render(context,request))

def success(request):
	if request.method == 'GET':
		context = {}
		template = loader.get_template('success.html')
	else:
		context = {
			'error' : '501 Invalid Request Protocol'
		}
		template = loader.get_template('error.html')
	return HttpResponse(template.render(context,request))
