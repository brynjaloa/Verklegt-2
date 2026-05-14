from django.http import Http404
from django.shortcuts import render

from .info_articles import INFO_ARTICLES


def info_view(request):
    return render(request, "info.html", {"articles": INFO_ARTICLES})


def info_article_view(request, slug):
    article = next(
        (article_item for article_item in INFO_ARTICLES if article_item["slug"] == slug),
        None,
    )

    if article is None:
        raise Http404("Article not found")

    article = article.copy()
    article["formatted_paragraphs"] = [
        paragraph.split(":", 1)
        if ":" in paragraph
        else [None, paragraph]
        for paragraph in article["paragraphs"]
    ]

    return render(request, "info_article.html", {"article": article})
