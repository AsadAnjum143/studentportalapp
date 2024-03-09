from django import forms
from . models import Notes, Homework, Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Install these thing --> pip install django-crispy-forms, pip install crispy-bootstrap4 - for crispy forms, in SETTINGS.PY --> CRISPY_TEMPLATE_PACK = "bootstrap4", CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4" and register 'crispy_forms', 'crispy_bootstrap4' this name in INSTALLED_APPS, and load this in template --> {% load crispy_forms_tags %} and in the form section inside form variable context {{ form|crispy }} add this filter.


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']
        
class DateInput(forms.DateInput):
    input_type = 'date'
        
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description','due','is_finished']
        
class SearchForm(forms.Form):
    text = forms.CharField(max_length=50, label="Enter your search")
    
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']
        
class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    
class ConversionLengthForm(forms.Form):
    CHOICES = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs = {'type':'number','placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(
        label = '', widget= forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label = '', widget= forms.Select(choices = CHOICES)
    )
    
class ConversionMassForm(forms.Form):
    CHOICES = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs= {'type':'number','placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(
        label = '', widget= forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label = '', widget= forms.Select(choices = CHOICES)
    )
    
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']