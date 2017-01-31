from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=45, required=True)
    last_name = forms.CharField(max_length=45, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

#Already have the bio and birthday fields defined in models.py, no need to add here
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birthday')

    def save(self, commit=True, on_register=False, user_obj=None):
        profile = super(ProfileForm, self).save(commit=False)
        if on_register and user_obj:
            profile.user = user_obj
        profile.bio = self.cleaned_data['bio']
        profile.birthday = self.cleaned_data['birthday']
        if commit:
            profile.save()
        return profile
