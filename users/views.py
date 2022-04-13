from django.dispatch import receiver
from django.shortcuts import render, redirect
from .models import profile,message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User 
from django.contrib import messages
from .forms import CustomUserCreationForm,ProfileForm,skillForm,messageForm
from django.contrib.auth.decorators import login_required
from .utils import searchprofiles,paginateprofile


# Create your views here.

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'username does not exist')
       
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else'account')
        else:
            messages.error (request,"username or password is incorrect") 
    
    return render(request, 'users/login_register.html')

def logoutuser(request):
    logout(request)
    messages.info(request,"user was logged out")
    return redirect('login')

def registeruser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User account has created!')

            login (request,user)
            return redirect('account')
        
        else:
            messages.error(request,'An error has beeen occurred buring registration')

    context = {'page': page,'form':form }
    return render(request,"users/login_register.html",context)

def profiles(request):
    profiles, search_query = searchprofiles(request)
    custom_range,profiles = paginateprofile(request, profiles, 1)

    context = {'profiles':profiles,'search_query':search_query,'custom_range':custom_range}
    return render(request, 'users/profiles.html',context )

def userprofile(request,pk): 
    profiles = profile.objects.get(Id=pk)
    topskills = profiles.skill_set.exclude(description__exact = "")
    otherskills = profiles.skill_set.filter(description="")
    context = {'profiles':profiles,'topskills':topskills,'otherskills':otherskills}
    return render(request,'users/user-profile.html',context)

@login_required (login_url="login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile':profile,'skills':skills,'projects':projects}
    return render(request,'users/account.html',context)
 
@login_required (login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {'form':form}
    return render(request,'users/profile_form.html',context)

@login_required (login_url="login")
def createskill (request):
    profile = request.user.profile
    form = skillForm()

    if request.method == "POST":
        form = skillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {'form':form}
    return render(request,'users/skill_form.html',context)

@login_required (login_url="login")
def editskill (request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(Id=pk)
    form = skillForm(instance=skill)

    if request.method == 'POST':
        form = skillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form}
    return render(request,'users/skill_form.html',context)

@login_required (login_url="login")
def deleteskill (request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(Id=pk)

    if request.method == 'POST':
        skill.delete()
        return redirect('account')

    context = {'object':skill}
    return render(request,'delete_template.html',context)

@login_required (login_url="login")
def inbox (request):
    profil = request.user.profile
    receiv = profil.messag.all()
    count = receiv.filter(is_read=False).count()

    context = {'receiv':receiv,'count':count}
    return render (request,"users/inbox.html",context)

@login_required (login_url="login")
def mess (request,pk):
    profil = request.user.profile
    receiv = profil.messag.get(Id=pk)
    
    if receiv.is_read == False :
        receiv.is_read = True
        receiv.save()
    
    context = {'receiv':receiv}
    return render (request,"users/message.html",context)

def messageform (request,pk):
    recip = profile.objects.get(Id=pk)
    form = messageForm()
    try:
        send = request.user.profile
    except:
        send = None
    
    if request.method == 'POST':
        form = messageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = send
            message.receiver = recip

            if send:
                message.sendername = send.name
                message.email = send.email
 
            message.save()
            return redirect('account')
        messages.success(request,'Message has been send!')
    context = {'form':form}
    return render (request,"users/message_form.html",context)