from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ArtworkForm
from .models import Artwork, ArtworkImage

def artwork_list(request):
    category = request.GET.get('category')
    style = request.GET.get('style')
    medium = request.GET.get('medium')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')

    artworks = Artwork.objects.all()

    if category:
        artworks = artworks.filter(category=category)
    if style:
        if category == 'Paintings':
            artworks = artworks.filter(painting_style=style)
        elif category == 'Sculptures':
            artworks = artworks.filter(sculpture_style=style)
        elif category == 'Furniture':
            artworks = artworks.filter(furniture_style=style)
        elif category == 'Photos':
            artworks = artworks.filter(photo_style=style)
    if medium:
        if category == 'Paintings':
            artworks = artworks.filter(painting_medium=medium)
        elif category == 'Sculptures':
            artworks = artworks.filter(sculpture_material=medium)
        elif category == 'Furniture':
            artworks = artworks.filter(furniture_material=medium)
        elif category == 'Photos':
            artworks = artworks.filter(photo_technique=medium)
    if year_from:
        artworks = artworks.filter(year__gte=year_from)
    if year_to:
        artworks = artworks.filter(year__lte=year_to)

    styles = []
    mediums = []

    if category == 'Paintings':
        styles = Artwork.PaintingStyle.choices
        mediums = Artwork.PaintingMedium.choices
    elif category == 'Sculptures':
        styles = Artwork.SculptureStyle.choices
        mediums = Artwork.SculptureMaterial.choices
    elif category == 'Furniture':
        styles = Artwork.FurnitureStyle.choices
        mediums = Artwork.FurnitureMaterial.choices
    elif category == 'Photos':
        styles = Artwork.PhotoStyle.choices
        mediums = Artwork.PhotoTechnique.choices

    return render(request, 'artworks/artwork_marketplace.html', {
        'artworks': artworks,
        'category': category,
        'styles': styles,
        'mediums': mediums,
    })


def home_view(request):
    recent_artworks = Artwork.objects.filter(is_sold=False).order_by("-listing_date", "-id")[:4]

    return render(request, "home.html", {
        "recent_artworks": recent_artworks,
    })


def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    extra_images = list(artwork.images.all())

    if not artwork.main_image and extra_images:
        extra_images = extra_images[1:]

    return render(request, "artworks/artwork_detail.html", {
        "artwork": artwork,
        "primary_image": artwork.primary_image,
        "extra_images": extra_images,
    })


@login_required
def add_artwork(request):
    if not hasattr(request.user, "seller"):
        return redirect("become_seller")

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.seller = request.user.seller
            artwork.save()
            ArtworkImage.objects.create(artwork=artwork, image=form.cleaned_data["second_image"])
            for image in form.cleaned_data["additional_images"]:
                ArtworkImage.objects.create(artwork=artwork, image=image)
            return redirect("artwork_detail", pk=artwork.pk)
    else:
        form = ArtworkForm()

    return render(request, "artworks/artworks_form.html", {"form": form, "form_title": "Add Artwork", "button_text": "Add Artwork"})


@login_required
def edit_artwork(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)

    if not hasattr(request.user, "seller") or artwork.seller != request.user.seller:
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


def category_list(request):
    categories = Artwork.Category.choices
    return render(request, 'Category/categories.html', {'categories': categories})
