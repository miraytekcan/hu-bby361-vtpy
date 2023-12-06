from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
baglanti = sqlite3.connect("MirayTekcan.db")
sorgu = baglanti.cursor()
eserTablosu = None
e1 = e2 = e3 = e4 = e5 = None
pencere = None
arama = None

def eserleriListele():
    eserTablosu.delete(*eserTablosu.get_children())
    sonuc = sorgu.execute("SELECT * FROM book")
    for index, eser in enumerate(sonuc.fetchall()):
        eserTablosu.insert(parent='', index='end', iid=index, text='',
                           values=(eser[0], eser[1], eser[2], eser[3], eser[4], eser[5]))

def eserEkle():
    global e1, e2, e3, e4, e5
    if not e1.get() or not e2.get() or not e3.get() or not e4.get() or not e5.get():
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
        return
    formVeri = (None, None, e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), None, None, None, None)
    sorgu.execute("INSERT INTO book VALUES(?,?,?,?,?,?,?,?,?,?,?)", formVeri)
    baglanti.commit()
    messagebox.showinfo(title="Katalog Bilgi", message="Eser başarıyla eklenmiştir!")

def eserEkleForm():
    global e1, e2, e3, e4, e5
    pencereEkle = Tk()
    pencereEkle.title('Yeni Eser Ekleme Alanı')
    pencereEkle.geometry('300x200')
    pencereEkle.resizable(True, True)
    pencereEkle['bg'] = '#ECECEC'
    eserCercevesi = ttk.Frame(pencereEkle, padding=10)
    eserCercevesi.pack()
    l1 = Label(eserCercevesi, text="Eser ID")
    e1 = Entry(eserCercevesi, width=25)
    l2 = Label(eserCercevesi, text="Eser Başlığı")
    e2 = Entry(eserCercevesi, width=25)
    l3 = Label(eserCercevesi, text="Eser Açıklaması")
    e3 = Entry(eserCercevesi, width=25)
    l4 = Label(eserCercevesi, text="Eser Dili")
    e4 = Entry(eserCercevesi, width=25)
    l5 = Label(eserCercevesi, text="Eser ISBN")
    e5 = Entry(eserCercevesi, width=25)
    b1 = Button(eserCercevesi, text="Yeni Eser Ekle", command=eserEkle)
    b2 = Button(eserCercevesi, text="Temizle", command=formTemizle)
    b3 = Button(eserCercevesi, text="Çıkış", command=pencereEkle.destroy)  # Çıkış butonu
    l1.grid(row=0, column=0, sticky=W, pady=2)
    e1.grid(row=0, column=1, pady=2)
    l2.grid(row=1, column=0, sticky=W, pady=2)
    e2.grid(row=1, column=1, pady=2)
    l3.grid(row=2, column=0, sticky=W, pady=2)
    e3.grid(row=2, column=1, pady=2)
    l4.grid(row=3, column=0, sticky=W, pady=2)
    e4.grid(row=3, column=1, pady=2)
    l5.grid(row=4, column=0, sticky=W, pady=2)
    e5.grid(row=4, column=1, pady=2)
    b1.grid(row=5, column=1, pady=2)
    b2.grid(row=5, column=0, pady=2)
    b3.grid(row=6, column=0, pady=2, columnspan=2)  # Çıkış butonu
    pencereEkle.mainloop()

def formTemizle():
    global e1, e2, e3, e4, e5
    e1.delete(0, 'end')
    e2.delete(0, 'end')
    e3.delete(0, 'end')
    e4.delete(0, 'end')
    e5.delete(0, 'end')

def aramaYap():
    anahtar = arama.get()
    aramaSonuc = sorgu.execute(
        "SELECT * FROM book WHERE title LIKE '%{}%' OR eserAciklama LIKE '%{}%' OR eserDili LIKE '%{}%' OR eserISBN LIKE '%{}%' ORDER BY title DESC".format(
            anahtar, anahtar, anahtar, anahtar
        )
    )
    eserTablosu.delete(*eserTablosu.get_children())
    for index, eser in enumerate(aramaSonuc.fetchall()):
        eserTablosu.insert(
            parent="",
            index="end",
            iid=index,
            text="",
            values=(
                eser[0],
                eser[1],
                eser[2],
                eser[3],
                eser[4],
                eser[5],
                eser[6],
                eser[7],
                eser[8],
                eser[9],
                eser[10],
            ),
        )

def temizle():
    arama.delete(0, 'end')

def eserSil():
    selected_item = eserTablosu.selection()
    if not selected_item:
        messagebox.showwarning("Uyarı", "Lütfen silinecek bir eser seçin.")
        return
    eser_id = eserTablosu.item(selected_item, 'values')[0]
    sorgu.execute("DELETE FROM book WHERE book_id=?", (eser_id,))
    baglanti.commit()
    messagebox.showinfo("Başarılı", "Eser başarıyla silindi.")
    eserleriListele()

def eserGuncelle():
    secili = eserTablosu.selection()
    if not secili:
        messagebox.showwarning("Uyarı", "Lütfen güncellemek istediğiniz eseri seçin.")
        return
    eser_id = eserTablosu.item(secili, 'values')[0]
    def guncelle():
        yeni_baslik_str = yeni_baslik.get()
        yeni_aciklama_str = yeni_aciklama.get()
        yeni_dil_str = yeni_dil.get()
        yeni_ISBN_str = yeni_ISBN.get()
        if not yeni_baslik_str or not yeni_aciklama_str or not yeni_dil_str or not yeni_ISBN_str:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return
        eserGuncelleDB(eser_id, yeni_baslik_str, yeni_aciklama_str, yeni_dil_str, yeni_ISBN_str)
        pencereGuncelle.destroy()
    pencereGuncelle = Tk()
    pencereGuncelle.title('Eser Güncelleme Alanı')
    pencereGuncelle.geometry('300x200')
    pencereGuncelle.resizable(True, True)
    pencereGuncelle['bg'] = '#ECECEC'
    eserCercevesi = ttk.Frame(pencereGuncelle, padding=10)
    eserCercevesi.pack()
    l1 = Label(eserCercevesi, text="Eserin Başlığı")
    yeni_baslik = Entry(eserCercevesi, width=25)
    l2 = Label(eserCercevesi, text="Eserin Açıklaması")
    yeni_aciklama = Entry(eserCercevesi, width=25)
    l3 = Label(eserCercevesi, text="Eserin Dili")
    yeni_dil = Entry(eserCercevesi, width=25)
    l4 = Label(eserCercevesi, text="Eserin ISBN Numarası")
    yeni_ISBN = Entry(eserCercevesi, width=25)
    b1 = Button(eserCercevesi, text="Eseri Güncelle", command=guncelle)
    b2 = Button(eserCercevesi, text="Çıkış", command=pencereGuncelle.destroy)
    l1.grid(row=0, column=0, sticky=W, pady=2)
    yeni_baslik.grid(row=0, column=1, pady=2)
    l2.grid(row=1, column=0, sticky=W, pady=2)
    yeni_aciklama.grid(row=1, column=1, pady=2)
    l3.grid(row=2, column=0, sticky=W, pady=2)
    yeni_dil.grid(row=2, column=1, pady=2)
    l4.grid(row=3, column=0, sticky=W, pady=2)
    yeni_ISBN.grid(row=3, column=1, pady=2)
    b1.grid(row=4, column=1, pady=2)
    b2.grid(row=4, column=0, pady=2)
    pencereGuncelle.mainloop()

def eserGuncelleDB(eser_id, yeni_baslik, yeni_aciklama, yeni_dil, yeni_ISBN):
    sorgu.execute("UPDATE book SET title=?, eserAciklama=?, eserDili=?, eserISBN=? WHERE book_id=?",
                  (yeni_baslik, yeni_aciklama, yeni_dil, yeni_ISBN, eser_id))
    baglanti.commit()
    messagebox.showinfo("Başarılı", "Eser başarıyla güncellendi.")
    eserleriListele()

def katalogUygulamasi():
    global eserTablosu, pencere, arama
    pencere = Tk()
    pencere.title('Miray Tekcan')
    pencere.geometry('800x400')
    pencere.resizable(True, True)
    pencere['bg'] = '#ECECEC'
    eserTabloCercevesi = ttk.Frame(pencere, padding=25)
    eserTabloCercevesi.pack()
    eserTablosu = ttk.Treeview(eserTabloCercevesi)
    eserTablosu['columns'] = ('id', 'title', 'author', 'genre', 'rating')
    eserTablosu.heading('#1', text='ID')
    eserTablosu.heading('#2', text='Başlık')
    eserTablosu.heading('#3', text='Açıklama')
    eserTablosu.heading('#4', text='Dil')
    eserTablosu.heading('#5', text='ISBN')
    eserTablosu.pack()
    menuCercevesi = Frame(pencere)
    menuCercevesi.pack()
    butonListele = Button(menuCercevesi, text="Eserleri Listele", command=eserleriListele)
    butonListele.grid(row=0, column=0, padx=5)
    butonEkle = Button(menuCercevesi, text="Yeni Eser Ekle", command=eserEkleForm)
    butonEkle.grid(row=0, column=1, padx=5)
    aramaBaslik = Label(eserTabloCercevesi, text="Aramak istediğiniz eserin adını girin:")
    arama = Entry(eserTabloCercevesi, width=25)
    ara = Button(eserTabloCercevesi, text="Ara", command=aramaYap)
    aramaBaslik.pack()
    arama.pack()
    ara.pack()
    temizleButton = Button(eserTabloCercevesi, text="Temizle", command=temizle)
    temizleButton.pack()
    butonSil = Button(menuCercevesi, text="Eseri Sil", command=eserSil)
    butonSil.grid(row=0, column=2, padx=5)
    butonGuncelle = Button(menuCercevesi, text="Eseri Güncelle", command=eserGuncelle)
    butonGuncelle.grid(row=0, column=3, padx=5)
    butonCikis = Button(menuCercevesi, text="Çıkış", command=on_cikis)
    butonCikis.grid(row=0, column=4, padx=5)
    pencere.mainloop()

def on_cikis():
    cevap = messagebox.askyesno("Çıkış", "Çıkış yapmak istediğinizden emin misiniz?")
    if cevap:
        pencere.destroy()

katalogUygulamasi()
