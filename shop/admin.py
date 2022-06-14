from django.contrib import admin
from .models import *


class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, SlugAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Slide)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Review)
