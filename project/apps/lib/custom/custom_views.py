from django.db.models.query import QuerySet
from project.apps.lib.custom.filter_backends import FlexFieldsFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_extensions.mixins import NestedViewSetMixin


class DestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        if self.service_class:
            self.service_class(instance).delete()
        else:
            instance.delete()


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        if self.service_class:
            instance = self.service_class().create(request.data)
            serializer = self.get_serializer(instance)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params.get('no-pagination'):
            self.pagination_class = None
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if self.service_class:
            instance = self.service_class(instance).update(request.data, partial=partial)
            serializer = self.get_serializer(instance)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class RelationalGenericViewSet(
    NestedViewSetMixin,
    viewsets.GenericViewSet
):
    filter_backends = (FlexFieldsFilterBackend,)

    permit_list_expands = []
    _expandable = True
    _force_expand = []

    def get_serializer_class(self):
        """ Dynamically adds properties to serializer_class from request's GET params. """
        expand = None
        # fields = None
        # is_valid_request = (
        #         hasattr(self, "request") and self.request and self.request.method == "GET"
        # )

        # if not is_valid_request:
        #     return self.serializer_class

        fields = self.request.query_params.get("fields")
        if not fields and hasattr(self, "fields"):
            fields = self.fields
        fields = fields.split(",") if fields else None

        if self._expandable:
            expand = self.request.query_params.get("expand")
            if not expand and hasattr(self, "expand"):
                expand = self.expand
            expand = expand.split(",") if expand else None
        elif len(self._force_expand) > 0:
            expand = self._force_expand
        if self.serializer_class:
            return type(
                str("Serializer"),
                (self.serializer_class,),
                {"expand": expand, "include_fields": fields},
            )
        else:
            return None

    def get_queryset(self):
        if hasattr(self, 'custom_queryset') and self.custom_queryset:
            return self.custom_queryset()
        assert self.queryset is not None, (
            f"'{self.__class__.__name__}' should either include "
            f"a `queryset` attribute, or override the `get_queryset()` method."
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        filter_kwargs = {}
        if hasattr(self, "relational_filter"):
            for key, value in self.relational_filter.items():
                filter_kwargs.update({key: self.kwargs[value]})
            queryset = queryset.filter(**filter_kwargs)
        return queryset

    def make_request_mutable(self, request):
        if hasattr(request.data, "_mutable"):
            request.data._mutable = True
        if hasattr(request.GET, "_mutable"):
            request.GET._mutable = True


class ListViewSet(
    ListModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListRetrieveUpdateViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `list`, `retrive` and `update` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class CreateViewSet(
    CreateModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `create` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListCreateViewSet(
    CreateModelMixin,
    ListModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `create`, `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class RetrieveViewSet(
    RetrieveModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class RetrieveUpdateViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, `update` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class RetrieveDestroyViewSet(
    RetrieveModelMixin,
    DestroyModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class RetrieveUpdateDestroyViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, `update`, `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListCreateRetrieveUpdateDestroyViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RelationalGenericViewSet,
):
    def get_serializer_context(self):
        return {"request": self.request}

    """
    A viewset that provides `retrieve`, `update`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListRetrieveViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, `update`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListCreateRetrieveUpdateViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    RelationalGenericViewSet,
):
    """
    A viewset that provides `retrieve`, `update`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListCreateRetrieveViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, `update`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class ListRetrieveUpdateDestroyViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, `update`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class CreateRetrieveUpdateViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    RelationalGenericViewSet
):
    """
    A viewset that provides `retrieve`, `update`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass
