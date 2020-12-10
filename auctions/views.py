from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.contrib import messages
from .forms import ListingForm, BidForm, CommentForm, WishlistForm, CategoryForm, WinnerForm
from .models import User, Listing, Bid, Comment, Wishlist, Category, Winner

from django.contrib import messages



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


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
      "listings": listings
    })

@login_required
def create(request):
  form = ListingForm()
  if request.method == "POST":

    form = ListingForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()

      form = ListingForm()
      return HttpResponseRedirect(reverse("index"))

    else:
      message = messages.error(request, 'Please check you entries')
      return render(request, "auctions/create.html", {
        "form": form, "message": message
      })
  return render(request, "auctions/create.html", {
    "form": ListingForm()
  })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    title = listing.title
    wishitem = Wishlist.objects.filter(title=title)
    # count = wishitem.count()
    close_form = WinnerForm()
    # print(wishitem)
    comment_form = CommentForm()
    if (wishitem is not None):
        if Bid.objects.filter(listing_id=listing_id):
          bid = Bid.objects.get(listing_id=listing_id)
          bid_form = BidForm()
          wish_form = WishlistForm()
          return render(request, "auctions/listing.html", {
            "listing": listing, "bid":bid,  "bid_form":bid_form, "wish_form":wish_form, "wishitem":wishitem, "comment_form":comment_form, "close_form":close_form
          })
        else:
          bid_form = BidForm()
          wish_form = WishlistForm()
          return render(request, "auctions/listing.html", {
            "listing": listing, "bid_form":bid_form, "wish_form":wish_form, "comment_form":comment_form, "wishitem":wishitem, "close_form":close_form
          })
        bid_form = BidForm()
        wish_form = WishlistForm()
        return render(request, "auctions/listing.html", {
          "listing": listing,  "bid_form":bid_form, "wish_form":wish_form, "wishitem":wishitem, "comment_form":comment_form, "close_form":close_form
        })
    else:
        if Bid.objects.filter(listing_id=listing_id):
          bid = Bid.objects.get(listing_id=listing_id)
          bid_form = BidForm()
          wish_form = WishlistForm()
          return render(request, "auctions/listing.html", {
            "listing": listing, "bid":bid,  "bid_form":bid_form, "wish_form":wish_form, "comment_form":comment_form, "close_form":close_form
          })
        else:
          bid_form = BidForm()
          wish_form = WishlistForm()
          return render(request, "auctions/listing.html", {
            "listing": listing, "bid_form":bid_form, "wish_form":wish_form, "comment_form":comment_form, "close_form":close_form
          })
        bid_form = BidForm()
        wish_form = WishlistForm()
        return render(request, "auctions/listing.html", {
          "listing": listing,  "bid_form":bid_form, "wish_form":wish_form, "comment_form": comment_form, "close_form":close_form
        })
    return render(request, "auctions/listing.html", {
      "listing": listing, "bid":bid,  "bid_form":bid_form, "wish_form":wish_form, "wishitem":wishitem, "comment_form":comment_form, "close_form":close_form
    })



@login_required
def bid(request, listing_id):
  comment_form =  CommentForm()
  bid_form = BidForm()
  close_form = WinnerForm()
  listing = Listing.objects.get(pk=listing_id)
  
  if request.method == "POST":
    # user = request.POST["admirer"]
    auctionier = listing.auctionier
    user = request.POST["bidder"]
    bidder = User.objects.get(pk=user)
    wishitem= Wishlist.objects.filter(admirer=user)
    count = wishitem.count()
    if (auctionier != bidder):
        if Bid.objects.filter(listing_id=listing_id): 
          bid = Bid.objects.get(listing_id=listing_id)
          prev_bid = bid.bid_amount
          new_bid = int(request.POST["bid_amount"])

          if (prev_bid >= new_bid):
            messages.error(request, "Sorry, you can't bid less than the current bid")
            return render(request, "auctions/listing.html", {
              "bid_form": BidForm(request.POST), "listing": listing, "bid":bid, "comment_form": comment_form, "wishitem":wishitem, "close_form":close_form
            })
          else:
            delete_item = Bid.objects.get(listing_id=listing_id)
            delete_item.delete()
            bid_form = BidForm(request.POST)
            bid_form.save()
            bid = Bid.objects.get(listing_id=listing_id)
            bid_form = BidForm()
            messages.success(request, "You have successful bidded for this item")
            return render(request, "auctions/listing.html", {
              "bid_form": bid_form, "listing": listing, "bid":bid, "comment_form": comment_form, "wishitem":wishitem, "close_form":close_form
            })
        else:
          listing = Listing.objects.get(pk=listing_id)
          s_price = listing.starting_price
          new_bid = int(request.POST["bid_amount"])
          if (s_price > new_bid):
            messages.error(request, "Sorry, you can't bid less than the Starting Price")
            return render(request, "auctions/listing.html", {
              "bid_form": BidForm(request.POST), "listing": listing, "comment_form": comment_form, "wishitem":wishitem, "close_form":close_form
            })
          else:
            bid_form = BidForm(request.POST)
            bid_form.save()
            bid = Bid.objects.get(listing_id=listing_id)
            bid_form = BidForm()
            messages.success(request, "You have successful bidded for this item")
            return render(request, "auctions/listing.html", {
              "bid_form": bid_form, "listing": listing, "bid":bid, "comment_form": comment_form, "wishitem":wishitem, "close_form":close_form
            })
          return render(request, "auctions/listing.html", {
            "bid_form": bid_form, "listing": listing, "bid":bid, "comment_form": comment_form, "wishitem":wishitem,"close_form":close_form
          })
    else:
      messages.error(request, "Ops! You can't bid on you own item")
      return render(request, "auctions/listing.html", {
        "bid_form": BidForm(), "listing": listing, "comment_form": comment_form, "wishitem":wishitem,"close_form":close_form
      })
  return render(request, "auctions/listing.html", {
    "bid_form": bid_form, "listing": listing, "bid":bid, "comment_form": comment_form, "wishitem":wishitem,"close_form":close_form
  })


@login_required
def end_bid(request, listing_id):
  # close_form = WinnerForm()
  listing = get_object_or_404(Listing, pk=listing_id) 
  if request.method == "POST":
    if Bid.objects.filter(listing_id=listing_id): 
      bid = Bid.objects.get(listing_id=listing_id)

      
      close_form = WinnerForm(request.POST)
      close_form.save()

      listing = Listing.objects.get(pk=listing_id)
      listing.delete()

      messages.success(request, "You have successful ended this Bid")                           
      return HttpResponseRedirect(reverse("index"))   
  
    else:
      close_form = WinnerForm(request.POST)
      close_form.save()

      listing = Listing.objects.get(pk=listing_id)
      listing.delete()
      messages.success(request, "You closed your auction without recieving any Bid")                           
      return HttpResponseRedirect(reverse("index"))   
      return render(request, "auctions/listing.html", {
        "listing": listing
      })       
  return render(request, "auctions/listing.html", {
    "listing": listing
  })



def closed_bid(request):
  closed_bids = Winner.objects.all()
  return render(request, "auctions/closed_bids.html", {"closed_bids":closed_bids})


def verdict(request, bid):
  closed_bids = Winner.objects.all()
  if request.method == "POST":
    item = request.POST["bid_item"]
    result = Winner.objects.get(victor=bid, item=item)
    winner = result.victor
    user = request.POST["user"]

    if (winner == user):
      result = Winner.objects.get(victor=bid, item=item)
      return render(request, "auctions/closed_bid_info.html", { "result":result })
    else:
      message = "You lost the Bid"
      return render(request, "auctions/closed_bid_info.html", { "message":message })
  return render(request, "auctions/closed_bids.html", {"closed_bids":closed_bids})



@login_required
def wishlist(request, user_id):  
  user = User.objects.get(pk=user_id)
  wishlist= Wishlist.objects.filter(admirer=user)
  count = wishlist.count()
  return render(request, "auctions/wishlist.html", {"wishlist":wishlist, "count":count})



@login_required
def wishitem(request, listing_id):
  comment_form =  CommentForm()
  bid_form = BidForm()
  listing = Listing.objects.get(pk=listing_id)
  title = listing.title
  wishitem = Wishlist.objects.filter(title=title)
  count = wishitem.count()
  if request.method == "POST":       
    listing = Listing.objects.get(pk=listing_id)
    if Bid.objects.filter(listing_id=listing_id): 
      bid = Bid.objects.get(listing_id=listing_id)
      wish_form = WishlistForm(request.POST)
      if wish_form.is_valid():
        title = listing.title
        wishitem = Wishlist.objects.filter(title=title)
        wishitem.delete()
        wishitem = wish_form.save()

        # user = User.objects.get(pk=user_id)
        user = request.POST["admirer"]
        wishitem= Wishlist.objects.filter(admirer=user)
        count = wishitem.count()
        # wish_form = WishlistForm()
        return render(request, "auctions/listing.html", { "listing":listing, "bid":bid, "wishitem":wishitem, "bid_form":bid_form, "count":count, "comment_form": comment_form})
      else:
        count = wishitem.count()
        return render(request, "auctions/listing.html", {
          "listing":listing, "bid":bid, "wish_form":WishlistForm(request.POST), "count":count, "wishitem":wishitem, "bid_form":bid_form, "comment_form": comment_form
        })
    else:
      wish_form = WishlistForm(request.POST)
      if wish_form.is_valid():
        wish_form.save()
        user = request.POST["admirer"]
        wishitem= Wishlist.objects.filter(admirer=user)
        count = wishitem.count()
        # wish_form = WishlistForm()
        bid_form = BidForm()
        return render(request, "auctions/listing.html", { "listing":listing, "wishitem":wishitem, "bid_form":bid_form, "count":count, "comment_form": comment_form })
      else:
        return render(request, "auctions/listing.html", {
          "listing":listing, "wish_form":WishlistForm(request.POST)
        })
  return render(request, "auctions/listing.html", { "listing":listing, "wishitem":wishitem, "count":count, "comment_form": comment_form  })


@login_required
def getlisting(request):
  comment_form =  CommentForm()
  if request.method == "POST":
    item = request.POST["wish"]
    wishitem = Wishlist.objects.get(title=item)
    listing =  get_object_or_404(Listing, title=item)
    if Bid.objects.filter(listing_id=listing): 
      bid = Bid.objects.get(listing_id=listing)
      bid_form = BidForm()
      wishitem
      return render(request, "auctions/listing.html", {"wishitem":wishitem, "listing":listing, "bid":bid,  "bid_form":bid_form, "comment_form": comment_form})
    else:
      wishitem = Wishlist.objects.get(title=item)
      bid_form = BidForm()
      return render(request, "auctions/listing.html", {"wishitem":wishitem, "listing":listing, "bid_form":bid_form, "comment_form": comment_form })

  return render(request, "auctions/wishlist.html", {"wishitem":wishitem, "comment_form": comment_form })


# @login_required
def removeWishitem(request):
  if request.method == "POST":
    item = request.POST["wish"]
    wishitem = Wishlist.objects.get(title=item)
    wishitem.delete()
    user = request.POST["you"]
    wishlist = Wishlist.objects.filter(admirer=user)
    count = wishlist.count()
    return render(request, "auctions/wishlist.html", { "wishlist":wishlist })



@login_required
def removeWish(request):
  comment_form =  CommentForm()
  bid_form = BidForm()
  if request.method == "POST":
    item = request.POST["wish"]
    wishitem = Wishlist.objects.get(title=item)
    wishitem.delete()
    listing =  get_object_or_404(Listing, title=item)
    if Bid.objects.filter(listing_id=listing): 
      bid = Bid.objects.get(listing_id=listing)
      bid_form = BidForm()
      return render(request, "auctions/listing.html", { "listing":listing, "bid":bid, "bid_form":bid_form, "comment_form": comment_form})
    else:
      bid_form = BidForm()
      return render(request, "auctions/listing.html", { "listing":listing, "bid_form":bid_form, "comment_form": comment_form })
  return render(request, "auctions/listing.html", { "listing":listing, "wishitem":wishitem, "bid_form":bid_form, "comment_form": comment_form})


def comment(request, listing_id):
  comment_form =  CommentForm()
  if request.method == "POST":
    listing =  get_object_or_404(Listing, pk=listing_id)
    # item = listing.title
    # wishitem =  get_object_or_404(Wishlist, title=item)
    comment = CommentForm(request.POST)
    comment.save()
    comment = CommentForm()
    if Bid.objects.filter(listing_id=listing): 
      bid = Bid.objects.get(listing_id=listing)
      bid_form = BidForm()
      return render(request, "auctions/listing.html", { "listing":listing, "bid":bid,  "bid_form":bid_form, "comment_form": comment_form, "wishitem":wishitem, })
    else:
      bid_form = BidForm()
      return render(request, "auctions/listing.html", { "listing":listing, "bid_form":bid_form, "comment_form": comment_form, "wishitem":wishitem,  })
    return render(request, "auctions/listing.html", {
      "comment_form": comment_form,  "listing": listing, "bid_form": bid_form, "wishitem":wishitem,
    })
    
  return render(request, "auctions/listing.html", {
    "comment_form": comment_form, "listing": listing
  })



@login_required
def add_cat(request):
  category = CategoryForm()
  if request.method == "POST":
    category = CategoryForm(request.POST)
    category.save()
    category = CategoryForm()
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {'categories':categories})
  return render(request, "auctions/add_category.html", {'category':category})


def categories(request):
  categories = Category.objects.all()
  return render(request, "auctions/categories.html", {'categories':categories})


def category(request, cats):
  category_listings = Listing.objects.filter(category=cats)
  return render(request, "auctions/category.html", {"cats":cats, "category_listings":category_listings })