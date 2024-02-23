from django.urls import path, include
from .views import Test, BookListViewSet, PublishersViewset, AuthorViewSet, BookListViewSetUnderAuthors, \
    ReturnUserNameExistsViewSet
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter

main_router = SimpleRouter()

book_router = main_router.register('all-books', BookListViewSet, basename="all_books")
author_router = main_router.register('all-authors', AuthorViewSet, basename="all_authors")

book_router.register("publishers",
                     PublishersViewset,
                     basename="publisher",
                     parents_query_lookups=["boi_id"])

author_router.register("books",
                       BookListViewSetUnderAuthors,
                       basename="booksbyauthor",
                       parents_query_lookups=["lekhok_id"])

urlpatterns = [
    path('test', Test.as_view()),
    path('check-username/', ReturnUserNameExistsViewSet.as_view())
]
urlpatterns = urlpatterns + main_router.urls
