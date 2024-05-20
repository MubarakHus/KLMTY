from django.urls import path

from . import views

urlpatterns = [
    path("", views.day_select, name="index"),
    path('search/', views.search_word_index, name='search_word_index'),
    path('update_daily_words/', views.update_daily_words, name='update_daily_words'),

]