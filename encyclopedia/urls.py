from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("search", views.searchEntries, name="searchEntries"),
    path("search/random", views.randomGetter, name="randomGetter"),
    path("wiki/<str:entryTitle>", views.title, name="title"),
    path("wiki/<str:entryTitle>/edit", views.editor, name="editor"),
    path("wiki/<str:entryTitle>/save", views.updateEntry, name="updateEntry")
]

"""
App level url file which will dictate the path of
various routes in my wiki app
"""
