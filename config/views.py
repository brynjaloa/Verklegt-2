from django.http import Http404
from django.shortcuts import render


INFO_ARTICLES = [
    {
        "slug": "buying-art-online",
        "title": "Buying Art Online",
        "image_url": "/media/Homepage/front-box-pic.jpg",
        "intro": (
            "A short introduction to what buyers should look for before placing "
            "a bid on artwork through ArtVault."
        ),
        "paragraphs": [
            (
                "This is placeholder article text. Replace this with the full "
                "article when the final text is ready."
            ),
            (
                "The article page supports multiple paragraphs, so longer text "
                "can be added without changing the page structure."
            ),
        ],
    },
    {
        "slug": "understanding-artwork-details",
        "title": "Understanding Artwork Details",
        "image_url": "/media/artworks/IMG_0476.jpg",
        "intro": (
            "Learn how details like year created, medium, style, size, and "
            "condition help buyers understand an artwork."
        ),
        "paragraphs": [
            (
                "This is placeholder article text for the full article page. "
                "You can replace it with the real article later."
            ),
            (
                "The preview on the Info page only shows the beginning, while "
                "this page shows the full article."
            ),
        ],
    },
    {
        "slug": "selling-through-artvault",
        "title": "Selling Through ArtVault",
        "image_url": "/media/artworks/IMG_0503.jpg",
        "intro": (
            "A quick guide for sellers preparing artwork listings with strong "
            "images, accurate details, and clear starting bids."
        ),
        "paragraphs": [
            (
                "This is placeholder article text for sellers. Add the final "
                "seller article here when it is ready."
            ),
            (
                "Each article can have its own image, heading, preview text, "
                "and full body text."
            ),
        ],
    },
]


def info_view(request):
    return render(request, "info.html", {"articles": INFO_ARTICLES})


def info_article_view(request, slug):
    article = next(
        (article_item for article_item in INFO_ARTICLES if article_item["slug"] == slug),
        None,
    )

    if article is None:
        raise Http404("Article not found")

    return render(request, "info_article.html", {"article": article})
