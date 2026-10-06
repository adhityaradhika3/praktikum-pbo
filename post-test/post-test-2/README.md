# Sistem Pengelolaan Pemesanan Makanan pada Kantin Fakultas Teknik

Posttest 2 - Mata Kuliah Pemrograman Berorientasi Objek (PBO)

## Deskripsi Program

Program ini mensimulasikan proses pemesanan makanan/minuman di kantin
Fakultas Teknik secara sederhana: pengelolaan **menu**, pendaftaran
**pelanggan**, pembuatan **pesanan**, hingga **pembayaran**. Seluruh
program ditulis dengan pendekatan Object-Oriented Programming (OOP).


- **Inheritance**: `Menu` menjadi superclass dengan dua subclass, yaitu `Makanan` dan `Minuman`.
- **Relasi UML**: asosiasi (`Kasir` - `Pesanan`), agregasi (`Kantin` - `Menu`), dan komposisi (`Pesanan` - `ItemPesanan`).

## Struktur Class

Ringkasan seluruh class:

| Class | Peran | Hubungan |
|---|---|---|
| `Menu` | **Superclass**: data dan perilaku umum semua menu | Diwarisi `Makanan` dan `Minuman`; dimiliki `Kantin` (agregasi) |
| `Makanan` | **Subclass** dari `Menu` | Pewarisan |
| `Minuman` | **Subclass** dari `Menu` | Pewarisan |
| `Pelanggan` | Pembeli di kantin | Dirujuk oleh `Pesanan` |
| `ItemPesanan` | Satu baris item (menu + jumlah) di dalam pesanan | Bagian dari `Pesanan` (komposisi) |
| `Pesanan` | Pesanan milik seorang pelanggan | Terdiri dari `ItemPesanan`; digunakan `Kasir` (asosiasi) |
| `Pembayaran` | Transaksi pembayaran atas sebuah pesanan | Merujuk `Pesanan` |
| `Kantin` | Pengelola daftar menu kantin | Memiliki banyak `Menu` (agregasi) |
| `Kasir` | Petugas yang melayani pembayaran | Menggunakan `Pesanan` (asosiasi) |

### 1. `Menu` (Superclass)
Merepresentasikan item menu secara umum (kategori **Makanan** atau **Minuman**).

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `nama_kantin`, `total_menu`, `kategori_valid` | Data bersama semua objek Menu (termasuk subclass) |
| Atribut instance (public) | `kode_menu`, `nama`, `kategori` | Unik tiap objek |
| Atribut instance (protected) | `_harga` | Harga dasar, boleh dipakai langsung oleh subclass, dibaca lewat property `harga` |
| Atribut instance (private) | `__stok` | Data inti milik `Menu`, hanya lewat property `stok` |
| Instance method | `tambah_stok()`, `kurangi_stok()`, `hitung_harga_jual()`, `tampilkan_info()` | |
| Class method | `dari_dict()` | Factory: buat objek dari dictionary |
| Static method | `validasi_kategori()` | Cek kategori valid (Makanan/Minuman) |
| Property | `harga` (getter), `stok` (getter & setter, validasi tidak boleh negatif) | |

### 2. `Makanan` (Subclass dari `Menu`)

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `porsi_valid`, `tambahan_jumbo` | Pilihan porsi dan tambahan harga porsi jumbo |
| Atribut khusus subclass | `porsi` | `"Reguler"` atau `"Jumbo"` |
| Method di-override | `hitung_harga_jual()`, `tampilkan_info()`, `dari_dict()` | Perilaku berbeda dari `Menu` |

### 3. `Minuman` (Subclass dari `Menu`)

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `ukuran_valid`, `tambahan_besar` | Pilihan ukuran dan tambahan harga ukuran besar |
| Atribut khusus subclass | `ukuran` | `"Reguler"` atau `"Besar"` |
| Method di-override | `hitung_harga_jual()`, `tampilkan_info()`, `dari_dict()` | Perilaku berbeda dari `Menu` |

### 4. `Pelanggan`
Merepresentasikan pembeli di kantin.

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `total_pelanggan`, `diskon_member` | |
| Atribut instance (public) | `id_pelanggan`, `nama`, `is_member` | |
| Atribut instance (private) | `__saldo` | Saldo kantin, hanya lewat property `saldo` |
| Instance method | `isi_saldo()`, `tampilkan_profil()` | |
| Class method | `dari_dict()` | Factory: buat objek dari dictionary |
| Static method | `validasi_nama()` | Cek nama tidak kosong |
| Property | `saldo` (getter & setter, validasi tidak boleh negatif) | |

### 5. `ItemPesanan`
Satu baris item di dalam pesanan. Objek ini hanya dibuat oleh `Pesanan` (komposisi).

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut instance | `menu`, `jumlah` | `menu` hanya merujuk objek Menu yang dibuat di luar |
| Method | `hitung_subtotal()`, `__str__()` | Subtotal memakai `hitung_harga_jual()` milik menu |

### 6. `Pesanan`
Menghubungkan objek `Pelanggan` dengan daftar `ItemPesanan`.

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `total_pesanan`, `status_valid` | |
| Atribut instance (public) | `id_pesanan`, `pelanggan`, `daftar_item` | `daftar_item` berisi objek `ItemPesanan` |
| Atribut instance (private) | `__status` | Status pesanan, hanya lewat property `status` |
| Instance method | `tambah_item()`, `hitung_total()`, `selesaikan_pesanan()`, `tampilkan_pesanan()` | |
| Class method | `buat_pesanan_baru()` | Factory: buat objek Pesanan untuk seorang pelanggan |
| Static method | `validasi_jumlah()` | Cek jumlah item pesanan valid |
| Property | `status` (getter & setter, validasi hanya boleh Diproses/Selesai/Dibatalkan) | |

### 7. `Pembayaran`
Merepresentasikan transaksi pembayaran atas sebuah `Pesanan`.

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `nama_kantin`, `total_pembayaran`, `metode_valid` | |
| Atribut instance (public) | `id_pembayaran`, `pesanan`, `metode` | |
| Atribut instance (private) | `__jumlah_bayar` | Data finansial, hanya lewat property `jumlah_bayar` |
| Instance method | `proses_pembayaran()`, `tampilkan_struk()` | |
| Class method | `dari_pesanan()` | Factory: buat objek Pembayaran dari objek Pesanan |
| Static method | `validasi_metode()` | Cek metode pembayaran didukung (Tunai/Saldo Kantin/QRIS) |
| Property | `jumlah_bayar` (getter & setter, validasi tidak boleh negatif) | |

### 8. `Kantin`
Menampung daftar `Menu` yang dijual (agregasi).

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut instance | `nama`, `lokasi`, `_daftar_menu` | `_daftar_menu` berisi referensi objek Menu dari luar |
| Method | `tambah_menu()`, `hapus_menu()`, `cari_menu()`, `tampilkan_daftar_menu()` | `tambah_menu()` menerima `Menu`, `Makanan`, maupun `Minuman` |
| Property | `jumlah_menu` | Banyak menu yang terdaftar |

### 9. `Kasir`
Melayani pembayaran pesanan (asosiasi).

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut instance | `nama`, `shift` | Tidak ada atribut `pesanan` |
| Method | `layani_pembayaran(pesanan, metode)` | `Pesanan` diterima lewat parameter |


## Penerapan Relasi UML

| Relasi | Class | Kata kunci | Letak di kode |
|---|---|---|---|
| Asosiasi | `Kasir` → `Pesanan` | "menggunakan" | `Kasir.layani_pembayaran(pesanan, metode)` |
| Agregasi | `Kantin` ◇— `Menu` | "memiliki" | `Kantin.tambah_menu(menu)` dan list `_daftar_menu` |
| Komposisi | `Pesanan` ◆— `ItemPesanan` | "terdiri dari" | `Pesanan.tambah_item()` membuat `ItemPesanan(menu, jumlah)` |

### Asosiasi: `Kasir` menggunakan `Pesanan`
`Pesanan` diterima sebagai parameter method, dipakai sesaat untuk membuat
dan memproses `Pembayaran`, lalu dilepas. `Kasir` tidak menyimpan
`Pesanan` sebagai atribut, sehingga keduanya hidup mandiri.


### Agregasi: `Kantin` memiliki `Menu`
Objek `Menu` (juga `Makanan`/`Minuman`) dibuat di luar `Kantin`, lalu
didaftarkan ke list `_daftar_menu`. Saat menu dikeluarkan dengan
`hapus_menu()` atau `Kantin` dihapus dengan `del`, objek `Menu` tetap ada
di memori. Hal ini dibuktikan pada bagian pengujian.


### Komposisi: `Pesanan` terdiri dari `ItemPesanan`
`ItemPesanan` dibuat langsung di dalam `Pesanan.tambah_item()` dan tidak
punya arti tanpa pesanannya. Jika `Pesanan` dihapus, seluruh `ItemPesanan`
di dalamnya ikut musnah, sedangkan objek `Menu` yang dirujuk tetap ada.


## Penerapan Inheritance

### Pengujian "is-a"

| Pernyataan | Hasil | Relasi yang tepat |
|---|---|---|
| `Makanan` adalah `Menu` | Benar | Inheritance |
| `Minuman` adalah `Menu` | Benar | Inheritance |
| `Kantin` adalah `Menu` | Salah | Kantin memiliki Menu (Agregasi) |
| `ItemPesanan` adalah `Pesanan` | Salah | Pesanan terdiri dari ItemPesanan (Komposisi) |
| `Kasir` adalah `Pesanan` | Salah | Kasir menggunakan Pesanan (Asosiasi) |

### Ketentuan Inheritance

| Ketentuan | Penerapan |
|---|---|
| Superclass & subclass | Superclass `Menu`, subclass `Makanan` dan `Minuman` |
| Penggunaan `super()` | `super().__init__(nama, harga, stok, "Makanan")` dan `super().__init__(nama, harga, stok, "Minuman")`, sehingga `kategori` terisi otomatis |
| Atribut tambahan subclass | `Makanan.porsi` dan `Minuman.ukuran` |
| Method overriding | `hitung_harga_jual()` di-override: `Makanan` menambah harga untuk porsi Jumbo, `Minuman` menambah harga untuk ukuran Besar. `tampilkan_info()` di-override dengan memanggil `super().tampilkan_info()` lalu menambah info khusus. `dari_dict()` juga di-override agar sesuai konstruktor subclass |
| Protected | `_harga` pada `Menu`, dipakai langsung oleh `hitung_harga_jual()` di subclass |
| Private | `__stok` pada `Menu`, tidak bisa diakses langsung dari luar maupun subclass. Subclass memakai property `stok` yang diwariskan |


Karena `Pesanan.hitung_total()` dan `ItemPesanan.hitung_subtotal()`
memakai `hitung_harga_jual()`, total pesanan otomatis mengikuti harga
versi masing-masing jenis menu (misalnya porsi Jumbo atau ukuran Besar).

## Cara Menjalankan

```bash
python 25091060130-RadhikaAdityaArifin-PT-2.py
```

Semua demonstrasi (pembuatan objek, pemanggilan method, dan pengujian
setter) akan langsung tercetak di terminal, tidak perlu input manual.

## Panduan Pengujian

Bagian `if __name__ == "__main__":` pada file program menjalankan
pengujian berikut secara berurutan.

1. **Objek Menu** — membuat 2 objek (`Nasi Goreng` via konstruktor biasa,
   `Es Teh Manis` via factory method `dari_dict()`), lalu memanggil
   instance method (`tambah_stok`) dan static method (`validasi_kategori`).
2. **Objek Pelanggan** — membuat 2 objek (`Andi` member, `Budi` bukan
   member via `dari_dict()`), memanggil `isi_saldo()` dan
   `validasi_nama()`.
3. **Objek Pesanan** — membuat 2 pesanan lewat class method
   `buat_pesanan_baru()`, menambahkan item, menampilkan total harga
   (otomatis kena diskon member lewat `Pelanggan.diskon_member`), dan
   memanggil `validasi_jumlah()`.
4. **Objek Pembayaran** — membuat 2 pembayaran (metode `Saldo Kantin`
   dan `Tunai`) lewat class method `dari_pesanan()` maupun konstruktor
   biasa, memproses pembayaran, menampilkan struk, dan memanggil
   `validasi_metode()`.
5. **Uji setter (encapsulation)** — setiap property (`stok`, `saldo`,
   `status`, `jumlah_bayar`) diisi dengan nilai valid (berhasil) lalu
   nilai tidak valid (memicu `ValueError` yang ditangkap dengan
   `try-except` dan dicetak sebagai pesan peringatan).
6. **Inheritance** — membuat 2 objek `Makanan` (`Ayam Geprek` porsi Jumbo
   via konstruktor, `Mie Goreng` via `dari_dict()`) dan 2 objek `Minuman`
   (`Es Jeruk` ukuran Besar via konstruktor, `Kopi Hitam` via
   `dari_dict()`). `tampilkan_info()` mencetak info `Menu` lalu baris
   tambahan khusus subclass.
7. **Method overriding** — `hitung_harga_jual()` dipanggil pada objek
   `Menu`, `Makanan`, dan `Minuman`.

   | Objek | Hasil yang diharapkan |
   |---|---|
   | Nasi Goreng (`Menu`) | Rp15,000 |
   | Ayam Geprek (Jumbo) | Rp23,000 (18,000 + 5,000) |
   | Mie Goreng (Reguler) | Rp12,000 |
   | Es Jeruk (Besar) | Rp10,000 (7,000 + 3,000) |

8. **Uji is-a dan tingkat akses** — `isinstance()` dan `issubclass()`
   membuktikan `Makanan` adalah `Menu` (True) dan bukan `Minuman` (False).
   Atribut protected `_harga` terbaca, sedangkan akses `__stok` dari luar
   memicu `AttributeError`. Setter `stok` yang diwariskan tetap menolak
   nilai negatif.
9. **Agregasi** — 6 menu dibuat di luar lalu didaftarkan ke `Kantin`.
   Mendaftarkan `"Teh Botol"` (bukan objek `Menu`) ditolak. Setelah
   `hapus_menu()`, jumlah menu berkurang menjadi 5 tetapi objek `Es Teh
   Manis` masih bisa ditampilkan.
10. **Asosiasi** — `Kasir` melayani dua pesanan baru:

    | Pesanan | Skenario | Hasil yang diharapkan |
    |---|---|---|
    | PS003 (Citra, member) | 1 Ayam Geprek Jumbo + 2 Es Jeruk Besar via Saldo Kantin | Total Rp38,700 (diskon member 10% dari Rp43,000), pembayaran berhasil |
    | PS004 (Deni, non-member) | Mie Goreng + Kopi Hitam (Rp18,000) via Saldo Kantin | Gagal karena saldo Deni (Rp15,000) tidak cukup |
    | PS004 (Deni) | Dibayar ulang via QRIS | Berhasil, struk tercetak |

11. **Komposisi** — isi `daftar_item` pada pesanan terbukti berupa objek
    `ItemPesanan`. Sebuah pesanan sementara dihapus dengan `del`, dan
    `ItemPesanan` di dalamnya ikut musnah, sedangkan objek `Mie Goreng`
    tetap ada.
12. **Siklus hidup agregasi** — `Kantin` dihapus dengan `del`, tetapi objek
    `Ayam Geprek` dan `Kopi Hitam` tetap ada dan masih bisa ditampilkan.
13. **Statistik akhir** — menampilkan atribut kelas `total_menu`,
    `total_pelanggan`, `total_pesanan`, dan `total_pembayaran`.
    Hasil yang diharapkan: 6 menu, 4 pelanggan, 5 pesanan, 5 pembayaran.