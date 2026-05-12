from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from artworks.models import Artwork
from .forms import SignUpForm, ProfileForm, SellerForm
from .models import Profile, Seller
from bids.models import Bid



def get_or_create_profile(user):
    name = user.get_full_name() or user.username
    profile, _ = Profile.objects.get_or_create(user=user, defaults={'name': name})
    return profile


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


def check_username_view(request):
    username = request.GET.get('username', '').strip()
    exists = bool(username) and User.objects.filter(username__iexact=username).exists()

    return JsonResponse({'exists': exists})


def check_email_view(request):
    email = request.GET.get('email', '').strip()
    exists = bool(email) and User.objects.filter(email__iexact=email).exists()

    return JsonResponse({'exists': exists})


@login_required
def profile_view(request):
    profile = get_or_create_profile(request.user)
    seller = None
    artworks = Artwork.objects.none()
    my_bids = Bid.objects.filter(user=request.user).select_related("artwork", "artwork__seller")

    if hasattr(request.user, 'seller'):
        seller = request.user.seller
        artworks = Artwork.objects.filter(seller=seller)

    context = {
        'profile': profile,
        'seller': seller,
        'artworks': artworks,
        "my_bids": my_bids,
    }
    return render(request,'accounts/profile.html',context)

@login_required
def edit_profile_view(request):
    profile = get_or_create_profile(request.user)

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
    profile = get_or_create_profile(request.user)

    if hasattr(request.user, 'seller'):
        return redirect('profile')

    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)

        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()

            profile.is_seller = True
            profile.save()

            messages.success(request, 'You are now registered as a seller.')
            return redirect('profile')

    else:
        form = SellerForm()

    return render(request, 'accounts/become_seller.html', {'form': form})
