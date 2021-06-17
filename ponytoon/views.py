from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files import File

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage as storage
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.db.models import Q, F, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, DeleteView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin

from django.urls import reverse, reverse_lazy
from adminpanel.models import LogEntry, LogCategory, LogAction, Report, ReportForm, Votes
from ponytoon.models import *
# from adminpanel.forms import ReportForm
from ponytoon.forms import *
import json
from el_pagination.decorators import page_template
from ipware import get_client_ip

def log_addition(request, category, action, desc=None, user=None, relate=None, relate_comment=None):
	# id = request.user.id
	# ip = '127.0.0.1'
	# cat = LogCategory.objects.get(logCategory=data[category])
	ip, is_routable = get_client_ip(request)
	# if ip is None:
	# 	pass
	# else:
	# 	if is_routable:
	# 		i

	category, created = LogCategory.objects.get_or_create(logCategory=category)
	action, created = LogAction.objects.get_or_create(logAction=action)
	l = LogEntry(user=user, category=category, ip=ip, action=action, desc=desc, relate=relate, relate_comment=relate_comment)
	l.save()
	# l = LogEntry.objects.get_or_create(category__logCategory__contains=category, ip=ip, action__logAction__contains=action, desc=desc)
	# l.save()

def index(request):
	time_threshold = timezone.now() - timedelta(days=7)
	images = Upload.objects.all().order_by('-upload_date').filter(visible=1, upload_date__gte=time_threshold) #gte stands for: greater than (or) equal (to), you may use lt/lte too
	images = images.order_by('-reputation')[:1]
	context = {
		'images': images
	}
	return render(request, 'ponytoon/index.html', context)

def gallery(request, template='ponytoon/gallery.html', page_template='ponytoon/pages/gallery_page.html'):
	images = Upload.objects.all().order_by('-upload_date').filter(visible=1)

	query = request.GET.get("q")
	if query:
		with open('ponytoon/search.json', 'r') as json_file:
			data = json.load(json_file)

		query = query.lower()
		for (k, v) in data.items():
			if k in query:
				query = query.replace(k, v)
		query = query.replace(' ', '')
		complex_query = Q()
		for name in query.split(','):
			if name:
				complex_query = Q(tags__name__icontains=name)
				images = images.filter(complex_query).distinct()

	page = request.GET.get('page')
	paginator = Paginator(images, 5)
	try:
		pass
		# images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		images = paginator.page(paginator.num_pages)
	# if you want to sort by OR tags (not AND), uncomment the 2 lines below
	#			complex_query |= Q(tags__name__icontains=name)
	#	images = images.filter(complex_query).distinct()

		# query = query.capitalize()
		# images = images.filter(tags__name__in=query.split(',')).distinct()
	context = {
		'images': images, 'page_template': page_template
	}
	if request.is_ajax():
		template = page_template
	return render(request, template, context)

def categories(request):
	return render(request, 'ponytoon/categories.html')

@login_required(login_url="/accounts/login/")
def upload(request):
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			im = Image.open(instance.pic)
			if im.mode in ("RGBA", "P"):
				im = im.convert("RGB")
			im_io = BytesIO()
			im.convert("P", palette=Image.ADAPTIVE) #zmiana na 8-bitową paletę kolorów
			im.save(im_io, 'JPEG', quality=85, optimize=True)
			im_io.seek(0)
			instance.pic = File(im_io, name=instance.pic.name)
			instance.save()
			form.save_m2m()
			log_addition(request=request, category='arts', action='add', user=request.user, relate=instance)
			return redirect('gallery')
	else:
		form = UploadForm()
	return render(request, 'ponytoon/upload.html', { 'form':form })


class CommentCreateView(CreateView):
	form_class = CommentForm
	model = Upload
	template_name = 'ponytoon/categories.html'
	def get_success_url(self):
		arts = self.kwargs['arts']
		return reverse_lazy('arts_detail', kwargs={'arts':arts})

	@method_decorator(login_required)
	def dispatch(self, request, queryset=None, *args, **kwargs):
		if queryset is None:
			queryset = self.get_queryset()
		link_kwarg = self.kwargs.get('arts')
		link = "undertail_{0}.gif".format(link_kwarg)
		if queryset.filter(pic="undertail_{0}.png".format(link_kwarg)):
			link = "undertail_{0}.png".format(link_kwarg)
		queryset = queryset.filter(pic=link)
		self.upload = get_object_or_404(queryset)
		log_addition(request=request, category='comment', action='add', user=request.user, relate=self.upload)
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.post = self.upload
		form.instance.author_id = self.request.user.id
		return super().form_valid(form)

class ArtsDetailView(DetailView):
	model = Upload
	template_name = 'ponytoon/detail.html'
	paginate_by = 1

	def get_context_data(self, **kwargs):
	# zwraca to samo co {{ upload.tags.all.category }} przez get_object
		# context = super(ArtsDetailView, self).get_context_data(**kwargs)
		# context['tags'] = Category.objects.filter(tags__uploads=self.object).distinct()
		# return context
		link_kwarg = self.kwargs.get('arts')
		link = "undertail_{0}.gif".format(link_kwarg)
		if Upload.objects.all().filter(pic="undertail_{0}.png".format(link_kwarg)).exists():
			link = "undertail_{0}.png".format(link_kwarg)
		comments = Comment.objects.select_related('post').all().order_by('-upload_date').filter(visible=True, post__pic__exact=link)
		context = super().get_context_data(form=CommentForm(), comments=comments, **kwargs)
		page = self.request.GET.get('page')

		try:
			pass
			# comments = paginator.page(page)
		except PageNotAnInteger:
			comments = paginator.page(1)
		except EmptyPage:
			comments = paginator.page(paginator.num_pages)
		context['comments'] = comments

		# comment = get_object_or_404(Comment, post=instance, pk=self.kwargs.get('number'))

		# if self.request.is_ajax():
		# 	self.template_name = 'ponytoon/pages/comment_page.html'
		return context

	def get_object(self, queryset=None):

	#Return the object the view is displaying.
	#Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
	#Subclasses can override this to return any object.

	# Use a custom queryset if provided; this is required for subclasses
	# like DateDetailView
		if queryset is None:
			queryset = self.get_queryset()
		link_kwarg = self.kwargs.get('arts')
		link = "undertail_{0}.gif".format(link_kwarg)
		if queryset.filter(pic="undertail_{0}.png".format(link_kwarg)).exists():
			link = "undertail_{0}.png".format(link_kwarg)

		if self.request.user.id == 1:
			queryset = queryset.filter(pic=link)
			obj = get_object_or_404(queryset)
		else:
			queryset = queryset.filter(pic=link, visible=1)
			obj = get_object_or_404(queryset)
		#from pudb import set_trace; set_trace()
		return obj

class ArtsDeleteView(DeleteView):
	model = Upload
	template_name = 'ponytoon/detail_delete.html'

	def get_object(self, queryset=None):
		if self.request.user.is_staff:
			if queryset is None:
				queryset = self.get_queryset()
			link = self.kwargs.get('arts')
			link = "undertail_{0}.png".format(link)
			queryset = queryset.filter(pic=link)
			obj = get_object_or_404(queryset)
			log_addition(request=request, category='arts', action='delete', user=self.request.user, relate=obj)
			return obj
		else:
			return ""

	def get_success_url(self):
		return reverse('gallery')

@login_required(login_url="/accounts/login/")
def file_toggle_visibility(request, arts, **kwarg):
	# arts = "undertail_{0}.png".format(arts)
	arts = f'undertail_{arts}.png'
	file = get_object_or_404(Upload, pic=arts)
	if request.user.id == file.author.id:
		file.visible = False
		file.save()
		log_addition(request=request, category='arts', action='vanish', user=request.user, relate=file)
	return redirect('gallery')

@login_required(login_url="/accounts/login/")
def reppos(request, arts):
	arts = f'undertail_{arts}.png'
	file = get_object_or_404(Upload, pic=arts)
	vote = Votes.objects.all().filter(user=request.user, post=file, comment=None)
	check_vote, created = vote.get_or_create(user=request.user, post=file, comment=None)
	if created:
		check_vote.value = True
		file.reputation = F('reputation') + 1
		file.author.reputation = F('reputation') + 1
		check_vote.save()
		file.author.save()
		file.save()
		log_addition(request=request, category='reputation', action='grant', user=request.user, relate=file)
	else:
		if check_vote.value == False:
			check_vote.value = True
			file.reputation = F('reputation') + 2
			file.author.reputation = F('reputation') + 2
			check_vote.save()
			file.author.save()
			file.save()
			log_addition(request=request, category='reputation', action='changed_to_grant', user=request.user, relate=file)
		else:
			file.reputation = F('reputation') - 1
			file.author.reputation = F('reputation') - 1
			check_vote.delete()
			file.author.save()
			file.save()
			log_addition(request=request, category='reputation', action='remove', user=request.user, relate=file)
	file.refresh_from_db()
	repp = file.reputation
	return JsonResponse({'result':'success', 'repp':repp})

@login_required(login_url="/accounts/login/")
def repneg(request, arts):
	arts = f'undertail_{arts}.png'
	file = get_object_or_404(Upload, pic=arts)
	check_vote, created = Votes.objects.get_or_create(user=request.user, post=file, comment=None)
	if created:
		check_vote.value = False
		file.reputation = F('reputation') - 1
		file.author.reputation = F('reputation') - 1
		check_vote.save()
		file.author.save()
		file.save()
		log_addition(request=request, category='reputation', action='take', user=request.user, relate=file)
	else:
		if check_vote.value == True:
			check_vote.value = False
			file.reputation = F('reputation') - 2
			file.author.reputation = F('reputation') - 2
			check_vote.save()
			file.author.save()
			file.save()
			log_addition(request=request, category='reputation', action='changed_to_take', user=request.user, relate=file)
		else:
			file.reputation = F('reputation') + 1
			file.author.reputation = F('reputation') + 1
			check_vote.delete()
			file.author.save()
			file.save()
			log_addition(request=request, category='reputation', action='remove', user=request.user, relate=file)
	file.refresh_from_db()
	repp = file.reputation
	return JsonResponse({'result':'success', 'repp':repp})

@login_required(login_url="/accounts/login/")
def artsdetailview_edit(request, arts):
	art = f'undertail_{arts}.png'
	instance = get_object_or_404(Upload, pic=art)
	form = DetailViewEditForm(request.POST or None, instance=instance)
	if instance.author.id == request.user.id:
		if form.is_valid():
			form_instance = form.save(commit=False)
			form_instance.tags.set(form.cleaned_data['tags'])
			form_instance.save()
			form.save_m2m()
			log_addition(request=request, category='arts', action='update', user=request.user, relate=instance)
			return redirect('arts_detail', arts=arts)
	context = {'form':form, 'arts':arts, 'upload':instance}
	return render(request, 'ponytoon/detail_edit.html', context)

@login_required(login_url="/accounts/login/")
def report(request, arts, number=None):
	art = f'undertail_{arts}.png'
	instance = get_object_or_404(Upload, pic=art)
	if number:
		comment = get_object_or_404(Comment, post=instance, pk=number)
	form = ReportForm(request.POST or None)
	url = request.path

	if request.user.is_authenticated:
		if form.is_valid():
			form_instance = form.save(commit=False)
			form_instance.user = request.user
			form_instance.relate = instance
			form_instance.relate_comment = comment
			form_instance.save()
			if number:
				log_addition(request=request, category='report', action='comment', user=request.user, relate=instance, relate_comment=comment, desc=form.cleaned_data['contents'])
			else:
				log_addition(request=request, category='report', action='art', user=request.user, relate=instance, desc=form.cleaned_data['contents'])
			return redirect('arts_detail', arts=arts)
	context = {'form':form, 'arts':arts, 'url':number}
	if number:
		return render(request, 'ponytoon/detail_report_comment.html', context)
	else:
		return render(request, 'ponytoon/detail_report.html', context)

@login_required(login_url="/accounts/login/")
def comment_reputation(request, arts, number):
	arts = f'undertail_{arts}.png'
	instance = get_object_or_404(Upload, pic=arts)
	comment = get_object_or_404(Comment, post=instance, pk=number)
	check_vote, created = Votes.objects.get_or_create(user=request.user, post=instance, comment=comment)
	if created:
		comment.points = F('points') + 1
		comment.author.reputation = F('reputation') + 1
		comment.author.save()
		comment.save()
		log_addition(request=request, category='reputation', action='add', user=request.user, relate=instance, relate_comment=comment)
	else:
		comment.points = F('points') - 1
		comment.author.reputation = F('reputation') - 1
		check_vote.delete()
		comment.author.save()
		comment.save()
		log_addition(request=request, category='reputation', action='remove', user=request.user, relate=instance, relate_comment=comment)

	# comment_reputation = comment.points
	# comment_pk = request.POST.get('comment_pk')
	comment.refresh_from_db()
	# import pdb; pdb.set_trace()
	return JsonResponse({'result':'success', 'comment_reputation':comment.points, 'number':number})
# @login_required(login_url="/accounts/login/")
# def report_comment(request, arts):
# 	art = f'undertail_{arts}.png'
# 	instance = get_object_or_404(Upload, pic=art)
# 	comment = get_object_or_404(Comment, post=instance)
# 	form = ReportForm(request.POST or None)
# 	import pdb; pdb.set_trace()
# 	if request.user.is_authenticated:
# 		if form.is_valid():
# 			form_instance = form.save(commit=False)
# 			form_instance.user = request.user
# 			form_instance.relate = instance
# 			form_instance.relate_comment = comment
# 			form_instance.save()
# 			import pdb; pdb.set_trace()
# 			log_addition(category='report', action='art', user=request.user, relate=instance, desc=form.cleaned_data['contents'])
# 			return redirect('arts_detail', arts=arts)
# 	context = {'form':form, 'arts':arts}
# 	return render(request, 'ponytoon/detail_report.html', context)


def premium(request):
	return render(request, 'premium')
def terms(request):
	return render(request, 'ponytoon/html_detail/info/terms.html')
def privacy(request):
	return render(request, 'ponytoon/html_detail/info/privacy.html')
def faq(request):
	return render(request, 'ponytoon/html_detail/info/faq.html')
def contact(request):
	return render(request, 'ponytoon/html_detail/info/contact.html')
