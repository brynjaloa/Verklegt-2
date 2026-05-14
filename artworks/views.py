import unicodedata

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.db.models import Count, Exists, Max, OuterRef, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from urllib.parse import urlparse

from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.paginator import Paginator
from .forms import ArtworkForm
from .models import Artwork, ArtworkImage

from bids.models import Bid
from bids.forms import BidForm

SOLD_BID_STATUSES = (Bid.Status.ACCEPTED, Bid.Status.FINALIZED)

CATEGORY_FILTER_FIELDS = {
    Artwork.Category.PAINTINGS: {
        "style": "painting_style",
        "medium": "painting_medium",
        "styles": Artwork.PaintingStyle.choices,
        "mediums": Artwork.PaintingMedium.choices,
    },
    Artwork.Category.SCULPTURES: {
        "style": "sculpture_style",
        "medium": "sculpture_material",
        "styles": Artwork.SculptureStyle.choices,
        "mediums": Artwork.SculptureMaterial.choices,
    },
    Artwork.Category.FURNITURE: {
        "style": "furniture_style",
        "medium": "furniture_material",
        "styles": Artwork.FurnitureStyle.choices,
        "mediums": Artwork.FurnitureMaterial.choices,
    },
    Artwork.Category.PHOTOS: {
        "style": "photo_style",
        "medium": "photo_technique",
        "styles": Artwork.PhotoStyle.choices,
        "mediums": Artwork.PhotoTechnique.choices,
    },
}

FEATURED_CATEGORY_STYLES = {
    Artwork.Category.PAINTINGS: (
        (Artwork.PaintingStyle.MODERNISM.value, "Modernism"),
        (Artwork.PaintingStyle.SURREALISM.value, "Surrealism"),
        (Artwork.PaintingStyle.REALISM.value, "Realism"),
        (Artwork.PaintingStyle.ABSTRACT_ART.value, "Abstract art"),
    ),
    Artwork.Category.SCULPTURES: (
        (Artwork.SculptureStyle.SURREALISM.value, Artwork.SculptureStyle.SURREALISM.label),
        (Artwork.SculptureStyle.CONTEMPORARY.value, "Contemporary"),
        (Artwork.SculptureStyle.MODERN_ART.value, "Modern art"),
        (Artwork.SculptureStyle.KINETIC_ART.value, "Kinetic art"),
    ),
    Artwork.Category.PHOTOS: (
        (Artwork.PhotoStyle.LANDSCAPE.value, Artwork.PhotoStyle.LANDSCAPE.label),
        (Artwork.PhotoStyle.PORTRAIT.value, Artwork.PhotoStyle.PORTRAIT.label),
        (Artwork.PhotoStyle.ARCHITECTURAL.value, "Architectural"),
        (Artwork.PhotoStyle.ABSTRACT.value, "Abstract"),
    ),
    Artwork.Category.FURNITURE: (
        (Artwork.FurnitureStyle.MINIMALISM.value, Artwork.FurnitureStyle.MINIMALISM.label),
        (Artwork.FurnitureStyle.ART_DECO.value, Artwork.FurnitureStyle.ART_DECO.label),
        (Artwork.FurnitureStyle.MODERNISM.value, "Modern"),
        (Artwork.FurnitureStyle.CONTEMPORARY.value, Artwork.FurnitureStyle.CONTEMPORARY.label),
    ),
}


BUILT_IN_STYLE_IMAGES = {
    Artwork.Category.PAINTINGS: {
        Artwork.PaintingStyle.MODERNISM.value: "built-in_artworks/Modernism_art.jpeg",
        Artwork.PaintingStyle.SURREALISM.value: "built-in_artworks/Surrealism_art.jpeg",
        Artwork.PaintingStyle.REALISM.value: "built-in_artworks/Realism_art.jpeg",
        Artwork.PaintingStyle.ABSTRACT_ART.value: "built-in_artworks/Abstract_art.jpeg",
    },
    Artwork.Category.SCULPTURES: {
        Artwork.SculptureStyle.SURREALISM.value: "built-in_artworks/Surrealism_sculpture.jpeg",
        Artwork.SculptureStyle.CONTEMPORARY.value: "built-in_artworks/Contemporary_sculpture.jpeg",
        Artwork.SculptureStyle.MODERN_ART.value: "built-in_artworks/Modern_art_sculpture.jpeg",
        Artwork.SculptureStyle.KINETIC_ART.value: "built-in_artworks/Kinetic_art_sculpture.jpeg",
    },
    Artwork.Category.PHOTOS: {
        Artwork.PhotoStyle.LANDSCAPE.value: "built-in_artworks/Landscape_photo.jpeg",
        Artwork.PhotoStyle.PORTRAIT.value: "built-in_artworks/Portrait_photos.jpeg",
        Artwork.PhotoStyle.ARCHITECTURAL.value: "built-in_artworks/Architecture_photos.jpeg",
        Artwork.PhotoStyle.ABSTRACT.value: "built-in_artworks/Abstract_photos.jpeg",
    },
    Artwork.Category.FURNITURE: {
        Artwork.FurnitureStyle.MINIMALISM.value: "built-in_artworks/Minimalism_furniture.jpeg",
        Artwork.FurnitureStyle.ART_DECO.value: "built-in_artworks/Art_deco_furniture.jpeg",
        Artwork.FurnitureStyle.MODERNISM.value: "built-in_artworks/Modern_furniture.jpeg",
        Artwork.FurnitureStyle.CONTEMPORARY.value: "built-in_artworks/Contemporary_furniture.jpeg",
    },
}


BUILT_IN_CATEGORY_IMAGES = {
    Artwork.Category.PAINTINGS: "built-in_artworks/Painting.jpeg",
    Artwork.Category.SCULPTURES: "built-in_artworks/Sculptures.jpeg",
    Artwork.Category.PHOTOS: "built-in_artworks/Photos.jpeg",
    Artwork.Category.FURNITURE: "built-in_artworks/Furniture.jpeg",
}


def styles_with_builtin_images(category, styles):
    image_paths = BUILT_IN_STYLE_IMAGES.get(category, {})

    return [
        (value, label, image_paths.get(value))
        for value, label in styles
    ]


def get_artwork_detail_back_url(request):
    referer = request.META.get("HTTP_REFERER")

    if referer and url_has_allowed_host_and_scheme(
        referer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        referer_path = urlparse(referer).path

        if referer_path != request.path:
            return referer

    return reverse("see_all")


def search_variants(query):
    normalized_query = unicodedata.normalize("NFKD", query)
    without_accents = "".join(
        character
        for character in normalized_query
        if not unicodedata.combining(character)
    )

    return {
        query,
        unicodedata.normalize("NFC", query),
        unicodedata.normalize("NFD", query),
        without_accents,
    }


def apply_title_search(artworks, query):
    if not query:
        return artworks

    title_query = Q()

    for variant in search_variants(query):
        if variant:
            title_query |= Q(title__icontains=variant)

    return artworks.filter(title_query)


def sort_artworks(artworks, sort):
    if sort == 'price_low':
        return artworks.order_by('starting_bid', '-listing_date', '-id')
    if sort == 'price_high':
        return artworks.order_by('-starting_bid', '-listing_date', '-id')

    return artworks.order_by('-listing_date', '-id')


def annotate_sold_by_bid(artworks):
    return artworks.annotate(
        sold_by_bid=Exists(
            Bid.objects.filter(
                artwork=OuterRef("pk"),
                status__in=SOLD_BID_STATUSES,
            )
        )
    )


def apply_status_filter(artworks, statuses_selected):
    if not statuses_selected or {"available", "sold"}.issubset(statuses_selected):
        return artworks

    if "available" in statuses_selected:
        return artworks.filter(is_sold=False, sold_by_bid=False)

    if "sold" in statuses_selected:
        return artworks.filter(Q(is_sold=True) | Q(sold_by_bid=True))

    return artworks


def latest_visible_bids_for_artwork(artwork):
    latest_bid_ids = (
        Bid.objects.filter(artwork=artwork)
        .exclude(status=Bid.Status.CANCELED)
        .values("user")
        .annotate(latest_id=Max("id"))
        .values("latest_id")
    )

    return Bid.objects.filter(id__in=latest_bid_ids).order_by("-bid_price", "-id")


def repair_bid_queue_for_artwork(artwork):
    if Bid.objects.filter(artwork=artwork, status=Bid.Status.FINALIZED).exists():
        return

    queue_statuses = [Bid.Status.PENDING, Bid.Status.CONTINGENT, Bid.Status.REJECTED]
    accepted_bid = Bid.objects.filter(artwork=artwork, status=Bid.Status.ACCEPTED).first()

    has_waiting_bids = Bid.objects.filter(
        artwork=artwork,
        status__in=[Bid.Status.PENDING, Bid.Status.CONTINGENT],
    ).exists()
    has_old_rejected_queue = Bid.objects.filter(
        artwork=artwork,
        status=Bid.Status.REJECTED,
    ).exists()

    if accepted_bid is None and has_old_rejected_queue and not has_waiting_bids:
        accepted_bid = Bid.objects.filter(
            artwork=artwork,
            status=Bid.Status.REJECTED,
        ).order_by("-bid_price", "date_of_bid", "id").first()

        if accepted_bid:
            accepted_bid.status = Bid.Status.ACCEPTED
            accepted_bid.buyer_accept_notification_seen = False
            accepted_bid.save(update_fields=["status", "buyer_accept_notification_seen"])

    if accepted_bid is None:
        Bid.objects.filter(
            artwork=artwork,
            status__in=[Bid.Status.CONTINGENT, Bid.Status.REJECTED],
        ).update(status=Bid.Status.PENDING)

        if artwork.is_sold:
            artwork.is_sold = False
            artwork.save(update_fields=["is_sold"])

        return

    queued_bids = list(
        Bid.objects.filter(
            artwork=artwork,
            status__in=queue_statuses,
        ).exclude(
            id=accepted_bid.id,
        ).order_by("-bid_price", "date_of_bid", "id")
    )

    for index, bid in enumerate(queued_bids):
        next_status = Bid.Status.CONTINGENT if index == 0 else Bid.Status.PENDING

        if bid.status != next_status:
            bid.status = next_status
            bid.save(update_fields=["status"])

    if artwork.is_sold:
        artwork.is_sold = False
        artwork.save(update_fields=["is_sold"])


def artwork_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    categories_selected = request.GET.getlist('category')
    styles_selected = request.GET.getlist('style')
    mediums_selected = request.GET.getlist('medium')
    editions_selected = request.GET.getlist('edition')
    statuses_selected = request.GET.getlist('status')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')

    artworks = annotate_sold_by_bid(Artwork.objects.all())


    for artwork in artworks:
        highest_bid = Bid.objects.filter(artwork=artwork).order_by("-bid_price").first()
        artwork.highest_bid = highest_bid

    artworks = apply_title_search(artworks, query)

    if categories_selected:
        artworks = artworks.filter(category__in=categories_selected)

    category_fields = CATEGORY_FILTER_FIELDS.get(category, {}) if len(categories_selected) <= 1 else {}
    style_field = category_fields.get("style")
    medium_field = category_fields.get("medium")

    if styles_selected and style_field:
        artworks = artworks.filter(**{f"{style_field}__in": styles_selected})
    elif styles_selected:
        artworks = artworks.filter(
            Q(painting_style__in=styles_selected)
            | Q(sculpture_style__in=styles_selected)
            | Q(furniture_style__in=styles_selected)
            | Q(photo_style__in=styles_selected)
        )
    if mediums_selected and medium_field:
        artworks = artworks.filter(**{f"{medium_field}__in": mediums_selected})
    elif mediums_selected:
        artworks = artworks.filter(
            Q(painting_medium__in=mediums_selected)
            | Q(sculpture_material__in=mediums_selected)
            | Q(furniture_material__in=mediums_selected)
            | Q(photo_technique__in=mediums_selected)
        )
    if editions_selected:
        artworks = artworks.filter(edition__in=editions_selected)
    artworks = apply_status_filter(artworks, statuses_selected)
    if year_from:
        artworks = artworks.filter(year__gte=year_from)
    if year_to:
        artworks = artworks.filter(year__lte=year_to)

    styles = category_fields.get("styles", [])
    featured_styles = styles_with_builtin_images(
        category,
        FEATURED_CATEGORY_STYLES.get(category, styles),
    )
    mediums = category_fields.get("mediums", [])
    show_style_shortcuts = not (
        query
        or styles_selected
        or mediums_selected
        or editions_selected
        or statuses_selected
        or year_from
        or year_to
    )

    sort = request.GET.get('sort', 'relevance')
    artworks = sort_artworks(artworks, sort)

    pagination_query = request.GET.copy()
    pagination_query.pop("page", None)

    paginator = Paginator(artworks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'artworks/artwork_marketplace.html', {
        'artworks': artworks,
        'query': query,
        'category': category,
        'styles': featured_styles,
        'show_style_shortcuts': show_style_shortcuts,
        'filter_styles': styles,
        'mediums': mediums,
        'selected_categories': categories_selected,
        'selected_styles': styles_selected,
        'selected_mediums': mediums_selected,
        'selected_editions': editions_selected,
        'selected_statuses': statuses_selected,
        'status_choices': (
            ("available", "Available"),
            ("sold", "Sold"),
        ),
        'page_obj': page_obj,
        'pagination_query': pagination_query.urlencode(),
        'sort': sort,
    })


def home_view(request):
    recent_artworks = Artwork.objects.all().order_by("-listing_date", "-id")[:8]
    recent_artworks = Artwork.objects.all().order_by("-listing_date", "-id")[:8]
    popular_artworks = (
        Artwork.objects.annotate(bid_count=Count("bid"))
        .filter(bid_count__gt=0)
        .order_by("-bid_count", "-listing_date", "-id")[:8]
    )

    return render(request, "home.html", {
        "recent_artworks": recent_artworks,
        "popular_artworks": popular_artworks,
    })


def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    repair_bid_queue_for_artwork(artwork)
    back_url = get_artwork_detail_back_url(request)
    highest_bids = latest_visible_bids_for_artwork(artwork)
    has_accepted_bid = Bid.objects.filter(
        artwork=artwork,
        status__in=[Bid.Status.ACCEPTED, Bid.Status.FINALIZED],
    ).exists()
    has_finalized_bid = Bid.objects.filter(
        artwork=artwork,
        status=Bid.Status.FINALIZED,
    ).exists()
    is_artwork_sold = artwork.is_sold or has_finalized_bid
    is_bidding_locked = has_accepted_bid and not has_finalized_bid

    if has_finalized_bid and not artwork.is_sold:
        artwork.is_sold = True
        artwork.save(update_fields=["is_sold"])

    extra_images = list(artwork.images.all())
    seller = getattr(request.user, "seller", None)
    can_edit_artwork = (
        request.user.is_authenticated
        and seller is not None
        and seller == artwork.seller
    )
    show_description_toggle = bool(artwork.description and len(artwork.description.split()) > 35)

    if not artwork.main_image and extra_images:
        extra_images = extra_images[1:]

    existing_bid = None

    if request.user.is_authenticated:
        existing_bid = Bid.objects.filter(
            artwork=artwork,
            user=request.user
        ).exclude(status=Bid.Status.CANCELED).order_by("-id").first()

    if request.method == "POST" and (is_artwork_sold or is_bidding_locked):
        return redirect("artwork_detail", pk=artwork.pk)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")

        if can_edit_artwork:
            return HttpResponseForbidden("You cannot bid on your own artwork.")

        is_resubmission = existing_bid is not None

        if existing_bid:
            form = BidForm(
                request.POST,
                instance=existing_bid,
                artwork=artwork,
            )

        else:
            form = BidForm(request.POST, artwork=artwork)

        if form.is_valid():
            bid = form.save(commit=False)
            bid.artwork = artwork
            bid.user = request.user
            bid.status = Bid.Status.PENDING
            bid.save()
            Bid.objects.filter(
                artwork=artwork,
                user=request.user,
            ).exclude(id=bid.id).delete()
            existing_bid = bid
            highest_bids = latest_visible_bids_for_artwork(artwork)

            return render(request, "artworks/artwork_detail.html", {

                "artwork": artwork,
                "primary_image": artwork.primary_image,
                "extra_images": extra_images,
                "can_edit_artwork": can_edit_artwork,
                "is_artwork_sold": is_artwork_sold,
                "is_bidding_locked": is_bidding_locked,
                "has_accepted_bid": has_accepted_bid,
                "show_description_toggle": show_description_toggle,
                "form": form,
                "existing_bid": existing_bid,
                "is_resubmission": is_resubmission,
                "show_popup": True,
                "bid_popup_message": "success",
                "highest_bids": highest_bids,
                "back_url": back_url,
            })

        return render(request, "artworks/artwork_detail.html", {
            "artwork": artwork,
            "primary_image": artwork.primary_image,
            "extra_images": extra_images,
            "can_edit_artwork": can_edit_artwork,
            "is_bidding_locked": is_bidding_locked,
            "show_description_toggle": show_description_toggle,
            "form": form,
            "existing_bid": existing_bid,
            "show_popup": True,
            "bid_popup_message": "minimum_bid_error",
            "highest_bids": highest_bids,
            "back_url": back_url,
        })

    else:
        if existing_bid:
            form = BidForm(instance=existing_bid, artwork=artwork)
        else:
            form = BidForm(artwork=artwork)

    return render(request, "artworks/artwork_detail.html", {
        "artwork": artwork,
        "primary_image": artwork.primary_image,
        "extra_images": extra_images,
        "can_edit_artwork": can_edit_artwork,
        "is_artwork_sold": is_artwork_sold,
        "is_bidding_locked": is_bidding_locked,
        "has_accepted_bid": has_accepted_bid,
        "show_description_toggle": show_description_toggle,
        "form": form,
        "existing_bid": existing_bid,
        "highest_bids": highest_bids,
        "back_url": back_url,
    })


@login_required
def add_artwork(request):
    seller = getattr(request.user, "seller", None)

    if seller is None:
        return redirect("become_seller")

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.seller = seller
            artwork.save()
            ArtworkImage.objects.create(artwork=artwork, image=form.cleaned_data["second_image"])
            for image in form.cleaned_data["additional_images"]:
                ArtworkImage.objects.create(artwork=artwork, image=image)
            return redirect("artwork_detail", pk=artwork.pk)
    else:
        form = ArtworkForm()

    return render(request, "artworks/artworks_form.html", {
        "form": form,
        "form_title": "Add Artwork",
        "button_text": "Add Artwork",
    })


@login_required
def edit_artwork(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    seller = getattr(request.user, "seller", None)

    if seller is None or artwork.seller != seller:
        return HttpResponseForbidden("You cannot edit this artwork.")

    if artwork.is_sold or Bid.objects.filter(
        artwork=artwork,
        status__in=[Bid.Status.ACCEPTED, Bid.Status.FINALIZED],
    ).exists():
        return HttpResponseForbidden("Sold artworks cannot be edited.")

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            artwork = form.save()
            if form.cleaned_data.get("second_image"):
                ArtworkImage.objects.create(artwork=artwork, image=form.cleaned_data["second_image"])
            for image in form.cleaned_data["additional_images"]:
                ArtworkImage.objects.create(artwork=artwork, image=image)
            return redirect("artwork_detail", pk=artwork.pk)
    else:
        form = ArtworkForm(instance=artwork)

    return render(request, "artworks/artworks_form.html", {
        "form": form,
        "form_title": "Edit Artwork",
        "button_text": "Save Changes",
        "artwork": artwork,
    })


@login_required
@require_POST
def delete_artwork(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    seller = getattr(request.user, "seller", None)

    if seller is None or artwork.seller != seller:
        return HttpResponseForbidden("You cannot remove this artwork.")

    if artwork.is_sold or Bid.objects.filter(
        artwork=artwork,
        status__in=[Bid.Status.ACCEPTED, Bid.Status.FINALIZED],
    ).exists():
        return HttpResponseForbidden("Accepted or sold artworks cannot be removed.")

    artwork.delete()
    return redirect("profile")


def category_list(request):
    categories = [
        (value, label, BUILT_IN_CATEGORY_IMAGES.get(value))
        for value, label in Artwork.Category.choices
    ]
    return render(request, 'Category/categories.html', {'categories': categories})

def artwork_see_all(request):
    query = request.GET.get('q', '').strip()
    painting_mediums_selected = request.GET.getlist('painting_medium')
    sculpture_materials_selected = request.GET.getlist('sculpture_material')
    furniture_materials_selected = request.GET.getlist('furniture_material')
    photo_techniques_selected = request.GET.getlist('photo_technique')
    legacy_mediums_selected = request.GET.getlist('medium')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    categories_selected = request.GET.getlist('category')
    painting_styles_selected = request.GET.getlist('painting_style')
    sculpture_styles_selected = request.GET.getlist('sculpture_style')
    furniture_styles_selected = request.GET.getlist('furniture_style')
    photo_styles_selected = request.GET.getlist('photo_style')
    legacy_styles_selected = request.GET.getlist('style')
    editions_selected = request.GET.getlist('edition')
    statuses_selected = request.GET.getlist('status')
    sort = request.GET.get('sort', 'relevance')

    artworks = annotate_sold_by_bid(Artwork.objects.all())

    artworks = apply_title_search(artworks, query)
    if categories_selected:
        artworks = artworks.filter(category__in=categories_selected)
    if legacy_mediums_selected:
        artworks = artworks.filter(
            Q(painting_medium__in=legacy_mediums_selected)
            | Q(sculpture_material__in=legacy_mediums_selected)
            | Q(furniture_material__in=legacy_mediums_selected)
            | Q(photo_technique__in=legacy_mediums_selected)
        )
    if painting_mediums_selected:
        artworks = artworks.filter(painting_medium__in=painting_mediums_selected)
    if sculpture_materials_selected:
        artworks = artworks.filter(sculpture_material__in=sculpture_materials_selected)
    if furniture_materials_selected:
        artworks = artworks.filter(furniture_material__in=furniture_materials_selected)
    if photo_techniques_selected:
        artworks = artworks.filter(photo_technique__in=photo_techniques_selected)
    if legacy_styles_selected:
        artworks = artworks.filter(
            Q(painting_style__in=legacy_styles_selected)
            | Q(sculpture_style__in=legacy_styles_selected)
            | Q(furniture_style__in=legacy_styles_selected)
            | Q(photo_style__in=legacy_styles_selected)
        )
    if painting_styles_selected:
        artworks = artworks.filter(painting_style__in=painting_styles_selected)
    if sculpture_styles_selected:
        artworks = artworks.filter(sculpture_style__in=sculpture_styles_selected)
    if furniture_styles_selected:
        artworks = artworks.filter(furniture_style__in=furniture_styles_selected)
    if photo_styles_selected:
        artworks = artworks.filter(photo_style__in=photo_styles_selected)
    if editions_selected:
        artworks = artworks.filter(edition__in=editions_selected)
    artworks = apply_status_filter(artworks, statuses_selected)
    if year_from:
        artworks = artworks.filter(year__gte=year_from)
    if year_to:
        artworks = artworks.filter(year__lte=year_to)

    artworks = sort_artworks(artworks, sort)
    paginator = Paginator(artworks, 24)
    page_obj = paginator.get_page(request.GET.get("page"))
    pagination_query = request.GET.copy()
    pagination_query.pop("page", None)
    all_styles = list({
        label: value
        for value, label in (
            list(Artwork.PaintingStyle.choices)
            + list(Artwork.SculptureStyle.choices)
            + list(Artwork.FurnitureStyle.choices)
            + list(Artwork.PhotoStyle.choices)
        )
    }.items())

    return render(request, 'artworks/see_all.html', {
        'artworks': page_obj,
        'page_obj': page_obj,
        'pagination_pages': paginator.get_elided_page_range(page_obj.number),
        'pagination_query': pagination_query.urlencode(),
        'categories': Artwork.Category.choices,
        'editions': Artwork.Edition.choices,
        'painting_mediums': Artwork.PaintingMedium.choices,
        'sculpture_materials': Artwork.SculptureMaterial.choices,
        'furniture_materials': Artwork.FurnitureMaterial.choices,
        'photo_techniques': Artwork.PhotoTechnique.choices,
        'painting_styles': Artwork.PaintingStyle.choices,
        'sculpture_styles': Artwork.SculptureStyle.choices,
        'furniture_styles': Artwork.FurnitureStyle.choices,
        'photo_styles': Artwork.PhotoStyle.choices,
        'all_styles': all_styles,
        'selected_categories': categories_selected,
        'selected_painting_mediums': painting_mediums_selected,
        'selected_sculpture_materials': sculpture_materials_selected,
        'selected_furniture_materials': furniture_materials_selected,
        'selected_photo_techniques': photo_techniques_selected,
        'selected_painting_styles': painting_styles_selected,
        'selected_sculpture_styles': sculpture_styles_selected,
        'selected_furniture_styles': furniture_styles_selected,
        'selected_photo_styles': photo_styles_selected,
        'selected_styles': legacy_styles_selected,
        'selected_editions': editions_selected,
        'selected_statuses': statuses_selected,
        'status_choices': (
            ("available", "Available"),
            ("sold", "Sold"),
        ),
        'query': query,
        'sort': sort,
    })

@login_required
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    if bid.artwork.seller != request.user.seller:
        return HttpResponseForbidden()

    if Bid.objects.filter(
        artwork=bid.artwork,
        status__in=SOLD_BID_STATUSES,
    ).exclude(id=bid.id).exists():
        return redirect("artwork_detail", pk=bid.artwork.id)

    Bid.objects.filter(artwork=bid.artwork).exclude(id=bid.id).update(
        status=Bid.Status.REJECTED
    )

    bid.status = Bid.Status.ACCEPTED
    bid.save(update_fields=["status"])
    bid.artwork.is_sold = True
    bid.artwork.save(update_fields=["is_sold"])

    return redirect(
        "artwork_detail",
        pk=bid.artwork.id
    )
