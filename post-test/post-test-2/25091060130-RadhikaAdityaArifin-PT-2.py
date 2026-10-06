class Menu:
    """Superclass: atribut dan method yang dimiliki SEMUA jenis menu (Makanan/Minuman)."""
    #Atribut kelas
    nama_kantin = "Kantin Fakultas Teknik"
    total_menu = 0
    kategori_valid = ["Makanan", "Minuman"]

    def __init__(self, nama, harga, stok, kategori):
        Menu.total_menu += 1
        #Atribut instance
        self.kode_menu = f"MN{Menu.total_menu:03d}" 
        self.nama = nama                              
        self._harga = harga                           # protected: dipakai langsung oleh subclass
        if not Menu.validasi_kategori(kategori):
            print(f"Peringatan: kategori '{kategori}' tidak dikenal.")
        self.kategori = kategori                      
        self.stok = stok                              # lewat setter -> private __stok (eksklusif milik Menu)

    #Instance method
    def tambah_stok(self, jumlah):
        """Menambah stok menu."""
        if jumlah <= 0:
            print("Jumlah tambah stok harus lebih dari 0.")
            return
        self.stok = self.stok + jumlah
        print(f"Stok {self.nama} bertambah {jumlah}. Stok sekarang: {self.stok}")

    def kurangi_stok(self, jumlah):
        """Mengurangi stok menu, dipakai saat ada pesanan masuk."""
        if jumlah > self.stok:
            print(f"Stok {self.nama} tidak cukup!")
            return False
        self.stok = self.stok - jumlah
        return True

    def hitung_harga_jual(self):
        """Harga jual per item. Method ini di-override oleh subclass."""
        return self._harga

    def tampilkan_info(self):
        print(f"[{self.kode_menu}] {self.nama} ({self.kategori}) - "
              f"Rp{self.harga:,} | Stok: {self.stok}")

    #Class method 
    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat objek Menu dari data dictionary."""
        return cls(data["nama"], data["harga"], data["stok"], data["kategori"])

    #Static method
    @staticmethod
    def validasi_kategori(kategori):
        """Mengecek apakah kategori termasuk kategori yang valid (Makanan/Minuman)."""
        return kategori in Menu.kategori_valid

    #Encapsulation: getter & setter
    @property
    def harga(self):
        """Getter harga dasar (nilainya disimpan di atribut protected _harga)."""
        return self._harga

    @property
    def stok(self):
        """Getter -- dipanggil seperti atribut biasa."""
        return self.__stok

    @stok.setter
    def stok(self, nilai):
        """Setter -- validasi agar stok tidak pernah negatif."""
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif.")
        self.__stok = nilai


class Makanan(Menu):
    """Subclass Menu: menambah atribut porsi dan harga tambahan untuk porsi jumbo."""
    #Atribut kelas
    porsi_valid = ["Reguler", "Jumbo"]
    tambahan_jumbo = 5000

    def __init__(self, nama, harga, stok, porsi="Reguler"):
        super().__init__(nama, harga, stok, "Makanan")   # kategori otomatis "Makanan"
        if porsi not in Makanan.porsi_valid:
            print(f"Peringatan: porsi '{porsi}' tidak dikenal, dipakai 'Reguler'.")
            porsi = "Reguler"
        self.porsi = porsi                                # atribut khusus Makanan

    #Method overriding
    def hitung_harga_jual(self):
        """Porsi Jumbo dikenakan tambahan harga."""
        if self.porsi == "Jumbo":
            return self._harga + Makanan.tambahan_jumbo   # _harga: protected, diakses langsung
        return self._harga

    def tampilkan_info(self):
        super().tampilkan_info()
        print(f"    Porsi: {self.porsi} | Harga jual: Rp{self.hitung_harga_jual():,}")

    #Class method (override)
    @classmethod
    def dari_dict(cls, data):
        """Factory method khusus Makanan (kategori tidak perlu diisi, porsi opsional)."""
        return cls(data["nama"], data["harga"], data["stok"], data.get("porsi", "Reguler"))


class Minuman(Menu):
    """Subclass Menu: menambah atribut ukuran dan harga tambahan untuk ukuran besar."""
    #Atribut kelas
    ukuran_valid = ["Reguler", "Besar"]
    tambahan_besar = 3000

    def __init__(self, nama, harga, stok, ukuran="Reguler"):
        super().__init__(nama, harga, stok, "Minuman")   # kategori otomatis "Minuman"
        if ukuran not in Minuman.ukuran_valid:
            print(f"Peringatan: ukuran '{ukuran}' tidak dikenal, dipakai 'Reguler'.")
            ukuran = "Reguler"
        self.ukuran = ukuran                              # atribut khusus Minuman

    #Method overriding
    def hitung_harga_jual(self):
        """Ukuran Besar dikenakan tambahan harga."""
        if self.ukuran == "Besar":
            return self._harga + Minuman.tambahan_besar
        return self._harga

    def tampilkan_info(self):
        super().tampilkan_info()
        print(f"    Ukuran: {self.ukuran} | Harga jual: Rp{self.hitung_harga_jual():,}")

    #Class method (override)
    @classmethod
    def dari_dict(cls, data):
        """Factory method khusus Minuman (kategori tidak perlu diisi, ukuran opsional)."""
        return cls(data["nama"], data["harga"], data["stok"], data.get("ukuran", "Reguler"))


class Pelanggan:
    """Merepresentasikan pelanggan/pembeli di kantin."""

    #Atribut kelas  
    total_pelanggan = 0
    diskon_member = 0.1 

    def __init__(self, nama, is_member, saldo_awal=0):
        Pelanggan.total_pelanggan += 1

        self.id_pelanggan = f"PL{Pelanggan.total_pelanggan:03d}"
        #Atribut instance
        self.nama = nama                                         
        self.is_member = is_member                                
        self.saldo = saldo_awal

    #Instance method
    def isi_saldo(self, jumlah):
        """Menambah saldo kantin milik pelanggan."""
        if jumlah <= 0:
            print("Jumlah isi saldo harus lebih dari 0.")
            return
        self.saldo = self.saldo + jumlah
        print(f"Saldo {self.nama} bertambah Rp{jumlah:,}. Saldo sekarang: Rp{self.saldo:,}")

    def tampilkan_profil(self):
        status = "Member" if self.is_member else "Non-member"
        print(f"[{self.id_pelanggan}] {self.nama} ({status}) - Saldo: Rp{self.saldo:,}")

    #Class method
    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat objek Pelanggan dari data dictionary."""
        return cls(data["nama"], data.get("is_member", False), data.get("saldo_awal", 0))

    #Static method
    @staticmethod
    def validasi_nama(nama):
        """Mengecek apakah nama pelanggan valid (bukan string kosong)."""
        return isinstance(nama, str) and len(nama.strip()) > 0

    #Encapsulation: getter & setter
    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, nilai):
        if nilai < 0:
            raise ValueError("Saldo tidak boleh negatif.")
        self.__saldo = nilai


class ItemPesanan:
    """Bagian dari Pesanan (KOMPOSISI): dibuat di dalam Pesanan dan tidak berdiri sendiri."""

    def __init__(self, menu, jumlah):
        self.menu = menu          # objek Menu dibuat di luar, ItemPesanan hanya merujuknya
        self.jumlah = jumlah

    def hitung_subtotal(self):
        return self.menu.hitung_harga_jual() * self.jumlah

    def __str__(self):
        return f"{self.jumlah}x {self.menu.nama} @Rp{self.menu.hitung_harga_jual():,}"


class Pesanan:
    """Merepresentasikan satu pesanan yang dibuat oleh seorang pelanggan."""

    #Atribut kelas 
    total_pesanan = 0
    status_valid = ["Diproses", "Selesai", "Dibatalkan"]

    def __init__(self, pelanggan):
        Pesanan.total_pesanan += 1
        self.id_pesanan = f"PS{Pesanan.total_pesanan:03d}"
        #Atribut instance
        self.pelanggan = pelanggan                  
        self.daftar_item = []                       # komposisi: berisi objek ItemPesanan
        self.status = "Diproses"                  

    #Instance method
    def tambah_item(self, menu, jumlah):
        """Menambahkan item menu ke pesanan sekaligus mengurangi stok menu."""
        if not Pesanan.validasi_jumlah(jumlah):
            print("Jumlah pesanan tidak valid.")
            return
        if menu.kurangi_stok(jumlah):
            self.daftar_item.append(ItemPesanan(menu, jumlah))   # ItemPesanan dibuat di dalam Pesanan
            print(f"{jumlah}x {menu.nama} ditambahkan ke pesanan {self.id_pesanan}")

    def hitung_total(self):
        """Menghitung total harga pesanan, otomatis diskon jika pelanggan member."""
        total = sum(item.hitung_subtotal() for item in self.daftar_item)
        if self.pelanggan.is_member:
            total = total * (1 - Pelanggan.diskon_member)
        return total

    def selesaikan_pesanan(self):
        self.status = "Selesai"

    def tampilkan_pesanan(self):
        print(f"--- Pesanan {self.id_pesanan} ({self.status}) ---")
        print(f"Pelanggan: {self.pelanggan.nama}")
        for item in self.daftar_item:
            print(f"  {item}")
        print(f"Total: Rp{self.hitung_total():,.0f}")

    #Class method
    @classmethod
    def buat_pesanan_baru(cls, pelanggan):
        """Factory method: membuat objek Pesanan baru untuk seorang pelanggan."""
        return cls(pelanggan)

    #Static method
    @staticmethod
    def validasi_jumlah(jumlah):
        """Mengecek apakah jumlah item pesanan valid (bilangan bulat positif)."""
        return isinstance(jumlah, int) and jumlah > 0

    #Encapsulation: getter & setter
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status_baru):
        if status_baru not in Pesanan.status_valid:
            raise ValueError(f"Status '{status_baru}' tidak valid.")
        self.__status = status_baru


class Pembayaran:
    """Merepresentasikan transaksi pembayaran atas sebuah pesanan."""

    #Atribut kelas
    nama_kantin = "Kantin Fakultas Teknik"
    total_pembayaran = 0
    metode_valid = ["Tunai", "Saldo Kantin", "QRIS"]

    def __init__(self, pesanan, metode):
        Pembayaran.total_pembayaran += 1
        #Atribut instance
        self.id_pembayaran = f"PB{Pembayaran.total_pembayaran:03d}"
        self.pesanan = pesanan                           
        self.metode = metode               
        self.jumlah_bayar = pesanan.hitung_total()

    #Instance method
    def proses_pembayaran(self):
        """Memproses pembayaran; jika metode Saldo Kantin, saldo pelanggan otomatis dipotong."""
        if not Pembayaran.validasi_metode(self.metode):
            print(f"Metode pembayaran '{self.metode}' tidak dikenal.")
            return
        if self.metode == "Saldo Kantin":
            pelanggan = self.pesanan.pelanggan
            if pelanggan.saldo < self.jumlah_bayar:
                print("Saldo pelanggan tidak cukup, pembayaran gagal.")
                return
            pelanggan.saldo = pelanggan.saldo - self.jumlah_bayar
        self.pesanan.selesaikan_pesanan()
        print(f"Pembayaran {self.id_pembayaran} berhasil via {self.metode}.")

    def tampilkan_struk(self):
        print(f"===== STRUK {self.id_pembayaran} =====")
        print(f"Kantin   : {Pembayaran.nama_kantin}")
        print(f"Pesanan  : {self.pesanan.id_pesanan}")
        print(f"Pelanggan: {self.pesanan.pelanggan.nama}")
        print(f"Metode   : {self.metode}")
        print(f"Total    : Rp{self.jumlah_bayar:,.0f}")
        print("================================")

    #Class method
    @classmethod
    def dari_pesanan(cls, pesanan, metode):
        """Factory method: membuat objek Pembayaran langsung dari objek Pesanan."""
        return cls(pesanan, metode)

    #Static method
    @staticmethod
    def validasi_metode(metode):
        """Mengecek apakah metode pembayaran termasuk yang didukung kantin."""
        return metode in Pembayaran.metode_valid

    #Encapsulation: getter & setter
    @property
    def jumlah_bayar(self):
        return self.__jumlah_bayar

    @jumlah_bayar.setter
    def jumlah_bayar(self, nilai):
        if nilai < 0:
            raise ValueError("Jumlah bayar tidak boleh negatif.")
        self.__jumlah_bayar = nilai


class Kantin:
    """AGREGASI: Kantin memiliki banyak Menu. Menu dibuat di luar lalu didaftarkan ke Kantin."""

    def __init__(self, nama, lokasi):
        self.nama = nama
        self.lokasi = lokasi
        self._daftar_menu = []        # menampung referensi objek Menu dari luar

    def tambah_menu(self, menu):
        """Menu (Menu/Makanan/Minuman) dibuat di luar dan didaftarkan ke kantin."""
        if isinstance(menu, Menu):
            self._daftar_menu.append(menu)
            print(f"[+] {menu.nama} masuk ke daftar menu {self.nama}")
        else:
            print("Peringatan: hanya objek Menu yang bisa didaftarkan.")

    def hapus_menu(self, kode_menu):
        """Melepas referensi menu dari kantin tanpa memusnahkan objek Menu aslinya."""
        awal = len(self._daftar_menu)
        self._daftar_menu = [m for m in self._daftar_menu if m.kode_menu != kode_menu]
        if len(self._daftar_menu) < awal:
            print(f"[-] Menu {kode_menu} dikeluarkan dari {self.nama}")

    def cari_menu(self, kode_menu):
        for menu in self._daftar_menu:
            if menu.kode_menu == kode_menu:
                return menu
        return None

    @property
    def jumlah_menu(self):
        return len(self._daftar_menu)

    def tampilkan_daftar_menu(self):
        print(f"\nDaftar Menu {self.nama} ({self.lokasi}) - Total: {self.jumlah_menu}")
        for menu in self._daftar_menu:
            menu.tampilkan_info()


class Kasir:
    """ASOSIASI: Kasir menggunakan Pesanan hanya sementara lewat parameter method."""

    def __init__(self, nama, shift):
        self.nama = nama
        self.shift = shift
        # Tidak ada self.pesanan = ... karena Kasir tidak memiliki Pesanan secara permanen

    def layani_pembayaran(self, pesanan, metode):
        """Pesanan diterima sebagai parameter, dipakai sesaat, lalu dilepas."""
        print(f"Kasir {self.nama} (shift {self.shift}) melayani pesanan {pesanan.id_pesanan}...")
        pembayaran = Pembayaran.dari_pesanan(pesanan, metode)
        pembayaran.proses_pembayaran()
        if pesanan.status == "Selesai":
            pembayaran.tampilkan_struk()
        return pembayaran


if __name__ == "__main__":
    print("=" * 55)
    print("DEMO SISTEM PENGELOLAAN PEMESANAN MAKANAN")
    print("KANTIN FAKULTAS TEKNIK")
    print("=" * 55)

    #1. Objek Menu
    print("\n--- Membuat Menu ---")
    nasi_goreng = Menu("Nasi Goreng", 15000, 20, "Makanan")
    es_teh = Menu.dari_dict({"nama": "Es Teh Manis", "harga": 5000, "stok": 50, "kategori": "Minuman"})
    nasi_goreng.tampilkan_info()
    es_teh.tampilkan_info()

    nasi_goreng.tambah_stok(10)                      # instance method
    print("Validasi kategori 'Makanan':", Menu.validasi_kategori("Makanan"))
    print("Validasi kategori 'Camilan':", Menu.validasi_kategori("Camilan"))

    #2. Objek Pelanggan
    print("\n--- Membuat Pelanggan ---")
    andi = Pelanggan("Andi", is_member=True, saldo_awal=100000)
    budi = Pelanggan.dari_dict({"nama": "Budi", "is_member": False, "saldo_awal": 20000})
    andi.tampilkan_profil()
    budi.tampilkan_profil()

    andi.isi_saldo(50000)                              # instance method
    print("Validasi nama 'Citra':", Pelanggan.validasi_nama("Citra"))
    print("Validasi nama '   ' :", Pelanggan.validasi_nama("   "))   

    #Objek Pesanan
    print("\n--- Membuat Pesanan ---")
    pesanan1 = Pesanan.buat_pesanan_baru(andi)
    pesanan1.tambah_item(nasi_goreng, 2)
    pesanan1.tambah_item(es_teh, 1)
    pesanan1.tampilkan_pesanan()

    pesanan2 = Pesanan.buat_pesanan_baru(budi)
    pesanan2.tambah_item(es_teh, 3)
    pesanan2.tampilkan_pesanan()

    print("Validasi jumlah 2 :", Pesanan.validasi_jumlah(2))
    print("Validasi jumlah -1:", Pesanan.validasi_jumlah(-1))

    #Objek Pembayaran
    print("\n--- Proses Pembayaran ---")
    bayar1 = Pembayaran.dari_pesanan(pesanan1, "Saldo Kantin")
    bayar1.proses_pembayaran()
    bayar1.tampilkan_struk()

    bayar2 = Pembayaran(pesanan2, "Tunai")
    bayar2.proses_pembayaran()
    bayar2.tampilkan_struk()

    print("Validasi metode 'QRIS'  :", Pembayaran.validasi_metode("QRIS")) 
    print("Validasi metode 'Kripto':", Pembayaran.validasi_metode("Kripto"))

    #Uji Setter: data valid & tidak valid
    print("\n--- Uji Validasi Setter (Encapsulation) ---")

    # Menu.stok
    try:
        nasi_goreng.stok = 30
        print("Stok nasi goreng diubah jadi:", nasi_goreng.stok)
        nasi_goreng.stok = -5
    except ValueError as e:
        print("Gagal ubah stok:", e)

    # Pelanggan.saldo
    try:
        budi.saldo = 75000
        print("Saldo Budi diubah jadi:", budi.saldo)
        budi.saldo = -10000
    except ValueError as e:
        print("Gagal ubah saldo:", e)

    # Pesanan.status
    try:
        pesanan1.status = "Selesai"
        print("Status pesanan1 diubah jadi:", pesanan1.status)
        pesanan1.status = "Dikirim"
    except ValueError as e:
        print("Gagal ubah status:", e)

    # Pembayaran.jumlah_bayar
    try:
        bayar2.jumlah_bayar = 25000
        print("Jumlah bayar2 diubah jadi:", bayar2.jumlah_bayar)
        bayar2.jumlah_bayar = -1000
    except ValueError as e:
        print("Gagal ubah jumlah bayar:", e)

    #A. Inheritance: Menu (superclass) -> Makanan & Minuman (subclass)
    print("\n--- Inheritance: Menu -> Makanan & Minuman ---")
    ayam_geprek = Makanan("Ayam Geprek", 18000, 15, "Jumbo")
    mie_goreng = Makanan.dari_dict({"nama": "Mie Goreng", "harga": 12000, "stok": 25})
    es_jeruk = Minuman("Es Jeruk", 7000, 30, "Besar")
    kopi_hitam = Minuman.dari_dict({"nama": "Kopi Hitam", "harga": 6000, "stok": 40})
    for menu in (ayam_geprek, mie_goreng, es_jeruk, kopi_hitam):
        menu.tampilkan_info()          # versi override: super().tampilkan_info() + info khusus subclass

    print("\n--- Method Overriding: hitung_harga_jual() ---")
    print(f"Nasi Goreng (Menu)   : Rp{nasi_goreng.hitung_harga_jual():,}")
    print(f"Ayam Geprek (Jumbo)  : Rp{ayam_geprek.hitung_harga_jual():,}")
    print(f"Mie Goreng (Reguler) : Rp{mie_goreng.hitung_harga_jual():,}")
    print(f"Es Jeruk (Besar)     : Rp{es_jeruk.hitung_harga_jual():,}")

    print("\n--- Uji Relasi Pewarisan (is-a) ---")
    print("Ayam Geprek adalah Menu?    ", isinstance(ayam_geprek, Menu))
    print("Ayam Geprek adalah Minuman? ", isinstance(ayam_geprek, Minuman))
    print("Minuman subclass dari Menu? ", issubclass(Minuman, Menu))

    print("\n--- Tingkat Akses pada Pewarisan ---")
    print("Protected _harga (dipakai subclass):", ayam_geprek._harga)
    try:
        print(ayam_geprek.__stok)
    except AttributeError as e:
        print("Akses private __stok dari luar gagal:", e)
    try:
        ayam_geprek.stok = 12          # setter milik Menu diwariskan ke Makanan
        print("Stok Ayam Geprek diubah jadi:", ayam_geprek.stok)
        ayam_geprek.stok = -3
    except ValueError as e:
        print("Gagal ubah stok subclass:", e)

    #B. Agregasi: Kantin memiliki Menu
    print("\n--- Agregasi: Kantin memiliki Menu ---")
    kantin = Kantin(Menu.nama_kantin, "Gedung Fakultas Teknik")
    for menu in (nasi_goreng, es_teh, ayam_geprek, mie_goreng, es_jeruk, kopi_hitam):
        kantin.tambah_menu(menu)
    kantin.tambah_menu("Teh Botol")    # bukan objek Menu -> ditolak
    kantin.tampilkan_daftar_menu()

    kantin.hapus_menu(es_teh.kode_menu)
    print("Jumlah menu di kantin sekarang:", kantin.jumlah_menu)
    es_teh.tampilkan_info()            # objek Menu tetap ada walau sudah keluar dari kantin

    #C. Asosiasi: Kasir menggunakan Pesanan
    print("\n--- Asosiasi: Kasir menggunakan Pesanan ---")
    kasir = Kasir("Sinta", "Pagi")
    citra = Pelanggan("Citra", is_member=True, saldo_awal=80000)
    deni = Pelanggan("Deni", is_member=False, saldo_awal=15000)

    pesanan3 = Pesanan.buat_pesanan_baru(citra)
    pesanan3.tambah_item(kantin.cari_menu("MN003"), 1)    # MN003 = Ayam Geprek
    pesanan3.tambah_item(es_jeruk, 2)
    pesanan3.tampilkan_pesanan()
    kasir.layani_pembayaran(pesanan3, "Saldo Kantin")

    pesanan4 = Pesanan.buat_pesanan_baru(deni)
    pesanan4.tambah_item(mie_goreng, 1)
    pesanan4.tambah_item(kopi_hitam, 1)
    kasir.layani_pembayaran(pesanan4, "Saldo Kantin")     # gagal: saldo Deni tidak cukup
    kasir.layani_pembayaran(pesanan4, "QRIS")             # berhasil

    #D. Komposisi: Pesanan terdiri dari ItemPesanan
    print("\n--- Komposisi: Pesanan terdiri dari ItemPesanan ---")
    print("Isi daftar_item pesanan3:", [type(item).__name__ for item in pesanan3.daftar_item])
    for item in pesanan3.daftar_item:
        print(f"  {item} -> subtotal Rp{item.hitung_subtotal():,}")

    pesanan_sementara = Pesanan.buat_pesanan_baru(deni)
    pesanan_sementara.tambah_item(mie_goreng, 1)
    del pesanan_sementara              # ItemPesanan ikut musnah bersama Pesanan
    print("Pesanan sementara dihapus, objek Menu tetap ada:")
    mie_goreng.tampilkan_info()

    #Bukti siklus hidup agregasi
    del kantin
    print("\nKantin dihapus, objek Menu tetap ada:")
    ayam_geprek.tampilkan_info()
    kopi_hitam.tampilkan_info()

    #Statistik dari atribut kelas
    print("\n--- Statistik Akhir (Atribut Kelas) ---")
    print("Total menu terdaftar     :", Menu.total_menu)
    print("Total pelanggan terdaftar:", Pelanggan.total_pelanggan)
    print("Total pesanan dibuat     :", Pesanan.total_pesanan)
    print("Total pembayaran diproses:", Pembayaran.total_pembayaran)