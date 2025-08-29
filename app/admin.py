from django.contrib import admin

from .models import Page, PageContent, Video, Audio, TextContent, Content


class PageContentInline(admin.TabularInline):
    model = PageContent
    extra = 1
    fields = ("content", "order")
    autocomplete_fields = ["content"]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    search_fields = ["^title"]
    list_display = ["title", "counter"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return False


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields = ["^title"]
    list_display = ["title"]
    inlines = [PageContentInline]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ["^title"]
    list_display = ["title", "counter"]


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    search_fields = ["^title"]
    list_display = ["title", "counter"]


@admin.register(TextContent)
class TextContentAdmin(admin.ModelAdmin):
    search_fields = ["^title"]
    list_display = ["title", "counter"]
