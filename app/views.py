from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from app.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



def registration(request):
    UFO=UserForm()
    PFO=ProfileForm()
    d={'UFO':UFO,'PFO':PFO}

    if request.method=='POST' and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        if UFD.is_valid() and PFD.is_valid():

            NSUFO=UFD.save(commit=False)
            submittedPW=UFD.cleaned_data['password']
            NSUFO.set_password(submittedPW)
            NSUFO.save()

            NSPO=PFD.save(commit=False)
            NSPO.username=NSUFO
            NSPO.save()

            send_mail('Registration',
                    'Registration is Successfull',
                      'jacksparrow.7828.007@gmail.com',
                      [NSUFO.email],
                      fail_silently=True
                      )
            return HttpResponse('Registration Mail Sending is Succeffully Done')
    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


def sign_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'sign_in.html')



@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))