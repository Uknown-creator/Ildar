from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import DataForm, UserForm, QuestionForm, MailForm, PasswordForm
import requests
from django.contrib.auth.models import User
from .models import UserUpgrade
from django.contrib import auth

def main_page(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            error = form.cleaned_data.get("error")
            error = error.encode("utf-8")
            response = requests.post('http://192.168.43.232:8800/', data=error)
            result = response.text
    else:
        form = DataForm()
        result = ''
    return render(request, 'main/index.html', {'form': form, 'result': result})


def about(request):
    return render(request, 'main/about.html')


def profile(request):
    return render(request, 'main/profile.html')


def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            password = form.cleaned_data.get("password")
            mail = form.cleaned_data.get("mail")
            user = User.objects.create_user(name, mail, password)
            user.save()
            for model in UserUpgrade.objects.all():
                if model.user == user:
                    model.question = form.cleaned_data['question']
                    model.answer = form.cleaned_data['answer']
                    model.save()
                    break
        return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserForm()
    return render(request, 'main/regis.html', {'form': form})


def reset(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            for user in User.objects.all():
                if user.email == mail:
                    return redirect(str(mail))
    else:
        form = MailForm()
    return render(request, 'main/reset.html', {'form': form})


def reset_2(request, mail):
    for user in User.objects.all():
        if user.email == mail:
            use = user
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            models = UserUpgrade.objects.all()
            for model in models:
                if model.user == use:
                    ans = model.answer
                    break
            if ans == form.cleaned_data['answer']:
                auth.login(request, use)
                return redirect('http://127.0.0.1:8000/password-change/')
    else:
        models = UserUpgrade.objects.all()
        for model in models:
            if model.user == use:
                ques = model.question
                form = QuestionForm()
                return render(request, 'main/reset_2.html', {'form': form, 'ques': ques})

def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            print(user.password)
            user.set_password(form.cleaned_data['password'])
            print(user.password)
            return redirect('http://127.0.0.1:8000/')
    else:
        form = PasswordForm()
    return render(request, 'main/change_password.html', {'form': form})