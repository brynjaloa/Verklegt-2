from django.shortcuts import render, get_object_or_404
from .models import Artwork

def artwork_list(request):
    artworks = Artwork.objects.all()
    return render(request, "artworks/artwork_list.html", {"artworks": artworks})

def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request, "artworks/artwork_detail.html", {"artwork": artwork})