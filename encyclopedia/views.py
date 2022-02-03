from django.shortcuts import render
from django.http import HttpResponse

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
            print("$$HELLO$$")
            return render(request, "encyclopedia/search.html" ,{"query": query ,"entry" : partial_match} )

        return render(request, "encyclopedia/search.html" ,{"query" : query} )
    
    else:
        return render(request, "encyclopedia/search.html")
