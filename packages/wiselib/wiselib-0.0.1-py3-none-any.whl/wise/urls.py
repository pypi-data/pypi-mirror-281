from django.urls import path

from wise.station.views import get_heap_node

urlpatterns = [
    path("station/heap/node", get_heap_node),
]
