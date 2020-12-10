from django.contrib import admin

from .models import User, Listing, Bid, Comment, Wishlist, Category, Winner


class UserAdmin(admin.ModelAdmin):
  list_display = ("id", "username", "first_name", "last_name", "email")


class CategoryAdmin(admin.ModelAdmin):
  list_display = ("id", "name")



class ListingAdmin(admin.ModelAdmin):
  list_display = ("id", "title", "category", "starting_price", "description",  "image", "auctionier")


class BidAdmin(admin.ModelAdmin):
  list_display = ("id", "listing_id", "bid_amount", "bidder")


class CommentAdmin(admin.ModelAdmin):
  list_display = ("listing", "poster", "date_posted", "comment")

class WishlistAdmin(admin.ModelAdmin):
  list_display = ("id", "title", "category", "bid_amount", "winner", "admirer")


class WinnerAdmin(admin.ModelAdmin):
  list_display = ("item", "amount", "victor", "date_closed")

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Winner, WinnerAdmin)