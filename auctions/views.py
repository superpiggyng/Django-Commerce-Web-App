from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Watchlist, Bid, Comment, Categories
from .forms import ListingForm, CommentForm

def index(request):
    listings = AuctionListing.objects.all()
    watchlist_items = None

    if request.user.is_authenticated:
        try:
            watchlist = Watchlist.objects.get(user=request.user)
            watchlist_items = watchlist.items.all()


        except Watchlist.DoesNotExist:
            watchlist_items = None

    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_items": watchlist_items
    })

def add_comment(request, pk):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.listing = listing
            new_comment.save()
    return redirect('listing_details', pk=pk)
    
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.seller_id = request.user.id
            new_listing.save()
            return redirect("listing_details",pk=new_listing.pk)
    else:
        form = ListingForm()
    
    return render(request,'auctions/create_listing.html', {'form': form})


def search_results(request):
    query = request.GET.get('q', '')
    if query:
        listings = AuctionListing.objects.filter(title__icontains=query)
    else:
        listings = AuctionListing.objects.all()
    
    return render(request, 'auctions/search_results.html', {
        'listings': listings,
        'search_query': query
    })

def user_listings(request, username):
    user = get_object_or_404(User, username=username)
    listings = AuctionListing.objects.filter(seller=user)

    return render(request, 'auctions/user_listings.html', {
        'listings': listings,
        'user': user
    })

    
def listing_details(request, pk=None, category_id=None):
    watchlist_items = None
    if request.user.is_authenticated:
        try:
            watchlist = Watchlist.objects.get(user=request.user)
            watchlist_items = watchlist.items.all()
        except Watchlist.DoesNotExist:
            pass

    if category_id:
        selected_category = Categories.objects.get(pk=category_id)
        listings = AuctionListing.objects.filter(product_category=selected_category)

        return render(request, 'auctions/listings_by_category.html', {
            'listings': listings,
            'watchlist_items': watchlist_items,
        })
    
    if pk:
        listing = AuctionListing.objects.get(pk=pk)
        bid_count = Bid.objects.filter(listing=listing).count()
        comment_form = CommentForm()
        comments = Comment.objects.filter(listing=listing)

        return render(request, 'auctions/listing_details.html', {
            'listing': listing,
            'watchlist_items': watchlist_items,
            'bid_count': bid_count,
            'comment_form': comment_form,
            'comments': comments,
        })


def place_bid(request, pk):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=pk)

        if listing.status == "Closed":
            return redirect('listing_details', pk=pk)

        bid_amount = request.POST.get('textbox')

        if bid_amount:
            try:
                bid_amount = float(bid_amount)
                if (listing.current_bid is not None and bid_amount > listing.current_bid) or (listing.current_bid is None and bid_amount > listing.price):
                    Bid.objects.create(
                        listing=listing,
                        bidder = request.user,
                        amount_bid = bid_amount
                    )
                    listing.current_bid = bid_amount
                    listing.save()
                    return redirect('listing_details', pk=pk)
                
                else:
                    error_message = "Please enter a valid amount. It has to be greater than the listing price or current highest bid."
                    bid_count = Bid.objects.filter(listing=listing).count()
                    return render(request, 'auctions/listing_details.html', {
                        'error_message': error_message,
                        'listing': listing,
                        'bid_count': bid_count
                    })
                

            except ValueError:
                error_message = "Please enter a valid amount."
                bid_count = Bid.objects.filter(listing=listing).count()
                return render(request, 'auctions/listing_details.html', {
                        'error_message': error_message,
                        'bid_count': bid_count,
                        'listing': listing
                    })

    return redirect('listing_details', pk=pk)

def close_auction(request, pk):
    listing = AuctionListing.objects.get(pk=pk)
    if request.method=="POST" and request.user == listing.seller:
        listing.status = 'Closed'
        listing.save()
    
    return redirect('listing_details', pk=pk)


@login_required
def watchlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if "add_to_watchlist" in request.POST:
                listing_id = request.POST.get("listing_id")
                listing = get_object_or_404(AuctionListing, pk=listing_id)
                try:
                    watchlist = Watchlist.objects.get(user=request.user)
                    watchlist.items.add(listing)
                except Watchlist.DoesNotExist:
                    watchlist = Watchlist.objects.create(user=request.user)
                    watchlist.items.add(listing)

                return redirect('watchlist')
            
            elif "remove_from_watchlist" in request.POST:
                listing_id = request.POST.get("listing_id")
                listing = get_object_or_404(AuctionListing, pk=listing_id)

                watchlist = Watchlist.objects.get(user=request.user)
                watchlist.items.remove(listing)

                return redirect('watchlist')

            
        try:
            watchlist = Watchlist.objects.get(user=request.user)
            watchlist_items = watchlist.items.all()
        except Watchlist.DoesNotExist:
            watchlist_items = None
        
        return render(request, 'auctions/watchlist.html', {
            'watchlist_items': watchlist_items
        })


#login_view was provided by scaffold
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

#logout_view was provided by scaffold
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#register was provided by scaffold
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        
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
