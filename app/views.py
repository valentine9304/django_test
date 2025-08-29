from rest_framework import generics
from rest_framework.response import Response

from .models import Page
from .serializers import PageListSerializer, PageDetailSerializer
from .tasks import increment_counter


class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer


class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        contents = instance.get_contents()
        data = serializer.data

        for content in contents:
            increment_counter.delay(content.id)

        return Response(data)
