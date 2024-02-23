from django.db import models


class BookList(models.Model):
    ISBN = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    author = models.ForeignKey("core.Author", related_name="books", on_delete=models.PROTECT)
    yearOfPublication = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    @property
    def getTitleInCaps(self):
        return self.title.upper()


class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, null=True, blank=True)
    born_year = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey("core.Genre", related_name="authors", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name.upper()


class Genre(models.Model):
    name = models.CharField(max_length=20)
    bengali_name = models.CharField(max_length=25)
    popular_in_countries = models.TextField()

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name.upper()


class Publisher(models.Model):
    book=models.ForeignKey("core.BookList",related_name="books",on_delete=models.PROTECT,null=True,blank=True)
    name = models.CharField(max_length=25)
    address = models.TextField()
    contact = models.IntegerField()
    country = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"

    def __str__(self):
        return self.name.upper() + " | " + self.country.upper()
