from django.contrib import admin

from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birth_date")
    search_fields = ("full_name",)
    prepopulated_fields = {"slug": ("full_name",)}