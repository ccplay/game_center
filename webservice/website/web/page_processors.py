# -*- coding: utf-8 -*-
from django.http import Http404
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category, Topic
from toolkit.helpers import get_global_site
from django.core.exceptions import ObjectDoesNotExist
from warehouse.models import Author

__all__ = ['vendors_fill', 'category_fill', 'ranking_fill']


def category_fill(request, page):
    cat_slug = 'game'
    if page.slug.endswith('game'):
        cat_slug = 'game'
    if page.slug.endswith('application'):
        cat_slug = 'application'

    root = Category.all_objects.get_cache_by_slug(site_id=get_global_site().pk,
                                                  slug=cat_slug)
    cat_pk = request.GET.get('category')
    category = None
    if cat_pk:
        category = Category.objects.get_cache_by(cat_pk)
    if not category:
        category = root

    topic_pk = request.GET.get('topic')
    topic = None
    if topic_pk:
        topic = Topic.objects.get_cache_by(topic_pk)

    data = dict(
        category=category,
        topic=topic,
        root_category=root,
        lang=request.GET.get('lang')
    )
    return data

processor_for('game')(category_fill)
processor_for('application')(category_fill)

@processor_for('vendors')
def vendors_fill(request, page):
    author_pk = request.GET.get('author')
    if not author_pk:
        author = None
    else:
        try:
            author = Author.objects.get(pk=author_pk)
        except ObjectDoesNotExist:
            author = None
    return dict(
        author=author
    )


def ranking_fill(request, page):
    if page.slug == 'ranking':
        cat_slug = 'game'
    else:
        cat_slug = page.slug.split('/')[1]
    category = Category.objects.get_cache_by_slug(get_global_site().pk, slug=cat_slug)

    return dict(
        category=category
    )

processor_for('ranking')(ranking_fill)
processor_for('ranking/game')(ranking_fill)
processor_for('ranking/application')(ranking_fill)
