from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Cart, Delivery, Dish, Items, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
import re


def home_page(request):
    return render(request, "order_site/homepage.html")


def login_user(request):
    if request.method == "POST":
        if request.POST["username"] == "" or request.POST["password"] == "":
            return render(
                request,
                "order_site/login.html",
                {"message": "*נא למלא את כל השדות"},
            )
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is not None:
            login(request, user)
            # מציבים את כל העגלות שנוצרו ברשימה
            carts = [c for c in user.cart_set.all()]
            cart = None
            # מציבים את העגלה האחרונה שנוצרה ובודקים האם היא עוד לא נסגרה
            if carts and carts[-1].delivery.address == "":
                cart = carts[-1]
            else:
                # יצירת עגלה עם פרטים ריקים שלאחר מכן יעודכנו
                new_cart(request)
            return redirect("categories")
        return render(
            request, "order_site/login.html", {"message": "שם משתמש או סיסמה שגויים"}
        )
    return render(request, "order_site/login.html")


def signup(request):
    if request.method == "POST":
        all_users = User.objects.all()
        for user in all_users:
            if user.username == request.POST["username"]:
                return render(
                    request, "order_site/signup.html", {"message3": "*שם משתמש תפוס"}
                )
        if (
            request.POST["username"] == ""
            or request.POST["password"] == ""
            or request.POST["first_name"] == ""
            or request.POST["last_name"] == ""
            or request.POST["email"] == ""
        ):
            return render(
                request, "order_site/signup.html", {"message": "*שדה זה הוא חובה"}
            )
        elif request.POST["password"] != request.POST["password2"]:
            return render(
                request, "order_site/signup.html", {"message2": "*הסיסמאות אינן תואמות"}
            )
        elif validate_email_address(request.POST["email"]) == False:
            return render(
                request, "order_site/signup.html", {"message4": "*אימייל לא נכון"}
            )
        else:
            new_user = User(
                username=request.POST["username"],
                password=make_password(request.POST["password"]),
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
            )
            new_user.save()
            return redirect("login")
    return render(request, "order_site/signup.html")


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def user_info(request):
    return render(request, "order_site/my_info.html")


@login_required(login_url="login")
def categories(request):
    all_categories = Category.objects.all()
    return render(request, "order_site/categories.html", {"categories": all_categories})


@login_required(login_url="login")
def show_by_category(request, id):
    category = Category.objects.get(id=id)
    return render(request, "order_site/show_by_category.html", {"category": category})


@login_required(login_url="login")
def remove_from_cart(request, id):
    item = Items.objects.get(id=id)
    item.delete()
    return redirect("cart")


@login_required(login_url="login")
def add_to_cart(request):
    if request.method == "POST":
        carts = [c for c in request.user.cart_set.all()]
        id = request.POST["dish"]
        dish = Dish.objects.get(id=id)
        for item in carts[-1].items_set.all():
            if item.dish.name == dish.name:
                item.amount += int(request.POST["amount"])
                item.save()
                return redirect("categories")
        else:
            new_item = Items(dish=dish, cart=carts[-1], amount=request.POST["amount"])
            new_item.save()
            return redirect("categories")


@login_required(login_url="login")
def checkout(request):
    if request.method == "POST":
        if request.POST["address"] == "" or request.POST["notes"] == "":
            return render(
                request, "order_site/checkout.html", {"message": "*שדה זה הוא חובה"}
            )
        else:
            carts = [c for c in request.user.cart_set.all()]
            cart = carts[-1]
            cart.delivery.address = request.POST["address"]
            cart.delivery.notes = request.POST["notes"]
            cart.delivery.save()
            new_cart(request)
            return redirect("mydeliveries")
    return render(request, "order_site/checkout.html")


@login_required(login_url="login")
def cart(request):
    carts = [c for c in request.user.cart_set.all()]
    cart = carts[-1]
    return render(
        request,
        "order_site/cart.html",
        {"items": cart.items_set.all(), "total": cart_amount(cart)},
    )


@login_required(login_url="login")
def edit_my_info(request):
    if request.method == "POST":
        user = request.user
        user.set_password(request.POST["password"])
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        user.save()
        return redirect("categories")
    return render(request, "order_site/edit_my_info.html")


@login_required(login_url="login")
def my_deliveries(request):
    carts = [c for c in request.user.cart_set.all()]
    return render(request, "order_site/deliveries.html", {"carts": carts[:-1]})


def cart_amount(cart):
    items = 0
    for i in cart.items_set.all():
        items += i.dish.price * i.amount
    return items


def new_cart(request):
    delivery1 = Delivery(
        is_delivered=False, address="", notes="", created=datetime.now()
    )
    delivery1.save()
    cart = Cart(user=request.user, delivery=delivery1)
    cart.save()


def validate_email_address(email_address):
    if not re.search(
        r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address
    ):
        print(f"The email address {email_address} is not valid")
        return False
    return True
