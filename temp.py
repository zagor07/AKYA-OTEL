import sqlite3
import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox

class ÖzelMesajKutusu:
    def __init__(self, ebeveyn, baslik, mesaj):
        self.win = tk.Toplevel(ebeveyn)
        self.win.title(baslik)
        self.win.geometry("380x160")
        self.win.configure(bg="#1f2937") 
        self.win.resizable(False, False)
        
        # Ana pencerenin üzerinde kalmasını sağla
        self.win.transient(ebeveyn)
        self.win.grab_set()
        
        # Pencereyi ekranda ortala
        self.win.update_idletasks()
        x = ebeveyn.winfo_x() + (ebeveyn.winfo_width() // 2) - (380 // 2)
        y = ebeveyn.winfo_y() + (ebeveyn.winfo_height() // 2) - (160 // 2)
        self.win.geometry(f"+{x}+{y}")

        # Şık Metin Simgesi
        tk.Label(self.win, text="✨", font=("Segoe UI", 24), 
                 fg="#34d399", bg="#1f2937").pack(pady=(15, 5))

        # Mesaj İçeriği
        tk.Label(self.win, text=mesaj, font=("Segoe UI", 10, "bold"), 
                 fg="#ffffff", bg="#1f2937", wraplength=340).pack(pady=5)

        # Tamam Butonu
        tk.Button(self.win, text="Tamam", font=("Segoe UI", 10, "bold"), 
                  bg="#10b981", fg="white", bd=0, width=12, cursor="hand2",
                  command=self.win.destroy).pack(pady=15)

class AdminGiriş:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("AKYA OTEL - Yönetici Girişi")
        self.pencere.geometry("400x300")
        self.pencere.configure(bg="#111827")
        self.pencere.resizable(False, False)
        
        tk.Label(pencere, text="AKYA OTEL PANELDEN GİRİŞ", 
                 font=("Segoe UI", 12, "bold"), 
                 fg="#34d399", bg="#111827").pack(pady=20)
        
        tk.Label(pencere, text="Kullanıcı Adı:", fg="#9ca3af", 
                 bg="#111827", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, padx=50)
        self.e_username = tk.Entry(pencere, font=("Segoe UI", 11), bg="#1f2937", 
                                   fg="white", bd=1, relief=tk.SOLID, insertbackground="white")
        self.e_username.pack(fill=tk.X, padx=50, pady=(0, 15), ipady=3)
        
        tk.Label(pencere, text="Şifre:", fg="#9ca3af", bg="#111827", 
                 font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, padx=50)
        self.e_password = tk.Entry(pencere, font=("Segoe UI", 11), bg="#1f2937", 
                                   fg="white", bd=1, relief=tk.SOLID, show="*", insertbackground="white")
        self.e_password.pack(fill=tk.X, padx=50, pady=(0, 20), ipady=3)
        
        tk.Button(pencere, text="Giriş Yap", bg="#10b981", fg="white", 
                  font=("Segoe UI", 10, "bold"), command=self.kontrol_et, bd=0, cursor="hand2").pack(fill=tk.X, padx=50, ipady=6)

    def kontrol_et(self):
        if self.e_username.get() == "admin" and self.e_password.get() == "akya123":
            self.pencere.destroy()
            ana_ekran_baslat()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

class AkyaOtelGelismişSistem:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("AKYA OTEL")
        self.pencere.geometry("1200x700")
        self.pencere.configure(bg="#111827")
        self.db_hazirla()
        self.stil_ayarla()
        self.ekran_ciz()
        self.sayfa_degis("resepsiyon")

    def db_hazirla(self):
        self.db_adi = "akya_otel_v4.db"
        self.conn = sqlite3.connect(self.db_adi)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rezervasyonlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                oda_no INTEGER,
                musteri_adi TEXT,
                giris_tarihi TEXT,
                cikis_tarihi TEXT,
                gunluk_fiyat REAL,
                toplam_tutar REAL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS oda_durumlari (
                id_no INTEGER PRIMARY KEY,
                durum TEXT
            )
        """)
        for i in range(1, 21):
            self.cursor.execute("""
                INSERT OR IGNORE INTO oda_durumlari (id_no, durum) VALUES (?, 'Temiz')
            """, (i,))
        self.conn.commit()

    def stil_ayarla(self):
        # Konsoldaki parantez hatalarının bittiği güvenli alan
        self.s = ttk.Style()
        self.s.theme_use("clam")
        self.s.configure("TLabel", background="#1f2937", foreground="#ffffff", font=("Segoe UI", 10))
        self.s.configure("Kart.TFrame", background="#1f2937", relief="flat")
        self.s.configure("Treeview", background="#1f2937", foreground="#ffffff", rowheight=28, fieldbackground="#1f2937")
        self.s.configure("Treeview.Heading", background="#374151", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        self.s.map("Treeview", background=[("selected", "#2563eb")])

    def ekran_ciz(self):
        menu_paneli = tk.Frame(self.pencere, bg="#1f2937", width=220)
        menu_paneli.pack(side=tk.LEFT, fill=tk.Y)
        menu_paneli.pack_propagate(False)
        tk.Label(menu_paneli, text="AKYA OTEL", font=("Segoe UI", 16, "bold"), fg="#34d399", bg="#1f2937").pack(pady=25)
        
        butonlar = [
            ("🛎️ Resepsiyon Giriş", "resepsiyon"),
            ("🧹 Oda Durum Takibi", "temizlik"),
            ("📊 Kasa & İstatistik", "kasa"),
            ("🧾 Fatura & Çıktı", "fatura")
        ]
        
        for metin, sayfa_id in butonlar:
            btn = tk.Button(menu_paneli, text=metin, font=("Segoe UI", 11, "bold"), 
                            bg="#374151", fg="white", activebackground="#2563eb", 
                            activeforeground="white", bd=0, cursor="hand2", anchor=tk.W, padx=20,
                            command=lambda s=sayfa_id: self.sayfa_degis(s))
            btn.pack(fill=tk.X, pady=4, ipady=8)
            
        self.icerik_alani = tk.Frame(self.pencere, bg="#111827")
        self.icerik_alani.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    def sayfa_degis(self, sayfa_adi):
        for widget in self.icerik_alani.winfo_children(): 
            widget.destroy()
        if sayfa_adi == "resepsiyon": self.sayfa_resepsiyon()
        elif sayfa_adi == "temizlik": self.sayfa_temizlik()
        elif sayfa_adi == "kasa": self.sayfa_kasa()
        elif sayfa_adi == "fatura": self.sayfa_fatura()

    def sayfa_resepsiyon(self):
        ana = tk.Frame(self.icerik_alani, bg="#111827")
        ana.pack(fill=tk.BOTH, expand=True)
        sol = ttk.Frame(ana, style="Kart.TFrame", padding=15)
        sol.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        tk.Label(sol, text="YENİ REZERVASYON", font=("Segoe UI", 12, "bold"), fg="#34d399", bg="#1f2937").pack(anchor=tk.W, pady=(0, 10))
        tk.Label(sol, text="Müşteri Adı Soyadı:", bg="#1f2937", fg="white").pack(anchor=tk.W)
        self.e_isim = tk.Entry(sol, font=("Segoe UI", 11), bg="#111827", fg="white", bd=1, relief=tk.SOLID)
        self.e_isim.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        tk.Label(sol, text="Oda Numarası (1-20):", bg="#1f2937", fg="white").pack(anchor=tk.W)
        self.e_oda = tk.Entry(sol, font=("Segoe UI", 11), bg="#111827", fg="white", bd=1, relief=tk.SOLID)
        self.e_oda.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        tk.Label(sol, text="Giriş Tarihi (GG.AA.YYYY):", bg="#1f2937", fg="white").pack(anchor=tk.W)
        self.e_grid = tk.Entry(sol, font=("Segoe UI", 11), bg="#111827", fg="white", bd=1, relief=tk.SOLID)
        self.e_grid.insert(0, datetime.date.today().strftime("%d.%m.%Y"))
        self.e_grid.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        tk.Label(sol, text="Çıkış Tarihi (GG.AA.YYYY):", bg="#1f2937", fg="white").pack(anchor=tk.W)
        self.e_cikis = tk.Entry(sol, font=("Segoe UI", 11), bg="#111827", fg="white", bd=1, relief=tk.SOLID)
        self.e_cikis.insert(0, (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y"))
        self.e_cikis.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        tk.Label(sol, text="Günlük Oda Fiyatı (TL):", bg="#1f2937", fg="white").pack(anchor=tk.W)
        self.e_fiyat = tk.Entry(sol, font=("Segoe UI", 11), bg="#111827", fg="white", bd=1, relief=tk.SOLID)
        self.e_fiyat.insert(0, "1000")
        self.e_fiyat.pack(fill=tk.X, pady=(0, 15), ipady=3)
        
        tk.Button(sol, text="Rezervasyon Yap", bg="#10b981", fg="white", font=("Segoe UI", 10, "bold"), command=self.rezervasyon_ekle, bd=0, cursor="hand2").pack(fill=tk.X, pady=5, ipady=5)
        tk.Button(sol, text="Seçili Kaydı Sil", bg="#ef4444", fg="white", font=("Segoe UI", 10, "bold"), command=self.rezervasyon_sil, bd=0, cursor="hand2").pack(fill=tk.X, pady=5, ipady=5)
        
        sag = tk.Frame(ana, bg="#111827")
        sag.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        ust = tk.Frame(sag, bg="#1f2937", padx=10, pady=10)
        ust.pack(fill=tk.X, pady=(0, 15))
        
        self.odalar = {}
        for i in range(1, 21):
            satir = 0 if i <= 10 else 1
            sutun = (i - 1) % 10
            b = tk.Button(ust, text=f"Oda {i}\nBoş", bg="#10b981", fg="white", font=("Segoe UI", 8, "bold"), width=8, height=2, bd=0, command=lambda o=i: self.oda_sec(o), cursor="hand2")
            b.grid(row=satir, column=sutun, padx=4, pady=4)
            self.odalar[i] = b
            
        alt = tk.Frame(sag, bg="#1f2937", padx=15, pady=15)
        alt.pack(fill=tk.BOTH, expand=True)
        
        sutunlar = ("id", "oda", "isim", "giris", "cikis", "fiyat", "tutar")
        self.tablo = ttk.Treeview(alt, columns=sutunlar, show="headings")
        for s in sutunlar: 
            self.tablo.heading(s, text=s.upper())
        self.tablo.pack(fill=tk.BOTH, expand=True)
        
        self.odalari_yenile()
        self.tablo_guncelle()

    def oda_sec(self, n):
        self.e_oda.delete(0, tk.END)
        self.e_oda.insert(0, str(n))

    def odalari_yenile(self):
        for i in range(1, 21): 
            self.odalar[i].configure(bg="#10b981", text=f"Oda {i}\nBoş")
        self.cursor.execute("SELECT oda_no, musteri_adi FROM rezervasyonlar")
        for o, m in self.cursor.fetchall():
            if 1 <= o <= 20:
                isim = m[:7] + ".." if len(m) > 7 else m
                self.odalar[o].configure(bg="#ef4444", text=f"Oda {o}\nDolu\n{isim}")

    def tablo_guncelle(self):
        for s in self.tablo.get_children(): 
            self.tablo.delete(s)
        self.cursor.execute("SELECT * FROM rezervasyonlar ORDER BY oda_no ASC")
        for r in self.cursor.fetchall(): 
            self.tablo.insert("", tk.END, values=r)

    def rezervasyon_ekle(self):
        isim, oda, giris, cikis, fiyat = self.e_isim.get().strip(), self.e_oda.get().strip(), self.e_grid.get().strip(), self.e_cikis.get().strip(), self.e_fiyat.get().strip()
        if not (isim and oda and giris and cikis and fiyat): 
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return
        
        try:
            o_no = int(oda)
            if not (1 <= o_no <= 20): raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Oda numarası 1 ile 20 arasında olmalıdır!")
            return

        self.cursor.execute("SELECT durum FROM oda_durumlari WHERE id_no=?", (o_no,))
        durum_res = self.cursor.fetchone()
        if durum_res and durum_res[0] == "Arızalı":
            messagebox.showerror("Hata", "Bu oda arızalı! Rezervasyon yapılamaz.")
            return

        try:
            g_d = datetime.datetime.strptime(giris, "%d.%m.%Y")
            c_d = datetime.datetime.strptime(cikis, "%d.%m.%Y")
            gun = (c_d - g_d).days
            if gun <= 0: 
                messagebox.showerror("Hata", "Çıkış tarihi giriş tarihinden sonra olmalıdır!")
                return
        except ValueError:
            messagebox.showerror("Hata", "Tarih formatı hatalı (GG.AA.YYYY)!")
            return
            
        toplam = gun * float(fiyat)
        self.cursor.execute("INSERT INTO rezervasyonlar (oda_no, musteri_adi, giris_tarihi, cikis_tarihi, gunluk_fiyat, toplam_tutar) VALUES (?,?,?,?,?,?)", (o_no, isim, giris, cikis, float(fiyat), toplam))
        self.conn.commit()
        self.odalari_yenile()
        self.tablo_guncelle()
        ÖzelMesajKutusu(self.pencere, "Başarılı", "Rezervasyon başarıyla eklendi!")

    def rezervasyon_sil(self):
        secili = self.tablo.selection()
        if not secili: 
            messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz kaydı tablodan seçin!")
            return
        val = self.tablo.item(secili)['values']
        kayit_id = val[0]
        oda_no = val[1]
        
        if messagebox.askyesno("Onay", "Kayıt silinsin mi?"):
            self.cursor.execute("DELETE FROM rezervasyonlar WHERE id=?", (kayit_id,))
            self.cursor.execute("UPDATE oda_durumlari SET durum='Kirli' WHERE id_no=?", (oda_no,))
            self.conn.commit()
            self.odalari_yenile()
            self.tablo_guncelle()

    def sayfa_temizlik(self):
        kart = tk.Frame(self.icerik_alani, bg="#1f2937", padx=20, pady=20)
        kart.pack(fill=tk.BOTH, expand=True)
        tk.Label(kart, text="🧹 ODA TEMİZLİK & TEKNİK DURUMU", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#1f2937").pack(anchor=tk.W, pady=(0, 20))
        
        kontrol_f = tk.Frame(kart, bg="#1f2937")
        kontrol_f.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(kontrol_f, text="Oda Seç:", bg="#1f2937", fg="white").pack(side=tk.LEFT, padx=5)
        self.cb_oda = ttk.Combobox(kontrol_f, values=[str(x) for x in range(1, 21)], width=8, state="readonly")
        self.cb_oda.pack(side=tk.LEFT, padx=5)
        
        tk.Label(kontrol_f, text="Durum Ayarla:", bg="#1f2937", fg="white").pack(side=tk.LEFT, padx=5)
        self.cb_durum = ttk.Combobox(kontrol_f, values=["Temiz", "Kirli", "Arızalı"], width=12, state="readonly")
        self.cb_durum.pack(side=tk.LEFT, padx=5)
        
        tk.Button(kontrol_f, text="Durumu Güncelle", bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), bd=0, command=self.durum_guncelle, cursor="hand2").pack(side=tk.LEFT, padx=10, ipady=2, ipadx=5)
        
        self.tablo_temizlik = ttk.Treeview(kart, columns=("oda", "durum"), show="headings")
        self.tablo_temizlik.heading("oda", text="ODA NUMARASI")
        self.tablo_temizlik.heading("durum", text="GÜNCEL DURUM")
        self.tablo_temizlik.pack(fill=tk.BOTH, expand=True)
        self.temizlik_tablo_doldur()

    def temizlik_tablo_doldur(self):
        for s in self.tablo_temizlik.get_children(): 
            self.tablo_temizlik.delete(s)
        self.cursor.execute("SELECT * FROM oda_durumlari ORDER BY id_no ASC")
        for r in self.cursor.fetchall(): 
            self.tablo_temizlik.insert("", tk.END, values=r)

    def durum_guncelle(self):
        o, d = self.cb_oda.get(), self.cb_durum.get()
        if o and d:
            self.cursor.execute("UPDATE oda_durumlari SET durum=? WHERE id_no=?", (d, int(o)))
            self.conn.commit()
            self.temizlik_tablo_doldur()
            ÖzelMesajKutusu(self.pencere, "Başarılı", f"Oda {o} durumu '{d}' olarak güncellendi.")
        else:
            messagebox.showwarning("Uyarı", "Lütfen oda ve durum seçimi yapın!")

    def sayfa_kasa(self):
        kart = tk.Frame(self.icerik_alani, bg="#1f2937", padx=20, pady=20)
        kart.pack(fill=tk.BOTH, expand=True)
        tk.Label(kart, text="📊 OTEL KASA & DOLULUK RAPORU", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#1f2937").pack(anchor=tk.W, pady=(0, 25))
        
        self.cursor.execute("SELECT SUM(toplam_tutar) FROM rezervasyonlar")
        para_res = self.cursor.fetchone()
        toplam_para = para_res[0] if para_res and para_res[0] is not None else 0.0
        
        self.cursor.execute("SELECT COUNT(DISTINCT oda_no) FROM rezervasyonlar")
        dolu_res = self.cursor.fetchone()
        dolu_oda = dolu_res[0] if dolu_res and dolu_res[0] is not None else 0
        doluluk_orani = (dolu_oda / 20) * 100
        
        kasa_f = tk.Frame(kart, bg="#10b981", padx=20, pady=20)
        kasa_f.pack(fill=tk.X, pady=10)
        tk.Label(kasa_f, text="TOPLAM KASA GELİRİ", font=("Segoe UI", 11, "bold"), bg="#10b981", fg="white").pack(anchor=tk.W)
        tk.Label(kasa_f, text=f"{toplam_para:,.2f} TL", font=("Segoe UI", 24, "bold"), bg="#10b981", fg="white").pack(anchor=tk.W)
        
        oran_f = tk.Frame(kart, bg="#3b82f6", padx=20, pady=20)
        oran_f.pack(fill=tk.X, pady=10)
        tk.Label(oran_f, text="OTEL DOLULUK ORANI", font=("Segoe UI", 11, "bold"), bg="#3b82f6", fg="white").pack(anchor=tk.W)
        tk.Label(oran_f, text=f"% {doluluk_orani:.1f} ({dolu_oda} / 20)", font=("Segoe UI", 24, "bold"), bg="#3b82f6", fg="white").pack(anchor=tk.W)

    def sayfa_fatura(self):
        kart = tk.Frame(self.icerik_alani, bg="#1f2937", padx=20, pady=20)
        kart.pack(fill=tk.BOTH, expand=True)
        tk.Label(kart, text="🧾 REZERVASYON FATURA KESME", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#1f2937").pack(anchor=tk.W, pady=(0, 15))
        
        self.tablo_fatura = ttk.Treeview(kart, columns=("id", "oda", "isim", "tutar"), show="headings")
        self.tablo_fatura.heading("id", text="ID")
        self.tablo_fatura.heading("oda", text="ODA")
        self.tablo_fatura.heading("isim", text="MÜŞTERI")
        self.tablo_fatura.heading("tutar", text="TOPLAM TUTAR")
        self.tablo_fatura.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.cursor.execute("SELECT id, oda_no, musteri_adi, toplam_tutar FROM rezervasyonlar")
        for r in self.cursor.fetchall(): 
            self.tablo_fatura.insert("", tk.END, values=r)
            
        tk.Button(kart, text="Fatura Kes", bg="#10b981", fg="white", font=("Segoe UI", 11, "bold"), bd=0, command=self.fatura_kes, cursor="hand2").pack(fill=tk.X, ipady=6)

    def fatura_kes(self):
        secili = self.tablo_fatura.selection()
        if not secili: 
            messagebox.showwarning("Uyarı", "Lütfen fatura kesmek için listeden bir rezervasyon seçin!")
            return
        val = self.tablo_fatura.item(secili)['values']
        kayit_id = val[0]
        
        self.cursor.execute("SELECT * FROM rezervasyonlar WHERE id=?", (kayit_id,))
        r = self.cursor.fetchone()
        if not r: return
        
        dosya_adi = f"Fatura_Oda_{r[1]}.txt"
        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write("========= REZERVASYON FATURASI =========\n")
            f.write(f"Fatura ID      : {r[0]}\n")
            f.write(f"Oda Numarası   : {r[1]}\n")
            f.write(f"Müşteri Bilgisi: {r[2]}\n")
            f.write(f"Giriş Tarihi   : {r[3]}\n")
            f.write(f"Çıkış Tarihi   : {r[4]}\n")
            f.write(f"Günlük Ücret   : {r[5]} TL\n")
            f.write("----------------------------------------\n")
            f.write(f"TOPLAM TUTAR   : {r[6]} TL\n")
            f.write("========================================\n")
            
        # Doğrudan net ve şık mesaj kutumuz tetikleniyor
        ÖzelMesajKutusu(self.pencere, "Başarılı", "Fatura başarıyla kesildi!")

def ana_ekran_baslat():
    global ana_root, app
    ana_root = tk.Tk()
    app = AkyaOtelGelismişSistem(ana_root)
    ana_root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = AdminGiriş(login_root)
    login_root.mainloop()