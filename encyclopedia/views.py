from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util

import random as rnd

from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):
    mrkdwn = Markdown()
    entry = mrkdwn.convert(util.get_entry(title))
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "entry": entry
    })


def search(request):

    # Reached via Search
    if 'q' in request.GET:
        query = request.GET['q']
        list_entries = util.list_entries()

        # Perfect Match
        for entry in list_entries:
            if query.upper() == entry.upper():
                return page(request, entry)

        # Partial Match
        partial_match = [
            entry for entry in list_entries if query.upper() in entry.upper()]

        if partial_match:

            return render(request, "encyclopedia/search.html", {"query": query, "entry": partial_match})

        # No Match
        return render(request, "encyclopedia/search.html", {"query": query.capitalize()})

    # Reached via incomplete URL
    else:
        return render(request, "encyclopedia/search.html")


class NewPageForm(forms.Form):
    new_title = forms.CharField(label='Title')
    new_body = forms.CharField(
        label='Type new entry here', widget=forms.Textarea)


def new_page(request):

    # Form Submited
    if request.method == 'POST':
        form = NewPageForm(request.POST)

        if form.is_valid():

            body = form.cleaned_data["new_body"]
            title = form.cleaned_data["new_title"]

            if title.upper() in (entry.upper() for entry in util.list_entries()):
                return HttpResponse("This page already exists")

            util.save_entry(title, body)

            # redirect to a new URL:
            return page(request, title)

    return render(request, "encyclopedia/new_page.html", {"form": NewPageForm()})


class EditPageForm(forms.Form):

    new_body = forms.CharField(label='Edit entry here', widget=forms.Textarea)


def edit_page(request, title):
    if request.method == 'POST':
        form = EditPageForm(request.POST)

        if form.is_valid():

            body = form.cleaned_data["new_body"]

            util.save_entry(title, body)

            return page(request, title)

    return render(request, "encyclopedia/edit.html", {"form": EditPageForm(initial={'new_body': util.get_entry(title)})})


def random(request):

    rnd.seed()

    all_entries = util.list_entries()
    return page(request, all_entries[rnd.randint(0, len(all_entries)-1)])
