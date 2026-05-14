import unicodedata

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count, Exists, Max, OuterRef, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils.formats import date_format
from django.utils.text import Truncator
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
    Artwork.Category.PAINTINGS.value: {
        "style": "painting_style",
        "medium": "painting_medium",
        "styles": Artwork.PaintingStyle.choices,
        "mediums": Artwork.PaintingMedium.choices,
    },
    Artwork.Category.SCULPTURES.value: {
        "style": "sculpture_style",
        "medium": "sculpture_material",
        "styles": Artwork.SculptureStyle.choices,
        "mediums": Artwork.SculptureMaterial.choices,
    },
    Artwork.Category.FURNITURE.value: {
        "style": "furniture_style",
        "medium": "furniture_material",
        "styles": Artwork.FurnitureStyle.choices,
        "mediums": Artwork.FurnitureMaterial.choices,
    },
    Artwork.Category.PHOTOS.value: {
        "style": "photo_style",
        "medium": "photo_technique",
        "styles": Artwork.PhotoStyle.choices,
        "mediums": Artwork.PhotoTechnique.choices,
    },
}

FEATURED_CATEGORY_STYLES = {
    Artwork.Category.PAINTINGS.value: (
        (Artwork.PaintingStyle.MODERNISM.value, "Modernism"),
        (Artwork.PaintingStyle.SURREALISM.value, "Surrealism"),
        (Artwork.PaintingStyle.REALISM.value, "Realism"),
        (Artwork.PaintingStyle.ABSTRACT_ART.value, "Abstract art"),
    ),
    Artwork.Category.SCULPTURES.value: (
        (Artwork.SculptureStyle.SURREALISM.value, Artwork.SculptureStyle.SURREALISM.label),
        (Artwork.SculptureStyle.CONTEMPORARY.value, "Contemporary"),
        (Artwork.SculptureStyle.MODERN_ART.value, "Modern art"),
        (Artwork.SculptureStyle.KINETIC_ART.value, "Kinetic art"),
    ),
    Artwork.Category.PHOTOS.value: (
        (Artwork.PhotoStyle.LANDSCAPE.value, Artwork.PhotoStyle.LANDSCAPE.label),
        (Artwork.PhotoStyle.PORTRAIT.value, Artwork.PhotoStyle.PORTRAIT.label),
        (Artwork.PhotoStyle.ARCHITECTURAL.value, "Architectural"),
        (Artwork.PhotoStyle.ABSTRACT.value, "Abstract"),
    ),
    Artwork.Category.FURNITURE.value: (
        (Artwork.FurnitureStyle.MINIMALISM.value, Artwork.FurnitureStyle.MINIMALISM.label),
        (Artwork.FurnitureStyle.ART_DECO.value, Artwork.FurnitureStyle.ART_DECO.label),
        (Artwork.FurnitureStyle.MODERNISM.value, "Modern"),
        (Artwork.FurnitureStyle.CONTEMPORARY.value, Artwork.FurnitureStyle.CONTEMPORARY.label),
    ),
}


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


def get_safe_back_url(request, fallback_url_name):
    requested_back_url = request.POST.get("back_url") or request.GET.get("back")

    if requested_back_url and url_has_allowed_host_and_scheme(
        requested_back_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return requested_back_url

    referer = request.META.get("HTTP_REFERER")

    if referer and url_has_allowed_host_and_scheme(
        referer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        parsed_referer = urlparse(referer)
        referer_path = parsed_referer.path
        referer_full_path = referer_path

        if parsed_referer.query:
            referer_full_path = f"{referer_full_path}?{parsed_referer.query}"

        if referer_full_path != request.get_full_path():
            return referer

    return reverse(fallback_url_name)


def get_artwork_detail_back_url(request):
    return get_safe_back_url(request, "see_all")


def clean_replacement_artwork_images(request, existing_images):
    cleaned_images = {}

    for image in existing_images:
        uploaded_image = request.FILES.get(f"replace_image_{image.pk}")

        if uploaded_image:
            cleaned_images[image.pk] = ArtworkForm.clean_image_file(uploaded_image)

    return cleaned_images


def edited_artwork_photo_count(artwork, form, existing_images, request):
    remove_image_ids = set(request.POST.getlist("remove_image"))
    main_image = form.cleaned_data.get("main_image")
    second_image = form.cleaned_data.get("second_image")
    additional_images = form.cleaned_data.get("additional_images", [])

    main_count = 1 if artwork.main_image else 0

    if main_image:
        main_count = 1
    elif request.POST.get("remove_main_image"):
        main_count = 0

    existing_extra_count = sum(
        1
        for image in existing_images
        if str(image.pk) not in remove_image_ids
    )

    return main_count + existing_extra_count + len(additional_images) + (1 if second_image else 0)


def apply_artwork_image_edits(artwork, form, existing_images, replacement_images, request):
    remove_image_ids = set(request.POST.getlist("remove_image"))
    remove_main_image = request.POST.get("remove_main_image") and not form.cleaned_data.get("main_image")

    if remove_main_image and artwork.main_image:
        artwork.main_image.delete(save=False)
        artwork.main_image = None
        artwork.save(update_fields=["main_image"])

    for image in existing_images:
        image_id = str(image.pk)

        if image_id in remove_image_ids:
            image.image.delete(save=False)
            image.delete()
            continue

        replacement_image = replacement_images.get(image.pk)

        if replacement_image:
            image.image.delete(save=False)
            image.image = replacement_image
            image.save(update_fields=["image"])


def sort_artworks(artworks, sort):
    if sort == 'price_low':
        return artworks.order_by('starting_bid', '-listing_date', '-id')
    if sort == 'price_high':
        return artworks.order_by('-starting_bid', '-listing_date', '-id')
    if sort == 'title_az':
        return artworks.order_by('title', '-listing_date', '-id')
    if sort == 'title_za':
        return artworks.order_by('-title', '-listing_date', '-id')

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


def get_marketplace_back_url(request, category):
    return get_safe_back_url(request, "category_list")


def get_page_url(page_number, pagination_query):
    if pagination_query:
        return f"?{pagination_query}&page={page_number}"

    return f"?page={page_number}"


def expand_filter_values(field_name, values):
    expanded_values = set(values)

    if field_name == "painting_medium":
        for value in values:
            cleaned_value = Artwork.clean_medium_label(value)
            expanded_values.add(cleaned_value)

            if cleaned_value == value and value not in {"Gouache", "Encaustic", "Tempera", "Fresco", "Ink", "Charcoal", "Chalk", "Graphite", "Other"}:
                expanded_values.add(f"{value} painting")
                expanded_values.add(f"{value} Painting")

    return [value for value in expanded_values if value]


def apply_any_field_filter(artworks, field_values):
    field_query = Q()

    for field_name, values in field_values:
        selected_values = expand_filter_values(
            field_name,
            [value for value in values if value],
        )

        if selected_values:
            field_query |= Q(**{f"{field_name}__in": selected_values})

    if not field_query:
        return artworks

    return artworks.filter(field_query)


def range_filter_value(value, default_value):
    if value in (None, "", default_value):
        return None

    return value


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

    if not artwork.is_sold:
        artwork.is_sold = True
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

    if mediums_selected and medium_field:
        artworks = apply_any_field_filter(artworks, ((medium_field, mediums_selected),))
    elif mediums_selected:
        artworks = apply_any_field_filter(artworks, (
            ("painting_medium", mediums_selected),
            ("sculpture_material", mediums_selected),
            ("furniture_material", mediums_selected),
            ("photo_technique", mediums_selected),
        ))
    if styles_selected and style_field:
        artworks = apply_any_field_filter(artworks, ((style_field, styles_selected),))
    elif styles_selected:
        artworks = apply_any_field_filter(artworks, (
            ("painting_style", styles_selected),
            ("sculpture_style", styles_selected),
            ("furniture_style", styles_selected),
            ("photo_style", styles_selected),
        ))
    if editions_selected:
        artworks = artworks.filter(edition__in=editions_selected)
    artworks = apply_status_filter(artworks, statuses_selected)
    year_from = range_filter_value(year_from, "1300")
    year_to = range_filter_value(year_to, "2026")

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

    paginator = Paginator(artworks, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    heading = f'Search results for "{query}"' if query else category or "All Artworks"
    clear_filters_url = reverse("artwork_list")

    if category or query:
        clear_query = request.GET.copy()
        clear_query.clear()

        if category:
            clear_query["category"] = category
        if query:
            clear_query["q"] = query

        clear_filters_url = f"{clear_filters_url}?{clear_query.urlencode()}"

    sort_options = (
        ("relevance", "Sort by: Relevance", sort in ("", "relevance")),
        ("price_low", "Sort by: Price (low to high)", sort == "price_low"),
        ("price_high", "Sort by: Price (high to low)", sort == "price_high"),
        ("title_az", "Sort by: A-Z", sort == "title_az"),
        ("title_za", "Sort by: Z-A", sort == "title_za"),
    )
    status_filter_options = [
        (value, label, value in statuses_selected)
        for value, label in (
            ("available", "Available"),
            ("sold", "Sold"),
        )
    ]
    medium_filter_options = [
        (value, label, value in mediums_selected)
        for value, label in mediums
    ]
    style_filter_options = [
        (value, label, value in styles_selected)
        for value, label in styles
    ]

    for artwork in page_obj:
        artwork.listing_date_display = date_format(artwork.listing_date, "M j, Y")
        artwork.status_class = "is-sold" if artwork.is_sold or artwork.sold_by_bid else "is-available"
        artwork.status_label = "Sold" if artwork.is_sold or artwork.sold_by_bid else "Available"

    pagination_query_string = pagination_query.urlencode()
    previous_page_url = (
        get_page_url(page_obj.previous_page_number(), pagination_query_string)
        if page_obj.has_previous()
        else ""
    )
    next_page_url = (
        get_page_url(page_obj.next_page_number(), pagination_query_string)
        if page_obj.has_next()
        else ""
    )

    return render(request, 'artworks/artwork_marketplace.html', {
        'artworks': artworks,
        'query': query,
        'category': category,
        'clear_filters_url': clear_filters_url,
        'heading': heading,
        'marketplace_back_url': get_marketplace_back_url(request, category),
        'styles': featured_styles,
        'show_style_shortcuts': show_style_shortcuts,
        'filter_styles': style_filter_options,
        'mediums': medium_filter_options,
        'selected_categories': categories_selected,
        'selected_styles': styles_selected,
        'selected_mediums': mediums_selected,
        'selected_editions': editions_selected,
        'selected_statuses': statuses_selected,
        'status_choices': status_filter_options,
        'page_obj': page_obj,
        'next_page_url': next_page_url,
        'pagination_query': pagination_query_string,
        'previous_page_url': previous_page_url,
        'sort': sort,
        'sort_options': sort_options,
    })


def home_view(request):
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
    highest_bid = highest_bids.first()
    has_accepted_bid = Bid.objects.filter(
        artwork=artwork,
        status__in=[Bid.Status.ACCEPTED, Bid.Status.FINALIZED],
    ).exists()
    has_finalized_bid = Bid.objects.filter(
        artwork=artwork,
        status=Bid.Status.FINALIZED,
    ).exists()
    is_artwork_sold = artwork.is_sold or has_accepted_bid or has_finalized_bid
    is_bidding_locked = has_accepted_bid and not has_finalized_bid

    if (has_accepted_bid or has_finalized_bid) and not artwork.is_sold:
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
    short_description = Truncator(artwork.description).words(35) if artwork.description else ""
    listing_date_display = date_format(artwork.listing_date, "M j, Y")

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
            highest_bid = highest_bids.first()

            return render(request, "artworks/artwork_detail.html", {

                "artwork": artwork,
                "primary_image": artwork.primary_image,
                "extra_images": extra_images,
                "can_edit_artwork": can_edit_artwork,
                "is_artwork_sold": is_artwork_sold,
                "is_bidding_locked": is_bidding_locked,
                "has_accepted_bid": has_accepted_bid,
                "listing_date_display": listing_date_display,
                "short_description": short_description,
                "show_description_toggle": show_description_toggle,
                "form": form,
                "existing_bid": existing_bid,
                "is_resubmission": is_resubmission,
                "show_popup": True,
                "bid_popup_message": "success",
                "highest_bid": highest_bid,
                "highest_bids": highest_bids,
                "back_url": back_url,
            })

        return render(request, "artworks/artwork_detail.html", {
            "artwork": artwork,
            "primary_image": artwork.primary_image,
            "extra_images": extra_images,
            "can_edit_artwork": can_edit_artwork,
            "is_bidding_locked": is_bidding_locked,
            "listing_date_display": listing_date_display,
            "short_description": short_description,
            "show_description_toggle": show_description_toggle,
            "form": form,
            "existing_bid": existing_bid,
            "show_popup": True,
            "bid_popup_message": "minimum_bid_error",
            "highest_bid": highest_bid,
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
        "listing_date_display": listing_date_display,
        "short_description": short_description,
        "show_description_toggle": show_description_toggle,
        "form": form,
        "existing_bid": existing_bid,
        "highest_bid": highest_bid,
        "highest_bids": highest_bids,
        "back_url": back_url,
    })


@login_required
def add_artwork(request):
    seller = getattr(request.user, "seller", None)

    if seller is None:
        return redirect("become_seller")

    back_url = get_safe_back_url(request, "profile")

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
        "back_url": back_url,
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

    back_url = get_safe_back_url(request, "profile")
    existing_images = list(artwork.images.all())

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            try:
                replacement_images = clean_replacement_artwork_images(request, existing_images)
            except forms.ValidationError as error:
                form.add_error(None, error)
            else:
                if edited_artwork_photo_count(artwork, form, existing_images, request) < 2:
                    form.add_error(None, "You have to have at least 2 photos.")
                else:
                    artwork = form.save()
                    apply_artwork_image_edits(
                        artwork,
                        form,
                        existing_images,
                        replacement_images,
                        request,
                    )
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
        "existing_images": existing_images,
        "back_url": back_url,
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
        (category.value, category.label, BUILT_IN_CATEGORY_IMAGES.get(category.value))
        for category in Artwork.Category
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
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    sort = request.GET.get('sort', 'relevance')

    artworks = annotate_sold_by_bid(Artwork.objects.all())

    artworks = apply_title_search(artworks, query)
    if categories_selected:
        artworks = artworks.filter(category__in=categories_selected)
    artworks = apply_any_field_filter(artworks, (
        ("painting_medium", legacy_mediums_selected + painting_mediums_selected),
        ("sculpture_material", legacy_mediums_selected + sculpture_materials_selected),
        ("furniture_material", legacy_mediums_selected + furniture_materials_selected),
        ("photo_technique", legacy_mediums_selected + photo_techniques_selected),
    ))
    artworks = apply_any_field_filter(artworks, (
        ("painting_style", legacy_styles_selected + painting_styles_selected),
        ("sculpture_style", legacy_styles_selected + sculpture_styles_selected),
        ("furniture_style", legacy_styles_selected + furniture_styles_selected),
        ("photo_style", legacy_styles_selected + photo_styles_selected),
    ))
    if editions_selected:
        artworks = artworks.filter(edition__in=editions_selected)
    artworks = apply_status_filter(artworks, statuses_selected)
    year_from = range_filter_value(year_from, "1300")
    year_to = range_filter_value(year_to, "2026")
    price_from = range_filter_value(price_from, "0")
    price_to = range_filter_value(price_to, "100000")

    if year_from:
        artworks = artworks.filter(year__gte=year_from)
    if year_to:
        artworks = artworks.filter(year__lte=year_to)
    if price_from:
        artworks = artworks.filter(starting_bid__gte=price_from)
    if price_to:
        artworks = artworks.filter(starting_bid__lte=price_to)

    artworks = sort_artworks(artworks, sort)
    paginator = Paginator(artworks, 24)
    page_obj = paginator.get_page(request.GET.get("page"))
    pagination_query = request.GET.copy()
    pagination_query.pop("page", None)

    return render(request, 'artworks/see_all.html', {
        'artworks': page_obj,
        'page_obj': page_obj,
        'pagination_pages': paginator.get_elided_page_range(page_obj.number),
        'pagination_query': pagination_query.urlencode(),
        'categories': [(category.value, category.label) for category in Artwork.Category],
        'editions': Artwork.Edition.choices,
        'painting_mediums': Artwork.PaintingMedium.choices,
        'sculpture_materials': Artwork.SculptureMaterial.choices,
        'furniture_materials': Artwork.FurnitureMaterial.choices,
        'photo_techniques': Artwork.PhotoTechnique.choices,
        'painting_styles': Artwork.PaintingStyle.choices,
        'sculpture_styles': Artwork.SculptureStyle.choices,
        'furniture_styles': Artwork.FurnitureStyle.choices,
        'photo_styles': Artwork.PhotoStyle.choices,
        'selected_categories': categories_selected,
        'selected_painting_mediums': painting_mediums_selected,
        'selected_sculpture_materials': sculpture_materials_selected,
        'selected_furniture_materials': furniture_materials_selected,
        'selected_photo_techniques': photo_techniques_selected,
        'selected_painting_styles': painting_styles_selected,
        'selected_sculpture_styles': sculpture_styles_selected,
        'selected_furniture_styles': furniture_styles_selected,
        'selected_photo_styles': photo_styles_selected,
        'selected_editions': editions_selected,
        'selected_statuses': statuses_selected,
        'status_choices': (
            ("available", "Available"),
            ("sold", "Sold"),
        ),
        'query': query,
        'price_from': price_from,
        'price_to': price_to,
        'sort': sort,
    })
