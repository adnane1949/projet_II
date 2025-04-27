from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Replace with your desired redirect
    else:
        form = CustomUserCreationForm()
    return render(request, 'utilisateurs/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Replace with your desired redirect
    else:
        form = AuthenticationForm()
    return render(request, 'utilisateurs/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'utilisateurs/profile.html', {'user': user})

@login_required
def user_list_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    users = CustomUser.objects.all()
    return render(request, 'utilisateurs/user_list.html', {'users': users})