from calendar import c
from dataclasses import field
from tkinter import Widget
from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django import forms
from django.views.generic.edit import CreateView
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.forms import HiddenInput, ModelForm, Textarea
from .models import  User, Category, Bid, Lot, Watchlist, Comment
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
    categoryies = Category.objects.all()
    lot = Lot.objects.filter(end_auction=False)
    return render(request, "auctions/index.html", {
        "categories": categoryies,
        "lots": lot,
    })

def lot_category(request, category_id):
    item_category = Category.objects.get(pk=category_id)
    lot_categories = item_category.category_lot.all()
    category = Category.objects.all()
    return render(request, "auctions/lot_of_category.html", {
        "lot_categories": lot_categories,
        "categories": category,
    })
#???????????????????????? ???????????????? "watchlist"
def watch_list(request, user_id):
   
    set = Watchlist.objects.all()
    if set.filter(watchlist_owner=user_id).exists():
        watchlist = Watchlist.objects.get(watchlist_owner=user_id)
        q = watchlist.watchlist_item.all()
        list = [lots for lots in q]
    else:
        list = []
    category = Category.objects.all()
    return render(request, "auctions/index.html", {
        "categories": category,
        "lots" : list
    })

class WatchlistForm(forms.Form):
    lot_id = forms.IntegerField(widget=forms.HiddenInput)
    user_id = forms.IntegerField(widget=forms.HiddenInput)

    
def lot(request, lot_id):
    lot = Lot.objects.get(pk=lot_id)
    return render(request, "auctions/lot.html", {
        "lot": lot,       
    })
    
#???????????????????????? ???????? ?????? ???????????????????????????????? ????????????????????????
def lot_au(request, lot_id, user_id):
    lot = Lot.objects.get(pk=lot_id)
    user = User.objects.get(pk=user_id)
    set = Watchlist.objects.all()
    if set.filter(watchlist_owner=user_id).exists():
        watchlist = Watchlist.objects.get(watchlist_owner=user_id)
        q = watchlist.watchlist_item.all()
        bool = q.filter(id=lot_id).exists()
    else:
        bool = False
        
    return render(request, "auctions/lot.html", {
        "lot": lot,
        "in_watchlist": bool,
        "form": WatchlistForm(
            {
                'lot_id': lot.id,
                'user_id': user.id
            })
    })

class AuctionForm(ModelForm):
    class Meta:
        model = Lot
        exclude = ['owner_name', 'end_auction']
        widgets = {
            'description':  Textarea(attrs={'cols':50, 'rows': 5})    
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body_comment']

        widgets = {
       'body_comment': Textarea(attrs={'class': 'form-control'})
        }       

class AddCommentView(CreateView):
    model = Comment
    template_name = 'auctions/add_comment.html'
    form_class = CommentForm
   
    
    def form_valid(self, form):
        lot = Lot.objects.get(pk=self.kwargs['lot_id'])
        form.instance.author_comment = self.request.user
        form.instance.item_comment = lot
        return super().form_valid(form) 
    
    def get_success_url(self):
        return reverse_lazy('lot_au', kwargs={'lot_id': self.kwargs['lot_id'], 'user_id': self.kwargs['user_id']})

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'
        bid = forms.DecimalField(required=False)
        widgets = {
            'bid_item': forms.HiddenInput,
            'bid_author': forms.HiddenInput,
            'bid': forms.NumberInput (attrs={
                'class': 'bid_input',
                'required': 'True'
            })
        }


def bid_view(request, lot_id, user_id):
    lot = Lot.objects.get(pk=lot_id)
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        bid = int(request.POST.get('bid'))            
        if lot.bids.last().bid >= bid:
            messages.error(request, "Your bid must be higher than current one")
            return render(request, 'auctions/bid_offer.html', {
            'lot': lot,
            'bid': bid,
            'form': BidForm(
                {
                    'bid_item': lot,
                    'bid_author': user,    
                })
            })
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('lot_au', args=(lot.id, user.id, )))         
    else:
        return render(request, 'auctions/bid_offer.html', {
            'lot': lot,
            'form': BidForm(
                {
                    'bid_item': lot,
                    'bid_author': user,
                })
        })    

def create_auction(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner_name = user
            instance.save()
            form.save_m2m()
            Bid(bid=instance.starting_price, bid_author=user, bid_item=Lot.objects.get(pk=instance.id)).save()
            return HttpResponseRedirect(reverse('lot_au', args=(instance.id, user.id, )))
         
    else:
        form = AuctionForm()
    return render(request, 'auctions/create_auction.html', {'form': form})

def edit_auction(request, lot_id):
    instance = Lot.objects.get(pk=lot_id)
    data= {'title': instance.title,
           'photo': instance.photo,
           'categories': instance.categories.all(),
           'description': instance.description,
           'starting_price': instance.starting_price
          }
    if request.method == 'POST':
        user = User.objects.get(pk=instance.owner_name.id)
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid:
            changed_instance = form.save(commit=False)
            changed_instance.owner_name = user
            changed_instance.id = lot_id
            if not changed_instance.photo:
                changed_instance.photo = instance.photo
             
            changed_instance.save()
            form.save_m2m()
            if instance.bids.all().count() == 1:
                instance.bids.get().delete()
                Bid(bid=changed_instance.starting_price, bid_item=Lot.objects.get(pk=lot_id), bid_author=user).save()
            return HttpResponseRedirect(reverse('lot_au', args=(changed_instance.id, user.id, )))         

    return render(request, 'auctions/edit_lot.html', {
        'form': AuctionForm(initial=data),
        'instance_id': instance.id,
    
    })

def watchlist(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(pk=user_id)
        lot_id = request.POST.get("lot_id")
        lot = Lot.objects.get(pk=lot_id)
        set = Watchlist.objects.all()
        if not set.filter(watchlist_owner=user_id).exists():
            Watchlist.objects.create(watchlist_owner=user)
        
        watchlist = Watchlist.objects.get(watchlist_owner=user_id)
        q = watchlist.watchlist_item.all()
        bool = q.filter(id=lot_id).exists()
    
        if not bool:
            watchlist.watchlist_item.add(lot)   
        else:
            watchlist.watchlist_item.remove(lot)    

        return HttpResponseRedirect(reverse('lot_au', args=(lot.id, user.id, )))

def end_au(request, lot_id):
    lot = Lot.objects.get(pk=lot_id)
    if request.method == "POST":
        lot.end_auction = "True"
        lot.save()
        return HttpResponseRedirect(reverse('lot_au', args=(lot.id, lot.owner_name.id)))
    else:
        return render(request, 'auctions/end_au.html', {'lot': lot})

def completed_au(request):
    completed_lot = Lot.objects.filter(end_auction=True)
    category = Category.objects.all()
    return render(request, "auctions/lot_of_category.html", {
        "lot_categories": completed_lot,
        "categories": category,
    })