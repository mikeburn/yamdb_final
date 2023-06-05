from api.permissions import (AdminOrReadonly, AuthorModeratorAdminOrReadOnly,
                             IsAdmin, IsAnonymousGuest)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import GetListCreateDestroyMixin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleGetSerializer, TitleSerializer, TokenSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAnonymousGuest])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    try:
        user, _ = User.objects.get_or_create(
            username=username,
            email=email
        )
    except IntegrityError as error:
        raise ValidationError(
            ('Не получилось создать пользователя с данными'
                f'username={username}, email={email}')
        ) from error
    user.save()

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Добро пожаловать на YaMDB!',
        from_email='YaMDB@project.com',
        recipient_list=(user.email,),
        message=confirmation_code
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if not default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    token = RefreshToken.for_user(user)
    return Response(
        {'token': str(token.access_token)},
        status=status.HTTP_200_OK
    )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadonly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return TitleGetSerializer


class GenreViewSet(GetListCreateDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadonly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(GetListCreateDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadonly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [AuthorModeratorAdminOrReadOnly, ]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AuthorModeratorAdminOrReadOnly, ]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
