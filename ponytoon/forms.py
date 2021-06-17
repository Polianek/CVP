from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from . import models
from accounts.models import User
from captcha.fields import CaptchaField


User = get_user_model()
#class UploadFileForm(forms.Form):
#    title = forms.CharField(max_length=50)
#    file = forms.FileField()

class RegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)
	captcha = CaptchaField()
	class Meta:
		model = User
		fields = ['email', 'username', 'password1', 'password2']

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user

class LoginForm(AuthenticationForm):
	captcha = CaptchaField()
	class Meta:
		model = User
		fields = ['email', 'password1']

class UploadFileForm(forms.ModelForm):
	class Meta:
		model = models.Upload
		fields = ['title', 'pic']

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['avatar', 'species', 'timezone']

class DetailViewEditForm(forms.ModelForm):
	class Meta:
		model = models.Upload
		fields = ['title', 'tags']

class CommentForm(forms.ModelForm):
	class Meta:
		model = models.Comment
		widgets = {
			'contents': forms.TextInput(attrs={'placeholder': 'Add comment..'}),
		}
		fields = ['contents']

	# def __init__(self, *args, **kwargs):


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

'''
class ImgUploadForm(forms.ModelForm):
	class Meta:
		model = ImgUpload
		fields = ('description', 'model_pic', )'''
#
# class CommentFileForm(forms.ModelForm):
# 	class Meta:
# 		model = models.Comment
# 		fields = ['com',]
