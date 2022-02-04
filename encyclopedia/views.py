from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
        
        return render(request, "encyclopedia/page.html", {
        "entry": util.get_entry(title)
    })

def search(request):
    

    if  'q' in  request.GET:
        query = request.GET['q']
        list_entries = util.list_entries()

## Perfect Match
        for entry in list_entries:
            if query.upper() == entry.upper():
                return page(request, entry)

## Partial Match
        partial_match = [entry for entry in list_entries if query.upper() in entry.upper()]

        

        if partial_match:
            
            return render(request, "encyclopedia/search.html" ,{"query": query ,"entry" : partial_match} )

        return render(request, "encyclopedia/search.html" ,{"query" : query} )
    
    else:
        return render(request, "encyclopedia/search.html")

def new_page(request):

    if request.method == 'POST':
        form = NewPageForm(request.POST)
        
        if form.is_valid():

            body = form.cleaned_data["new_body"]
            title = form.cleaned_data["new_title"]
            util.save_entry(title,body)

            # redirect to a new URL:
            return page(request, title)

    return render(request, "encyclopedia/new_page.html", {"form": NewPageForm()})

class NewPageForm(forms.Form):
    new_title = forms.CharField(label='Title')
    new_body = forms.CharField(label='Type new entry here')

def edit_page(request, title): 

    return render(request, "encyclopedia/edit.html", {"form": EditPageForm(initial={'new_title':title, 'new_body': util.get_entry(title) })})
    

class EditPageForm(forms.Form):

    
    new_title = forms.CharField(label='Edit Title' )
    new_body = forms.CharField(label='Edit entry here', widget=forms.Textarea)


