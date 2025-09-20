from datetime import datetime, timezone
import uuid
from django.db import models

# Menghubungkan setiap objek Product dengan user yang membuatnya
from django.contrib.auth.models import User

# Ingat setiap mau ada perubahan di models.py, harus migrate dan makemigrations
# IMPORTANT!!!
# Setiap kali kamu melakukan perubahan pada model, seperti menambahkan atau 
# mengubah atribut, kamu WAJIB melakukan migrasi untuk merefleksikan perubahan tersebut.

# Migrasi model adalah cara Django melacak perubahan pada model basis data kamu.
# Migrasi ini adalah instruksi untuk mengubah struktur tabel basis data sesuai dengan 
# perubahan model yang didefinisikan dalam kode terbaru kamu.

# makemigrations menciptakan berkas migrasi yang berisi perubahan model
# yang belum diaplikasikan ke dalam basis data.

class Product(models.Model):

    # Kode di bawah berfungsi untuk menghubungkan satu produk dengan satu user melalui sebuah relationship
    # Setiap news dapat terasosiasi dengan seorang user (many-to-one relationship)
    # null=True memungkinkan news yang sudah ada sebelumnya tetap valid tanpa harus memiliki user
    # on_delete=models.CASCADE berarti jika user dihapus, semua news milik user tersebut juga akan ikut terhapus

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('jersey', 'Jersey'),
        ('brand', 'Brand'),
    ]

    # Dari Tugas 2
    # ID Produk
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=20)
    
    # Tambahan dari Neal
    product_views = models.PositiveIntegerField(default=0)
    stock = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    brand_name = models.CharField(max_length=255, default="Generic Brand")
    
    # Dari Tutorial
    title = models.CharField(max_length=255, default="Produk")
    content = models.TextField(default="")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)
    news_views = models.PositiveIntegerField(default=0)
    # created_at = models.DateTimeField(default=lambda: datetime.now(timezone.utc))
    is_featured = models.BooleanField(default=False)
    
    # Mengembalikan nama produk
    def __str__(self):
        return self.name

    def increment_views(self):
        self.product_views += 1
        self.save()

    def get_stock(self):
        return self.stock
    
    def add_stock(self, amount):
        if amount > 0:
            self.stock += amount
            self.save()

    @property
    def is_out_of_stock(self):
        return self.stock <= 0
    
    @property
    def is_product_hot(self):
        return self.product_views > 20
    
    @property
    def price_in_rupiah(self):
        return f"Rp{self.price:,}".replace(',', '.')
