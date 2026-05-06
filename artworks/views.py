from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArtworkForm
from .models import Artwork
from .models import Seller

def add_artwork(request):
    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)

        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.seller = Seller.objects.get(user=request.user)
            artwork.save()
            return redirect("home")
    else:
        form = ArtworkForm()

    return render(request, "artworks/artworks_form.html", {"form": form})

def artwork_list(request):
    artworks = Artwork.objects.all()
    return render(request, "artworks/artwork_list.html", {"artworks": artworks})

def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request, "artworks/artwork_detail.html", {"artwork": artwork})