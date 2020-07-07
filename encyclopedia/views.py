from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from . import forms
from . import util
import random
import markdown2


def index(request):  # URL "" , index
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchBar": forms.searchBar(),
    })


def newEntry(request):  # URL "/newEntry"
    if request.method == "POST":
        newEntryData = forms.pgNewEntry(request.POST)
        if newEntryData.is_valid():
            getPgTitle = newEntryData.cleaned_data["pageTitle"]
            getPgInfo = newEntryData.cleaned_data["pageInfo"]
            if util.get_entry(getPgTitle):
                return HttpResponseNotFound('<h1>' + getPgTitle + ' already exists</h1>')
            else:
                getPgTitle = getPgTitle.capitalize()
                util.save_entry(getPgTitle, getPgInfo)
                return HttpResponseRedirect(reverse('title', args=(getPgTitle,)))
        else:
            HttpResponseNotFound('<h1>Error in this search</h1>')
    else:
        return render(request, "encyclopedia/newEntry.html", {
            "pgNewEntry": forms.pgNewEntry(),
        })


def searchEntries(request):  # URL /
    if request.method == "POST":
        searchData = forms.searchBar(request.POST)
        if searchData.is_valid():
            cleanedSearchData = searchData.cleaned_data["searchQ"]
            if util.get_entry(cleanedSearchData):
                return HttpResponseRedirect(reverse('title', args=(cleanedSearchData,)))
            else:
                subStringData = [i for i in util.list_entries(
                ) if cleanedSearchData in i]
                return render(request, "encyclopedia/search.html", {
                    "searchBar": forms.searchBar(),
                    "entries": subStringData
                })

    else:  # URL "search/"
        return HttpResponseRedirect(reverse('index',))


def randomGetter(request):  # URL search/random
    listEntries = util.list_entries()
    getRandPg = random.choice(listEntries)
    return render(request, "encyclopedia/title.html", {
        "entryTitle": getRandPg.capitalize(),
        "entryTitleInfo": markdown2.markdown(util.get_entry(getRandPg))
    })


def title(request, entryTitle):  # "search/title"
    if util.get_entry(entryTitle):
        return render(request, "encyclopedia/title.html", {
            "entryTitle": entryTitle.capitalize(),
            "entryTitleInfo": markdown2.markdown(util.get_entry(entryTitle))

        })
    else:
        return HttpResponseNotFound('<h1>Error: Result Not Found</h1>')


def editor(request, entryTitle):  # "search/<str:name>/edit"
    if util.get_entry(entryTitle):
        initialEntryInfo = util.get_entry(entryTitle)
        return render(request, "encyclopedia/editor.html", {
            "entryTitle": entryTitle.capitalize(),
            "pgSaveEntry": forms.pgSaveEntry(initial={'saveInfo': initialEntryInfo}),
            # "entryTitle": entryTitle.capitalize()
        })
    else:
        return HttpResponseNotFound('<h1>Error: Result Not Found</h1>')


def updateEntry(request, entryTitle):  # "search/<str:name>/save"
    if request.method == "POST":
        savedData = forms.pgSaveEntry(request.POST)
        if savedData.is_valid():
            newPgInfo = savedData.cleaned_data["saveInfo"]
            if util.get_entry(entryTitle):
                entryTitle = entryTitle.capitalize()
                util.save_entry(entryTitle, newPgInfo)
                return HttpResponseRedirect(reverse('title', args=(entryTitle,)))
        else:
            HttpResponseNotFound('<h1>Error in this search</h1>')
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "searchBar": forms.searchBar(),
        })
