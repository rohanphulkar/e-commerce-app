from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password')
        if " " in full_name:
            first_name = full_name.split(' ')[0]
            last_name = full_name.split(' ')[1]
        else:
            first_name = full_name
            last_name = ""
        user = User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password)
        user.save()
        
        user = authenticate(
            username=email,
            password=password,
        )
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'register.html')


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(
            username=email,
            password=password,
        )
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url='/login/')
def logoutPage(request):
    logout(request)
    return redirect('home')
    
    