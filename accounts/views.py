from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Exists, OuterRef
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from artworks.models import Artwork
from .forms import SignUpForm, ProfileForm, SellerForm, SellerEditForm
from .models import Profile, Seller
from bids.models import Bid



def get_or_create_profile(user):
    name = user.get_full_name() or user.username
    profile, _ = Profile.objects.get_or_create(user=user, defaults={'name': name})
    return profile


def login_view(request):
    return render(request, 'accounts/login.html')


def csrf_failure_view(request, reason=""):
    messages.error(request, "Your login session expired. Please try again.")
    return redirect('login')


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
@never_cache
def profile_view(request):
    profile = get_or_create_profile(request.user)
    seller = None
    artworks = Artwork.objects.none()
    user_bids = Bid.objects.filter(user=request.user).select_related("artwork", "artwork__seller")
    my_bids = user_bids.exclude(status__in=[Bid.Status.FINALIZED, Bid.Status.CANCELED])
    my_purchases = user_bids.filter(status=Bid.Status.FINALIZED)
    accepted_bid_notifications = list(
        user_bids.filter(
            status=Bid.Status.ACCEPTED,
            buyer_accept_notification_seen=False,
        )
    )
    rejected_bid_notifications = list(
        user_bids.filter(
            status=Bid.Status.REJECTED,
            buyer_reject_notification_seen=False,
        )
    )
    canceled_bid_notifications = []

    if accepted_bid_notifications:
        Bid.objects.filter(
            id__in=[bid.id for bid in accepted_bid_notifications]
        ).update(buyer_accept_notification_seen=True)

    if rejected_bid_notifications:
        Bid.objects.filter(
            id__in=[bid.id for bid in rejected_bid_notifications]
        ).update(buyer_reject_notification_seen=True)

    if hasattr(request.user, 'seller'):
        seller = request.user.seller
        finalized_bids = Bid.objects.filter(
            artwork=OuterRef("pk"),
            status=Bid.Status.FINALIZED,
        )
        artworks = Artwork.objects.filter(seller=seller).annotate(
            has_finalized_bid=Exists(finalized_bids)
        )
        canceled_bid_notifications = list(
            Bid.objects.filter(
                artwork__seller=seller,
                status=Bid.Status.CANCELED,
                seller_cancel_notification_seen=False,
            ).select_related("artwork", "user")
        )

        if canceled_bid_notifications:
            Bid.objects.filter(
                id__in=[bid.id for bid in canceled_bid_notifications]
            ).update(seller_cancel_notification_seen=True)

    context = {
        'profile': profile,
        'seller': seller,
        'artworks': artworks,
        "my_bids": my_bids,
        "my_purchases": my_purchases,
        "accepted_bid_notifications": accepted_bid_notifications,
        "rejected_bid_notifications": rejected_bid_notifications,
        "canceled_bid_notifications": canceled_bid_notifications,
    }
    return render(request,'accounts/profile.html',context)


def seller_profile_view(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    requested_back_url = request.GET.get("back")
    back_url = requested_back_url if (
        requested_back_url
        and url_has_allowed_host_and_scheme(
            requested_back_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
    ) else reverse("see_all")
    artworks = Artwork.objects.filter(seller=seller).annotate(
        sold_by_bid=Exists(
            Bid.objects.filter(
                artwork=OuterRef("pk"),
                status__in=[Bid.Status.ACCEPTED, Bid.Status.FINALIZED],
            )
        )
    ).order_by("-listing_date", "-id")

    for artwork in artworks:
        artwork.highest_bid = Bid.objects.filter(artwork=artwork).order_by("-bid_price").first()

    return render(request, "accounts/seller_profile.html", {
        "seller": seller,
        "artworks": artworks,
        "back_url": back_url,
    })

@login_required
def edit_profile_view(request):
    profile = get_or_create_profile(request.user)
    seller = getattr(request.user, 'seller', None)

    if request.method == 'POST':
        if seller:
            seller_form = SellerEditForm(request.POST, request.FILES, instance=seller)

            if seller_form.is_valid():
                seller_form.save()
                messages.success(request, 'Seller information updated successfully.')
                return redirect('profile')

            messages.error(request, 'Something went wrong. Please try again.')
            profile_form = None
        else:
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            seller_form = None

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')

            messages.error(request, 'Something went wrong. Please try again.')

    else:
        profile_form = ProfileForm(instance=profile) if not seller else None
        seller_form = SellerEditForm(instance=seller) if seller else None

    return render(request, 'accounts/edit_profile.html', {
        'profile_form': profile_form,
        'seller_form': seller_form,
        'seller': seller,
    })


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
