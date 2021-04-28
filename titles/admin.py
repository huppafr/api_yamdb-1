from django.contrib import admin

from .models import Category, Ganre, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ganre)
class GanreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'ganre', 'category')
    search_fields = ('name', 'category', 'genre',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    # prepopulated_fields = {"slug": ("name",)}
