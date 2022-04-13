from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import profile,skill,message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','username','password1','password2']
        labels = {
            'first_name':'Name',
        }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self ).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    
class ProfileForm(ModelForm):
    class Meta:
        model = profile
        fields = ['name','username','location','email','short_intro','bio','profile_image','social_github','social_twitter','social_youtube','social_linkedin']
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self ).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class skillForm(ModelForm):
    class Meta:
        model = skill
        fields = ['name','description']
    
    def __init__(self, *args, **kwargs):
        super(skillForm, self ).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class messageForm(ModelForm):
    class Meta:
        model = message
        fields = ['sendername','email','subject','body']
    
    def __init__(self, *args, **kwargs):
        super(messageForm, self ).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})