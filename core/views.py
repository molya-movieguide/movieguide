from django.views.generic import ListView

from movies.models import Movie


class HomeView(ListView):
    template_name = "core/home.html"
    context_object_name = "movies"

    def get_queryset(self):
        return (
            Movie.objects.filter(status=Movie.Status.PUBLISHED)
            .select_related("director")
            .order_by("-rating")[:12]
        )