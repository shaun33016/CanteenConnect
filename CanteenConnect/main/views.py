from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.decorators import user_passes_test
from .models import Menu
from datetime import date
from .forms import Menu_form
from django.http import HttpResponseRedirect



#Testing
def chef_check(user):
    '''To check if user is chef'''
    return user.groups.filter(name='chef').exists()
def student_check(user):
    '''To check if user is student'''
    return user.groups.filter(name='student').exists()



#Functions 
def login(request):
    '''allows user to log into site is & capable of diffrentiating between chef and student'''
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            if user.groups.filter(name='chef').exists():
                return redirect('home_c')
            return redirect('home_s')
        else:
            messages.error(request,'Username or Password Incorrect.')
            return render (request,'login.html')#Redirects if error is present
    else:
        return render(request,'login.html')#Not sure what this is for

def logout(request):
    auth.logout(request)
    return redirect('login')



#Site Rendering Functions
@user_passes_test(student_check)#to only allow if user is student
#Student Homepage
def student_home(request):
    Data_Object=Menu.objects.filter(Date__gte=str(date.today()))
    return render(request,'student_home.html',{"Data_Objects":Data_Object})

#Chef HomePage ie results page
@user_passes_test(chef_check)#to only allow if user is chef
def chef_home(request):
    Data_Object=Menu.objects.filter(Date__gte=str(date.today()))
    return render(request,'chef_home.html',{"Data_Objects":Data_Object})


@user_passes_test(chef_check)
def chef_select(request):
    submitted=False
    if request.method=="POST":
        form=Menu_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/chef/selection?submitted=True')
            
    else:
        form=Menu_form
        if 'submitted' in request.GET:
            submitted=True
             
    return render(request,'chef_inserter.html',{'form':form,'submitted':submitted})


