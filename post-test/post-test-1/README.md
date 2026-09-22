# Sistem Pengelolaan Pemesanan Makanan pada Kantin Fakultas Teknik

Posttest 1 - Mata Kuliah Pemrograman Berorientasi Objek (PBO)

## Deskripsi Program

Program ini mensimulasikan proses pemesanan makanan/minuman di kantin
Fakultas Teknik secara sederhana: pengelolaan **menu**, pendaftaran
**pelanggan**, pembuatan **pesanan**, hingga **pembayaran**. Seluruh
program ditulis dengan pendekatan Object-Oriented Programming (OOP).

## Struktur Class

### 1. `Menu`
Merepresentasikan satu item menu (kategori **Makanan** atau **Minuman**).

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `nama_kantin`, `total_menu`, `kategori_valid` | Data bersama semua objek Menu |
| Atribut instance (public) | `kode_menu`, `nama`, `harga`, `kategori` | Unik tiap objek |
| Atribut instance (private) | `__stok` | Data inti, hanya lewat property `stok` |
| Instance method | `tambah_stok()`, `kurangi_stok()`, `tampilkan_info()` | |
| Class method | `dari_dict()` | Factory: buat objek dari dictionary |
| Static method | `validasi_kategori()` | Cek kategori valid (Makanan/Minuman) |
| Property | `stok` (getter & setter, validasi tidak boleh negatif) | |

### 2. `Pelanggan`
Merepresentasikan pembeli di kantin.

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `nama_kampus`, `total_pelanggan`, `diskon_member` | |
| Atribut instance (public) | `id_pelanggan`, `nama`, `is_member` | |
| Atribut instance (private) | `__saldo` | Saldo kantin, hanya lewat property `saldo` |
| Instance method | `isi_saldo()`, `tampilkan_profil()` | |
| Class method | `dari_dict()` | Factory: buat objek dari dictionary |
| Static method | `validasi_nama()` | Cek nama tidak kosong |
| Property | `saldo` (getter & setter, validasi tidak boleh negatif) | |

### 3. `Pesanan`
Menghubungkan objek `Pelanggan` dengan daftar objek `Menu` yang dipesan.

| Jenis | Nama | Keterangan |
|---|---|---|
| Atribut kelas | `nama_kantin`, `total_pesanan`, `status_valid` | |
| Atribut instance (public) | `id_pesanan`, `pelanggan`, `daftar_item` | |
| Atribut instance (private) | `__status` | Status pesanan, hanya lewat property `status` |
| Instance method | `tambah_item()`, `hitung_total()`, `selesaikan_pesanan()`, `tampilkan_pesanan()` | |
| Class method | `buat_pesanan_baru()` | Factory: buat objek Pesanan untuk seorang pelanggan |
| Static method | `validasi_jumlah()` | Cek jumlah item pesanan valid |
| Property | `status` (getter & setter, validasi hanya boleh Diproses/Selesai/Dibatalkan) | |

### 4. `Pembayaran`
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

## Cara Menjalankan

```bash
python 25091060130-RadhikaAdityaArifin-PT-1.py
```

Semua demonstrasi (pembuatan objek, pemanggilan method, dan pengujian
setter) akan langsung tercetak di terminal — tidak perlu input manual.

## Panduan Pengujian

Bagian `if __name__ == "__main__":` di `main.py` menjalankan pengujian
berikut secara berurutan:

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
6. **Statistik akhir** — menampilkan atribut kelas `total_menu`,
   `total_pelanggan`, `total_pesanan`, dan `total_pembayaran` untuk
   membuktikan atribut kelas terbagi ke seluruh objek.