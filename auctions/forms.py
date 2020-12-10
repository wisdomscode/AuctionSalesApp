from django import forms
from django.forms import ModelForm


from .models import Listing, Bid, Comment, Wishlist, Category, Winner
 
# choices = [('fashion','Fashion'), ('cars', 'Cars'), ('phone','Phone')]

choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for item in choices:
  choice_list.append(item)




class CategoryForm(ModelForm):
  class Meta:
    model = Category
    fields = '__all__'

    widgets =  {
      'name': forms.TextInput(attrs={'class': 'form-control'}),
    }



class ListingForm(ModelForm):
  class Meta:
    model = Listing
    fields = ('title', 'category', 'starting_price', 'description', 'image', 'auctionier')

    widgets =  {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
      'starting_price': forms.NumberInput({'class': 'form-control'}),
      'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your post here'}),
      'image': forms.FileInput(attrs={'class': 'form-control'}),
      'auctionier': forms.TextInput(attrs={'class': 'form-control', 'id':'auctionier', 'value':'', 'type':'hidden'}),
    }




class BidForm(ModelForm):
  class Meta:
    model = Bid
    fields = ('listing_id', 'bidder', 'bid_amount')

    widgets =  {
      'listing_id': forms.TextInput(attrs={'class': 'form-control', 'id':'listing_id', 'value':'', 'type':'hidden'}),
      'bidder': forms.TextInput(attrs={'class': 'form-control', 'id':'bidder', 'value':'', 'type':'hidden'}),
      'bid_amount': forms.NumberInput({'class': 'form-control'})
     
    }



class WishlistForm(ModelForm):
  class Meta:
    model = Wishlist
    fields = ('title', 'category', 'bid_amount', 'winner', 'admirer')

    widgets =  {
      'title': forms.TextInput(attrs={'class': 'form-control', 'id':'title', 'value':'', 'type':'hidden'}),
      'category': forms.TextInput(attrs={'class': 'form-control', 'id':'category', 'value':'', 'type':'hidden'}),
      'bid_amount': forms.NumberInput(attrs={'class': 'form-control', 'id':'bid_amount', 'value':'', 'type':'hidden'}),
      'winner': forms.TextInput(attrs={'class': 'form-control', 'id':'winner', 'value':'', 'type':'hidden'}),
      'admirer': forms.TextInput(attrs={'class': 'form-control', 'id':'admirer', 'value':'', 'type':'hidden'}),
    }




class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ('listing', 'poster', 'comment')

    widgets =  {
      'listing': forms.TextInput(attrs={'class': 'form-control', 'id':'listing', 'value':'', 'type':'hidden'}),
      'poster': forms.TextInput(attrs={'class': 'form-control', 'id':'poster', 'value':'', 'type':'hidden'}),
      'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your comment here', "rows":3, "cols":20})
    }



class WinnerForm(ModelForm):
  class Meta:
    model = Winner
    fields = ('item', 'amount', 'victor')

    widgets =  {
      'item': forms.TextInput(attrs={'class': 'form-control', 'id':'item', 'value':'', 'type':'hidden'}),
      'amount': forms.NumberInput(attrs={'class': 'form-control', 'id':'amount', 'value':'', 'type':'hidden'}),
      'victor': forms.TextInput(attrs={'class': 'form-control', 'id':'victor', 'value':'', 'type':'hidden'})
    }
