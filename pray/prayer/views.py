from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import Prayer, Users
from .forms import forms
from django.template import loader
import hashlib


#Create your views here.


#Login and Login Help Views
def login(request):
	if request.method == 'GET':
		form = forms.Login()
		template = loader.get_template('form.html')
		context = {
			'action' : 'login'
		}
	elif request.method == 'POST':
		form = forms.Login(request.POST)
		if form.isvalid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			if valid('username',username):
				if valid('password',password):
					form.save()
				else:
					template = loader.get_template('error.html')
					context = {
						'errorL' : 'Incorrect Password'
					}
			else:
				template = loader.get_template('error.html')
				context = {
					'errorL' : 'Username Not Located'
				}
			
		else:
			template = loader.get_template('error.html')
			context = {
				'errorF' : '501p Invalid Form'
			}
	else:
		template = loader.get_template('error.html')
		context = {
			'errorP' : 'Invalid Protocol'
		}
	return HttpResponse(template.render(context,request))

def valid(dbfield,dbval,**filters):
	try:
		if(dbfield=='username'):
			s = dbval[0:4]
			vals = Users.objects.filter(username__startswith=s).values()
			for val in vals:
				if(val['username']==dbval):
					return True
			return False
		elif(dbfield=='password'):
			s = hashlib.sha256(dbval).hexdigest()
			vals = Users.objects.filter(password__startswith=s[0:5]).values()
			for val in vals:
				if(val['password']==dbval):
					return True
			return False
		elif(dbfield=='answer'):
			s = filters['username']
			q = filters['question']
			vals = Users.objects.filter(username__startswith=s[0:5]).values()
			for val in vals:
				if(val['answer']==dbval):
					if(val['question']==q):
						return True
			return False
			
	except Exception:
		#log(Exception)
		print(Exception)
		return False

def help(request):
	if request.method == 'GET':
		form = forms.Help()
		template = loader.get_template('form.html')
		context = {
			'action' : 'help'
		}
	elif request.method == 'POST':
		form = forms.Help(request.POST)
		if form.isvalid():
			if(form.cleaned_data.get('username')):
				username = form.cleaned_data.get('username')
				if(valid('username',username):	
					question = form.cleaned_data.get('question')
					answer = form.cleaned_data.get('answer')
					if(valid('answer',answer,question,username)
						context = {
							'username' : username,
							'question' : question,
							'answer' : answer,
						}
					#redirect with context
				else:
					template = loader.get_template('error.html')
					context = {
						'errorH' : 'Username Not Located'
					}
			elif(form.cleaned_data.get('email')):
				email = form.cleaned_data.get('email')
			if valid('username',username):
				if valid('password',password):
					form.save()
				else:
					template = loader.get_template('error.html')
					context = {
						'errorL' : 'Incorrect Password'
					}
			else:
				template = loader.get_template('error.html')
				context = {
					'errorL' : 'Username Not Located'
				}
			
		else:
			template = loader.get_template('error.html')
			context = {
				'errorF' : '501p Invalid Form'
			}
	else:
		template = loader.get_template('error.html')
		context = {
			'errorP' : 'Invalid Protocol'
		}
	return HttpResponse(template.render(context,request))	
#def new():

#def emailhelp():

#def passwordhelp():




#Individual User Views

def prayerrequests(request):
	#Load completed and current as separate lists
	user_current_prayer_list = Prayer.objects.all().order_by('prayer_request_date')
	user_answered_prayer_list = Prayer.objects.all().order_by('-prayer_request_date')
	template = loader.get_template('viewprayerrequests.html')
	context = {
		'prayer_list' : user_current_prayer_list,
		'answered_prayer_list': user_answered_prayer_list
	}
	return HttpResponse(template.render(context,request))
	

def prayerrequest(request):
	if request.method == 'GET':
		form = forms.PrayerRequestForm()
		return render(request, 'prayerrequestform.html',{'form': form})
	elif request.method == 'POST':
		#prayer_request_date = request.POST['prayer_request_date']
		#prayer_answer_date = request.POST['prayer_answer_date']
		#prayer_description = request.POST['prayer_description']
		#prayer_recipients = request.POST['prayer_recipients']
		#prayer_recipients_email = request.POST['prayer_recipients_email']
		#prayer_categories = request.POST['prayer_categories']
		#prayer_answered = request.POST['prayer_answered']
		#prayer_updates = request.POST['prayer_updates']
		#prayer_image = request.POST['prayer_image']
		#prayer_answered_image = request.POST['prayer_answered_image']
		#validate each field in some way to account for SQL injection, etc.
		form = forms.PrayerRequestForm(request.POST)
		print(form.errors)
		if form.is_valid():
			#prayer = form.save(commit=False)
			#prayer.prayer_request_date = request.prayer_request_date
			#prayer.prayer_answer_date = request.prayer_answer_date
			#prayer.prayer_description = request.prayer_description
			#prayer.prayer_recipients = request.prayer_recipients
			#prayer.prayer_recipients_email = request.prayer_recipients_email
			#prayer.prayer_categories = request.prayer_categories
			#prayer.prayer_answered = request.prayer_answered
			#prayer.prayer_updates = request.prayer_updates
			#prayer.prayer_image = request.prayer_image
			#prayer.prayer_answered_image = request.prayer_answered_image
			form.save()
			return redirect('/success')
		else:
			context = {
				'error' : '501pri'
			}
			template = loader.get_template('error.html')
			return HttpResponse(template.render(context,request))

def prayeredit(request,prayer_id):
	if request.method == 'GET':
		prayer = Prayer.objects.get(prayer_id=prayer_id)
		#form = forms.PrayerRequestEditForm()
		#PrayerFormSet = formset_factory(Prayer.objects.get(prayer_id=prayer_id),fields=('prayer_description','prayer_recipients','prayer_recipients_email','prayer_updates'))
		PrayerFormSet = formset_factory(forms.PrayerRequestEditForm)	
		formset = PrayerFormSet(initial=[
			{
				'prayer_description':prayer.prayer_description,
				'prayer_recipients':prayer.prayer_recipients,
				'prayer_recipients_email':prayer.prayer_recipients_email,
				'prayer_updates':prayer.prayer_updates
			}	
		])
		context = {
			'form' : formset,
			'prayer' : prayer,
		}
		template = loader.get_template('editrequestform.html')
		print(prayer.prayer_description)
		return HttpResponse(template.render(context,request))
	elif request.method == 'POST':
		#prayer_request_date = request.POST['prayer_request_date']
		#prayer_answer_date = request.POST['prayer_answer_date']
		#prayer_description = request.POST['prayer_description']
		#prayer_recipients = request.POST['prayer_recipients']
		#prayer_recipients_email = request.POST['prayer_recipients_email']
		#prayer_categories = request.POST['prayer_categories']
		#prayer_answered = request.POST['prayer_answered']
		#prayer_updates = request.POST['prayer_updates']
		#prayer_image = request.POST['prayer_image']
		#prayer_answered_image = request.POST['prayer_answered_image']
		#validate each field in some way to account for SQL injection, etc.
		#form = forms.PrayerRequestEditForm(request.POST)
		#prayer = Prayer.objects.get(prayer_id=prayer_id)
		PrayerFormSet = formset_factory(Prayer,fields=('prayer_description','prayer_recipients','prayer_recipients_email','prayer_updates','prayer_id'),absolute_max=2,max_num=2,min_num=0)
		prayerFilter = Prayer.objects.filter(prayer_id=prayer_id)
		data = {
			'form-TOTAL-FORMS':'2',
			'form-INITIAL-FORMS':'0',
			'queryset':prayerFilter,
		}
		formset = PrayerFormSet(request.POST,request.FILES,data)
		print(str(formset))
		if formset.is_valid():
			#prayer = form.save(commit=False)
			#prayer_request_date = form.cleaned_data.get('prayer_request_date')
			#prayer_answer_date = form.cleaned_data.get('prayer_answer_date')
			#prayer_description = form.cleaned_data.get('prayer_description')
			#prayer_recipients = form.cleaned_data.get('prayer_recipients')
			#prayer_recipients_email = form.cleaned_data.get('prayer_recipients_email')
			#prayer_categories = form.cleaned_data.get('prayer_categories')
			#prayer_answered = form.cleaned_data.get('prayer_answered')
			#prayer_updates = form.cleaned_data.get('prayer_updates')
			#prayer_image = form.cleaned_data.get('prayer_image')
			#prayer_answered_image = form.cleaned_data.get('prayer_answered_image')
			formset.save()
			return redirect('/success')
		else:
			context = {
				'error' : 501,
				'formset' : formset
			}
			template = loader.get_template('error.html')
			return HttpResponse(template.render(context,request))

#def security(request, user_id):

#def success(request, user_id, prayer_id):

#Community and Pray Views
def home(request):
	template = loader.get_template('home.html')
	context = {}
	return HttpResponse(template.render(context,request))

def latest(request):
	#Retrieve top 20 latest prayers -- modify retrieval 
	latest_prayer_list = Prayer.objects.all()
	template = loader.get_template('prayerboard.html')
	context = {
		'prayer_list' : latest_prayer_list
	}
	return HttpResponse(template.render(context,request))

def mostprayedfor(request):
        #Retrieve top 20 most active prayers -- modify retrieval 
        most_prayer_list = Prayer.objects.all()
        template = loader.get_template('prayerboard.html')
        context = {
                'prayer_list' : most_prayer_list
        }
        return HttpResponse(template.render(context,request))

def recentlyanswered(request):
        #Retrieve top 20 latest answered prayers -- modify retrieval 
        recent_prayer_list = Prayer.objects.all()
        template = loader.get_template('prayerboard.html')
        context = {
                'prayer_list' : recent_prayer_list
        }
        return HttpResponse(template.render(context,request))

def prayer(request,prayer_id):
	#View an individual prayer to pray for it
	if request.method == 'GET':
		try:
			prayer = Prayer.objects.get(pk=prayer_id)
			print(prayer.prayer_description)
			form = forms.PrayerRequest
			template = loader.get_template('prayerrequest.html')
			context = {
				'prayer' : prayer,
				'form' : form
			}
			return HttpResponse(template.render(context,request))
		except Prayer.DoesNotExist:
			raise Http404("Prayer ID is not in database")
	else:
		context = {
			'error' : '501pv' #501 prayer view error
		}
		template = loader.get_template('error.html')
		return HttpResponse(template.render(context,request))

def pray(request, prayer_id, user_id):
	if request.method == 'GET':
		try:
			prayer = Prayer.objects.get(pk=prayer_id)
			form = forms.PrayView
			template = loader.get_template('pray.html')
			context = {
				'prayer_title' : prayer.prayer_title,
				'prayer_id' : prayer.prayer_id,
				'form' : form
			}
			return HttpResponse(template.render(context,request))
		except Prayer.DoesNotExist:
			raise Http404('Prayer ID is not in database')
	elif request.method == 'POST':
		try:
			prayer = Prayer.objects.get(pk=prayer_id)
			form = forms.Pray(request.POST)
			if form.isvalid():
				#potentially reference other fields in prayer object to populate the rest of the form
				form.save()
			else:
				context = {
					'error' : '501pif' #501 prayer input form error
				}
				template = loader.get_template('error.html')
				return HttpResponse(template.render(context,request))
		except Prayer.DoesNotExist:
			raise Http404("Prayer ID is not in database")
	else:
		context = {
			'error' : '501p' #501 pray error
		}
		template = loader.get_template('error.html')
		return HttpResponse(template.render(context,request))
