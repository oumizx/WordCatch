from django.conf.urls import url
from .views import Index, Grammar_check_view, Speech_search
urlpatterns = [
    url(r'^$', Index, name='index'),
    url(r'^grammar_check_direct/', Grammar_check_view.as_view(), name='grammar_check_direct'),
    url(r'^grammar_check/', Grammar_check_view.as_view(), name='grammar_check'),
    url(r'^speech_search/', Speech_search, name='speech_search'),
]