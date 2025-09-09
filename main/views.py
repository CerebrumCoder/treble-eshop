# "from django.shortcuts import render" berguna untuk mengimpor fungsi render dari modul django.shortcuts
# Fungsi render akan digunakan untuk render tampilan HTML dengan menggunakan data yang diberikan.

from django.shortcuts import render
from django.http import HttpResponse

def show_main(request):
    context = {
        'nama_aplikasi': 'Treble Eshop',
        'npm': '2406348282',
        'name': 'Neal Guarddin',
        'class': 'PBP A',
    }
    # Fungsi ini akan merender template main.html
    return render(request, 'main.html', context)


# def index(request):
#     context = {
#         'nama_aplikasi': 'Treble Eshop',
#         'npm': '2406348282',
#         'name': 'Neal Guarddin',
#         'class': 'PBP A',
#     }
#     return render(request, 'index.html', context)