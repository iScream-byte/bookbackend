from rest_framework.views import APIView
from rest_framework import filters
from project.apps.lib.custom.custom_views import *
from core.serializers import BookListSerializer, PublisherSerializer, AuthorSerializer
from rest_framework.response import Response
from core.models import BookList, Publisher, Author
from auth_user.models import User
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny



class Test(APIView):
    def get(self, request):
        return Response("API Cholchhe")


class BookListViewSet(ListRetrieveUpdateViewSet):
    model = BookList
    serializer_class = BookListSerializer
    service_class = ""
    queryset = model.objects.all()
    filter_backends = [filters.SearchFilter]
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    search_fields = [
        'author__genre__bengali_name',
        'title',
        'author__name'
    ]

    def get_queryset(self):
        queryset = self.queryset.filter()
        return queryset

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class BookListViewSetUnderAuthors(ListRetrieveViewSet):
    model = BookList
    serializer_class = BookListSerializer
    service_class = ""
    queryset = model.objects.all()
    filter_backends = [filters.SearchFilter]
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        parent_lookup_lekhok_id=self.kwargs.get("parent_lookup_lekhok_id")
        queryset = self.queryset.filter(author_id=parent_lookup_lekhok_id)
        return queryset

    relational_filter = {"book_id": "parent_lookup_lekhok_id"}

class AuthorViewSet(ListRetrieveViewSet):
    model = Author
    serializer_class = AuthorSerializer
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = model.objects.all()
    lookup_field = "id"
    def get_queryset(self):
        queryset = self.queryset.filter()
        return queryset


class PublishersViewset(ListRetrieveViewSet):
    model = Publisher
    serializer_class = PublisherSerializer
    queryset = model.objects.all()
    lookup_field = "id"
    relational_filter = {"book_id": "parent_lookup_boi_id"}

    # def get_queryset(self):
    #     print(self.relational_filter)
    #     queryset = self.queryset.filter()
    #     return queryset


class ReturnUserNameExistsViewSet(APIView):
    def post(self,request):
        username=(request.data.get("username"))
        user_object=User.objects.filter(username=username)
        print(user_object)
        if user_object.exists():
            return Response(True)
        else:
            return Response(False)
