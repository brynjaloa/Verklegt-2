from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ArtworkForm
from .models import Artwork

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
def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request, "artworks/artwork_detail.html", {"artwork": artwork})


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
            return redirect("artwork_detail", pk=artwork.pk)
    else:
        form = ArtworkForm()

    return render(request, "artworks/artworks_form.html", {"form": form})


def category_list(request):
    categories = Artwork.Category.choices
    return render(request, 'Category/categories.html', {'categories': categories})
