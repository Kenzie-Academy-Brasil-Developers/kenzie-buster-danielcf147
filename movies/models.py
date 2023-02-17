from django.db import models


class RatingOptions(models.TextChoices):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        choices=RatingOptions.choices, max_length=20, default=RatingOptions.G
    )
    synopsis = models.CharField(max_length=300, null=True, default=None)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies", null=False
    )

    orders = models.ManyToManyField(
        "users.User", through="movies.MovieOrder", related_name="ordered_movies"
    )

    def __repr__(self) -> str:
        return f"<Movie [{self.id}] - {self.title}>"


class MovieOrder(models.Model):
    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="movie_orders"
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_order"
    )

    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __repr__(self) -> str:
        return f"<MovieOrder [{self.id}] - {self.price}>"
