from django.urls import path, re_path

from .views import EchoView, CarView

urlpatterns = [
    # path('', index, name='index'),
    re_path(r'^tutorial/?$', EchoView.as_view()),
    re_path(r'^cars/?$', CarView.as_view()),
]
