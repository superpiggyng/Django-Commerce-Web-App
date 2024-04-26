from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Categories, AuctionListing, Watchlist, Bid, Comment
from .forms import ListingForm, CommentForm

# Create your tests here.

class ModelsTestCases(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='tester123', password='123')
        self.client.login(username='tester123', password='123')
        self.category = Categories.objects.create(category='Test Category')
        self.create_listing_url = reverse('create_listing')
        self.listing = AuctionListing.objects.create(
            title= 'Test Listing',
            model_name = 'TestCase',
            price = 20.00,
            product_category = self.category,
            seller = self.user
        )
    
    def test_AuctionListing_currentBidUpdate(self):
        Bid.objects.create(listing=self.listing, bidder=self.user, amount_bid=25.00)
        Bid.objects.create(listing=self.listing, bidder=self.user, amount_bid=30.00)

        self.listing.update_current_bid()

        self.assertEqual(self.listing.current_bid, 30.00)

    
    def test_AuctionListing_HighestBidder(self):
        first_bidder = get_user_model().objects.create_user(username='first_bidder', password='aaa')
        second_bidder = get_user_model().objects.create_user(username='second_bidder', password='bbb')
        Bid.objects.create(listing=self.listing, bidder=first_bidder, amount_bid='40.00')
        Bid.objects.create(listing=self.listing, bidder=second_bidder,amount_bid='42.00')

        highest_bidder = self.listing.highest_bidder()

        self.assertEqual(highest_bidder, second_bidder)

    def test_post_valid_listing(self):
        post_data = {
            'title' : 'testB',
            'price' : '20.00',
            'product_category' : self.category.pk
        }

        response = self.client.post(self.create_listing_url, post_data)
        self.assertEqual(AuctionListing.objects.count(), 2) # 2 because in setup created 1
        new_listing = AuctionListing.objects.get(pk=2)
        self.assertEqual(new_listing.title, 'testB')
        self.assertEqual(new_listing.seller, self.user)
        self.assertRedirects(response, reverse('listing_details', kwargs = {'pk':new_listing.pk}))
    
    def test_post_invalid_listing(self):
        post_data = {
            'title' : '',
            'price' : '20.00',
            'product_category' : self.category.pk
        }

        response = self.client.post(self.create_listing_url, post_data)
        self.assertEqual(AuctionListing.objects.count(),1) # 1 because in setup created 1
        self.assertTrue(response.context['form'].errors)

    
    def test_watchlist(self):
        watchlist, created = Watchlist.objects.get_or_create(user=self.user)
        watchlist.items.add(self.listing)
        self.assertEqual(watchlist.items.count(),1)
        self.assertTrue(watchlist.items.filter(pk=self.listing.pk).exists())
    
    def test_comment(self):
        Comment.objects.create(comment='Test comment',listing=self.listing,user=self.user)
        comments = Comment.objects.filter(listing=self.listing)
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments.first().comment,'Test comment')
    


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testerA', password='000')
        self.category = Categories.objects.create(category='Test Category')
        self.listing = AuctionListing.objects.create(
            title= 'Test Listing',
            model_name = 'TestCase',
            price = 20.00,
            product_category = self.category,
            seller = self.user
        )
    
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/index.html')
        self.assertContains(response, 'Test Listing')

    

    def test_watchlist_view_loggedin(self):
        self.client.login(username='testerA', password='000')
        watchlist, created = Watchlist.objects.get_or_create(user=self.user)
        watchlist.items.add(self.listing)
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/watchlist.html')
        self.assertContains(response, 'Test Listing')
    
    def test_comment_view(self):
        Comment.objects.create(listing=self.listing, user=self.user, comment='Test Comment')

        response = self.client.get(reverse('listing_details', kwargs={'pk' : self.listing.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/listing_details.html')
        self.assertContains(response, 'Test Comment')


class FormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testerB', password='123')
        self.category = Categories.objects.create(category='Test Category')
    
    def test_valid_listing_form(self):
        form_info = {
            'title' : 'Test Listing',
            'model' : 'Test mod',
            'brand' : 'Test',
            'price' : '20.00',
            'Category' : self.category
        }

        form = ListingForm(data=form_info)
        self.assertTrue(form.is_valid())
    
    def test_invalid_listing_form(self):
        form_info = {
            'title' : '',
            'model' : 'Test mod',
            'brand' : 'Test',
            'price' : '20.00',
            'Category' : self.category
        }

        form = ListingForm(data=form_info)
        self.assertFalse(form.is_valid())
    
    def test_comment_valid_form(self):
        form_info = {
            'comment' : 'Test Comment'
        }

        form = CommentForm(data=form_info)
        self.assertTrue(form.is_valid())
    
    def test_comment_invalid_form(self):
        form_info = {
            'comment' : ''
        }
        form = CommentForm(data=form_info)
        self.assertFalse(form.is_valid())       