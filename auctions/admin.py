from django.contrib import admin
from .models import User, Auctions, Lot, Bid, Category, Watchlist, Profile, Comments
# Register your models here.
class WatchlistAdmin(admin.ModelAdmin):
   #exclude = ("watchlist_owner",)
   filter_horizontal = ("watchlist_item",)

admin.site.register(User)
admin.site.register(Auctions)
admin.site.register(Comments)
admin.site.register(Lot)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Profile)
