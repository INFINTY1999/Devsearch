from django.shortcuts import redirect, render
from django.forms import ModelForm 
from django.http import HttpResponse 
from .models import project
from .forms import ProjectsForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utility import searchproject,paginateprojects
from django.contrib import messages

def projects(request):
    search_project , projec = searchproject(request)
    custom_range , projec = paginateprojects(request,projec,6)

    cotext =  {'custom_range':custom_range,'projects':projec,'search_project':search_project}
    return render(request,'projects/project.html',cotext)

def project1(request,pk):
    projectobj = project.objects.get(Id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectobj
        review.owner = request.user.profile
        review.save()
        #update project vote count
        projectobj.getvotecount 

        messages.success(request,'your review is successfuly submited ') 
        return redirect('project', pk=projectobj.Id)

    cotext = {'projectobj':projectobj,'forms':form}
    return render(request,'projects/single-pro.html',cotext)

@login_required (login_url="login")
def createproject(request):
    profile = request.user.profile
    form = ProjectsForm()

    if request.method == 'POST':
        form = ProjectsForm(request.POST,request.FILES)
        if form.is_valid():
                project = form.save(commit=False)
                project.owner = profile
                project.save()
                return redirect('account')
    
    forms = ProjectsForm()
    cotext = {'form':forms}
    return render(request,'projects/project_form.html',cotext)

@login_required (login_url="login")
def updateproject(request,pk):
    profile = request.user.profile
    upproject = profile.project_set.get(Id=pk)
    form = ProjectsForm(instance=upproject)

    if request.method == 'POST':
        form = ProjectsForm(request.POST,request.FILES,instance=upproject)
        if form.is_valid():
            form.save()
            return redirect('account')
            

    cotext = {'form':form}
    return render(request,'projects/project_form.html',cotext)

@login_required (login_url="login")
def deleteproject(request,pk):
    profile = request.user.profile
    projec = profile.project_set.get(Id=pk)
    cotext = {'object':projec}
    if request.method =='POST':
        projec.delete()
        return redirect('account')

    return render(request,'delete_template.html',cotext)