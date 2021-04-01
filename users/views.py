from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {user_name}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
        print("Loops==================")
    return render(request, 'users/register.html', {'form': form, 'user': request.user})