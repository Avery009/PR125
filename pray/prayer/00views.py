from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import Prayer
from .forms import forms
from django.template import loader
from django.contrib.auth import login, logout, authenticate
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
			user = authenticate(request, username=u, password=hashlib.sha256(p).hexdigest())
			if user is not None:
				login(request, user)
				#request.session['canpray'] = True
				request.session['prayUser'] = u
				return redirect('home/')
			else:
				template = loader.get_template('form.html')
				form = forms.Login()
				context = {
					'errorU' : True,
					'form' : form
				}
			
		else:
			form = forms.Login()
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
			if helpChoice[0] == 'u': #helpChoice should be either username or email based on a toggle or radio button group selection
				u = form.cleaned_data.get('username')
				user = User.objects.get(username=u).values()
				if(user is not None):	
					question = form.cleaned_data.get('question')
					answer = form.cleaned_data.get('answer')
					if(user['question']==question): #check to see if this is a valid dict reference and that there is only one user object returned in queryset
						if(user['answer']==answer):
							request.session['prayValidated'] = True #validate in DB upon success during testing
							request.session['prayUsername'] = username
							return redirect('/password') #this should go to the PWhelp page where session vars can be checked
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
						if(user['answer']==answer): #this may need to be a try..except depending on testing results
							request.session['prayValidated'] = True
							request.session['prayEmail'] = user['email']
							return redirect('/password')
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

def new(request):
	if request.method == 'GET':
		form = forms.NewUser()
		template = loader.get_template('form.html')
		context = {
			'action' : 'new',
			'form' : form
		}
	elif request.method == 'POST':
		form = forms.NewUser(request.POST)
		if form.isvalid():
			u = request.POST['username']
			p = request.POST['password']
			if len(u) > 8: #username needs to be at least 8 characters
				if len(p) > 14: #password needs to be at least 14 characters -- potential link to 1Password -- potential ask for starting with two characters to mitigate dictionary attacks
					user = Users.objects.get.filter(username=u).values()
					if user is None: #this would mean a value is not already located in the DB for username which should be a PK
						#createUser
					else:
						form = forms.NewUser()
						template = loader.get_template('form.html')
						context = {
							'form' : form,
							'errorU' : True, #recycling binary flag to cut down on data transmitted and improve latency
							'errorL' : False #adding additional user located flag to account for this type of error
						}
						
				else:
					form = forms.NewUser()
					template = loader.get_template('form.html')
					context = {
						'form' : form,
						'errorP' : False #error password indicates password is too short
					}
			else:
				form = forms.NewUser()
				template = loader.get_template('form.html')
				context = {
					'form' : form,
					'errorU' : False #False is still a value -- binary T or F with T indicating not located, F indicating too short
				}
		else:
			form = forms.NewUser()
			template = loader.get_template('form.html')
			context = {
				'form' : form,
				'errorF' : True #error form validation 
			}
	else:
		template = loader.get_template('error.html')
		context = {
			'errorP' : True, #error protocol
			'protocol' : str(request.method)
		}
	return HttpResponse(template.render(context,request))

def passwordhelp(request):
	#determine how to set the request method to check for GET or POST
	if request.method == 'GET':
		if request.session['prayEmail']: #indicates prior email validated choice
			val = {'email':str(request.session['prayEmail'])}
			form = forms.ChangePassword(initial=val) #validate that this will work with only one field update given necessity of other password fields 
			template = loader.get_template('form.html')
			context = {
				'form' : form,
			}
		elif request.session['prayUser']: #indicates prior username validate choice
			val = {'username':str(request.session['prayUser'])}
			form = forms.ChangePassword(initial=val) #validate that this will work with only one field update given necessity of other password fields 
			template = loader.get_template('form.html')
			context = {
				'form' : form,
			}
		else: #indicates going to this URL with no prior choice
			template = loader.get_template('error.html')
			context = {
				'errorP': False, #Recycling protocol error flag -- may need to modify
			}
	elif request.method == 'POST':
		if request.session['prayEmail']: #indicates prior email validated choice -- again, check if this needs a try catch in testing
			e = request.session['prayEmail']
			form = forms.ChangePassword(request.POST)
			try:
				newpassword = form.cleaned_data.get('newpassword')
				if(form.cleaned_data.get('oldpassword')==form.cleaned_data.get('newpassword')):
					u = User.objects.get(email__exact=e)
					u.set_password(newpassword)
					u.save()
					form = forms.Login()
					template = loader.get_template('form.html')
					context = {
						'form' : form,
						'new' : True #new user flag
					}
				else:
					form = forms.ChangePassword()
					template = loader.get_template('form.html')
					context = {
						'form' : form,
						'errorC' : True #change password error
					}
			except:
				template = loader.get_template('form.html')
				context = {
					'form' : form,
					'errorC' : False #change password failure
				}
		elif request.session['prayUser']: #indicates prior username validate choice
			e = request.session['prayUser']
                        form = forms.ChangePassword(request.POST)
                        try:
                                newpassword = form.cleaned_data.get('newpassword')
                                if(form.cleaned_data.get('oldpassword')==form.cleaned_data.get('newpassword')):
                                        u = User.objects.get(username__exact=e)
                                        u.set_password(newpassword)
                                        u.save()
                                        form = forms.Login()
                                        template = loader.get_template('form.html')
                                        context = {
                                                'form' : form,
                                                'new' : True #new user flag
                                        }
                                else:
                                        form = forms.ChangePassword()
                                        template = loader.get_template('form.html')
                                        context = {
                                                'form' : form,
                                                'errorC' : True #change password error
                                        }
                        except:
                                template = loader.get_template('form.html')
                                context = {
                                        'form' : form,
                                        'errorC' : False #change password failure
                                }
		else: #indicates going to this URL with no prior choice
			template = loader.get_template('error.html')
			context = {
				'errorP': False, #Recycling protocol error flag -- may need to modify
			}
	else:
		template = loader.get_template('error.html')
		context = {
			'errorP': True,
			'protocol': str(request.method)
		}
	return HttpResponse(template.render(context,request))
		



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
			try:
				form = forms.PrayerRequestForm(initial=vals)
				form.save()
				return redirect('/success')
			except Exception:
				print(str(Exception)
				form = forms.PrayerRequest()
				template = loader.get_template('form.html')
				context = {
					'form': form,
					'errorF' : True,
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
		#PrayerFormSet = formset_factory(Prayer.objects.get(prayer_id=prayer_id),fields=('prayer_description','prayer_recipients','prayer_recipients_email','prayer_updates'))
		vals = {
				'prayer_description':prayer.prayer_description,
				'prayer_recipients':prayer.prayer_recipients,
				'prayer_recipients_email':prayer.prayer_recipients_email,
		}
		form = forms.PrayerRequestEditForm(initial=vals)	
		context = {
			'action' : edit,
			'form' : form
		}
		template = loader.get_template('form.html')
	elif request.method == 'POST':
		try:
			form = forms.PrayerEdit(request.POST)
		#prayer_request_date = request.POST['prayer_request_date']
		#prayer_answer_date = request.POST['prayer_answer_date']
			prayer_description = request.POST['prayer_description']
			prayer_recipients = request.POST['prayer_recipients']
			prayer_recipients_email = request.POST['prayer_recipients_email']
		#prayer_categories = request.POST['prayer_categories']
		#prayer_answered = request.POST['prayer_answered']
		#prayer_updates = request.POST['prayer_updates']
		#prayer_image = request.POST['prayer_image']
		#prayer_answered_image = request.POST['prayer_answered_image']
		#validate each field in some way to account for SQL injection, etc.
		#form = forms.PrayerRequestEditForm(request.POST)
		#prayer = Prayer.objects.get(prayer_id=prayer_id)
			prayer = Prayer.objects.get(prayer_id__exact=prayer_id)
		#PrayerFormSet = formset_factory(Prayer,fields=('prayer_description','prayer_recipients','prayer_recipients_email','prayer_updates','prayer_id'),absolute_max=2,max_num=2,min_num=0)
		#prayerFilter = Prayer.objects.filter(prayer_id=prayer_id)
			if formset.is_valid():
				prayer_request_date = prayer.prayer_request_date
				prayer_answer_date = prayer.prayer_answer_date
			#prayer_description = form.cleaned_data.get('prayer_description')
			#prayer_recipients = form.cleaned_data.get('prayer_recipients')
			#prayer_recipients_email = form.cleaned_data.get('prayer_recipients_email')
			#prayer_categories = form.cleaned_data.get('prayer_categories')
			#prayer_answered = form.cleaned_data.get('prayer_answered')
				prayer_updates = prayer.prayer_updates
			#prayer_image = form.cleaned_data.get('prayer_image')
			#prayer_answered_image = form.cleaned_data.get('prayer_answered_image')
				form.save()
				return redirect('/success')
		except Exception:
			form = forms.Prayer
			context = {
				'errorE' : True,
				'error' : str(Exception),
				'form' : form
			}
			template = loader.get_template('form.html')
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
	latest_prayer_list = Prayer.objects.all().order_by('prayer_request_date')
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
			'errorP' : True
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
		except Exception:
			form = forms.Pray()
			context = {
				'errorE' : True,
				'error' : str(Exception),
				'form' : form
			}
			template = loader.get_template('form.html')
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
				post.prayer_count = count
				post.save()
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
