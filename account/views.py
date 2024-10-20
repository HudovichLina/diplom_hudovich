from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegistrationForm, UserEditForm, ProfileEditForm 
from django.contrib.auth.decorators import login_required
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login') 
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_edit(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.userprofile)

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.userprofile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    #  добавить сообщение об успехе
    return render(request,
                    'registration/user_profile.html',
                    {'user_form': user_form,
                    'profile_form': profile_form,
                    'profile': profile})
