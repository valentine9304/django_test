from rest_framework.test import APITestCase
from .models import Page, Video, Audio, PageContent


class PageAPITests(APITestCase):
    def setUp(self):
        self.page = Page.objects.create(title='СТРАНИЦА')
        content1 = Audio.objects.create(title='МУЗЫКА', text='Lyrics')
        PageContent.objects.create(page=self.page, content=content1, order=1)
        content2 = Video.objects.create(title='ВИДЕО', video_url='http://example.com/video.mp4', subtitles_url='')
        PageContent.objects.create(page=self.page, content=content2, order=2)

    def test_list_pages(self):
        response = self.client.get('/pages/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'СТРАНИЦА')

    def test_detail_page(self):
        response = self.client.get(f'/pages/{self.page.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'СТРАНИЦА')
        self.assertIn('contents', response.data)
        self.assertEqual(len(response.data['contents']), 2)
        self.assertEqual(response.data['contents'][0]['title'], 'МУЗЫКА')
        self.assertEqual(response.data['contents'][0]['type'], 'audio')
        self.assertEqual(response.data['contents'][0]['text'], 'Lyrics')
        self.assertEqual(response.data['contents'][1]['title'], 'ВИДЕО')
        self.assertEqual(response.data['contents'][1]['type'], 'video')
        self.assertEqual(response.data['contents'][1]['video_url'], 'http://example.com/video.mp4')