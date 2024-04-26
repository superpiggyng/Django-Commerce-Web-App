from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Categories(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    model_name = models.CharField(max_length=200, blank=True)
    brand = models.CharField(max_length=200, blank=True)
    image = models.URLField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    current_bid= models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True) # current bid should be updated based on the latest bids
    date_created = models.DateTimeField(default=timezone.now)
    product_category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    Active = 'Active'
    Closed= 'Closed'
    AUCTION_STATUS_CHOICES = [
        (Active, 'Active'),
        (Closed, 'Closed'),
    ]
    status = models.CharField(
        max_length=20,
        choices=AUCTION_STATUS_CHOICES,
        default='Active'
    )

    def update_current_bid(self):
        latest_bid = Bid.objects.filter(listing=self).order_by("-amount_bid").first()

        if latest_bid:
            self.current_bid = latest_bid.amount_bid
            self.save()

    def highest_bidder(self):
        highest_bid = Bid.objects.filter(listing=self).order_by('-amount_bid').first()
        if highest_bid:
            return highest_bid.bidder
        return None

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_bid = models.DecimalField(max_digits=10,decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.listing.update_current_bid()

    def __str__(self):
        return f"{self.bidder} created a bid for {self.listing} at ${self.amount_bid}"

class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} made a comment on {self.listing}"

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    items= models.ManyToManyField(AuctionListing, blank=True)

    def __str__(self):
        return f"Watchlist for {self.user.username}"