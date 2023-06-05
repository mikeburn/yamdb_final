import datetime as dt

from api.validators import check_username
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        return check_username(value)


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True, max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        return check_username(value)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name', 'slug'
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = 'name', 'slug'
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        required=True, slug_field='slug',
        queryset=Category.objects.all())

    genre = serializers.SlugRelatedField(
        required=True, many=True, slug_field='slug',
        queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = [
            'id', 'name', 'year', 'description', 'genre', 'category'
        ]

    def validate_year(self, data):
        year = dt.date.today().year
        if year < data:
            raise serializers.ValidationError(
                f'Год {data} больше текущего!',
            )
        return data


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.rating

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class CommentSerializer(serializers.ModelSerializer):
    '''Сериалайзер комментариев.'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'pub_date', 'text')
        read_only_fields = ('id', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            request = self.context['request']
            author = request.user
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('Отзыв уже есть')
        return data
