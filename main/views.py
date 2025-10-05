# UserCreationForm adalah impor formulir bawaan yang memudahkan pembuatan formulir 
# pendaftaran pengguna dalam aplikasi web. Jadinya kita engga buat form dari nol banget.

# Singkatnya, fungsi authenticate dan login yang di-import di atas adalah fungsi bawaan 
# Django yang dapat digunakan untuk melakukan autentikasi dan login (jika autentikasi berhasil)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# "from django.shortcuts import render" berguna untuk mengimpor fungsi render dari modul django.shortcuts
# Fungsi render akan digunakan untuk render tampilan HTML dengan menggunakan data yang diberikan.

from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from main.forms import ProductForm

# Untuk mengembalikan data dalam bentuk XML
# HttpResponse merupakan class yang digunakan 
# untuk menyusun respon yang ingin dikembalikan oleh server ke user
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core import serializers

# Untuk AJAX
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404

# Untuk merestriksi akses halaman tersebut berarti membatasi siapa saja yang boleh 
# membuka halaman tersebut, misalnya hanya pengguna yang sudah login atau admin
from django.contrib.auth.decorators import login_required

# Untuk menggunakan data dari cookies. 
import datetime
from django.urls import reverse

# Potongan kode di bawah ini untuk restriksi bisa akses laman itu apabila sudah login
@login_required(login_url='/login')
def show_main(request):
    # Default filternya "all"
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        product_list = Product.objects.all()

    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        'npm': '2406348282',
        'name': request.user.username.capitalize(),
        'class': 'PBP A',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    # Fungsi ini akan merender template main.html
    return render(request, 'main.html', context)

# Buatin form untuk mobil baru
# Bedanya <a> dan <button>
# def create_car(request):
#     form = CarForm(request.POST or None)

#     if form.is_valid() and request.method == "POST":
#         new_car = Car.objects.create(
#             name = form.cleaned_data["name"],
#             brand = form.cleaned_data["brand"],
#             stock = form.cleaned_data["stock"],
#         )

#     return render(request, "index.html")

# Untuk tambah produk baru
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        # Parameter commit=False pada potongan kode di atas 
        # digunakan agar Django tidak langsung menyimpan objek 
        # hasil form ke database. Dengan begitu, kita memiliki 
        # kesempatan untuk memodifikasi objek tersebut terlebih 
        # dahulu sebelum disimpan
        product_entry = form.save(commit=False)
        product_entry.user = request.user  # Mengaitkan produk dengan user yang sedang login
        product_entry.save()
        
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "create_product.html", context)


# Potongan kode di bawah ini untuk restriksi bisa akses laman itu apabila sudah login
@login_required(login_url='/login') 
# Untuk melihat produk secara detail
def show_product(request, id):
    # Ambil produk berdasarkan id
    product = get_object_or_404(Product, pk=id)
    # Tambahkan jumlah views
    product.increment_views()

    context = {
        'product': product,
    }

    return render(request, "product_detail.html", context)


# <----------------- SHOW DATA AS XML AND JSON ----------------->
# Untuk mengembalikan data semua produk dalam bentuk XML
def show_xml(request):
    product_list = Product.objects.all()

    # serializers digunakan untuk translate objek 
    # model menjadi format lain seperti dalam fungsi ini adalah XML.
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

# Untuk mengembalikan data berdasarkan ID dalam bentuk XML
def show_xml_by_id(request, product_id):
    # Untuk mendapatkan data berdasarkan ID, kita dapat menggunakan 
    # berbagai jenis method milik Django, dua di antaranya adalah filter() 
    # dan get(). Namun, kedua method ini memiliki perbedaan yang cukup signifikan. 
    # filter() dapat digunakan untuk mengambil data satu objek atau berbagai objek 
    # yang memenuhi kondisi yang ditetapkan, sedangkan get() dapat digunakan untuk 
    # mengambil data satu objek saja.
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
       return HttpResponse(status=404)

# Untuk mengembalikan data berdasarkan ID dalam bentuk JSON
def show_json_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        json_data = serializers.serialize("json", product_item)
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
       return HttpResponse(status=404)


# <----------------- USER AUTHENTICATION ----------------->

# Untuk menghasilkan formulir registrasi secara otomatis dan menghasilkan 
# akun pengguna ketika data di-submit dari form
def register(request):
    """
    Support dua mode:
    - Non-AJAX (render template biasa)  -> untuk submit normal
    - AJAX (fetch dari register.html)   -> balas JSON {ok:bool, errors?, redirect?}
    """
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        # Deteksi AJAX sederhana: header dari fetch()
        is_ajax = (
            request.headers.get("X-Requested-With", "").lower() in ("fetch", "xmlhttprequest")
            or "application/json" in request.headers.get("Accept", "").lower()
        )

        if form.is_valid():
            # Simpan user baru
            form.save()

            if is_ajax:
                # ✔️ Berhasil — balas JSON + arahkan ke halaman login
                return JsonResponse(
                    {"ok": True, "redirect": reverse("main:login")},
                    status=201,  # Created
                )

            # Non-AJAX: pakai messages + redirect
            messages.success(request, "Your account has been successfully created!")
            return redirect("main:login")

        # Gagal validasi form
        if is_ajax:
            # Format errors jadi dict[str, list[str]] supaya gampang ditampilkan di JS
            errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
            # Balas 400 agar res.ok === false pada fetch()
            return JsonResponse({"ok": False, "errors": errors}, status=400)

        # Non-AJAX: render ulang halaman dengan error bawaan form
        return render(request, "register.html", {"form": form})
    
    # GET — render form kosong
    return render(request, "register.html", {"form": form})


# Untuk mengautentikasi pengguna yang ingin login.
def login_user(request):
    # Digunakan untuk memeriksa apakah pengguna mengirimkan 
    # permintaan login melalui halaman login
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        # Anggap request AJAX jika header ini ada/accept json
        is_ajax = (
            request.headers.get('X-Requested-With', '').lower() in ('fetch', 'xmlhttprequest')
            or 'application/json' in request.headers.get('Accept', '').lower()
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            resp = HttpResponseRedirect(reverse("main:show_main"))
            resp.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))

            if is_ajax:
                return JsonResponse({"ok": True, "redirect": reverse("main:show_main")}, status=200)
            return resp

        # ---- INVALID CREDENTIALS ----
        if is_ajax:
            # kembalikan 400 agar fetch tidak mengira sukses
            return JsonResponse({"ok": False, "error": "Email/username atau password salah"}, status=400)

        # non-AJAX: render ulang dengan error bawaan form
        return render(request, 'login.html', {"form": form})

    # GET
    form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})

# Untuk melakukan mekanisme logout
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


# Fungsi untuk menambahkan fitur edit product pada web aplikasi
def edit_product(request, id):
    products = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=products)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    
    context = {
        'form': form,
    }

    return render(request, 'edit_product.html', context)

# Fungsi untuk menambahkan fitur hapus product pada web aplikasi
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

# Untuk mengembalikan data semua produk dalam bentuk JSON
# ---- LIST JSON dgn filter ?mine=1 ----
def show_json(request):
    qs = Product.objects.all().order_by('-id')

    # Query param ?mine=1 → tampilkan milik user saja
    mine = (request.GET.get('mine') or '').strip().lower()
    if mine in ('1', 'true', 'yes'):
        if request.user.is_authenticated:
            qs = qs.filter(user=request.user)
        else:
            return JsonResponse([], safe=False)  # belum login → kosong

    # _pdict() kirim field yang dibutuhkan front-end (termasuk is_owner)
    data = [_pdict(p, request) for p in qs]
    return JsonResponse(data, safe=False)

# ============== AJAX (Tutorial 5 style) ==============

# ---- Serializer ringan utk Product -> dict ----
def _pdict(p, request=None):
    # NOTE: kalau sering render dari JSON ke HTML, biasakan "trim" string
    def s(v): return (v or "").strip()

    d = {
        "id": str(p.id),
        "name": s(p.name),
        "description": s(p.description),
        "price": int(getattr(p, "price", 0)),
        "stock": int(getattr(p, "stock", 0)),
        "thumbnail": s(getattr(p, "thumbnail", "")),
        "brand_name": s(getattr(p, "brand_name", "")),
        "rating": int(getattr(p, "rating", 0)),
        "product_views": int(getattr(p, "product_views", 0)),
        "is_product_hot": bool(getattr(p, "is_product_hot", False)),
    }
    if hasattr(p, "created_at") and p.created_at:
        d["created_at"] = p.created_at.isoformat()

    # Tampilkan tombol Edit/Delete hanya utk pemilik
    d["is_owner"] = bool(request and request.user.is_authenticated and getattr(p, "user_id", None) == request.user.id)
    return d

@require_POST
def add_product_entry_ajax(request):
    name = strip_tags((request.POST.get("name") or "").strip())
    description = strip_tags((request.POST.get("description") or "").strip())
    price = request.POST.get("price")
    stock = request.POST.get("stock") or 0
    thumbnail = strip_tags((request.POST.get("thumbnail") or "").strip())

    if not name:
        return HttpResponseBadRequest("Name is required")
    try:
        price = int(price); stock = int(stock)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid number")

    p = Product(name=name, description=description, price=price)
    if hasattr(p, "stock"): p.stock = stock
    if hasattr(p, "thumbnail"): p.thumbnail = thumbnail
    if request.user.is_authenticated and hasattr(p, "user"):
        p.user = request.user

    p.save()
    return JsonResponse(_pdict(p, request), status=201)  # balas item utk prepend di UI

@require_POST
def edit_product_entry_ajax(request, id):
    p = get_object_or_404(Product, pk=id)

    # NOTE: batasi edit utk pemilik (aktifkan kalau perlu)
    # if p.user_id != request.user.id: return HttpResponse(status=403)

    if "name" in request.POST:
        p.name = strip_tags((request.POST.get("name") or "").strip())
    if "description" in request.POST:
        p.description = strip_tags((request.POST.get("description") or "").strip())
    if "price" in request.POST:
        try: p.price = int(request.POST.get("price"))
        except (TypeError, ValueError): return HttpResponseBadRequest("Invalid price")
    if "stock" in request.POST and hasattr(p, "stock"):
        try: p.stock = int(request.POST.get("stock"))
        except (TypeError, ValueError): return HttpResponseBadRequest("Invalid stock")
    if "thumbnail" in request.POST and hasattr(p, "thumbnail"):
        p.thumbnail = strip_tags((request.POST.get("thumbnail") or "").strip())

    p.save()
    return JsonResponse(_pdict(p, request), status=200)  # balas item utk replace di UI

@require_POST
def delete_product_ajax(request, id):
    p = get_object_or_404(Product, pk=id)
    # NOTE: batasi delete utk pemilik (aktifkan kalau perlu)
    # if p.user_id != request.user.id: return HttpResponse(status=403)

    pid = str(p.id)
    p.delete()
    return JsonResponse({"ok": True, "id": pid}, status=200)  # UI remove card by data-id