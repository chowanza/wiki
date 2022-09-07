from turtle import width
from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect

import random

from . import util

class New(forms.Form):
    titles = forms.CharField(max_length=100, label="Title")
    contents = forms.CharField(widget=forms.Textarea, label="Content")

def md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    htmlContent = md_to_html(title)
    if htmlContent == None:
        return render(request, "encyclopedia/error.html", {
            "error_message": "Sorry, this entry does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlContent
        })

def search(request):
    if request.method =="POST":
        entrySearch = request.POST['q']
        htmlContent = md_to_html(entrySearch)
        if htmlContent is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": entrySearch,
            "content": htmlContent
        })
        else:
            allEntries = util.list_entries()
            recomm = []
            for entry in allEntries:
                if entrySearch.lower() in entry.lower():
                    recomm.append(entry)
            return render(request,"encyclopedia/search.html", {
                "recomm": recomm
            })

def newPage(request):
    if request.method =="GET":
        return render(request, "encyclopedia/new.html", {
            "form": New()
        })
    else:
        form = New(request.POST)
        if form.is_valid():
            title = form.cleaned_data["titles"]
            content = form.cleaned_data["contents"]
            titleExist = util.get_entry(title)
            if titleExist is not None:
                return render(request, "encyclopedia/error.html", {
                    "error_message": "Entry page already exists."
                })
            else:
                util.save_entry(title, content)
                htmlContent = md_to_html(title)
                return render(request, "encyclopedia/entry.html",{
                    "title": title,
                    "content": htmlContent
                })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "stuff": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        htmlContent = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlContent
        })

def rand(request):
    allEntries = util.list_entries()
    random_entry = random.choice(allEntries)
    htmlContent = md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html",{
        "title": random_entry,
        "content": htmlContent
    })