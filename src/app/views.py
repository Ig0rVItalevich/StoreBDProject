from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import auth
from django.http import JsonResponse
from django.db import connection
from app.models import (
    Product,
    Order,
    Review,
    LikeProduct,
    LikeReview,
    Profile,
    Category,
    Orders_products,
)
from app.forms import RegisterForm, LoginForm, ReviewForm, SettingsForm, SearchForm

from .my_utils import my_paginator
from .cart import Cart

top_categories = Category.objects.top()
top_products = Product.objects.top()

search_form = SearchForm()


def index(request):
    products = Product.objects.by_update_date()
    current_page, pages = my_paginator(request, products, 10)

    return render(
        request,
        "main-page.html",
        {
            "search_form": search_form,
            "products": current_page,
            "pages": pages,
            "top_categories": top_categories,
            "top_products": top_products,
        },
    )


def products(request, sort_name):
    if sort_name == "by_update_date":
        products = Product.objects.by_update_date()
        sort_name = "by update date"
    elif sort_name == "ascending_price":
        products = Product.objects.ascending_price()
        sort_name = "ascending price"
    elif sort_name == "descending__price":
        products = Product.objects.descending__price()
        sort_name = "descending price"
    elif sort_name == "according_to_reviews":
        products = Product.objects.according_to_reviews()
        sort_name = "according to reviews"
    elif sort_name == "by_popularuty":
        products = []
        with connection.cursor() as cursor:
            query = """SELECT * FROM popular_products();"""
            cursor.execute(query, ())
            result = cursor.fetchall()
            for x in result:
                products.append(Product.objects.get(pk=x[0]))
        sort_name = "by popularuty"
    else:
        products = Product.objects.by_rating()
        sort_name = "by rating"

    current_page, pages = my_paginator(request, products, 10)

    return render(
        request,
        "products.html",
        {
            "search_form": search_form,
            "sort_name": sort_name,
            "products": current_page,
            "pages": pages,
            "top_categories": top_categories,
            "top_products": top_products,
        },
    )


@login_required(login_url="login")
def add_review(request, number):
    form = ReviewForm(data=request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        profile = Profile.objects.get(user=request.user)

        product = get_object_or_404(Product, id=number)
        review.profile = profile
        review.product = product
        review.save()
        return redirect("product", number)


def product(request, number):
    form = ReviewForm()

    if request.method == "POST":
        return add_review(request, number)

    product = get_object_or_404(Product, id=number)
    reviews = Review.objects.by_product(number)
    current_page, pages = my_paginator(request, reviews, 5)

    return render(
        request,
        "single-product.html",
        {
            "search_form": search_form,
            "product": product,
            "reviews": current_page,
            "pages": pages,
            "top_categories": top_categories,
            "top_products": top_products,
            "form": form,
        },
    )


def category(request, category_name):
    products = Product.objects.get_category(category_name)
    current_page, pages = my_paginator(request, products, 10)

    return render(
        request,
        "category-sort.html",
        {
            "search_form": search_form,
            "products": current_page,
            "pages": pages,
            "top_categories": top_categories,
            "top_products": top_products,
            "category": category_name,
        },
    )


def login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "GET":
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)

            if user is not None:
                auth.login(request, user)

                return redirect("index")
            else:
                form.add_error(None, "Пользователь не найден")

    return render(
        request,
        "login.html",
        {
            "search_form": search_form,
            "top_categories": top_categories,
            "top_products": top_products,
            "form": form,
        },
    )


@login_required(login_url="login")
def logout(request):
    auth.logout(request)

    return redirect("index")


def signup(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "GET":
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                User.objects.get(username=form.cleaned_data["username"])
            except BaseException:
                try:
                    User.objects.get(username=form.cleaned_data["email"])
                except BaseException:
                    form_avatar = form.cleaned_data.pop("avatar")
                    form_address = form.cleaned_data.pop("address")
                    form_birth_date = form.cleaned_data.pop("birth_date")
                    form_sex = form.cleaned_data.pop("sex")
                    if not (form_avatar):
                        form_avatar = "img/ava.jpg"
                    user = User.objects.create_user(**form.cleaned_data)
                    user.save()

                    Profile.objects.create(
                        user=user,
                        birth_date=form_birth_date,
                        sex=form_sex,
                        address=form_address,
                        avatar=form_avatar,
                    )
                    return redirect("index")
                else:
                    form.add_error(None, "User exist")
            else:
                form.add_error(None, "User exist")

    return render(
        request,
        "register.html",
        {
            "search_form": search_form,
            "top_categories": top_categories,
            "top_products": top_products,
            "form": form,
        },
    )


@login_required(login_url="login")
def settings(request):
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        data = {
            "email": profile.user.email,
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name,
            "address": profile.address,
        }
        form = SettingsForm(initial=data)
    else:
        form = SettingsForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            profile = Profile.objects.get(user=request.user)

            form_avatar = form.cleaned_data["avatar"]
            if form_avatar:
                profile.avatar = form_avatar
            profile.address = form.cleaned_data["address"]
            profile.user.email = form.cleaned_data["email"]
            profile.user.first_name = form.cleaned_data["first_name"]
            profile.user.last_name = form.cleaned_data["last_name"]
            profile.user.save()
            profile.save()

            return redirect("index")

    return render(
        request,
        "settings.html",
        {
            "search_form": search_form,
            "top_categories": top_categories,
            "top_products": top_products,
            "form": form,
        },
    )


@login_required(login_url="login")
def bag(request):
    cart = Cart(request)
    products = []
    for x in cart.cart:
        product = Product.objects.get(id=x)
        total = int(product.cost) * int(cart.cart[x]["cnt"])
        _product = {
            "id": product.id,
            "title": product.title,
            "cost": str(product.cost),
            "count": cart.cart[x]["cnt"],
            "total": total,
        }

        products.append(_product)

    total_price = int(cart.get_total_cost())

    return render(
        request,
        "bag.html",
        {
            "search_form": search_form,
            "products": products,
            "total_price": total_price,
            "top_categories": top_categories,
            "top_products": top_products,
        },
    )


def search(request):
    if request.method == "GET":
        return redirect("index")
    else:
        _search_form = SearchForm(data=request.POST)

        if _search_form.is_valid():
            search_name = _search_form.cleaned_data["title"]
            products = Product.objects.search_products(search_name)
        else:
            return redirect("index")
    current_page, pages = my_paginator(request, products, 10)
    sort_name = 'search "' + search_name + '"'

    return render(
        request,
        "products.html",
        {
            "search_form": _search_form,
            "sort_name": sort_name,
            "products": current_page,
            "pages": pages,
            "top_categories": top_categories,
            "top_products": top_products,
        },
    )


@require_POST
def grade(request):
    data = request.POST
    if not request.user.is_authenticated:
        data._mutable = True
        data["redirect"] = "/login"
        return JsonResponse(data)
    if data["type"] == "review":
        rid = data["rid"]
        action = data["action"]
        review = Review.objects.get(id=rid)
        inc = 1

        if action == "dislike":
            inc = -1
        review_likes = review.likes.filter(profile_id=request.user.profile.id).all()

        if len(review_likes) and review_likes[len(review_likes) - 1].mark == inc:
            return JsonResponse(data, status=400)

        response = JsonResponse(data, status=200)

        if len(review_likes):
            response.set_cookie(key="new", value="False")
            if review_likes[0].mark != inc:
                review_likes[0].mark = inc
                review_likes[0].save()
        else:
            LikeReview.objects.create(
                mark=inc, profile=request.user.profile, review=review
            )
            response.set_cookie(key="new", value="True")

        return response
    else:
        pid = data["pid"]
        action = data["action"]
        product = Product.objects.get(id=pid)
        inc = 1

        if action == "dislike":
            inc = -1

        product_likes = product.likes.filter(profile_id=request.user.profile.id).all()

        if len(product_likes) and product_likes[0].mark == inc:
            return JsonResponse(data, status=400)

        response = JsonResponse(data, status=200)

        if len(product_likes):
            response.set_cookie(key="new", value="False")
            if product_likes[0].mark != inc:
                product_likes[0].mark = inc
                product_likes[0].save()
        else:
            LikeProduct.objects.create(
                mark=inc, profile=request.user.profile, product=product
            )
            response.set_cookie(key="new", value="True")

        return response


@login_required(login_url="login")
def order(request, number):
    try:
        order = Order.objects.get(id=number)
    except:
        return redirect("index")

    if request.user.profile.id != order.profile.id:
        return redirect("index")

    products = []
    for product in order.products.all():
        cost = Orders_products.objects.filter(product_id=product.id, order_id=order.id)[0].cost

        cnt = Orders_products.objects.filter(product_id=product.id, order_id=order.id)[
            0
        ].cnt
        total = cnt * cost
        _product = {
            "id": product.id,
            "title": product.title,
            "cost": cost,
            "count": cnt,
            "total": total,
        }
        products.append(_product)

        with connection.cursor() as cursor:
            try:
                query = """SELECT * FROM total_price(%s);"""
                cursor.execute(query, (str(order.id),))
                result = cursor.fetchall()
            except BaseException:
                result = [0]

    return render(
        request,
        "order.html",
        {
            "search_form": search_form,
            "order": order,
            "total_price": result[0][0],
            "products": products,
            "top_categories": top_categories,
            "top_products": top_products,
        },
    )


@login_required(login_url="login")
def order_history(request):
    orders = request.user.profile.orders.by_update_date()
    _orders = []

    with connection.cursor() as cursor:
        for order in orders:
            query = """SELECT * FROM total_price(%s);"""
            cursor.execute(query, (str(order.id),))
            result = cursor.fetchall()

            _order = {
                "id": order.id,
                "order_date": str(order.order_date.strftime("%m.%d.%Y, %H:%M")),
                "status": order.status,
                "comment": order.comment,
                "total_price": result[0][0],
            }

            _orders.append(_order)

    return render(
        request,
        "order_history.html",
        {
            "search_form": search_form,
            "orders": _orders,
            "top_categories": top_categories,
            "top_products": top_products,
        },
    )


@require_POST
def make_order(request):
    data = request.POST

    if not request.user.is_authenticated:
        data._mutable = True
        data["redirect"] = "/login"
        return JsonResponse(data)

    cart = Cart(request)

    comment = ""

    del_products = []

    for product_id in cart.cart:
        product = Product.objects.get(id=product_id)

        if product.count == 0:
            del_products.append(product_id)
            comment += "Out of stock: %s" % (product.title)
        elif product.count < int(cart.cart[product_id]["cnt"]):
            cart.cart[product_id]["cnt"] = str(product.count)
            comment += "Product quantity changed to %s: %s" % (
                cart.cart[product_id]["cnt"],
                product.title,
            )

    for prod in del_products:
        cart.remove(prod)

    if len(cart) > 0:
        order = Order.objects.create(profile=request.user.profile)

        for product_id in cart.cart:
            product = Product.objects.get(id=product_id)
            order.products.add(
                product, through_defaults={"cnt": int(cart.cart[product_id]["cnt"]), 
                                           "cost": int(cart.cart[product_id]["cost"])}
            )

        order.comment = comment
        order.save()

    cart.clear()

    return JsonResponse(data, status=200)


@require_POST
def add_to_cart(request):
    data = request.POST

    if not request.user.is_authenticated:
        data._mutable = True
        data["redirect"] = "/login"

        return JsonResponse(data)

    pid = data["pid"]
    product = Product.objects.get(id=pid)

    cart = Cart(request)
    cart.add(product)

    return JsonResponse(data, status=200)


@require_POST
def reduce_amount_cart(request):
    data = request.POST

    if not request.user.is_authenticated:
        data._mutable = True
        data["redirect"] = "/login"

        return JsonResponse(data)

    pid = data["pid"]
    product = Product.objects.get(id=pid)

    cart = Cart(request)
    cart.reduce_amount(product)

    return JsonResponse(data, status=200)


@require_POST
def increase_amount_cart(request):
    data = request.POST

    if not request.user.is_authenticated:
        data._mutable = True
        data["redirect"] = "/login"

        return JsonResponse(data)

    pid = data["pid"]
    product = Product.objects.get(id=pid)

    cart = Cart(request)
    cart.increase_amount(product)

    return JsonResponse(data, status=200)
