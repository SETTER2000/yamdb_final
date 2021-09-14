import datetime

from django.db.models import Avg
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    """Custom serializer for User model."""

    lookup_field = "username"

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "username",
            "bio",
            "email",
            "role",
        )
        model = User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    class Meta:
        fields = ("id", "author", "text", "pub_date")
        model = Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title

    def get_rating(self, obj):
        if Review.objects.filter(title_id=obj.id):
            rating = int(
                Review.objects.filter(title_id=obj.id).aggregate(
                    rating=Avg("score")
                )["rating"]
            )
        else:
            rating = None
        return rating

    def validate_year(self, value):
        now_year = datetime.datetime.now().year
        if value < 0 or value > now_year:
            raise serializers.ValidationError(
                f"Не верный год [ 0 .. {now_year} ]"
            )
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password"]
        del self.fields["username"]
        self.fields["confirmation_code"] = serializers.CharField(required=True)
        self.fields["email"] = serializers.EmailField(required=True)

    def validate(self, attrs):
        data = {}
        user = User.objects.get(email=attrs["email"])
        confirmation_code = User.objects.get(
            confirmation_code=attrs["confirmation_code"]
        )
        refresh = self.get_token(user)
        if user and confirmation_code:
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)
            user.confirmation_code = ""
            user.save()
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
