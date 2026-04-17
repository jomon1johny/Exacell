import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import Sheet
from django.template.loader import get_template
from django.http import HttpResponse

try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None


User = get_user_model()


# SAFE FLOAT FUNCTION
def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0


# ---------------- REGISTER ----------------
def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_approved=False
        )

        return render(request, "register.html", {
            "success": "Registration successful. Wait for admin approval."
        })

    return render(request, "register.html")


# ---------------- LOGIN ----------------
@never_cache
def login_page(request):

    if request.user.is_authenticated:
        return redirect("sheet")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            if not user.is_approved:
                messages.error(
                    request,
                    "Your account is waiting for admin approval."
                )
                return redirect("login")

            login(request, user)
            return redirect("sheet")

        else:
            messages.error(
                request,
                "Invalid Username or Password."
            )

    return render(request, "login.html")


# ---------------- LOGOUT ----------------
@never_cache
def logout_page(request):
    logout(request)
    request.session.flush()
    return redirect("login")


# ---------------- SHEET PAGE ----------------
@never_cache
@login_required(login_url='login')
def sheet(request):
    return render(request, "sheet.html")


# ---------------- USER VIEW DATA ----------------
@login_required
def view_data(request):

    data = Sheet.objects.filter(
        user=request.user
    ).order_by("-id")

    return render(request, "view_data.html", {
        "data": data
    })


# ---------------- AUTOSAVE ----------------
@login_required
@require_POST
def autosave(request):

    try:
        data = json.loads(request.body)

        sheet = Sheet()

        sheet.user = request.user

        sheet.gem = data.get("gem")
        sheet.date = data.get("date") or None
        sheet.place = data.get("place")
        sheet.officer = data.get("officer")
        sheet.contact = data.get("contact")
        sheet.marketing = data.get("marketing")
        sheet.item = data.get("item")

        sheet.rate = safe_float(data.get("rate"))
        sheet.gst = safe_float(data.get("gst"))

        sheet.company = data.get("company")
        sheet.bill = data.get("bill")
        sheet.billdate = data.get("billdate") or None

        sheet.qty = safe_float(data.get("qty"))
        sheet.price = safe_float(data.get("price"))
        sheet.amount = safe_float(data.get("amount"))

        sheet.fr = safe_float(data.get("fr"))
        sheet.fb = safe_float(data.get("fb"))
        sheet.tfr = safe_float(data.get("tfr"))

        sheet.orderby = data.get("orderby")

        sheet.save()

        return JsonResponse({
            "status": "success",
            "id": sheet.id
        })

    except Exception as e:

        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)


# ---------------- ADMIN DATA ----------------
@staff_member_required
def admin_data(request):

    data = Sheet.objects.filter(
        user__is_superuser=True
    ).select_related("user").order_by("-id")

    return render(request, "admin_data.html", {
        "data": data
    })
# ---------------- ADMIN OWN DATA ----------------
@staff_member_required
def admin_own_data(request):

    data = Sheet.objects.filter(
        user=request.user
    ).order_by("-id")

    return render(request, "admin_own_data.html", {
        "data": data
    })


# ---------------- UPDATE DATA ----------------
@login_required
def update_data(request, id):

    sheet = get_object_or_404(Sheet, id=id)

    if not request.user.is_staff and sheet.user != request.user:
        return redirect("sheet")

    if request.method == "POST":

        sheet.gem = request.POST.get("gem")
        sheet.date = request.POST.get("date") or None
        sheet.place = request.POST.get("place")
        sheet.officer = request.POST.get("officer")
        sheet.contact = request.POST.get("contact")
        sheet.marketing = request.POST.get("marketing")
        sheet.item = request.POST.get("item")

        sheet.rate = safe_float(request.POST.get("rate"))
        sheet.gst = safe_float(request.POST.get("gst"))

        sheet.company = request.POST.get("company")
        sheet.bill = request.POST.get("bill")
        sheet.billdate = request.POST.get("billdate") or None

        sheet.qty = safe_float(request.POST.get("qty"))
        sheet.price = safe_float(request.POST.get("price"))
        sheet.amount = safe_float(request.POST.get("amount"))

        sheet.fr = safe_float(request.POST.get("fr"))
        sheet.fb = safe_float(request.POST.get("fb"))
        sheet.tfr = safe_float(request.POST.get("tfr"))

        sheet.orderby = request.POST.get("orderby")

        sheet.save()

        if request.user.is_staff:
            return redirect("admin_data")
        else:
            return redirect("view_data")

    return render(request, "update_data.html", {
        "data": sheet
    })


# ---------------- DELETE DATA ----------------
@login_required
def delete_data(request, id):

    sheet = get_object_or_404(Sheet, id=id)

    if not request.user.is_staff and sheet.user != request.user:
        return redirect("sheet")

    sheet.delete()

    if request.user.is_staff:
        return redirect("admin_data")

    return redirect("view_data")


# ---------------- MANAGE USERS ----------------
@staff_member_required
def manage_users(request):

    if not request.user.is_superuser:
        return redirect("sheet")

    users = User.objects.all().order_by("-id")

    return render(request, "manage_users.html", {
        "users": users
    })


# ---------------- APPROVE USER ----------------
@staff_member_required
def approve_user(request, id):

    if not request.user.is_superuser:
        return redirect("sheet")

    user = get_object_or_404(User, id=id)

    user.is_approved = True
    user.save()

    return redirect("manage_users")


# ---------------- DELETE USER ----------------
@staff_member_required
def delete_user(request, id):

    if not request.user.is_superuser:
        return redirect("sheet")

    user = get_object_or_404(User, id=id)

    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect("manage_users")

    user.delete()

    return redirect("manage_users")


# ---------------- TOGGLE STAFF ----------------
@staff_member_required
def toggle_staff(request, id):

    if not request.user.is_superuser:
        return redirect("sheet")

    user = get_object_or_404(User, id=id)

    if user == request.user:
        messages.error(request, "You cannot change your own staff status.")
        return redirect("manage_users")

    user.is_staff = not user.is_staff
    user.save()

    return redirect("manage_users")

@staff_member_required
def all_data(request):

    data = Sheet.objects.select_related("user").order_by("-id")

    return render(request, "all_data.html", {
        "data": data
    })
    
    
@staff_member_required
def download_pdf(request):

    if not request.user.is_superuser:
        return redirect("sheet")

    if not pisa:
        return HttpResponse("PDF feature not available in production")

    data = Sheet.objects.select_related("user").order_by("-id")

    template = get_template("pdf_template.html")

    html = template.render({
        "data": data
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="exacell_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("PDF Generation Error")

    return response