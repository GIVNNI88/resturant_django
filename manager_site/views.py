from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from order_site.models import Category, Dish, Delivery, User
from django.core.exceptions import PermissionDenied
from order_site.views import new_cart
from django.contrib.auth import login, authenticate, logout

# Create your views here.


def login_manager(request):
    if request.method == "POST":
        if request.POST["username"] == "" or request.POST["password"] == "":
            return render(
                request,
                "manager_site/login_manager.html",
                {"message": "*נא למלא את כל השדות"},
            )
        user = authenticate(
            request,
            password=request.POST["password"],
            username=request.POST["username"],
        )
        if user is not None:
            if user.is_staff == True:
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
            return redirect("login")
            
        else:
            return render(
                request,
                "manager_site/login_manager.html",
                {"message": "שם משתמש או סיסמה שגויים"},
            )
    return render(request, "manager_site/login_manager.html")


@login_required(login_url="login")
def add_dish(request):
    if not request.user.is_staff:
        raise PermissionDenied()
    if request.method == "POST":
        if (
            request.POST["name"] == ""
            or request.POST["description"] == ""
            or request.POST["imageUrl"] == ""
            or request.POST["price"].isdigit() == False
            or "category" not in request.POST
        ):
            return render(
                request,
                "manager_site/add_dish.html",
                {
                    "categories": Category.objects.all(),
                    "message": "*שדה זה הוא חובה",
                    "message2": "*מחיר צריך להיות מספר",
                },
            )
        else:
            new_dish = Dish(
                name=request.POST["name"],
                price=request.POST["price"],
                description=request.POST["description"],
                imageUrl=request.POST["imageUrl"],
                is_gluten_free=request.POST["is_gluten_free"],
                is_vegeterian=request.POST["is_vegeterian"],
                category_id=request.POST["category"],
            )
            new_dish.save()
            return redirect("categories")
    return render(
        request, "manager_site/add_dish.html", {"categories": Category.objects.all()}
    )


@login_required(login_url="login")
def edit_dish(request, id):
    dish = Dish.objects.get(id=id)
    categories = Category.objects.all()
    categoryName = ""
    for category in categories:
        if category.id == dish.category_id:
            categoryName = category.name
    if not request.user.is_staff:
        raise PermissionDenied()
    if request.method == "POST":
        dish.name = request.POST["name"]
        dish.price = request.POST["price"]
        dish.description = request.POST["description"]
        dish.imageUrl = request.POST["imageUrl"]
        dish.is_gluten_free = request.POST["is_gluten_free"]
        dish.is_vegeterian = request.POST["is_vegeterian"]
        dish.category_id = request.POST["category"]
        dish.save()
        return redirect("categories")
    return render(
        request,
        "manager_site/edit_dish.html",
        {
            "id": id,
            "categories": categories,
            "dish": dish,
            "categoryName": categoryName,
        },
    )


@login_required(login_url="login")
def delete_dish(request, id):
    if not request.user.is_staff:
        raise PermissionDenied()
    else:
        dish = Dish.objects.get(id=id)
        dish.delete()
        return redirect("categories")


@login_required(login_url="login")
def add_category(request):
    if not request.user.is_staff:
        raise PermissionDenied()
    if request.method == "POST":
        if request.POST["name"] == "" or request.POST["imageUrl"] == "":
            return render(
                request,
                "manager_site/add_category.html",
                {"message": "*שדה זה הוא חובה"},
            )
        else:
            new_category = Category(
                name=request.POST["name"], imageUrl=request.POST["imageUrl"]
            )
            new_category.save()
            return redirect("categories")
    return render(request, "manager_site/add_category.html")


@login_required(login_url="login")
def edit_category(request, id):
    cat = Category.objects.get(id=id)
    if not request.user.is_staff:
        raise PermissionDenied()
    if request.method == "POST":
        cat.name = request.POST["name"]
        cat.imageUrl = request.POST["imageUrl"]
        cat.save()
        return redirect("categories")
    return render(request, "manager_site/edit_category.html", {"id": id, "cat": cat})


@login_required(login_url="login")
def delete_category(request, id):
    if not request.user.is_staff:
        raise PermissionDenied()
    else:
        cat = Category.objects.get(id=id)
        cat.delete()
        return redirect("categories")


@login_required(login_url="login")
def confirm_delivery(request, id):
    delivery = Delivery.objects.get(id=id)
    if not request.user.is_staff:
        raise PermissionDenied()
    if request.method == "POST":
        delivery.is_delivered = request.POST["is_delivered"] == "on"
        delivery.save()
        return redirect("manage_del")


@login_required(login_url="login")
def manage_delivery(request):
    deliveries = Delivery.objects.all()
    if not request.user.is_staff:
        raise PermissionDenied()
    return render(
        request, "manager_site/manage_delivery.html", {"deliveries": deliveries}
    )


@login_required(login_url="login")
def manage_user(request):
    users = User.objects.all()
    if not request.user.is_staff:
        raise PermissionDenied()
    return render(request, "manager_site/manage_users.html", {"users": users})


@login_required(login_url="login")
def confirm_manager(request, id):
    users = User.objects.get(id=id)
    if not request.user.is_staff:
        raise PermissionDenied()
    if request.method == "POST":
        users.is_staff = request.POST["is_staff"] == "on"
        users.save()
        return redirect("manage_users")
