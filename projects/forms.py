from cProfile import label
from tkinter.ttk import LabeledScale
from django import forms
from django.forms import ModelForm, widgets
from .models import project,Review

class ProjectsForm (ModelForm):
    class Meta:
        model = project
        fields = ['Title','Discription','Demo_link','Source_link','Tags','image']
        widgets = {'Tags':forms.CheckboxSelectMultiple(),}
    def __init__(self, *args, **kwargs):
        super(ProjectsForm, self ).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class ReviewForm (ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        labels = {
            'value': 'place your vote' ,
            'body' : 'Add comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self ).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})