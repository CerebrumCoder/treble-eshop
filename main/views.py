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

def show_main(request):
    product_list = Product.objects.all()
    context = {
        'nama_aplikasi': 'Treble Eshop',
        'npm': '2406348282',
        'name': 'Neal Guarddin',
        'class': 'PBP A',
        'product_list': product_list
    }
    # Fungsi ini akan merender template main.html
    return render(request, 'main.html', context)

# Untuk tambah produk baru
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

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

# def add_employee(request):
#     employee = Employee.objects.create(
#         name = "Neal",
#         age = 15,
#         persona = "Neal adalah mahasiswa S1 Fasilkom UI",
#     )
#     context = {
#         'name': employee.name,
#         'age': employee.age,
#         'persona': employee.persona
#     }

#     return render(request, "employee.html", context)