# app/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random

from app.models import Video, Audio, TextContent, Page, PageContent, Content

LOCALE = "ru_RU"
VIDEOS = 30
AUDIOS = 30
TEXTS = 30
PAGES = 15
MIN_PER_PAGE = 3
MAX_PER_PAGE = 6


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **kwargs):
        fake = Faker(LOCALE)

        self.stdout.write("Создаём Video...")
        for _ in range(VIDEOS):
            Video.objects.create(
                title=fake.sentence(nb_words=4),
                video_url=fake.url(),
                subtitles_url=(fake.url() if random.random() < 0.5 else None),
                counter=0,
            )

        self.stdout.write("Создаём Audio...")
        for _ in range(AUDIOS):
            Audio.objects.create(
                title=fake.sentence(nb_words=4),
                text=fake.paragraph(nb_sentences=5),
                counter=0,
            )

        self.stdout.write("Создаём TextContent...")
        for _ in range(TEXTS):
            TextContent.objects.create(
                title=fake.sentence(nb_words=4),
                text=fake.paragraph(nb_sentences=8),
                counter=0,
            )

        all_content_ids = list(Content.objects.values_list("id", flat=True))
        total_contents = len(all_content_ids)
        self.stdout.write(f"Всего контента: {total_contents}")

        pages = [Page(title=fake.sentence(nb_words=3)) for _ in range(PAGES)]
        Page.objects.bulk_create(pages, batch_size=500)
        pages = list(Page.objects.all())

        rels = []
        for page in pages:
            if total_contents == 0:
                break
            k = random.randint(MIN_PER_PAGE, MAX_PER_PAGE)
            if k == 0:
                continue
            picked_ids = set(random.sample(all_content_ids, k=min(k, total_contents)))
            for order, cid in enumerate(picked_ids):
                rels.append(PageContent(page=page, content_id=cid, order=order))

        if rels:
            PageContent.objects.bulk_create(
                rels, batch_size=1000, ignore_conflicts=True
            )

        self.stdout.write(self.style.SUCCESS("Success"))
