from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, black, white

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
W, H = A4
M = 1.6 * cm
GRI = HexColor("#F2F2F2"); CIZGI = HexColor("#BBBBBB"); KOYU = HexColor("#333333")
c = canvas.Canvas("AHP_Yargi_Formu.pdf", pagesize=A4)
c.setTitle("AHP Yargı Formu: Kredi Onay Kriterlerinin Göreli Önemi")
c.setAuthor("Mehmet Egemen Kılınç")
form = c.acroForm


def paragraf(metin, x, y, genislik, font="DV", boyut=10, satir=13.5):
    kelimeler, satirlar, s = metin.split(), [], ""
    for k in kelimeler:
        aday = (s + " " + k).strip()
        if pdfmetrics.stringWidth(aday, font, boyut) > genislik:
            satirlar.append(s); s = k
        else:
            s = aday
    satirlar.append(s)
    c.setFont(font, boyut)
    for l in satirlar:
        c.drawString(x, y, l); y -= satir
    return y


def baslik(metin, y, boyut=12):
    c.setFont("DVB", boyut); c.setFillColor(black); c.drawString(M, y, metin); return y - 0.55 * cm


def tablo(satirlar, y, gen, kalin_ilk=True, boyut=9, yuk=0.62 * cm):
    x0 = M
    for i, r in enumerate(satirlar):
        if i == 0 and kalin_ilk:
            c.setFillColor(GRI); c.rect(x0, y - yuk + 0.15 * cm, sum(gen), yuk, stroke=0, fill=1)
        c.setFillColor(black); c.setFont("DVB" if (i == 0 and kalin_ilk) else "DV", boyut)
        x = x0
        for metin, g in zip(r, gen):
            c.drawString(x + 0.15 * cm, y - 0.28 * cm, metin); x += g
        c.setStrokeColor(CIZGI); c.line(x0, y - yuk + 0.15 * cm, x0 + sum(gen), y - yuk + 0.15 * cm)
        y -= yuk
    return y


# ---------- SAYFA 1 ----------
y = H - M
c.setFont("DVB", 15); c.drawString(M, y, "AHP Yargı Formu"); y -= 0.6 * cm
c.setFont("DV", 11); c.setFillColor(KOYU); c.drawString(M, y, "Kredi onay kriterlerinin göreli önemi"); y -= 0.9 * cm
c.setFillColor(black)
y = baslik("Amaç", y)
y = paragraf("Bu form, bireysel kredi başvurusunda onay ya da ret kararı verirken 6 kriterin birbirine göre ne kadar "
             "önemli olduğunu belirlemek için hazırlandı. Cevaplarınız yalnızca bir ders projesinde (Karar Destek "
             "Sistemleri, Muğla Sıtkı Koçman Üniversitesi, Bilişim Sistemleri Mühendisliği) kriter ağırlıklarını "
             "hesaplamak için kullanılacaktır.", M, y, W - 2 * M)
y -= 0.15 * cm
y = paragraf("Doğru ya da yanlış cevap yoktur; kendi mesleki deneyiminize göre yanıtlayın. Formu doldurmak yaklaşık "
             "10 dakika sürer. İsim yazmanız gerekmez.", M, y, W - 2 * M)
y -= 0.5 * cm
y = baslik("Kriterler", y)
y = tablo([["Kod", "Kriter", "Açıklama"],
           ["K1", "Temerrüt olasılığı (PD)", "Modelin başvuranın ödeme güçlüğü olasılığı için tahmini; bir tür risk notu"],
           ["K2", "Kredi / gelir oranı", "İstenen kredi tutarının başvuranın gelirine oranı"],
           ["K3", "Taksit / gelir oranı", "Taksit tutarının gelire oranı (ödeme yükü)"],
           ["K4", "Gelir", "Başvuranın beyan ettiği gelir"],
           ["K5", "İstihdam süresi", "Mevcut işte çalışılan yıl"],
           ["K6", "Geçmiş gecikme", "Kredi bürosu kayıtlarında gecikme izi olan kredi sayısı"]],
          y, [1.2 * cm, 4.4 * cm, W - 2 * M - 5.6 * cm], boyut=8.6)
y -= 0.6 * cm
y = baslik("Ölçek (Saaty 1–9)", y)
y = tablo([["Değer", "Anlamı"], ["1", "İkisi eşit önemde"], ["3", "Biri diğerinden biraz daha önemli"],
           ["5", "Biri diğerinden belirgin şekilde daha önemli"], ["7", "Biri diğerinden çok daha önemli"],
           ["9", "Biri diğerinden kesinlikle daha önemli"], ["2, 4, 6, 8", "Ara değerler"]],
          y, [2.6 * cm, W - 2 * M - 2.6 * cm], boyut=9)
y -= 0.6 * cm
y = baslik("Nasıl doldurulur?", y)
y = paragraf("Sonraki sayfadaki her satırda önce hangi kriterin daha önemli olduğunu işaretleyin (Sol, Eşit ya da Sağ), "
             "sonra ne kadar daha önemli olduğunu 1–9 arasında işaretleyin. İkisi eşitse Eşit ve 1 işaretleyin. "
             "Örneğin bir satırda Sol ve 5 işaretlemek, soldaki kriterin sağdakinden belirgin şekilde daha önemli "
             "olduğunu söyler.", M, y, W - 2 * M)
y -= 0.15 * cm
y = paragraf("Cevapların birbiriyle tutarlı olması önemlidir: A, B'den; B de C'den önemliyse A'nın C'den de önemli "
             "olması beklenir. Tutarlılık hesaplanacak; gerekirse birkaç satırı yeniden düşünmeniz istenebilir.",
             M, y, W - 2 * M)
y -= 0.15 * cm
c.setFillColor(KOYU)
y = paragraf("Form yazdırılıp kalemle ya da bir PDF okuyucuda (ör. Adobe Acrobat Reader) tıklanarak doldurulabilir.",
             M, y, W - 2 * M, boyut=9)
c.setFillColor(black)
c.setFont("DV", 8); c.drawRightString(W - M, M * 0.6, "Sayfa 1 / 2")
c.showPage()

# ---------- SAYFA 2 ----------
y = H - M
c.setFont("DVB", 13); c.drawString(M, y, "İkili karşılaştırmalar (15 çift)"); y -= 0.8 * cm
KR = ["K1 Temerrüt olasılığı", "K2 Kredi/gelir", "K3 Taksit/gelir", "K4 Gelir", "K5 İstihdam süresi", "K6 Geçmiş gecikme"]
ciftler = [(i, j) for i in range(6) for j in range(i + 1, 6)]
x_no, x_sol, x_sag = M, M + 0.7 * cm, M + 4.6 * cm
x_yon = M + 8.5 * cm
x_deg = M + 12.0 * cm
adim_yon, adim_deg = 1.05 * cm, 0.62 * cm
# başlık satırı
c.setFillColor(GRI); c.rect(M, y - 0.35 * cm, W - 2 * M, 0.75 * cm, stroke=0, fill=1); c.setFillColor(black)
c.setFont("DVB", 8.5)
c.drawString(x_no, y, "#"); c.drawString(x_sol, y, "Sol kriter"); c.drawString(x_sag, y, "Sağ kriter")
c.drawString(x_yon, y + 0.05 * cm, "Daha önemli olan")
c.drawString(x_deg, y + 0.05 * cm, "Ne kadar daha önemli? (1–9)")
c.setFont("DV", 7.5)
for k, et in enumerate(["Sol", "Eşit", "Sağ"]):
    c.drawCentredString(x_yon + 0.3 * cm + k * adim_yon, y - 0.3 * cm, et)
for k in range(9):
    c.drawCentredString(x_deg + 0.3 * cm + k * adim_deg, y - 0.3 * cm, str(k + 1))
y -= 1.05 * cm
satir_y = 1.13 * cm
for n, (i, j) in enumerate(ciftler, start=1):
    if n % 2 == 0:
        c.setFillColor(HexColor("#FAFAFA")); c.rect(M, y - 0.42 * cm, W - 2 * M, satir_y, stroke=0, fill=1)
    c.setFillColor(black); c.setFont("DV", 9)
    c.drawString(x_no, y, str(n)); c.drawString(x_sol, y, KR[i]); c.drawString(x_sag, y, KR[j])
    # Yazdırmada her görüntüleyicide temiz görünsün: sabit çizilmiş halka + üstünde kenarlıksız tıklanabilir düğme
    c.setStrokeColor(KOYU); c.setLineWidth(0.8)
    for k, deger in enumerate(["Sol", "Esit", "Sag"]):
        cx, cy = x_yon + 0.3 * cm + k * adim_yon, y + 3
        c.circle(cx, cy, 6.5, stroke=1, fill=0)
        form.radio(name=f"yon_{n:02d}", value=deger, x=cx - 6, y=cy - 6, size=12, buttonStyle="circle",
                   borderWidth=0, borderColor=None, fillColor=None, textColor=black, tooltip=f"Çift {n}: {deger}")
    for k in range(9):
        cx, cy = x_deg + 0.3 * cm + k * adim_deg, y + 3
        c.circle(cx, cy, 6, stroke=1, fill=0)
        form.radio(name=f"deger_{n:02d}", value=str(k + 1), x=cx - 5.5, y=cy - 5.5, size=11, buttonStyle="circle",
                   borderWidth=0, borderColor=None, fillColor=None, textColor=black, tooltip=f"Çift {n}: {k + 1}")
    c.setStrokeColor(CIZGI); c.line(M, y - 0.42 * cm, W - M, y - 0.42 * cm)
    y -= satir_y

y -= 0.4 * cm
y = baslik("Yargıç bilgisi (isim gerekmez)", y, boyut=11)
for etiket, ad in [("Görev / uzmanlık (ör. banka çalışanı, kredi analisti):", "gorev"),
                   ("Kredi değerlendirme deneyimi (yıl):", "deneyim"), ("Formu doldurma tarihi:", "tarih")]:
    c.setFont("DV", 9); c.drawString(M, y, etiket)
    form.textfield(name=ad, x=M + 8.6 * cm, y=y - 0.15 * cm, width=W - 2 * M - 8.6 * cm, height=0.55 * cm,
                   borderColor=CIZGI, fillColor=white, textColor=black, fontSize=9, borderWidth=0.6, forceBorder=True)
    y -= 0.8 * cm
y -= 0.2 * cm
c.setFont("DV", 9)
c.drawString(M, y, "Katılımınız için teşekkür ederim. Sorularınız için: Mehmet Egemen Kılınç (projeyi yürüten öğrenci).")
c.setFont("DV", 8); c.drawRightString(W - M, M * 0.6, "Sayfa 2 / 2")
c.showPage()
c.save()
print("ok")
