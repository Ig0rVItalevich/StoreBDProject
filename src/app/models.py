from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse


class ProductManager(models.Manager):
    def by_update_date(self):
        return self.order_by('-pub_date')

    def ascending_price(self):
        return self.order_by('cost')

    def descending__price(self):
        return self.order_by('-cost')

    def according_to_reviews(self):
        return self.annotate(count_reviews=Count('reviews')).order_by('-count_reviews')

    def by_rating(self):
        return self.order_by('-rating')

    def get_id(self, id):
        return self.get(id=id)

    def top(self, count=10):
        return self.order_by('-rating')[:count]

    def get_category(self, category):
        return self.filter(categories__name=category).order_by('pub_date')

    def search_products(self, search_name):
        return self.filter(title__icontains=search_name)


class OrderManager(models.Manager):
    def by_update_date(self):
        return self.order_by('-order_date')


class ReviewManager(models.Manager):
    def by_product(self, id):
        return self.filter(product_id=id).order_by('review_date')


class CategoryManager(models.Manager):
    def top(self, count=10):
        return self.annotate(count=Count('products')).order_by('-count')[:count]


class ProfileManager(models.Manager):
    def top(self, count=10):
        return self.annotate(count=Count('reviews')).order_by('-count')[:count]


class Product(models.Model):
    title = models.CharField(max_length=100)
    categories = models.ManyToManyField('Category', related_name='products')
    content = models.TextField()
    count = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    product_image = models.ImageField(
        upload_to='img/%Y/%m/%d/', default='img/1.jpg')
    pub_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    volume = models.IntegerField(default=100)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={"number": self.pk})
    


class Order(models.Model):
    status = models.CharField(max_length=50, default="Pending")
    order_date = models.DateTimeField(auto_now_add=True)
    date_of_completion = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(default="")
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(
        'Product', through="Orders_products", related_name='orders')

    objects = OrderManager()

    def get_absolute_url(self):
        return reverse("order", kwargs={"number": self.pk})


class Orders_products(models.Model):
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, related_name='ordersproducts')
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='ordersproducts')
    cnt = models.IntegerField(default=1)


class Review(models.Model):
    content = models.CharField(max_length=150)
    review_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='reviews')

    objects = ReviewManager()


class LikeProduct(models.Model):
    mark = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name="likes")
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name="product_likes")


class LikeReview(models.Model):
    mark = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name="likes")
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name="review_likes")


class Category(models.Model):
    name = models.CharField(max_length=50)

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_name": self.name})


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=150)
    sex = models.CharField(max_length=10)
    avatar = models.ImageField(
        upload_to='img/%Y/%m/%d/', default='img/ava.jpg')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username
