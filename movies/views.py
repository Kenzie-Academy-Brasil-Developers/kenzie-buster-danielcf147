from rest_framework.views import APIView, Response, Request, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Movie
from .serializer import MovieSerializer, MovieOrderSerializer
from .permissions import IsAdmOrReadOnly


class MovieView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmOrReadOnly]
    pagination_class = PageNumberPagination
    page_size = 2

    def get(self, request: Request) -> Response:
        # movies = Movie.objects.all()
        movies = Movie.objects.order_by("pk")

        paginator = self.pagination_class()
        paginated_movies = paginator.paginate_queryset(movies, request)

        serializer = MovieSerializer(paginated_movies, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(
            data=request.data, context={"added_by": request.user.email}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        # ipdb.set_trace()
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieOrderSerializer(
            data=request.data,
            context=[{"buyed_by": request.user.email}, {"buyed_by": movie_id}],
        )
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, movie=movie)

        return Response(serializer.data, status.HTTP_201_CREATED)
