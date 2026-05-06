from django.shortcuts import render, get_object_or_404
from .models import Artwork

def artwork_list(request):
    category = request.GET.get('category')
    medium = request.GET.get('medium')
    style = request.GET.get('style')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')

    artworks = Artwork.objects.all()

    if category:
        artworks = artworks.filter(category=category)
    if medium:
        artworks = artworks.filter(painting_medium=medium)
    if style:
        artworks = artworks.filter(painting_style=style)
    if year_from:
        artworks = artworks.filter(year__gte=year_from)
    if year_to:
        artworks = artworks.filter(year__lte=year_to)

    return render(request, 'artworks/artwork_list.html', {
        'artworks': artworks,
        'category': category,
    })

def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request, "artworks/artwork_detail.html", {"artwork": artwork})

def category_list(request):
    categories = Artwork.Category.choices
    return render(request, 'Category/categories.html', {'categories': categories})