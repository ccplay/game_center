# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, Resolver404
from django.http import Http404
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category, Topic
from mezzanine.conf import settings

from website.ios_pc_models import get_package_by_package_name, get_packageversion_by_package
from website.ios_pc_models import get_root_category_slug_by_package, get_all_categories, get_leaf_categories
from website.ios_pc_models import filter_packages_by_category_slug, get_all_packages, get_authors_by_topic
from website.ios_pc_models import is_topic_slug, get_topic_slug, get_topic_by_slug, filter_packages_by_topic
from website.ios_pc_models import paginize_items, get_supported_language, filter_packages_by_supported_language
from website.ios_pc_models import get_category_slug, get_all_sub_cats, get_all_collections, get_packages_by_topic
from website.ios_pc_models import get_comments_by_packageversion


categories_page_slug = 'categories'
@processor_for(categories_page_slug)
def categories_fill(request, page):
    data = dict()
    if request.method == "GET":
        try:
            func, args, kwargs = resolve(request.path_info)
            # mezzine.pages.views.page contains kwargs['slug']
            # with value "categories", replace it to default category slug
            slug = kwargs.get('slug')
            if categories_page_slug == slug:
                slug = settings.GC_CATEGORIES_DEFAULT_SLUG
            if slug is None:
                slug = settings.GC_CATEGORIES_DEFAULT_SLUG
            data['category'] = Category.objects.get(slug=slug)
        except (Resolver404, Category.DoesNotExist) as e:
            raise Http404()
    return data

topics_page_slug = 'topics'
@processor_for(topics_page_slug)
def topics_fill(request, page):
    data = dict()
    if request.method == "GET":
        try:
            func, args, kwargs = resolve(request.path_info)
            slug = kwargs.get('slug')
            if topics_page_slug == slug:
                slug = settings.GC_TOPICS_CHOICE_SLUG
            if slug is None:
                slug = settings.GC_TOPICS_CHOICE_SLUG
            data['topic'] = Topic.objects.get(slug=slug)
        except (Resolver404, Topic.DoesNotExist) as e:
            raise Http404()
    return data

masterpiece_page_slug = 'masterpiece'
@processor_for(masterpiece_page_slug)
def masterpiece_fill(request, page):
    data = dict()
    if request.method == "GET":
        try:
            data['topic'] = Topic.objects.get(slug=settings.GC_TOPICS_MASTERPIECE_SLUG)
        except Topic.DoesNotExist as e:
            raise Http404()

    return data


iospc_games_page_slug = 'iospc/games'
@processor_for(iospc_games_page_slug)
def games_page(request, page):
    slug = 'game'
    other_slug = None
    package_query = 'name'
    data  = {}

    if request.method == "GET":
        all_packages = get_all_packages()
        packages = filter_packages_by_category_slug(all_packages, slug)
        category_slug, category_query = get_category_slug(request)
        if category_slug != False:
            packages = filter_packages_by_category_slug(packages, category_slug)
        elif request.GET.get('topic', None):
            other_slug = request.GET.get('topic')
            topic_slug = get_topic_slug(other_slug, slug)
            topic = get_topic_by_slug(topic_slug)
            packages = filter_packages_by_topic(packages, topic)
        elif request.GET.get('pub', None) == 'latest':
            other_slug = request.GET.get('pub')
            packages = packages.by_published_order()
        elif request.GET.get('lang', None):
            other_slug = request.GET.get('lang')
            lang = get_supported_language(other_slug)
            if lang:
                packages = filter_packages_by_supported_language(packages, lang)
            else:
                packages = []
        else:
            pass

        sub_cats = get_leaf_categories(get_all_sub_cats(slug))
        pkgs, page_query, limit_range = paginize_items(request, packages)

        data = {
            'items': pkgs,
            'slug': slug,
            'cats': sub_cats,
            'page_query': page_query,
            'category_query': category_query,
            'category_slug': category_slug,
            'other_slug': other_slug,
            'limit_range': limit_range,
            'package_query': package_query,
        }

    return data


iospc_topics_page_slug = 'iospc/topics'
@processor_for(iospc_topics_page_slug)
def topics_page(request, page):
    data  = {}

    if request.method == "GET":
        collections = get_all_collections()

        result = []
        for collection in collections:
            packages = get_packages_by_topic(collection)
            result.append({
                'collection': collection,
                'packages': packages,
            })

        items, page_query, limit_range = paginize_items(request, result, 2)

        data = {
            'items': items,
            'page_query': page_query,
            'current_page': 'collection',
            'limit_range': limit_range,
        }

    return data


iospc_masterpiece_page_slug = 'iospc/masterpiece'
@processor_for(iospc_masterpiece_page_slug)
def masterpiece_page(request, page):
    slug = 'topic-xiaomo'
    data  = {}

    if request.method == "GET":
        collection = get_topic_by_slug(slug)
        print (collection)

        if collection:
            packages = get_packages_by_topic(collection)
            print (packages)

        items, page_query, limit_range = paginize_items(request, packages, 2)
        data =  {
            'items': items,
            'page_query': page_query,
            'current_page': 'masterpiece',
            'limit_range': limit_range,
        }

    return data


iospc_vendors_page_slug = 'iospc/vendors'
@processor_for(iospc_vendors_page_slug)
def vendors_page(request, page):
    data  = {}
    slug = 'spec-top-author'
    current_vendor = None

    if request.method == "GET":
        vendors = []
        id = request.GET.get('id', None)
        try:
            pk = int(id)
        except:
            pk = None
        topic = get_topic_by_slug(slug)
        if topic:
            vendors = get_authors_by_topic(topic)
            #print (vendors.count())
            if vendors and pk:
                try:
                    current_vendor = vendors.get(pk=pk)
                except:
                    pass

        if vendors and current_vendor is None:
            current_vendor = vendors[0]

        packages = current_vendor.packages.published()
        items, page_query, limit_range = paginize_items(request, packages, 1)

        #print (len(items))
        data = {
            'current_vendor': current_vendor,
            'items': items,
            'vendors': vendors,
            'page_query': page_query,
            'current_page': 'vendor',
            'limit_range': limit_range,
        }

    return data


iospc_topic_page_slug = 'iospc/topic'
@processor_for(iospc_topic_page_slug)
def topic_page(request, page):
    data  = {}
    packages = []

    if request.method == "GET":
        slug = request.GET.get('slug', None)
        collection = get_topic_by_slug(slug)

        if collection:
            packages = get_packages_by_topic(collection)

        data = {
            'collection': collection,
            'packages': packages,
            'current_page': 'collection',
        }


    return data


iospc_package_page_slug = 'iospc/package'
@processor_for(iospc_package_page_slug)
def package_page(request, page):
    other_slug = None
    package_query = 'name'
    data  = {}

    if request.method == "GET":
        package_name = request.GET.get(package_query, None)
        pkg = get_package_by_package_name(package_name)
        all_cats = get_all_categories(pkg)
        leaf_cats = get_leaf_categories(all_cats)

        data['pkgver'] = get_packageversion_by_package(pkg)
        data['slug'] = get_root_category_slug_by_package(pkg)
        data['cats'] = leaf_cats
        data['current_page'] = data['slug']
        try:
            category = pkg.categories.all()[0]
        except:
            category = ''

        data['root_cat'] = data['slug']
        data['sub_cat_name'] = category.name if category else ''
        data['sub_cat_slug'] = category.slug if category else ''
        data['package_title'] = pkg.title if pkg.title else ''
        comments = get_comments_by_packageversion(data['pkgver'])
        items, page_query, limit_range = paginize_items(request, comments, 1)
        data['items'] = items
        data['limit_range'] = limit_range
        data['page_query'] = page_query

    return data
