from django.shortcuts import render
from basicApp.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'basicApp/index.html')



def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        user_profile_info_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and user_profile_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = user_profile_info_form.save(commit = 'False')
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print("error 404")
    else:
        user_form = UserForm()
        user_profile_info_form = UserProfileInfoForm
    return render(request,'basicApp/registration.html',{'user_form':user_form, 'profile_form':user_profile_info_form, 'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('un')
        password = request.POST.get('pw')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT INACTIVE')
        else:
            return HttpResponse("invalid Username or Password")
    else:
        return render(request, 'basicApp/login.html')

        
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
