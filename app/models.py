from django.db import models
from polymorphic.models import PolymorphicModel


class Content(PolymorphicModel):
    title = models.CharField(max_length=255)
    counter = models.IntegerField(default=0)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Video(Content):
    video_url = models.URLField()
    subtitles_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Video Content"
        verbose_name_plural = "Video Contents"


class Audio(Content):
    text = models.TextField(blank=True)

    class Meta:
        verbose_name = "Audio Content"
        verbose_name_plural = "Audio Contents"


class TextContent(Content):
    text = models.TextField(blank=True)

    class Meta:
        verbose_name = "Text Content"
        verbose_name_plural = "Text Contents"


class Page(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def get_contents(self):
        return [pc.content for pc in self.page_contents.order_by("order")]

    class Meta:
        ordering = ['title']


class PageContent(models.Model):
    page = models.ForeignKey(
        Page, related_name="page_contents", on_delete=models.CASCADE
    )
    content = models.ForeignKey(
        Content, related_name="content_pages", on_delete=models.CASCADE
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ["page", "content"]
