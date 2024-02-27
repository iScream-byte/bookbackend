from project.apps.lib.custom.custom_serializers import FlexFieldsModelSerializer, CustomURIField
from core.models import BookList, Author, Genre, Publisher, Author
from rest_framework.serializers import ModelSerializer


class GenreSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    expandable_fields = {
        "genre": (GenreSerializer, {"source": "genre"}),
    }


class PublisherSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class BookListSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = BookList
        fields = '__all__'

    expandable_fields = {
        "author": (AuthorSerializer, {"source": "author"}),
        }
