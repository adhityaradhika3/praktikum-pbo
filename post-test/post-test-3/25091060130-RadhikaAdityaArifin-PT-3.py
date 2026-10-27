from abc import ABC, abstractmethod


class Menu(ABC):
    """Kontrak abstrak untuk semua menu kantin."""

    def __init__(self, nama, harga, stok):
        self.nama = nama
        self._harga = harga
        self.__stok = stok

    @property
    def stok(self):
        return self.__stok

    def kurangi_stok(self, jumlah):
        if jumlah <= 0 or jumlah > self.__stok:
            return False
        self.__stok -= jumlah
        return True

    @abstractmethod
    def hitung_harga_jual(self):
        """Menghasilkan harga jual sesuai jenis menu."""

    @abstractmethod
    def detail(self):
        """Menghasilkan keterangan khusus dari subclass."""

    def tampilkan_info(self):
        """Method konkret yang dipakai bersama oleh seluruh subclass."""
        print(f"{self.nama} | {self.detail()} | Rp{self.hitung_harga_jual():,} | stok {self.stok}")

    def __str__(self):
        return f"{self.nama} (Rp{self.hitung_harga_jual():,})"

    def __lt__(self, menu_lain):
        return self.hitung_harga_jual() < menu_lain.hitung_harga_jual()


class Makanan(Menu):
    tambahan_jumbo = 5000

    def __init__(self, nama, harga, stok, porsi="Reguler"):
        super().__init__(nama, harga, stok)
        self.porsi = porsi

    def hitung_harga_jual(self):
        if self.porsi == "Jumbo":
            return self._harga + Makanan.tambahan_jumbo
        return self._harga

    def detail(self):
        return f"Makanan, porsi {self.porsi}"


class Minuman(Menu):
    tambahan_besar = 3000

    def __init__(self, nama, harga, stok, ukuran="Reguler"):
        super().__init__(nama, harga, stok)
        self.ukuran = ukuran

    def hitung_harga_jual(self):
        if self.ukuran == "Besar":
            return self._harga + Minuman.tambahan_besar
        return self._harga

    def detail(self):
        return f"Minuman, ukuran {self.ukuran}"


class Pelanggan:
    def __init__(self, nama, is_member=False):
        self.nama = nama
        self.is_member = is_member


class ItemPesanan:
    """Bagian dari Pesanan: dibuat dan dimiliki oleh pesanan (komposisi)."""

    def __init__(self, menu, jumlah):
        self.menu = menu
        self.jumlah = jumlah

    def hitung_subtotal(self):
        return self.menu.hitung_harga_jual() * self.jumlah

    def __str__(self):
        return f"{self.jumlah}x {self.menu.nama}"


class Pesanan:
    def __init__(self, pelanggan):
        self.pelanggan = pelanggan
        self.daftar_item = []

    def tambah_item(self, menu, jumlah):
        if menu.kurangi_stok(jumlah):
            self.daftar_item.append(ItemPesanan(menu, jumlah))
            return True
        print(f"Stok {menu.nama} tidak cukup atau jumlah tidak valid.")
        return False

    def hitung_total(self):
        total = sum(item.hitung_subtotal() for item in self.daftar_item)
        return total * 0.9 if self.pelanggan.is_member else total

    def tampilkan(self):
        print(f"Pesanan untuk {self.pelanggan.nama}:")
        for item in self.daftar_item:
            print(f"  {item} = Rp{item.hitung_subtotal():,}")
        print(f"Total: Rp{self.hitung_total():,.0f}")


class Kantin:
    """Menyimpan referensi menu yang dibuat secara mandiri di luar Kantin."""

    def __init__(self, nama):
        self.nama = nama
        self._daftar_menu = []

    def tambah_menu(self, menu):
        self._daftar_menu.append(menu)

    def tampilkan_menu(self):
        print(f"Daftar menu {self.nama}:")
        for menu in self._daftar_menu:
            menu.tampilkan_info()


class Kasir:
    """Berkolaborasi dengan Pesanan yang diberikan saat melayani (asosiasi)."""

    def __init__(self, nama):
        self.nama = nama

    def layani(self, pesanan):
        print(f"Kasir {self.nama} melayani pesanan.")
        pesanan.tampilkan()


class EmailNotifier:
    def kirim_pesan(self, pesan):
        print(f"Email: {pesan}")


class LayarKasir:
    def kirim_pesan(self, pesan):
        print(f"Layar kasir: {pesan}")


def umumkan(notifier, pesan):
    """Duck typing: cukup memiliki method kirim_pesan()."""
    notifier.kirim_pesan(pesan)


def main():
    print("=== SISTEM PEMESANAN KANTIN ===")

    # Bukti kelas abstrak tidak dapat dibuat menjadi objek.
    try:
        Menu("Menu abstrak", 1000, 1)
    except TypeError as error:
        print(f"Bukti abstraksi: Menu tidak dapat diinstansiasi ({error})")

    ayam_geprek = Makanan("Ayam Geprek", 18000, 5, "Jumbo")
    mie_goreng = Makanan("Mie Goreng", 12000, 8)
    es_jeruk = Minuman("Es Jeruk", 7000, 10, "Besar")
    kopi = Minuman("Kopi Hitam", 6000, 10)

    kantin = Kantin("Kantin Fakultas Teknik")
    for menu in (ayam_geprek, mie_goreng, es_jeruk, kopi):
        kantin.tambah_menu(menu)
    kantin.tampilkan_menu()

    # Polimorfisme pewarisan: satu loop, implementasi method subclass berbeda.
    print("\nHarga jual (method yang dioverride):")
    for menu in (ayam_geprek, mie_goreng, es_jeruk, kopi):
        print(f"{menu.nama}: Rp{menu.hitung_harga_jual():,}")

    pelanggan = Pelanggan("Radhika", is_member=True)
    pesanan = Pesanan(pelanggan)
    pesanan.tambah_item(ayam_geprek, 1)
    pesanan.tambah_item(es_jeruk, 2)
    kasir = Kasir("Dina")
    kasir.layani(pesanan)

    # Duck typing: dua kelas yang tidak berhubungan memakai satu fungsi.
    print("\nDemo duck typing:")
    for notifier in (EmailNotifier(), LayarKasir()):
        umumkan(notifier, "Pesanan siap diambil")

    # Operator overloading: __str__ dan __lt__ pada Menu.
    print(f"\nRepresentasi menu: {ayam_geprek}")
    print(f"{kopi.nama} lebih murah dari {es_jeruk.nama}: {kopi < es_jeruk}")


if __name__ == "__main__":
    main()
