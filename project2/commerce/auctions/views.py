from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import User, Create_listing, Category, Watchlist


def create(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image_url = request.POST["image_url"]
        category_name = request.POST["category"]
        
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return render(request, "auctions/create_listing.html", {
                "error": "Category does not exist"
            })
        
        newListing = Create_listing(
            title=title,
            description=description,
            bid=float(bid),
            image_url=image_url,
            category=category
        )
        newListing.save()
        return HttpResponseRedirect(reverse('index'))


def watchlist(request):
    if request.user.is_authenticated:
        watchlist_items = Watchlist.objects.filter(user=request.user)
        return render(request, "auctions/watchlist.html", {
            "watchlist_items": watchlist_items
        })
    else:
        return redirect('login')


def add_to_watchlist(request, listing_id):
    if request.user.is_authenticated:
        try:
            listing = Create_listing.objects.get(id=listing_id)
            watchlist, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)
            return redirect('view_listing', listing_id=listing_id)
        except Create_listing.DoesNotExist:
            return render(request, "auctions/listing.html", {
                "error": "Listing not found"
            })
    else:
        return redirect('login')


def remove_from_watchlist(request, listing_id):
    if request.user.is_authenticated:
        try:
            listing = Create_listing.objects.get(id=listing_id)
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
            return redirect('view_listing', listing_id=listing_id)
        except Create_listing.DoesNotExist:
            return render(request, "auctions/listing.html", {
                "error": "Listing not found"
            })
    else:
        return redirect('login')


def index(request):
    listings = Create_listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings
    })


def view_listing(request, listing_id):
    listing = get_object_or_404(Create_listing, id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": request.user
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
