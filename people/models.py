from django.db import models

from core.models import TimeStampedModel


class Person(TimeStampedModel):
    full_name = models.CharField("Аты-жөні", max_length=200)
    slug = models.SlugField(unique=True)
    birth_date = models.DateField("Туған күні", null=True, blank=True)
    bio = models.TextField("Өмірбаяны", blank=True)
    photo = models.ImageField("Фото", upload_to="people/", blank=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Тұлға"
        verbose_name_plural = "Тұлғалар"

    def __str__(self):
        return self.full_name