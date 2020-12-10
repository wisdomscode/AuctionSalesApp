from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass



class Category(models.Model):
  name = models.CharField(max_length=64)

  def __str__(self):
    return self.name 



class Listing(models.Model):
  title = models.CharField(max_length=64)
  category = models.CharField(max_length=64)
  starting_price = models.IntegerField()
  description = models.TextField(max_length=10000)
  image = models.ImageField(upload_to="gallery")
  auctionier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

  def __str__(self):
    return self.title + ' | ' + str(self.starting_price) + ' | ' + str(self.auctionier) 



class Bid(models.Model):
  listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
  bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
  bid_amount = models.IntegerField()

  def __str__(self):
    return str(self.listing_id)  + ' | ' + str(self.bidder)  + ' | ' + str(self.bid_amount)



class Wishlist(models.Model):
  title = models.CharField(max_length=64)
  category = models.CharField(max_length=64, null=True, blank=True)
  bid_amount = models.IntegerField(null=True, blank=True)
  winner = models.CharField(max_length=64, null=True, blank=True)
  admirer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admirer")
  
  def __str__(self):
    return self.title



class Comment(models.Model):
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
  poster = models.CharField(max_length=255)
  comment = models.CharField(max_length=10000)
  date_posted = models.DateTimeField(auto_now_add=True)


      
  def __str__(self):
    return str(self.listing) + ' | ' + str(self.poster)


class Winner(models.Model):
  item = models.CharField(max_length=64)
  amount = models.IntegerField()
  victor = models.CharField(max_length=64)
  date_closed = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.item + ' | ' + self.victor