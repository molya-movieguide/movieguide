from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import TimeStampedModel
from people.models import Person


class Genre(TimeStampedModel):
    name = models.CharField("Атауы", max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанрлар"

    def __str__(self):
        return self.name


class Movie(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Жарияланған"

    title = models.CharField("Атауы", max_length=200)
    slug = models.SlugField(unique=True)
    year = models.PositiveSmallIntegerField(
        "Шыққан жылы",
        validators=[MinValueValidator(1888), MaxValueValidator(2100)],
    )
    rating = models.DecimalField(
        "Рейтинг",
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    duration = models.PositiveSmallIntegerField("Ұзақтығы (минут)")
    description = models.TextField("Қысқаша мазмұны")
    poster = models.ImageField("Постер", upload_to="posters/", blank=True)
    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="directed_movies",
        verbose_name="Режиссер",
    )
    genres = models.ManyToManyField(
        Genre, related_name="movies", verbose_name="Жанрлар"
    )
    cast = models.ManyToManyField(
        Person,
        through="MovieCast",
        related_name="acted_in",
        verbose_name="Актерлер",
    )
    status = models.CharField(
        "Статусы",
        max_length=10,
        choices=Status.choices,
        default=Status.PUBLISHED,
    )

    class Meta:
        ordering = ["-year", "title"]
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмдер"
        indexes = [
            models.Index(fields=["year"]),
            models.Index(fields=["rating"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=0) & models.Q(rating__lte=10),
                name="movie_rating_0_10",
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.year})"


class MovieCast(TimeStampedModel):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="cast_members"
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="roles"
    )
    character_name = models.CharField("Рөл аты", max_length=200, blank=True)
    order = models.PositiveSmallIntegerField("Реті", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Актер құрамы"
        verbose_name_plural = "Актер құрамы"
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "person"], name="unique_movie_person"
            ),
        ]

    def __str__(self):
        return f"{self.person} → {self.movie}"