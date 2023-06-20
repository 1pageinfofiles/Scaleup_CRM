from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class NewUserForm(UserCreationForm):
    fname = forms.CharField(required=True, label='First name')
    lname = forms.CharField(required=True, label='Last name')
    email = forms.EmailField(required=True, help_text=None)
    username = forms.CharField(help_text=None)
    password1 = forms.CharField(help_text=None, widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(help_text=None, widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ("fname", "lname", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']
        if commit:
            user.save()
        return user
class CompanyDetailsForm(forms.ModelForm):
    class Meta:
        model = CompanyDetails
        fields = ['catalogue_status', 'business_name', 'customer_name','mobile', 'alt_mobile', 'email','links','remarks']
        widgets = {
            'catalogue_status': forms.Select(attrs={'class': 'form-control'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'alt_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'links': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'})
        }
class CompanyDetailsRemarksPivoteForm(forms.ModelForm):
    class Meta:
        model = CompanyDetailsRemarkPivot
        fields = ['catalogue_status','remarks']
        widgets = {
            'catalogue_status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'})
        }