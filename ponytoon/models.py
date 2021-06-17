import os
from pathlib import Path
from django.db import models
from django.forms import ModelForm
from PIL import Image
from io import BytesIO
from django.core.files import File
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .validators import validate_file_size

User = get_user_model()

class Category(models.Model):
	name = models.CharField(max_length=25)

	def __str__(self):
		return self.name

class Tag(models.Model):
	id = models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	name = models.CharField(max_length=25)
	category = models.ForeignKey(Category, related_name='tags', on_delete=models.CASCADE)

	def __str__(self):
		# return self.name + ' (' + self.cetegories
		# category_str = ", ".join(self.cetegories.values_list('type', flat=True))
		return "{0} {1} ({2})".format(self.id, self.name, str(self.category))

	def tag_name(self):
		return "{0}".format(self.name)

def upload_to(instance, filename):
	file_extension = os.path.splitext(filename)[-1].lower()
	if file_extension.lower() in ('.png', '.jpg', '.jpeg', '.webp'):
		ctx = 'undertail.png'
	elif file_extension.lower() in ('.gif'):
		ctx = 'undertail.gif'
	else:
		raise ValidationError("No nie ma takiego rozszerzenia dodanego w kodzie, sora")
	return ctx

class Upload(models.Model):
	# user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	#, widget=forms.BrowseFile(attrs={'class':'UploadBtn'})
	title = models.TextField(max_length=1500, null=True)
	pic = models.ImageField(upload_to=upload_to, validators=[validate_file_size])
	upload_date=models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, related_name='uploads', blank=True)
	reputation = models.IntegerField(default=0)
	visible = models.BooleanField(default=True)
	# verbose_name="Choose a file"

	def __str__(self):
		if self.visible == False:
			visible = " - (Hidden)"
		else:
			visible = ""
		return self.pic.name + visible

	@property
	def pic_name(self):
		# return str(Path(self.pic.name)).split('.')[0].split('_')[1] # do the same thing what's here VVV
		return Path(self.pic.name).stem.split('_')[1]


# FileUpload form class.
class UploadForm(ModelForm):
	class Meta:
		model = Upload
		fields = ('pic','title', 'tags',)

class DetailViewEdit(ModelForm):
	class Meta:
		model = Upload
		fields = ('title', 'tags',)

class Comment(models.Model):
	contents = models.TextField(max_length=2000, null=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE)
	upload_date=models.DateTimeField(auto_now_add=True)
	# post = models.TextField(max_length=255, null=True)
	# post = models.ManyToManyField(Upload, related_name='comments')
	post = models.ForeignKey(Upload, related_name='comments', on_delete=models.CASCADE)
	points = models.IntegerField(default=0)
	visible = models.BooleanField(default=True)

	def __str__(self):
		if self.visible == False:
			visible = " - (Hidden)"
		else:
			visible = ""
		return "{0} | {1} {2}".format(self.post.pic.name, self.contents[:45], visible)

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ('contents',)

	# def clean_pic(self):
	# 	if self.cleaned_data['pic'] != True:
	# 		raise ValidationError(_('Picture isnt deleted'))
