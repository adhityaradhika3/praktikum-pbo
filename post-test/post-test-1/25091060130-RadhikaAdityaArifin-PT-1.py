class Menu:
    """Merepresentasikan satu item menu (makanan/minuman) di kantin."""
    #Atribut kelas
    nama_kantin = "Kantin Fakultas Teknik"
    total_menu = 0
    kategori_valid = ["Makanan", "Minuman"]

    def __init__(self, nama, harga, stok, kategori):
        Menu.total_menu += 1
        #Atribut instance
        self.kode_menu = f"MN{Menu.total_menu:03d}" 
        self.nama = nama                              
        self.harga = harga                            
        if not Menu.validasi_kategori(kategori):
            print(f"Peringatan: kategori '{kategori}' tidak dikenal.")
        self.kategori = kategori                      
        self.stok = stok                      

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
    def stok(self):
        """Getter -- dipanggil seperti atribut biasa."""
        return self.__stok

    @stok.setter
    def stok(self, nilai):
        """Setter -- validasi agar stok tidak pernah negatif."""
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif.")
        self.__stok = nilai


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
        self.daftar_item = []                             
        self.status = "Diproses"                  

    #Instance method
    def tambah_item(self, menu, jumlah):
        """Menambahkan item menu ke pesanan sekaligus mengurangi stok menu."""
        if not Pesanan.validasi_jumlah(jumlah):
            print("Jumlah pesanan tidak valid.")
            return
        if menu.kurangi_stok(jumlah):
            self.daftar_item.append((menu, jumlah))
            print(f"{jumlah}x {menu.nama} ditambahkan ke pesanan {self.id_pesanan}")

    def hitung_total(self):
        """Menghitung total harga pesanan, otomatis diskon jika pelanggan member."""
        total = sum(menu.harga * jumlah for menu, jumlah in self.daftar_item)
        if self.pelanggan.is_member:
            total = total * (1 - Pelanggan.diskon_member)
        return total

    def selesaikan_pesanan(self):
        self.status = "Selesai"

    def tampilkan_pesanan(self):
        print(f"--- Pesanan {self.id_pesanan} ({self.status}) ---")
        print(f"Pelanggan: {self.pelanggan.nama}")
        for menu, jumlah in self.daftar_item:
            print(f"  {jumlah}x {menu.nama} @Rp{menu.harga:,}")
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

    #Statistik dari atribut kelas
    print("\n--- Statistik Akhir (Atribut Kelas) ---")
    print("Total menu terdaftar     :", Menu.total_menu)
    print("Total pelanggan terdaftar:", Pelanggan.total_pelanggan)
    print("Total pesanan dibuat     :", Pesanan.total_pesanan)
    print("Total pembayaran diproses:", Pembayaran.total_pembayaran)