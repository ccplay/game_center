# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import ListView

from apksite.apis import ApiFactory, ApiResponseException
from apksite.views.base import ApiParamFilterBackendViewMixin, pageobj_with_visible_range, PRODUCT
from apksite.views.filters import BaseParamFilterBackend, PaginatorParamFilterBackend


class VenderParamFilterBackend(BaseParamFilterBackend):

    def filter_params(self, request, *args, **kwargs):
        author_id = request.GET.get('author') or kwargs.get('author_id')
        if not author_id:
            raise Http404()
        return dict(author_id=author_id)


class VenderView(ApiParamFilterBackendViewMixin,
                 ListView):

    context_object_name = 'packages'
    paginate_by = 18

    filter_param_backends = (
        VenderParamFilterBackend,
        PaginatorParamFilterBackend,
    )

    template_name = 'apksite/pages/vender/index.html'

    product = PRODUCT

    def get_queryset(self):
        api = ApiFactory.factory('author.packageList')
        params = self.filter_params(self.request, *self.args, **self.kwargs)
        return self.api_list_result_class(api=api, name=api.name, params=params)

    def get_vender_list(self):
        api = ApiFactory.factory('vender.getList')
        try:
            resposne = api.request()
            venders = api.get_response_data(response=resposne, name=api.name)
        except ApiResponseException as e:
            raise Http404()

        return venders

    def get_context_data(self, **kwargs):
        kwargs = super(VenderView, self).get_context_data(**kwargs)
        kwargs['product'] = self.product
        kwargs['page_obj'] = pageobj_with_visible_range(kwargs['page_obj'],
                                                        max_paging_links=10)
        return kwargs

    def pre_context_data(self):
        kwargs = dict()
        kwargs['vender_list'] = self.get_vender_list()
        author_id = self.request.GET.get('author') or self.kwargs.get('author_id')
        try:
            if not author_id:
                kwargs['author_id'] = kwargs['vender_list'][0]['id']
            else:
                self.kwargs['author_id'] = kwargs['author_id'] = int(author_id)
        except:
            raise Http404()
        kwargs['current_author_id'] = kwargs.get('author_id')
        return kwargs

    def get(self, request, *args, **kwargs):
        context_kwargs = self.pre_context_data()
        self.kwargs['author_id'] = context_kwargs['author_id']
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404()
        context = self.get_context_data(object_list=self.object_list, **context_kwargs)
        return self.render_to_response(context)
