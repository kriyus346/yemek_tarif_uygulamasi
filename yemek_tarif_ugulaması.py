import tkinter as tk
from tkinter import simpledialog, messagebox, Text
from datetime import datetime
import random

tarifler = []

class Tarif:
    def __init__(self, ad, malzemeler, aciklama):
        self.ad = ad
        self.malzemeler = malzemeler
        self.aciklama = aciklama
        self.eklenme_tarihi = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.puanlar = []

    def puan_ver(self, puan):
        if 1 <= puan <= 5:
            self.puanlar.append(puan)
            messagebox.showinfo("Başarılı", f"'{self.ad}' tarifine {puan} puan verdiniz.")
        else:
            messagebox.showerror("Hata", "Puan 1 ile 5 arasında olmalıdır.")

    def ortalama_puan(self):
        if self.puanlar:
            return sum(self.puanlar) / len(self.puanlar)
        return None

def tarif_ekle_manuel(ad, malzemeler_str, aciklama):
    malzemeler = [{"ad": m.split(":")[0].strip(), "miktar": m.split(":")[1].strip()} for m in malzemeler_str.split(",")]
    tarif = Tarif(ad, malzemeler, aciklama)
    tarifler.append(tarif)

def tarif_ekle():
    ad = simpledialog.askstring("Tarif Ekle", "Tarif Adı:")
    if not ad:
        return

    malzemeler = []
    malzeme_penceresi = tk.Toplevel()
    malzeme_penceresi.title("Malzeme Ekle")

    def yeni_malzeme_ekle():
        malzeme_adi = simpledialog.askstring("Malzeme Ekle", "Malzeme Adı:")
        if not malzeme_adi:
            return
        malzeme_miktari = simpledialog.askstring("Malzeme Ekle", f"{malzeme_adi} Miktarı:")
        if malzeme_miktari is not None:
            malzemeler.append({"ad": malzeme_adi, "miktar": malzeme_miktari})
            messagebox.showinfo("Bilgi", f"'{malzeme_adi}' ({malzeme_miktari}) eklendi.")

    def tamamla_fonksiyonu():
        malzeme_penceresi.destroy()
        if not malzemeler:
            messagebox.showwarning("Uyarı", "Lütfen en az bir malzeme ekleyin.")
            return
        aciklama = simpledialog.askstring("Tarif Ekle", "Tarif Açıklaması:")
        if aciklama is not None:
            tarif = Tarif(ad, malzemeler, aciklama)
            tarifler.append(tarif)
            messagebox.showinfo("Başarılı", f"'{ad}' adlı tarif eklendi.")

    ekle_butonu = tk.Button(malzeme_penceresi, text="Yeni Malzeme Ekle", command=yeni_malzeme_ekle)
    ekle_butonu.pack(pady=5)

    tamam_butonu = tk.Button(malzeme_penceresi, text="Tamam", command=tamamla_fonksiyonu)
    tamam_butonu.pack(pady=5)

def tarif_sil():
    if not tarifler:
        messagebox.showinfo("Bilgi", "Silinecek tarif bulunmuyor.")
        return

    silme_penceresi = tk.Toplevel()
    silme_penceresi.title("Tarif Sil")

    liste_etiketi = tk.Label(silme_penceresi, text="Silmek istediğiniz tarifi seçin:")
    liste_etiketi.pack(pady=5)

    tarif_isimleri = [tarif.ad for tarif in tarifler]
    liste_kutusu = tk.Listbox(silme_penceresi, width=50)
    for isim in tarif_isimleri:
        liste_kutusu.insert(tk.END, isim)
    liste_kutusu.pack(pady=5)

    def sil():
        secilen_index = liste_kutusu.curselection()
        if secilen_index:
            secilen_tarif = tarifler[secilen_index[0]]
            onay = messagebox.askyesno("Onay", f"'{secilen_tarif.ad}' tarifini silmek istediğinize emin misiniz?")
            if onay:
                del tarifler[secilen_index[0]]
                messagebox.showinfo("Başarılı", f"'{secilen_tarif.ad}' tarifi silindi.")
                silme_penceresi.destroy()
                tarif_sil()
        else:
            messagebox.showerror("Hata", "Lütfen silmek için bir tarif seçin.")

    sil_butonu = tk.Button(silme_penceresi, text="Sil", command=sil)
    sil_butonu.pack(pady=5)

    iptal_butonu = tk.Button(silme_penceresi, text="İptal", command=silme_penceresi.destroy)
    iptal_butonu.pack(pady=5)

def tarif_ara():
    arama_terimi = simpledialog.askstring("Tarif Ara", "Aramak istediğiniz kelime (tarif adı veya malzeme):")
    if not arama_terimi:
        return
    sonuclar = [t for t in tarifler if arama_terimi.lower() in t.ad.lower() or any(arama_terimi.lower() in m['ad'].lower() for m in t.malzemeler)]
    if sonuclar:
        sonuc_penceresi = tk.Toplevel()
        sonuc_penceresi.title("Arama Sonuçları")
        sonuc_text = Text(sonuc_penceresi)
        for i, tarif in enumerate(sonuclar):
            ortalama = tarif.ortalama_puan()
            puan_bilgisi = f"(Ort. Puan: {ortalama:.2f})" if ortalama is not None else "(Henüz Puanlanmamış)"
            sonuc_text.insert(tk.END, f"{i+1}. {tarif.ad} {puan_bilgisi}\n")
        sonuc_text.config(state="disabled")
        sonuc_text.pack()

        def tarif_goruntule():
            secim = simpledialog.askinteger("Tarif Görüntüle", "Görüntülemek istediğiniz tarifin numarasını girin:")
            if secim and 1 <= secim <= len(sonuclar):
                secilen_tarif = sonuclar[secim-1]
                detay_penceresi = tk.Toplevel()
                detay_penceresi.title(secilen_tarif.ad)
                detay_text = Text(detay_penceresi)
                detay_text.insert(tk.END, f"Tarif Adı: {secilen_tarif.ad}\n")
                detay_text.insert(tk.END, "Malzemeler:\n")
                for malzeme in secilen_tarif.malzemeler:
                    detay_text.insert(tk.END, f"- {malzeme['ad']}: {malzeme['miktar']}\n")
                detay_text.insert(tk.END, f"\nAçıklama:\n{secilen_tarif.aciklama}\n")
                detay_text.insert(tk.END, f"Eklenme Tarihi: {secilen_tarif.eklenme_tarihi}\n")
                ortalama = secilen_tarif.ortalama_puan()
                puan_bilgisi = f"Ortalama Puan: {ortalama:.2f}" if ortalama is not None else "Ortalama Puan: Henüz Puanlanmamış"
                detay_text.insert(tk.END, f"{puan_bilgisi}\n")
                detay_text.config(state="disabled")
                detay_text.pack()

                def puan_ver_arayuzu():
                    puan = simpledialog.askinteger("Puan Ver", f"'{secilen_tarif.ad}' için puanınızı girin (1-5):")
                    if puan is not None:
                        secilen_tarif.puan_ver(puan)
                        ortalama = secilen_tarif.ortalama_puan()
                        puan_bilgisi = f"Ortalama Puan: {ortalama:.2f}" if ortalama is not None else "Ortalama Puan: Henüz Puanlanmamış"
                        detay_text.config(state=tk.NORMAL)
                        detay_text.delete("end - 1 line", tk.END)
                        detay_text.insert(tk.END, f"{puan_bilgisi}\n")
                        detay_text.config(state="disabled")

                puan_ver_button = tk.Button(detay_penceresi, text="Puan Ver", command=puan_ver_arayuzu)
                puan_ver_button.pack()

            elif secim:
                messagebox.showerror("Hata", "Geçersiz seçim.")

        goruntule_button = tk.Button(sonuc_penceresi, text="Tarifi Görüntüle", command=tarif_goruntule)
        goruntule_button.pack()
    else:
        messagebox.showinfo("Bilgi", "Aradığınız kriterlere uygun tarif bulunamadı.")

def tum_tarifleri_goster():
    if tarifler:
        siralanmis_tarifler = sorted(tarifler, key=lambda tarif: tarif.ortalama_puan() if tarif.ortalama_puan() is not None else -1, reverse=True)
        goster_penceresi = tk.Toplevel()
        goster_penceresi.title("Tüm Tarifler (Puana Göre Sıralı)")
        goster_text = Text(goster_penceresi)
        for i, tarif in enumerate(siralanmis_tarifler):
            ortalama = tarif.ortalama_puan()
            puan_bilgisi = f"(Ort. Puan: {ortalama:.2f})" if ortalama is not None else "(Henüz Puanlanmamış)"
            goster_text.insert(tk.END, f"{i+1}. {tarif.ad} {puan_bilgisi} (Eklenme: {tarif.eklenme_tarihi})\n")
        goster_text.config(state="disabled")
        goster_text.pack()

        def tarif_detay_goster():
            secim = simpledialog.askinteger("Tarif Detay", "Detayını görmek istediğiniz tarifin numarasını girin:")
            if secim and 1 <= secim <= len(siralanmis_tarifler):
                secilen_tarif = siralanmis_tarifler[secim-1]
                detay_penceresi = tk.Toplevel()
                detay_penceresi.title(secilen_tarif.ad)
                detay_text = Text(detay_penceresi)
                detay_text.insert(tk.END, f"Tarif Adı: {secilen_tarif.ad}\n")
                detay_text.insert(tk.END, "Malzemeler:\n")
                for malzeme in secilen_tarif.malzemeler:
                    detay_text.insert(tk.END, f"- {malzeme['ad']}: {malzeme['miktar']}\n")
                detay_text.insert(tk.END, f"\nAçıklama:\n{secilen_tarif.aciklama}\n")
                detay_text.insert(tk.END, f"Eklenme Tarihi: {secilen_tarif.eklenme_tarihi}\n")
                ortalama = secilen_tarif.ortalama_puan()
                puan_bilgisi = f"Ortalama Puan: {ortalama:.2f}" if ortalama is not None else "Ortalama Puan: Henüz Puanlanmamış"
                detay_text.insert(tk.END, f"{puan_bilgisi}\n")
                detay_text.config(state="disabled")
                detay_text.pack()

                def puan_ver_arayuzu():
                    puan = simpledialog.askinteger("Puan Ver", f"'{secilen_tarif.ad}' için puanınızı girin (1-5):")
                    if puan is not None:
                        secilen_tarif.puan_ver(puan)
                        ortalama = secilen_tarif.ortalama_puan()
                        puan_bilgisi = f"Ortalama Puan: {ortalama:.2f}" if ortalama is not None else "Ortalama Puan: Henüz Puanlanmamış"
                        detay_text.config(state=tk.NORMAL)
                        detay_text.delete("end - 1 line", tk.END)
                        detay_text.insert(tk.END, f"{puan_bilgisi}\n")
                        detay_text.config(state="disabled")

                puan_ver_button = tk.Button(detay_penceresi, text="Puan Ver", command=puan_ver_arayuzu)
                puan_ver_button.pack()

            elif secim:
                messagebox.showerror("Hata", "Geçersiz seçim.")

        detay_button = tk.Button(goster_penceresi, text="Tarif Detaylarını Göster", command=tarif_detay_goster)
        detay_button.pack()
    else:
        messagebox.showinfo("Bilgi", "Henüz hiç tarif eklenmemiş.")

def sasirt_beni():
    if not tarifler:
        messagebox.showinfo("Bilgi", "Henüz hiç tarif eklenmemiş.")
        return

    yuksek_puanli_tarifler = [tarif for tarif in tarifler if tarif.ortalama_puan() is not None]
    if not yuksek_puanli_tarifler:
        messagebox.showinfo("Bilgi", "Henüz hiç puanlanmış tarif yok.")
        return

    en_yuksek_puan = max(tarif.ortalama_puan() for tarif in yuksek_puanli_tarifler)
    en_iyi_tarifler = [tarif for tarif in yuksek_puanli_tarifler if tarif.ortalama_puan() == en_yuksek_puan]
    secilen_tarif = random.choice(en_iyi_tarifler)

    detay_penceresi = tk.Toplevel()
    detay_penceresi.title(secilen_tarif.ad)
    detay_text = Text(detay_penceresi)
    detay_text.insert(tk.END, f"Tarif Adı: {secilen_tarif.ad}\n")
    detay_text.insert(tk.END, "Malzemeler:\n")
    for malzeme in secilen_tarif.malzemeler:
        detay_text.insert(tk.END, f"- {malzeme['ad']}: {malzeme['miktar']}\n")
    detay_text.insert(tk.END, f"\nAçıklama:\n{secilen_tarif.aciklama}\n")
    detay_text.insert(tk.END, f"Eklenme Tarihi: {secilen_tarif.eklenme_tarihi}\n")
    ortalama = secilen_tarif.ortalama_puan()
    puan_bilgisi = f"Ortalama Puan: {ortalama:.2f}" if ortalama is not None else "Ortalama Puan: Henüz Puanlanmamış"
    detay_text.insert(tk.END, f"{puan_bilgisi}\n")
    detay_text.config(state="disabled")
    detay_text.pack()

    def puan_ver_arayuzu():
        puan = simpledialog.askinteger("Puan Ver", f"'{secilen_tarif.ad}' için puanınızı girin (1-5):")
        if puan is not None:
            secilen_tarif.puan_ver(puan)
            ortalama = secilen_tarif.ortalama_puan()
            puan_bilgisi = f"Ortalama Puan: {ortalama:.2f}" if ortalama is not None else "Ortalama Puan: Henüz Puanlanmamış"
            detay_text.config(state=tk.NORMAL)
            detay_text.delete("end - 1 line", tk.END)
            detay_text.insert(tk.END, f"{puan_bilgisi}\n")
            detay_text.config(state="disabled")

    puan_ver_button = tk.Button(detay_penceresi, text="Puan Ver", command=puan_ver_arayuzu)
    puan_ver_button.pack()


def baslat():
    ana_pencere = tk.Tk()
    ana_pencere.title("Yemek Tarifi Uygulaması")

    # Önceden tanımlanmış 5 tarif ekle
    tarif_ekle_manuel("Mercimek Çorbası", "Kırmızı mercimek:1 su bardağı,Soğan:1 adet,Havuç:1 adet,Su:6 su bardağı,Tuz:1 tatlı kaşığı", "Mercimeği yıkayın, sebzeleri doğrayın, tencerede kavurun, su ve tuzu ekleyip pişirin. Blendırdan geçirin ve nane ile servis yapın.")
    tarif_ekle_manuel("Domates Çorbası", "Domates:4 adet,Soğan:Yarım adet,Sarımsak:2 diş,Zeytinyağı:2 yemek kaşığı,Salça:1 yemek kaşığı,Su:4 su bardağı,Fesleğen:Birkaç yaprak", "Domatesleri doğrayın, soğan ve sarımsağı kavurun, salçayı ekleyin, su ve fesleğen ile pişirin. Blendırdan geçirin ve servis yapın.")
    tarif_ekle_manuel("Tavuk Sote", "Tavuk göğsü:500 gr,Biber:2 adet,Soğan:1 adet,Soya sosu:2 yemek kaşığı,Sıvı yağ:3 yemek kaşığı,Kekik:1 tatlı kaşığı", "Tavukları küp küp doğrayın, biberleri ve soğanı doğrayın. Tavukları sıvı yağda soteleyin, biber ve soğanları ekleyin, soya sosu ve kekik ile pişirin.")
    tarif_ekle_manuel("Makarna Bolonez", "Spagetti:500 gr,Kıyma:300 gr,Soğan:1 adet,Havuç:1 adet,Domates salçası:2 yemek kaşığı,Domates konservesi:400 gr,Zeytinyağı:4 yemek kaşığı", "Spagettiyi haşlayın. Kıyma, soğan ve havucu kavurun. Salça ve domates konservesi ekleyip pişirin. Makarna ile karıştırın.")
    tarif_ekle_manuel("Salata", "Marul:1 adet,Domates:2 adet,Salatalık:1 adet,Zeytinyağı:3 yemek kaşığı,Limon suyu:Yarım limon,Tuz:Bir tutam", "Marulu doğrayın, domates ve salatalığı doğrayın. Zeytinyağı, limon suyu ve tuz ile karıştırın.")


    for yazi, fonk in [
        ("Yeni Tarif Ekle", tarif_ekle),
        ("Tarif Ara", tarif_ara),
        ("Tüm Tarifleri Göster", tum_tarifleri_goster),
        ("Tarif Sil", tarif_sil),
        ("Şaşırt Beni", sasirt_beni),
        ("Çık", ana_pencere.quit)
    ]:
        tk.Button(ana_pencere, text=yazi, command=fonk).pack(pady=5)

    ana_pencere.mainloop()

if __name__ == "__main__":
    baslat()
