from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):

    def load_users(self):
        for row in DictReader(
                open('../../../static/data/users.csv',
                     encoding='utf-8-sig')
        ):
            user = User(
                id=row['id'], username=row['username'],
                email=row['email'], role=row['role'],
                bio=row['bio'], first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()

    def load_categories(self):
        for row in DictReader(
                open('../../../static/data/category.csv',
                     encoding='utf-8-sig')
        ):
            category = Category(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            category.save()

    def load_genres(self):
        for row in DictReader(
                open('../../../static/data/genre.csv',
                     encoding='utf-8-sig')
        ):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()

    def load_titles(self):
        for row in DictReader(
                open('../../../static/data/titles.csv',
                     encoding='utf-8-sig')
        ):
            title = Title(
                id=row['id'], name=row['name'],
                year=row['year'], category_id=row['category']
            )
            title.save()

    def load_reviews(self):
        for row in DictReader(
                open('../../../static/data/review.csv',
                     encoding='utf-8-sig')
        ):
            review = Review(
                id=row['id'], title_id=row['title_id'],
                text=row['text'], author_id=row['author'],
                score=row['score'], pub_date=row['pub_date']
            )
            review.save()

    def load_comments(self):
        for row in DictReader(
                open('../../../static/data/comments.csv',
                     encoding='utf-8-sig')
        ):
            comment = Comment(
                id=row['id'], review_id=row['review_id'],
                text=row['text'], author_id=row['author'],
                pub_date=row['pub_date']
            )
            comment.save()

    def handle(self, *args, **options):
        self.load_users()
        self.load_categories()
        self.load_genres()
        self.load_titles()
        self.load_reviews()
        self.load_comments()
