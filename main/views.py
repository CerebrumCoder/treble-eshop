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
from django.http import HttpResponse
from django.core import serializers

# Untuk merestriksi akses halaman tersebut berarti membatasi siapa saja yang boleh 
# membuka halaman tersebut, misalnya hanya pengguna yang sudah login atau admin
from django.contrib.auth.decorators import login_required

# Untuk menggunakan data dari cookies. 
import datetime
from django.http import HttpResponseRedirect
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
        'name': request.user.username,
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

# Untuk mengembalikan data semua produk dalam bentuk JSON
def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

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
    # Pake Form hasil buatan UserCreationForm()
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():

            # Untuk membuat dan menyimpan data dari form tersebut
            form.save()
            # Untuk menampilkan pesan kepada pengguna setelah melakukan suatu aksi
            messages.success(request, "Your account has been successfully created!")
            # Untuk melakukan redirect setelah data form berhasil disimpan
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)


# Untuk mengautentikasi pengguna yang ingin login.
def login_user(request):
    # Digunakan untuk memeriksa apakah pengguna mengirimkan 
    # permintaan login melalui halaman login
    if request.method == "POST":
        # Authentikasi pengguna memakai AuthenticationForm
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login.html', context)

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