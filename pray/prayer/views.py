from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import Prayer
from .forms import forms
from django.template import loader
from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import User
import hashlib,datetime


#Create your views here.


#Login and Login Help Views
def login(request):
	if request.method == 'GET':
		form = forms.Login()
		template = loader.get_template('form.html')
		context = {
			'action' : 'login',
			'form' : form
		}
	elif request.method == 'POST':
		form = forms.Login(request.POST)
		if form.isvalid():
			u = form.cleaned_data.get('username')
			p = form.cleaned_data.get('password')
			user = authenticate(request, username=u, password=hashlib.sha256(p).hexdigest()
			if user is not None:
				login(request, user)
				#request.session['canpray'] = True
				request.session['prayUser'] = u
				return redirect('home/')
			else:
				template = loader.get_template('form.html')
				form = forms.Login()
				context = {
					'errorL' : True,
					'form' : form
				}
			
		else:
			form = forms.Login()
			template = loader.get_template('form.html')
			context = {
				'errorF' : True
			}
	else:
		template = loader.get_template('error.html')
		context = {
			'errorP' : True,
			'protocol' : str(request.method)
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
			'action' : 'help',
			'form' : form
		}
	elif request.method == 'POST':
		form = forms.Help(request.POST)
		helpChoice = form.cleaned_data.get('helpChoice')
		if form.isvalid():
			if helpChoice[0] == 'u':
				u = form.cleaned_data.get('username')
				user = User.objects.get(username=u).values()
				if(user is not None):	
					question = form.cleaned_data.get('question')
					answer = form.cleaned_data.get('answer')
					if(user['question']==question):
						if(user['answer']==answer):
							request.session['prayValidated'] = True
							request.session['prayUsername'] = username
							#redirect
						else:
							form = forms.Help()
							template = loader.get_template('form.html')
							context = {
								'errorA' : True,
								'form' : form
							}
							request.session['prayUser']=user['username']
					else:
						form = forms.Help()
						template = loader.get_template('form.html')
						context = {
							'errorQ' : True,
							'form' : form
						}
						request.session['prayUser']=user['username']
				else:
					form = forms.Help()
					template = loader.get_template('form.html')
					context = {
						'errorU' : True,
						'form' : form
					}
			elif helpChoice[0]=='e':
				e = form.cleaned_data.get('email')
				user = User.objects.get(email=e).values()
				if(user is not None):	
					question = form.cleaned_data.get('question')
					answer = form.cleaned_data.get('answer')
					if(user['question']==question):
						if(user['answer']==answer):
							request.session['prayValidated'] = True
							request.session['prayEmail'] = user['email']
							#redirect
						else:
							form = forms.Help()
							template = loader.get_template('form.html')
							context = {
								'errorA' : True,
								'form' : form
							}
							request.session['prayEmail']=user['email']
					else:
						form = forms.Help()
						template = loader.get_template('form.html')
						context = {
							'errorQ' : True,
							'form' : form
						}
						request.session['prayEmail']=user['email']
				else:
					form = forms.Help()
					template = loader.get_template('form.html')
					context = {
						'errorU' : True,
						'form' : form
					}
			else:
				form = forms.Help()
				template = loader.get_template('form.html')
				context = {
					'errorC' : True,
					'form' : form
				}
		else:
			form = forms.Help()
			template = loader.get_template('form.html')
			context = {
				'errorF' : True,
				'form' : form
			}

	else:
		template = loader.get_template('error.html')
		context = {
			'errorP' : True,
			'protocol' : str(request.method)
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
	if not request.user.is_authenticated:
		form = forms.NewUser()
		template = loader.get_template('form.html')
		context = {
			'form' : form
		}
		return HttpResponse(template.render(context,request))
	elif request.method == 'GET':
		form = forms.PrayerRequest()
		return render(request, 'prayerrequestform.html',{'form': form})
	elif request.method == 'POST':
		form = forms.PrayerRequest(request.POST)
		if form.isvalid()
			prayer_request_date = datetime.now()
			prayer_answer_date = None
			prayer_description = request.POST['prayer_description']
			prayer_recipients = request.POST['prayer_recipients']
			#prayer_recipients_email = request.POST['prayer_recipients_email']
			#prayer_categories = request.POST['prayer_categories']
			prayer_answered = False
			prayer_updates = None
			#prayer_image = request.POST['prayer_image']
			#prayer_answered_image = request.POST['prayer_answered_image']
			#validate each field in some way to account for SQL injection, etc.
			vals = {
				'prayer_request_date' : prayer_request_date,
				'prayer_answer_date' : prayer_answer_date,
				'prayer_description' : prayer_description,
				'prayer_recipients' : prayer_recipients,
				'prayer_answered' : prayer_answered,
				'prayer_updates' : prayer_updates
			}
			form = forms.PrayerRequestForm(initial=vals)
			form.save()
			
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
	if not request.user.is_authenticated:
		form = forms.NewUser()
		template = loader.get_template('form.html')
		context = {
			'form' : form
		}
		return HttpResponse(template.render(context,request))
	elif request.method == 'GET':
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
	if not request.user.is_authenticated:
		form = NewUser
		template = loader.get_template('form.html')
		context = {
			'form' : form
		}
		return HttpResponse(template.render(context,request))
	#View an individual prayer to pray for it
	elif request.method == 'GET':
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

def pray(request, prayer_id):
	if not request.user.is_authenticated:
		form = NewUser
		template = loader.get_template('form.html')
		context = {
			'form' : form
		}
		return HttpResponse(template.render(context,request))
	elif request.method == 'GET':
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
