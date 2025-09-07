import uuid
from django.db import models

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
    # CATEGORY_CHOICES = [
    #     ('transfer', 'Transfer'),
    #     ('update', 'Update'),
    #     ('exclusive', 'Exclusive'),
    #     ('match', 'Match'),
    #     ('rumor', 'Rumor'),
    #     ('analysis', 'Analysis'),
    # ]

    # Dari Tugas 2
    # ID Produk
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50)
    is_featured = models.BooleanField(default=False)

    # Tambahan dari Neal
    product_views = models.PositiveIntegerField(default=0)
    
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # title = models.CharField(max_length=255)
    # content = models.TextField()
    # category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    # thumbnail = models.URLField(blank=True, null=True)
    # news_views = models.PositiveIntegerField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    # is_featured = models.BooleanField(default=False)
    
    # Mengembalikan nama produk
    def __str__(self):
        return self.name
    
    @property
    def is_product_hot(self):
        return self.product_views > 20

    def increment_views(self):
        self.product_views += 1
        self.save()