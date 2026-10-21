from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("Құрылған уақыты", auto_now_add=True)
    updated_at = models.DateTimeField("Өзгертілген уақыты", auto_now=True)

    class Meta:
        abstract = True