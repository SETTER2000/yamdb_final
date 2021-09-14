from functools import partial

from api_yamdb.settings import DEFAULT_FROM_EMAIL, ROLES_PERMISSIONS
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import TitleFilter
from .mixin import CreateListDestroyModelMixinViewSet
from .models import Category, Comment, Genre, Review, Title, User
from .permissions import IsAuthorOrReadOnly, PermissonForRole
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
)


class UserModelViewSet(viewsets.ModelViewSet):
    """Custщm User model with custom action."""

    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Users")),
    )

    @action(
        methods=["PATCH", "GET"],
        permission_classes=[permissions.IsAuthenticated],
        detail=False,
        url_path="me",
    )
    def user_me(self, request) -> Response:
        """Custom url for checking by user his profile and avialiable edit."""
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class TitleModelViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Titles")),
    )
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        slugs_genre = self.request.POST.getlist("genre")
        slug_category = self.request.data["category"]
        category = get_object_or_404(Category, slug=slug_category)
        title = serializer.save(category_id=category.id)
        for slug in slugs_genre:
            genre = get_object_or_404(Genre, slug=slug)
            title.genre.add(genre)

    def perform_update(self, serializer):
        if "genre" in self.request.data:
            slug_str = self.request.data["genre"]
            slugs = [x.strip() for x in slug_str.split(",")]
            genre = Genre.objects.none()
            for i in slugs:
                genre_a = Genre.objects.filter(slug=i)
                genre = genre.union(genre_a)
            genre_title = self.get_object().genre.all()
            genre = genre_title.union(genre)
        else:
            genre = self.get_object().genre.all()
        if "category" in self.request.data:
            category = get_object_or_404(
                Category, slug=self.request.data["category"]
            )
        else:
            slug = self.get_object().category.slug
            category = get_object_or_404(Category, slug=slug)
        serializer.save(
            genre=genre,
            category_id=category.id,
        )


class CategoryModelViewSet(CreateListDestroyModelMixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Categories")),
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data["name"], slug=self.request.data["slug"]
        )

    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        serializer.delete()


class GenreModelViewSet(CreateListDestroyModelMixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Genres")),
    )
    filter_backends = (filters.SearchFilter,)

    search_fields = ("name",)
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data["name"], slug=self.request.data["slug"]
        )

    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Genre, slug=self.kwargs.get("slug"))
        serializer.delete()


class ReviewModelViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        (IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly)
        | partial(PermissonForRole, ROLES_PERMISSIONS.get("Reviews")),
    )

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs["title_id"])
        user = User.objects.get(username=self.request.user)
        if user is None:
            raise ParseError("Неверный запрос!")

        review = Review.objects.filter(
            title=self.kwargs["title_id"], author=self.request.user.id
        )

        if review.exists():
            raise ParseError(detail="Ваш отзыв уже существует!")

        serializer.save(author=user, title=title)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs["title_id"])


class CommentModelViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        (IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly)
        | partial(PermissonForRole, ROLES_PERMISSIONS.get("Reviews")),
    )

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs["review_id"])
        title = get_object_or_404(Title, pk=self.kwargs["title_id"])
        serializer.save(author=self.request.user, review=review, title=title)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs["review_id"])


@api_view(["POST"])
def email_auth(request):
    """Check email and send to it confirmation code for token auth."""
    user = get_object_or_404(User, email=request.data["email"])
    confirmation_code = get_random_string()
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject="Код для генерации токена аутентификации YAMDB",
        message=str(confirmation_code),
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(request.data["email"],),
    )
    return Response(
        data="Письмо с кодом для аутентификации",
        status=status.HTTP_201_CREATED,
    )
