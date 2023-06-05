from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Genre, Title


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for row in DictReader(
                open('./static/data/category.csv')
        ):
            category = Category(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            category.save()
        for row in DictReader(
                open('./static/data/genre.csv')
        ):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()
        for row in DictReader(
                open('./static/data/titles.csv')
        ):
            title = Title(
                id=row['id'], name=row['name'],
                year=row['year'], category_id=row['category_id']
            )
            title.save()
