from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from blog.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# class SignUp(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'


def choose(request, username):
    user = User.objects.get(username=username)
    user_ = UserProfile.objects.get(user=user)

    user_.visit = 1
    temp = []
    if request.POST.get('0'):
        print(request.POST.get('0'))
        temp.append('0')
        print(0)
    if request.POST.get('1'):
        print(request.POST.get('1'))
        temp.append('1')
        print(1)
    if request.POST.get('2'):
        print(request.POST.get('2'))
        temp.append('2')
        print(2)
    if request.POST.get('3'):
        print(request.POST.get('3'))
        temp.append('3')
        print(3)
    if request.POST.get('4'):
        print(request.POST.get('4'))
        temp.append('4')
        print(4)
    if request.POST.get('5'):
        print(request.POST.get('5'))
        temp.append('5')
        print(5)
    user_.tags = temp
    user_.save()
    return redirect('blog:home', user.username)



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            user_ = UserProfile.objects.get(user=user)
            # return render(request, 'accounts/choose.html', {'username': username})
            if user_.visit == 0:
                return render(request, 'accounts/choose.html', {'username': username})
            else :
                return redirect('blog:home', username)

        else:
            form = UesrForm()
            return render(request, 'accounts/login.html', {'form': form, 'error': 'wrong credentials'})
    else:
        form = UesrForm()
        return render(request, 'accounts/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if User.objects.filter(username=username).exists():
            form = SignUpForm()
            return render(request, 'accounts/signup.html', {'form': form, 'profile_form': profile_form, 'error':'Username already exist'})
        if password1 != password2:
            form = SignUpForm()
            return render(request, 'accounts/signup.html', {'form': form, 'profile_form': profile_form, 'error':'password not matches'})
        if User.objects.filter(email=email).exists():
            form = SignUpForm()
            return render(request, 'accounts/signup.html', {'form': form, 'profile_form': profile_form, 'error':'email already exist'})


        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()


            # send_mail(subject, message, from_email,to_list, fail_silently=True)
            subject = 'Thank you'
            message = 'hello'
            from_email = settings.EMAIL_HOST_USER
            to_list = [ settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)


            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user1 = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user1)
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/signup.html', {'form': form, 'profile_form': profile_form,  'error':'Weak Password'})
    else:
        form = SignUpForm()
        profile_form = ProfileForm()
        return render(request, 'accounts/signup.html', {'form': form, 'profile_form': profile_form})


    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password1 = request.POST['password1']
    #     password2 = request.POST['password2']
    #     email = request.POST['email']
    #     if User.objects.filter(username=username).exists():
    #         form = SignUpForm()
    #         return render(request, 'accounts/signup.html', {'form': form, 'error':'Username already exist'})
    #     if password1 != password2:
    #         form = SignUpForm()
    #         return render(request, 'accounts/signup.html', {'form': form, 'error':'password not matches'})
    #     if User.objects.filter(email=email).exists():
    #         form = SignUpForm()
    #         return render(request, 'accounts/signup.html', {'form': form, 'error':'email already exist'})
    #
    #     form = SignUpForm(request.POST, instance=request.user)
    #     profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
    #     if form.is_valid() and profile_form.is_valid():
    #         form.save()
    #         profile.save()
    #
    #
    #         # send_mail(subject, message, from_email,to_list, fail_silently=True)
    #         subject = 'Thank you'
    #         message = 'hello'
    #         from_email = settings.EMAIL_HOST_USER
    #         to_list = [ settings.EMAIL_HOST_USER]
    #         send_mail(subject, message, from_email, to_list, fail_silently=True)
    #
    #
    #         username = form.cleaned_data.get('username')
    #         raw_password = form.cleaned_data.get('password1')
    #         user1 = auth.authenticate(username=username, password=raw_password)
    #         auth.login(request, user1)
    #         return redirect('accounts:login')
    # else:
    #     form = SignUpForm(instance=request.user)
    #     profile_form = ProfileForm(instance=request.user.userprofile)
    #     return render(request, 'accounts/signup.html', {'form': form, 'profile_form': profile_form})

def logout(request):
    auth.logout(request)
    return redirect('accounts:login')