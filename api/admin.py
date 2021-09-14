from django.contrib import admin

from api.models import Category, Comment, Genre, Review, Title, User

EVD = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description',)
    search_fields = ('text',)
    list_filter = ('year',)
    empty_value_display = EVD


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_filter = ('slug',)
    empty_value_display = EVD


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_filter = ('slug',)
    empty_value_display = EVD


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'id', 'author', 'pub_date', 'text', 'score')
    list_filter = ('pub_date',)
    empty_value_display = EVD


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'review', 'pub_date', 'text')
    list_filter = ('pub_date',)
    empty_value_display = EVD


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'email')
    empty_value_display = EVD
