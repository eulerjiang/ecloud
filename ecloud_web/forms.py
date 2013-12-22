import re

from django.core.exceptions import ObjectDoesNotExist
from django import forms

from django.contrib.admin import widgets

from datetimewidget.widgets import DateTimeWidget
from datetime import datetime
from datetime import timedelta

from ecloud_web.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField( label='Username', max_length=30)
    email = forms.EmailField( label='Email' )
    password1 = forms.CharField( label='Password',widget=forms.PasswordInput() )
    password2 = forms.CharField( label='Password (Again)', widget=forms.PasswordInput() )

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        include = ('name','description')

class OrderForm(forms.Form):  
    project = forms.CharField(label='Project')
    templateName = forms.CharField(label='Template')

    currentDate = datetime.now()
    maxDate = currentDate + timedelta(days=14)
    
    startDateTimeOptions = {
'startDate' : currentDate.strftime('%Y/%m/%d %H:%M:%S'),
'endDate' : currentDate.strftime('%Y/%m/%d %H:%M:%S')
}

    expiredDateTimeOptions = {
'startDate' : currentDate.strftime('%Y/%m/%d %H:%M:%S'),
'endDate' : maxDate.strftime('%Y/%m/%d %H:%M:%S')
}

    startTime = forms.DateTimeField(label='Start Date', initial=datetime.now())
    #startTime = forms.DateTimeField(label='Start Date', widget=DateTimeWidget(attrs={'id':"startTime"}, usel10n = True, options= startDateTimeOptions) )
    expiredTime = forms.DateTimeField(label='Expired Date', widget=DateTimeWidget(attrs={'id':"expiredTime"}, usel10n = True, options= expiredDateTimeOptions) )
    #expiredTime = forms.DateTimeField(label='Expired Date', initial=maxDate)

    resourceType = forms.CharField(label='Resource')
           
    def setItems(self, projectChoices, imageChoices , resourceChoices):
        self.fields['templateName'] = forms.CharField( label='Template', widget = forms.Select(choices=imageChoices) )
        self.fields['resourceType'] = forms.CharField( label='Resource', widget = forms.Select(choices=resourceChoices) )
        self.fields['project'] = forms.CharField( label='Project', widget = forms.Select(choices=projectChoices) )
