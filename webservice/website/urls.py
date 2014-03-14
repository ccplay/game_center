# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

slug_pattern = '[\w_.-]+'
urlpatterns = patterns('website.views',
        url(r'^packages/(?P<package_name>%s)(/(?P<version_name>%s)?)?' % (slug_pattern, slug_pattern),
            'packageversion_detail', name='packageversion_detail'),
        url(r'^download/packageversion/(?P<pk>\d+)(/(?P<filetype>\w+)?)?',
            'download_packageversion', name='download_packageversion'),
        url(r'^download/package/(?P<package_name>%s)'
            '(/(?P<version_name>%s)?)?(/(?P<filetype>\w+)?)?' % (slug_pattern, slug_pattern),
            'download_package', name='download_package'),
        url(r'^categories/$', 'category_package_list', name='category_default_page'),
        url(r'^categories/(?P<slug>%s)' % slug_pattern, 'category_package_list', name='category_package_list'),
        url(r'^masterpiece/$', 'masterpiece_view', name='masterpiece_page'),
        url(r'^topics/$', 'topics_view', name='topics_page'),
        url(r'^topics/(?P<slug>%s)' % slug_pattern, 'topic_package_list', name='topic_package_list'),
        url(r'^feedbacks/cdn/(?P<slug>%s)' % slug_pattern, 'cdn_feedback', name='cdn_feedback'),

)

