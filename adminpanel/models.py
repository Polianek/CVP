from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.contrib.contenttypes.fields import GenericForeignKey
from ponytoon.models import Upload, Comment

class LogCategory(models.Model):
    logCategory = models.CharField(max_length=30)

    def __str__(self):
        return self.logCategory

class LogAction(models.Model):
    logAction = models.CharField(max_length=45)

    def __str__(self):
        return self.logAction

class LogEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='logentrys_user')
    category = models.ForeignKey(LogCategory, related_name='logentrys_category', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=20)
    action = models.ForeignKey(LogAction, related_name='logentrys_action', on_delete=models.CASCADE)
    desc = models.TextField(max_length=800, blank=True, null=True)
    relate = models.ForeignKey(Upload, related_name='logentrys_upload', on_delete=models.CASCADE, null=True)
    relate_comment = models.ForeignKey(Comment, related_name='logentrys_comment', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{0} {1} by {2} | {3}".format(self.action, self.category, self.user.username, self.date.strftime("%d.%m.%Y at %H:%M"))

class ReportCategory(models.Model):
    reportCategory = models.CharField(max_length=40)

    def __str__(self):
        return self.reportCategory

class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='reports_user')
    category = models.ForeignKey(ReportCategory, related_name='reports_category', on_delete=models.CASCADE)
    contents = models.TextField(max_length=360)
    date = models.DateTimeField(auto_now_add=True)
    relate = models.ForeignKey(Upload, related_name='reports_upload', on_delete=models.CASCADE, null=True)
    relate_comment = models.ForeignKey(Comment, related_name='reports_comment', on_delete=models.CASCADE, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        if self.relate_comment is not None:
            return "{0}".format(str(self.relate_comment)[:40])
        else:
            return "{0}".format(str(self.relate)[:40])
            # return "{0} for {1} by {2} | {3}".format(self.relate, self.category, self.user, self.date.strftime("%d.%m.%Y at %H:%M"))

class ReportForm(ModelForm):
	class Meta:
		model = Report
		fields = ('category','contents',)

class Suggestions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='suggestions_user')
    contents = models.TextField(max_length=1500)
    date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return "{0} suggested {1}".format(self.contents, self.user)

class Votes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Upload, related_name='votes', blank=True, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='votes', blank=True, null=True, on_delete=models.CASCADE)
    value = models.BooleanField(default=True) #true=+ false=- rep
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.value:
            return "{0} upvoted {1}{2}".format(self.user, self.post, self.comment)
        else:
            return "{0} downvoted {1}{2}".format(self.user, self.post, self.comment)
