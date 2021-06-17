from PIL import Image
from io import BytesIO
from django.core.files import File

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db.models import Count, Sum

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from ponytoon.models import *
from ponytoon.forms import RegisterForm, LoginForm, UserEditForm

User = get_user_model()

@login_required(login_url="/accounts/login/")
def profile(request):
	u = request.user.id
	q = Upload.objects.filter(author_id=u, visible=1).count()
	reputation_art = Upload.objects.filter(author_id=u, visible=1).aggregate(Sum('reputation')).get("reputation__sum")
	reputation_comment = Comment.objects.filter(author_id=u, visible=1).aggregate(Sum('points')).get("points__sum")
	reputation = (reputation_art or 0) + (reputation_comment or 0)
	if Upload.objects.filter(author_id=u, visible=1):
		z = Upload.objects.filter(author_id=u, visible=1).values().order_by('-reputation')[0]
		images = Upload.objects.filter(author_id=u, visible=1).order_by('-upload_date')
		bestimgurl = list(z.values())[2].split('.')[0].split('_')[1]
		context = {'q':q, 'u':u, 'z':z, 'images':images, 'bestimgurl':bestimgurl, 'reputation':reputation}
	else:
		context = {'q':q, 'u':u, 'reputation':reputation}
	return render(request, 'profile.html', context)

def profileid(request, id):
	user = get_object_or_404(User, pk=id)
	q = Upload.objects.filter(author_id=user, visible=1).count()
	reputation_art = Upload.objects.filter(author_id=user, visible=1).aggregate(Sum('reputation')).get("reputation__sum")
	reputation_comment = Comment.objects.filter(author_id=user, visible=1).aggregate(Sum('points')).get("points__sum")
	reputation = (reputation_art or 0) + (reputation_comment or 0)
	if Upload.objects.filter(author_id=user, visible=1):
		z = Upload.objects.filter(author_id=user, visible=1).values().order_by('-reputation')[0]
		images = Upload.objects.filter(author_id=user, visible=1).order_by('-upload_date')
		link = list(z.values())[2].split('.')[0].split('_')[1]
		context = {'player': user, 'q':q, 'reputation':reputation, 'z':z, 'images':images, 'link':link, 'id': id}
	else:
		context = {'player': user, 'q':q, 'reputation':reputation, 'id': id}
	return render(request, 'profileid.html', context)

@login_required(login_url="/accounts/login/")
def profile_edit(request):
	id = request.user.id
	q = Upload.objects.filter(author_id=id, visible=1).count()
	reputation_art = Upload.objects.filter(author_id=id, visible=1).aggregate(Sum('reputation')).get("reputation__sum")
	reputation_comment = Comment.objects.filter(author_id=id, visible=1).aggregate(Sum('points')).get("points__sum")
	reputation = (reputation_art or 0) + (reputation_comment or 0)
	instance = get_object_or_404(User, id=id)
	form = UserEditForm(data=request.POST or None, files=request.FILES or None, instance=instance)
	if request.user.is_authenticated:
		if form.is_valid():
			form_instance = form.save(commit=False)
			im = Image.open(form_instance.avatar)
			if im.mode in ("RGBA", "P"):
				im = im.convert("RGB")
			im_io = BytesIO()
			im.save(im_io, 'JPEG', quality=100)
			ext = form_instance.avatar.name.split(".")[-1]
			form_instance.avatar = File(im_io, name="avatar_" + str(id) + "." + ext)
			form_instance.save()
			return redirect('accounts:profile')
	return render(request, 'edit_profile.html', {'form': form, 'reputation':reputation, 'q':q})

def signup(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		if request.method == 'POST':
			form = RegisterForm(request.POST)
			if form.is_valid():
				user = form.save()
				user.is_active = False
				user.save()
				current_site = get_current_site(request)
				subject = "[Ponyheck] Activate your ponyheck account."
				# message = "Welcome to Ponyheck. This is just testing mail transition so don't be mad if it will spam a little bit :)"
				message = render_to_string('registration/activate_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid':urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				from_email = settings.EMAIL_HOST_USER
				to_list = [user.email]

				send_mail(subject, message, from_email, to_list, fail_silently=False)

				# login(request, user)
				return redirect('accounts:signup_done')
#				return HttpResponse('Please confirm your email address to complete the registration')
		else:
			form = RegisterForm()
		context = {'form':form,}
		return render(request, 'registration/signup.html', context)

def signupDone(request):
	return render(request, 'registration/signup_done.html')

def authentication(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		if request.method == 'POST':
			form = LoginForm(data=request.POST)
			if form.is_valid():
				if form.get_user():
					user = form.get_user()
					login(request, user)
					if 'next' in request.POST:
						return redirect(request.POST.get('next'))
					else:
						return redirect('index')
				else:
					raise ValidationError("Account is not active, you need to activate your account before login.")
		else:
			form = LoginForm()

		context = {'form':form}
		return render(request, 'registration/login.html', context)

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		# return redirect('home')
	return render(request, 'registration/signup_activate.html', {'user':user})
	# 	return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
	# else:
	# 	return HttpResponse('Activation link is invalid!')
