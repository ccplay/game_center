# -*- encoding=utf-8 -*-
from warehouse.models import Package, Author

from rest_framework import viewsets, mixins, routers
from warehouse.serializers import PackageSummarySerializer,\
    PackageDetailSerializer,\
    AuthorSerializer

# ViewSets define the view behavior.
class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.published()
    serializer_class = PackageSummarySerializer

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class
        self.serializer_class = PackageDetailSerializer
        response = super(PackageViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response

class PackageNewestViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    #routes = [
    #    routers.Route(url=r'^{prefix}$',
    #          mapping={'get': 'list'},
    #          name='{basename}-list',
    #          initkwargs={'suffix': 'List'}),
    #    routers.Route(url=r'^{prefix}/{lookup}$',
    #          mapping={'get': 'retrieve'},
    #          name='{basename}-detail',
    #          initkwargs={'suffix': 'Detail'})
    #]
    queryset = Package.objects\
        .published().by_published_order(newest=True)
    serializer_class = PackageSummarySerializer

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.activated()
    serializer_class = AuthorSerializer
