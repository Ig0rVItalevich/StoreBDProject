from unicodedata import category
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Product, Review, Order, LikeProduct, LikeReview, Profile, Category

from faker import Faker
import random
import json

COUNT_USERS = 100
COUNT_PRODUCTS = 465
COUNT_REVIEWS = 10000
COUNT_LIKES = 500
COUNT_ORDERS = 100
COUNT_CATEGORIES = 25

categories_titles = ['edt', 'edp', 'cologne', 'perfum', 'men', 'women',
                     'solid perfume', 'oil perfume', 'perfume oil', 'tester', 'otlivant', 'miniature', 'gift wrap']

volumes = [30, 50, 90, 100]


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        self.users_generate(COUNT_USERS)
        self.categories_generate(COUNT_CATEGORIES)
        self.product_generate(COUNT_PRODUCTS)
        self.review_generate(COUNT_REVIEWS)
        self.order_generate(COUNT_ORDERS)
        self.like_generate(COUNT_LIKES)
        self.apply_likes()

    def users_generate(self, count):
        for i in range(count + 1):
            username = self.faker.unique.user_name()
            first_name = self.faker.unique.first_name()
            last_name = self.faker.unique.last_name()
            email = self.faker.email()
            password = self.faker.password()

            gender = ["Male", "Female"]
            sex = gender[random.randint(0, 1)]
            birth_date = self.faker.date()
            address = self.faker.address()[:50]

            user = User.objects.create(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)

            Profile.objects.create(
                user=user, sex=sex, birth_date=birth_date, address=address)

    def categories_generate(self, count):
        for i in range(count + 1):
            Category.objects.create(name=categories_titles[random.randint(1, len(categories_titles)) - 1])

    def product_generate(self, count):
        with open("/home/kirill/Documents/bd_cp/src/app/management/commands/items.json","r") as read_file: 
            items = json.load(read_file)
        cnt_categories = Category.objects.all().count()
        category_id = Category.objects.order_by('id')[0].id
        for i in range(count):
            item = items[i]
            cnt_categories_p = random.randint(1, 3)
            title = item['title']
            content = item['content']
            count = random.randint(0, 50)
            cost = int(item['price'])
            rating = random.randint(1, 10)
            img = 'img'+item['img'][1:]
            product = Product.objects.create(
                title=title, content=content, count=count, cost=cost, rating=rating, product_image=img)

            for j in range(cnt_categories_p):
                category = Category.objects.get(
                    id=random.randint(category_id, category_id+cnt_categories-1))
                product.categories.add(category)

    def review_generate(self, count):
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_product_id = Product.objects.order_by('id')[0].id
        max_product_id = Product.objects.order_by('-id')[0].id
        for i in range(count + 1):
            content = self.faker.paragraph(random.randint(1, 2))
            profile = random.randint(min_profile_id, max_profile_id)
            product = random.randint(min_product_id, max_product_id)
            rating = random.randint(1, 10)
            review = Review.objects.create(
                content=content, rating=rating, profile_id=profile, product_id=product)

    def order_generate(self, count):
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_product_id = Product.objects.order_by('id')[0].id
        max_product_id = Product.objects.order_by('-id')[0].id
        for i in range(count + 1):
            status = self.faker.word()
            comment = self.faker.paragraph(1)
            profile_id = random.randint(min_profile_id, max_profile_id)
            order = Order.objects.create(
                status=status, comment=comment, profile_id=profile_id)

            for j in range(random.randint(1, 10)):
                product = Product.objects.get(
                    id=random.randint(min_product_id, max_product_id-1))
                order.products.add(product, through_defaults={
                                   "cnt": random.randint(1, 10)})

    def like_generate(self, count):
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_product_id = Product.objects.order_by('id')[0].id
        max_Product_id = Product.objects.order_by('-id')[0].id
        for i in range(round(count / 2 + 1)):
            while True:
                like = random.randint(0, 1)
                profile_id = random.randint(min_profile_id, max_profile_id)
                product_id = random.randint(min_product_id, max_Product_id)
                if like > 0:
                    like = 1
                else:
                    like = -1
                check = LikeProduct.objects.filter(
                    product_id=product_id, profile_id=profile_id).count()
                if not check:
                    LikeProduct.objects.create(
                        product_id=product_id, profile_id=profile_id, mark=like)
                    break

        min_review_id = Review.objects.order_by('id')[0].id
        max_review_id = Review.objects.order_by('-id')[0].id
        for i in range(round(count / 2 + 1)):
            while True:
                like = random.randint(0, 1)
                profile_id = random.randint(min_profile_id, max_profile_id)
                review_id = random.randint(min_review_id, max_review_id)
                if like > 0:
                    like = 1
                else:
                    like = -1
                check = LikeReview.objects.filter(
                    review_id=review_id, profile_id=profile_id).count()
                if not check:
                    LikeReview.objects.create(
                        review_id=review_id, profile_id=profile_id, mark=like)
                    break

    def apply_likes(self):
        for product in Product.objects.all():
            product.rating = 0
            product.save()

        likes_p = LikeProduct.objects.all()
        for like_p in likes_p:
            product = Product.objects.get(id=like_p.product)
            if like_p.mark == 1:
                product.rating += 1
            else:
                product.rating -= 1
            product.save()

        likes_r = LikeReview.objects.all()
        for like_r in likes_r:
            review = Review.objects.get(id=like_r.review)
            if like_r.mark == 1:
                review.rating += 1
            else:
                review.rating -= 1
            review.save()
