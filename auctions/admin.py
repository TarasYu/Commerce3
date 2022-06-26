from django.contrib import admin
from .models import User, Lot, Bid, Category, Watchlist, Comment
# Register your models here.
class WatchlistAdmin(admin.ModelAdmin):
   #exclude = ("watchlist_owner",)
   filter_horizontal = ("watchlist_item",)

class BidAdmin(admin.ModelAdmin):
   list_display = ('bid_item', 'bid', 'bid_author')
   search_fields = ('bid_item__title', 'bid_author__username')

class CommentAdmin(admin.ModelAdmin):
   list_display = ('item_comment', 'author_comment')
   search_fields = ('item_comment__title', 'author_comment__username')
   

admin.site.register(User)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Lot)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category)
admin.site.register(Watchlist, WatchlistAdmin)

