from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form' : form})


def logout_view(request):
    logout(request)
    return redirect('login')