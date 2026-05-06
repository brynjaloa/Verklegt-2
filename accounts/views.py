from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignUpForm, ProfileForm, SellerForm
from .models import Profile, Seller


def login_view(request):
    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            Profile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                profile_image=form.cleaned_data.get('profile_image')
            )

            login(request, user)
            return redirect('profile')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def edit_profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Something went wrong. Please try again.')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def become_seller_view(request):
    if hasattr(request.user, 'seller'):
        return redirect('profile')

    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)

        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()

            request.user.profile.is_seller = True
            request.user.profile.save()

            messages.success(request, 'You are now registered as a seller.')
            return redirect('profile')

    else:
        form = SellerForm()

    return render(request, 'accounts/become_seller.html', {'form': form})