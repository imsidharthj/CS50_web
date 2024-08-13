from django.shortcuts import render, redirect
import markdown
from . import util
import random

def convert(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = convert(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {"message":"Requested page was not found."})
    return render(request, "encyclopedia/entry.html", {"title":title, "content":entry_content})


def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title":entry_search,
                "content":html_content
            })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation":recommendation
            })


def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new_page.html", {
                "error_message": "An entry with this title already exists."
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/new_page.html")


def edit(request, title):
    if request.method == "POST":
        updated_content = request.POST.get("content")
        util.save_entry(title, updated_content)
        return redirect("entry", title=title)
    current_content = util.get_entry(title)
    if current_content is None:
        return render(request, "encyclopedia/error.html", {"message": "Entry not found."})
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": current_content
    })


def random_entry(request):
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {"message": "No entries available"})
    random_page = random.choice(entries)
    random_html = convert(random_page)
    return render(request, "encyclopedia/entry.html", {
        "title":random_page,
        "content":random_html
    })