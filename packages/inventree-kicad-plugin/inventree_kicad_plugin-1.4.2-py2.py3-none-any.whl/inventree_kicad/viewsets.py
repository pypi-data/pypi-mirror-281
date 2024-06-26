from rest_framework import generics, permissions, response, views

from InvenTree.helpers import str2bool
from part.models import PartCategory, Part


from inventree_kicad import serializers


class Index(views.APIView):
    """Index view which provides a list of available endpoints"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        """Provide an index of the available endpoints"""

        # Get the base URL for the request, and construct secondary urls based on this
        # TODO: There is probably a better way of handling this!
        base_url = request.build_absolute_uri('/plugin/kicad-library-plugin/v1/')

        return response.Response(
            data={
                'categories': base_url + 'categories/',
                'parts': base_url + 'parts/',
            }
        )


class CategoryList(generics.ListAPIView):
    """List of available KiCad categories"""

    serializer_class = serializers.KicadCategorySerializer

    def get_queryset(self):
        """Return only PartCategory objects which are mapped to a SelectedCategory"""

        from .models import SelectedCategory

        category_ids = SelectedCategory.objects.all().values_list('category_id', flat=True)

        return PartCategory.objects.filter(pk__in=category_ids)


class PartsPreviewList(generics.ListAPIView):
    """Preview list for all parts in a given category"""

    serializer_class = serializers.KicadPreviewPartSerializer

    def get_serializer(self, *args, **kwargs):
        """Add the parent plugin instance to the serializer contenxt"""

        kwargs['plugin'] = self.kwargs['plugin']

        return self.serializer_class(*args, **kwargs)

    def get_queryset(self):
        """Return a list of parts in the specified category
        
        We check if the plugin setting KICAD_ENABLE_SUBCATEGORY is enabled,
        to determine if sub-category parts should be returned also
        """

        category_id = self.kwargs.get('id', None)

        # Get a reference to the plugin instance
        plugin = self.kwargs['plugin']

        cascade = str2bool(plugin.get_setting('KICAD_ENABLE_SUBCATEGORY', False))

        queryset = Part.objects.all()

        category = PartCategory.objects.filter(id=category_id).first()

        if category is not None:
            if cascade:
                queryset = queryset.filter(
                    category__in=category.get_descendants(include_self=True)
                )
            else:
                queryset = queryset.filter(category=category)

        queryset = serializers.KicadPreviewPartSerializer.annotate_queryset(queryset)

        return queryset


class PartDetail(generics.RetrieveAPIView):
    """Detailed information endpoint for a single part instance.
    
    Here, the lookup id (pk) is the part id.
    The custom plugin serializer formats the data into a KiCad compatible format.
    """

    serializer_class = serializers.KicadDetailedPartSerializer
    queryset = Part.objects.all()

    def get_queryset(self):
        """Prefetch related fields to speed up query"""

        queryset = super().get_queryset()

        queryset = queryset.prefetch_related(
            'parameters',
        )

        return queryset

    def get_serializer(self, *args, **kwargs):
        """Add the parent plugin instance to the serializer contenxt"""

        kwargs['plugin'] = self.kwargs['plugin']
        kwargs['context'] = {'request': self.request}

        return self.serializer_class(*args, **kwargs)
