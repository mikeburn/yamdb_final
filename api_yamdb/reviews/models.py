from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True
    )

    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )

    role = models.CharField(
        max_length=15,
        default=USER,
        choices=USER_ROLES,
        verbose_name='Роль'
    )

    confirmation_code = models.TextField(
        'Код подтверждения',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return str(self.username)


class Category(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    slug = models.SlugField(max_length=50,
                            verbose_name='Слаг',
                            unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    slug = models.SlugField(max_length=50,
                            verbose_name='Слаг',
                            unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=256,
                            db_index=True,
                            verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    description = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='Описание')

    category = models.ForeignKey(
        Category,
        related_name='titles',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )

    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        verbose_name='Оценка произведения',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Обзор'

        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            )
        ]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ревью'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
