from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings



from .models import Product, Contact
from .forms import ContactForm, RegisterForm


def list(request):
    # ملاحظة: هذي الأسطر بتعطي KeyError لو m أو price مو موجودين بالـ session
    # إذا تبين نخليها آمنة قولي لي
    print(request.session['m'])
    tax = request.session['price']
    request.session['value'] = "welcome"
    tax = tax + (tax * 0.15)
    request.session['price'] = tax

    cat_id = request.GET.get("category_id")
    _search = request.GET.get("search")

    products = Product.objects.all()

    if cat_id:
        products = Product.objects.filter(Category_id=cat_id)

    if _search:
        products = Product.objects.filter(name__icontains=_search)

    context = {
        "prod": products,
    }
    return render(request, "products/list.html", context)


def product_details(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related('details'),
        id=product_id
    )

    context = {
        "product": product
    }
    return render(request, "products/product_info.html", context)


def cart_view(request):
    cart = request.session.get('cart', {})
    context = {"cart": cart}
    return render(request, "products/cart.html", context)


def add_to_cart(request, pid):
    product = get_object_or_404(Product, id=pid)

    cart = request.session.get('cart', {})
    pid_str = str(pid)

    if pid_str in cart:
        cart[pid_str]['quantity'] += 1
    else:
        cart[pid_str] = {
            'id': pid,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart
    request.session['cart_counter'] = sum(item['quantity'] for item in cart.values())
    request.session.modified = True

    messages.success(request, 'تمت الإضافة للسلة')
    return redirect(request.META.get('HTTP_REFERER', 'list'))


@login_required(login_url='login')
def checkout(request):
    return render(request, "products/checkout.html")


def auth_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('list')
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


def auth_register(request):
    if request.method == "POST":
        form = RegisterForm(request, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})



def send_email(request,email):
    send_mail(
        'شركة المنار للتسويق الالكتروني ',
        'تم استلام بريدك الالكتروني وسيتم معالجة طلبك خلال 3 ايام عمل شكرا لك ',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
    
# -----------------ex:11-----------------------------
def contact(request):
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            
            clean_name = form.cleaned_data['name']
            clean_email = form.cleaned_data['email']
            clean_subject = form.cleaned_data['subject']
            clean_message = form.cleaned_data['message']

            
            Contact.objects.create(
                name=clean_name,
                email=clean_email,
                subject=clean_subject,
                message=clean_message
            )

            
            send_email(request, clean_email)
            
            messages.success(request, 'تم إرسال رسالتك بنجاح')
            return render(request, 'contact.html', {'form': ContactForm()})
        else:
            messages.error(request, 'يرجى التاكد من صحة البيانات ')

    return render(request, 'contact.html', {'form': form})