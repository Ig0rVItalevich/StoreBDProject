from django.contrib import admin

from app.models import Product, Review, LikeProduct, LikeReview, Order, Profile, Orders_products

admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Orders_products)
admin.site.register(LikeProduct)
admin.site.register(LikeReview)

admin.site.site_title = 'Perfume administration'
admin.site.site_header = 'Perfume administration'