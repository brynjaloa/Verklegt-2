from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import ArtworkForm
from .models import Artwork, ArtworkImage

from bids.models import Bid
from bids.forms import BidForm

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


def artwork_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    styles_selected = request.GET.getlist('style')
    mediums_selected = request.GET.getlist('medium')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')

    artworks = Artwork.objects.all()


    for artwork in artworks:
        highest_bid = Bid.objects.filter(artwork=artwork).order_by("-bid_price").first()
        artwork.highest_bid = highest_bid

    if query:
        artworks = artworks.filter(title__icontains=query)

    if category:
        artworks = artworks.filter(category=category)

    category_fields = CATEGORY_FILTER_FIELDS.get(category, {})
    style_field = category_fields.get("style")
    medium_field = category_fields.get("medium")

    if styles_selected and style_field:
        artworks = artworks.filter(**{f"{style_field}__in": styles_selected})
    if mediums_selected and medium_field:
        artworks = artworks.filter(**{f"{medium_field}__in": mediums_selected})
    if year_from:
        artworks = artworks.filter(year__gte=year_from)
    if year_to:
        artworks = artworks.filter(year__lte=year_to)

    styles = category_fields.get("styles", [])
    featured_styles = FEATURED_CATEGORY_STYLES.get(category, styles)
    mediums = category_fields.get("mediums", [])

    return render(request, 'artworks/artwork_marketplace.html', {
        'artworks': artworks,
        'query': query,
        'category': category,
        'styles': featured_styles,
        'filter_styles': styles,
        'mediums': mediums,
        'selected_styles': styles_selected,
        'selected_mediums': mediums_selected,
    })


def home_view(request):
    recent_artworks = Artwork.objects.filter(is_sold=False).order_by("-listing_date", "-id")[:10]

    return render(request, "home.html", {
        "recent_artworks": recent_artworks,
    })


def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    highest_bids = Bid.objects.filter(artwork=artwork).order_by("-bid_price")[:3]
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
        ).first()

    if request.method == "POST":
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
            bid.save()
            existing_bid = bid

            return render(request, "artworks/artwork_detail.html", {

                "artwork": artwork,
                "primary_image": artwork.primary_image,
                "extra_images": extra_images,
                "can_edit_artwork": can_edit_artwork,
                "show_description_toggle": show_description_toggle,
                "form": form,
                "existing_bid": existing_bid,
                "show_popup": True,
                "bid_popup_message": "success",
                "highest_bids": highest_bids,
            })

        return render(request, "artworks/artwork_detail.html", {
            "artwork": artwork,
            "primary_image": artwork.primary_image,
            "extra_images": extra_images,
            "can_edit_artwork": can_edit_artwork,
            "show_description_toggle": show_description_toggle,
            "form": form,
            "existing_bid": existing_bid,
            "show_popup": True,
            "bid_popup_message": "minimum_bid_error",
            "highest_bids": highest_bids,
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
        "show_description_toggle": show_description_toggle,
        "form": form,
        "existing_bid": existing_bid,
        "highest_bids": highest_bids,
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

    artwork.delete()
    return redirect("profile")


def category_list(request):
    categories = Artwork.Category.choices
    return render(request, 'Category/categories.html', {'categories': categories})

def artwork_see_all(request):
    mediums_selected = request.GET.getlist('medium')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    categories_selected = request.GET.getlist('category')
    styles_selected = request.GET.getlist('style')
    editions_selected = request.GET.getlist('edition')

    artworks = Artwork.objects.all()

    if categories_selected:
        artworks = artworks.filter(category__in=categories_selected)
    if mediums_selected:
        artworks = artworks.filter(
            Q(painting_medium__in=mediums_selected)
            | Q(sculpture_material__in=mediums_selected)
            | Q(furniture_material__in=mediums_selected)
            | Q(photo_technique__in=mediums_selected)
        )
    if styles_selected:
        artworks = artworks.filter(
            Q(painting_style__in=styles_selected)
            | Q(sculpture_style__in=styles_selected)
            | Q(furniture_style__in=styles_selected)
            | Q(photo_style__in=styles_selected)
        )
    if editions_selected:
        artworks = artworks.filter(edition__in=editions_selected)
    if year_from:
        artworks = artworks.filter(year__gte=year_from)
    if year_to:
        artworks = artworks.filter(year__lte=year_to)

    artworks = artworks.order_by("-listing_date", "-id")
    paginator = Paginator(artworks, 24)
    page_obj = paginator.get_page(request.GET.get("page"))
    pagination_query = request.GET.copy()
    pagination_query.pop("page", None)

    all_styles = list({label: value for value, label in (
            list(Artwork.PaintingStyle.choices) +
            list(Artwork.SculptureStyle.choices) +
            list(Artwork.FurnitureStyle.choices) +
            list(Artwork.PhotoStyle.choices)
    )}.items())

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
        'all_styles': all_styles,
        'selected_categories': categories_selected,
        'selected_mediums': mediums_selected,
        'selected_styles': styles_selected,
        'selected_editions': editions_selected,
    })

@login_required
def accept_bid(request, bid_id):

    bid = get_object_or_404(Bid, id=bid_id)

    if bid.artwork.seller != request.user.seller:
        return HttpResponseForbidden()

    bid.status = "Accepted"
    bid.save()

    return redirect(
        "artwork_detail",
        pk=bid.artwork.id
    )
