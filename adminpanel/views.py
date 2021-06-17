from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import *

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@staff_required(login_url="/accounts/login/")
def panel(request):
	return render(request, 'panel.html')

@staff_required(login_url="/accounts/login/")
def logs(request):
	reputation = LogEntry.objects.select_related('category').all().order_by('-date').filter(category__logCategory__contains='reputation')
	arts = LogEntry.objects.select_related('category').all().order_by('-date').filter(category__logCategory__contains='arts')
	comments = LogEntry.objects.select_related('category').all().order_by('-date').filter(category__logCategory__contains='comments')
	context = {
	'reputation':reputation,
	'arts':arts,
	'comments':comments
	}
	return render(request, 'logs.html', context)

@staff_required(login_url="/accounts/login/")
def reports(request):
	reports = Report.objects.all().order_by('-date')
	context = {
	'reports':reports
	}
	return render(request, 'reports.html', context)

@staff_required(login_url="/accounts/login/")
def suggestions(request):
	return render(request, 'suggestions.html')
