Link PWS Tugas 2:\
https://neal-guarddin-trebleeshop.pbp.cs.ui.ac.id/\
Link Github Tugas 2:\
https://github.com/CerebrumCoder/treble-eshop

Jawaban pertanyaan:
1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

2. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html

3. Jelaskan peran settings.py dalam proyek Django!\
settings.py dalam Django memegang peran krusial sebagai pusat kendali utama dalam sebuah proyek. Anggap sebagai "otak" dari web aplikasi kita.
Pada intinya settings.py adalah sebuah "buku instruksi" yang memberi tahu Django semua yang perlu dia ketahui supaya dapat berjalan dengan benar.
Tanpa file ini, kita tidak akan tahu:
    - Database mana yang harus digunakan
    - Aplikasi mana saja yang menjadi bagian dari proyek
    - Cara mengamankan aplikasi dengan SECRET_KEY dan ALLOWED_HOSTS
    - Cara menangani file statis Template seperti CSS dan JavaScript
    - Apakah proyek web aplikasi sedang berjalan dalam mode pengembangan (banyak info error ketika DEBUG diset jadi TRUE) atau mode produksi (terkunci
dan efisien)

4. Bagaimana cara kerja migrasi database di Django?\
Secara sederhana, migrasi Django kerjanya mirip version control system (Git) untuk struktur database kita. Proses ini memastikan bahwa perubahan pada kode model (models.py) tercermin secara aman dan konsisten di dalam database yang sebenarnya. Analoginya seperti membangun rumah dengan arsitek dan tim konstruksi:
    - Arsitek (Kita dan makemigrations): Merancang cetak biru (blueprint) perubahan
    - Tim konstruksi (migrate): membaca cetak biru dan membangun atau mengubah struktur fisik bangunan

    Proses migrate melibatkan 3 komponen utama: kode kita (models.py), file migrasi (di dalam folder migrations/), dan tabel khusus di database kita bernama django_migrations.

    **Langkah 1: Kita mengubah models.py**\
    Kita membuka file models.py di web aplikasi dan melakukan perubahan/ Contohnya nambah line baris baru dalam models.py. Saat ini database kita belum berubah sama sekali. Kode python dan struktur database tidak sinkron.

    **Langkah 2: Kita menjalankan python manage.py makemigrations**\
    Django melakukan hal ini ketika command makemigrations dipanggil"
    1. Memeriksa perbedaan: Django membandingkan keadaan models.py saat ini dengan catatan file migrasi terakhir yang dibuat
    2. Mendeteksi perubahan: ternyata class di dalam models.py ada perubahan nambah baris kode nih
    3. Membuat cetak biru/blueprint: Django kemudian membuat sebuah file Python baru di dalam folder migrations/ web aplikasi. File ini bukan kode SQL. Tapi representasi perubahan dalam Python yang bersifat database-agnostik \

    **Langkah 3: Kita menjalankan python manage.py migrate**\
    Ketika ini dijalankan, Django melakukan tugas-tugas penting berikut:
    1. Django melihat dalam database kita dan memeriksa apakah ada perubahan atau tidak
    2. Membandingkan catatan: Django membandingkan catatan perubahan sebelum dan sesudah
    3. Menemukan migrasi baru: ketemu bahwa kode dalam file models.py ada perubahan. Berarti migrasi tersebut belum diterapkan
    4. Menerjemahkan ke SQL: Django membaca instruksi dari file migrasi dan menerjemahkannya ke dalam bahasa SQL yang sesuai dengan database yang kita gunakan (misalnya, PostgreSQL, MySQL, atau SQLite) 
    5. Eksekusi Perintah SQL: Django menjalankan perintah SQL tersebut pada database kita. Sekarang, struktur tabel di dalam model database kita benar-benar diubah
    6. Mencatat Pekerjaan Selesai ✅: Setelah berhasil, Django menambahkan satu baris baru ke tabel django_migrations yang mencatat bahwa migrasi tambahan baris kode telah berhasil diterapkan. Ini sangat penting untuk memastikan Django tidak mencoba menjalankan migrasi yang sama dua kali.

5. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?\
Karena Django memiliki filosofi "Batteries-Included" (semua sudah termasuk). Artinya Django datang sebagai paket lengkap yang menyediakan hampir semua alat yang dibutuhkan seorang developer untuk membangun aplikasi web yang kompleks dari awal hingga akhir. Bagi pemula, ini sangat berharga karena mengurangi kebingungan dan memungkinkan mereka pada fokus pada konsep-konsep inti pengembangan. Meskipun ada framework lain yang mungkin lebih "ringan" atau "fleksibel", Django unggul sebagai platform pembelajaran karena ia bertindak sebagai guru yang terstruktur. Ia tidak hanya memberi alat, tetapi juga mengajarkan cara membangun aplikasi yang aman, terukur, dan terorganisir dengan baik.\
Bagi seorang pemula, Django mengurangi beban kognitif dan menyediakan jalur yang jelas dari "tidak tahu apa-apa" menjadi "mampu membangun aplikasi web yang fungsional," menjadikannya fondasi yang sangat kokoh untuk karir di bidang pengembangan perangkat lunak


6. Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya? \
Tidak ada saya bisa memahami penjelasan Django dengan baik. Akhirnya tidak perlu melihat ke sumber lain karena cukup dari website PBP bisa mengerti sepenuhnya. 