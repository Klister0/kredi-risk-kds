const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType,
        ShadingType, BorderStyle, CheckBox, PageBreak, VerticalAlign, HeightRule, Footer, PageNumber } = require("docx");

const FONT = "Arial";
const GRI = "F2F2F2", CIZGI = "BBBBBB";
const kenar = { style: BorderStyle.SINGLE, size: 4, color: CIZGI };
const kenarlar = { top: kenar, bottom: kenar, left: kenar, right: kenar };
const p = (text, o = {}) => new Paragraph({ spacing: { after: o.after ?? 120 }, alignment: o.align,
  children: [new TextRun({ text, font: FONT, size: o.size ?? 21, bold: o.bold, color: o.color })] });
const h = (text) => new Paragraph({ spacing: { before: 200, after: 100 }, keepNext: true,
  children: [new TextRun({ text, font: FONT, size: 24, bold: true })] });
const hucre = (text, w, o = {}) => new TableCell({
  width: { size: w, type: WidthType.DXA }, borders: kenarlar, columnSpan: o.span,
  verticalAlign: VerticalAlign.CENTER,
  shading: o.baslik ? { type: ShadingType.CLEAR, color: "auto", fill: GRI } : (o.fill ? { type: ShadingType.CLEAR, color: "auto", fill: o.fill } : undefined),
  margins: { top: 50, bottom: 50, left: 70, right: 70 },
  children: [new Paragraph({ alignment: o.align ?? AlignmentType.LEFT,
    children: [new TextRun({ text, font: FONT, size: o.size ?? 18, bold: o.baslik })] })] });
const kutu = (w, fill) => new TableCell({
  width: { size: w, type: WidthType.DXA }, borders: kenarlar, verticalAlign: VerticalAlign.CENTER,
  shading: fill ? { type: ShadingType.CLEAR, color: "auto", fill } : undefined,
  margins: { top: 40, bottom: 40, left: 20, right: 20 },
  children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new CheckBox({ checked: false })] })] });

function basitTablo(satirlar, gen) {
  const top = gen.reduce((a, b) => a + b, 0);
  return new Table({ width: { size: top, type: WidthType.DXA }, columnWidths: gen,
    rows: satirlar.map((r, i) => new TableRow({ tableHeader: i === 0,
      children: r.map((t, j) => hucre(t, gen[j], { baslik: i === 0 })) })) });
}

// ---- Sayfa 1 ----
const TAM = 9746; // A4, 0,75" kenar boşluğu
const s1 = [
  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "AHP Yargı Formu", font: FONT, size: 34, bold: true })] }),
  p("Kredi onay kriterlerinin göreli önemi", { color: "555555", size: 22, after: 200 }),
  h("Amaç"),
  p("Bu form, bireysel kredi başvurusunda onay ya da ret kararı verirken 6 kriterin birbirine göre ne kadar önemli olduğunu belirlemek için hazırlandı. Cevaplarınız yalnızca bir ders projesinde (Karar Destek Sistemleri, Muğla Sıtkı Koçman Üniversitesi, Bilişim Sistemleri Mühendisliği) kriter ağırlıklarını hesaplamak için kullanılacaktır."),
  p("Doğru ya da yanlış cevap yoktur; kendi mesleki deneyiminize göre yanıtlayın. Formu doldurmak yaklaşık 10 dakika sürer. İsim yazmanız gerekmez."),
  h("Kriterler"),
  basitTablo([["Kod", "Kriter", "Açıklama"],
    ["K1", "Temerrüt olasılığı (PD)", "Modelin başvuranın ödeme güçlüğü olasılığı için tahmini; bir tür risk notu"],
    ["K2", "Kredi / gelir oranı", "İstenen kredi tutarının başvuranın gelirine oranı"],
    ["K3", "Taksit / gelir oranı", "Taksit tutarının gelire oranı (ödeme yükü)"],
    ["K4", "Gelir", "Başvuranın beyan ettiği gelir"],
    ["K5", "İstihdam süresi", "Mevcut işte çalışılan yıl"],
    ["K6", "Geçmiş gecikme", "Kredi bürosu kayıtlarında gecikme izi olan kredi sayısı"]], [800, 2700, TAM - 3500]),
  h("Ölçek (Saaty 1–9)"),
  basitTablo([["Değer", "Anlamı"], ["1", "İkisi eşit önemde"], ["3", "Biri diğerinden biraz daha önemli"],
    ["5", "Biri diğerinden belirgin şekilde daha önemli"], ["7", "Biri diğerinden çok daha önemli"],
    ["9", "Biri diğerinden kesinlikle daha önemli"], ["2, 4, 6, 8", "Ara değerler"]], [1600, TAM - 1600]),
  h("Nasıl doldurulur?"),
  p("Sonraki sayfadaki her satırda önce hangi kriterin daha önemli olduğunu işaretleyin (Sol, Eşit ya da Sağ), sonra ne kadar daha önemli olduğunu 1–9 arasında işaretleyin. Her satırda iki kutu işaretlenir: biri yön, biri değer. İkisi eşitse Eşit ve 1 işaretleyin. Örneğin bir satırda Sol ve 5 işaretlemek, soldaki kriterin sağdakinden belirgin şekilde daha önemli olduğunu söyler."),
  p("Cevapların birbiriyle tutarlı olması önemlidir: A, B'den; B de C'den önemliyse A'nın C'den de önemli olması beklenir. Tutarlılık hesaplanacak; gerekirse birkaç satırı yeniden düşünmeniz istenebilir."),
  p("Word'de kutulara tıklayarak işaretleyebilir ya da formu yazdırıp kalemle doldurabilirsiniz.", { color: "555555", size: 19 }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---- Sayfa 2: karşılaştırma tablosu ----
const KR = ["K1 Temerrüt olasılığı", "K2 Kredi/gelir", "K3 Taksit/gelir", "K4 Gelir", "K5 İstihdam süresi", "K6 Geçmiş gecikme"];
const G = { no: 420, sol: 2050, sag: 2050, yon: 520, deg: 400 };
const kolonlar = [G.no, G.sol, G.sag, G.yon, G.yon, G.yon, ...Array(9).fill(G.deg)];
const toplam = kolonlar.reduce((a, b) => a + b, 0);
const ust = new TableRow({ tableHeader: true, children: [
  hucre("#", G.no, { baslik: true }), hucre("Sol kriter", G.sol, { baslik: true }), hucre("Sağ kriter", G.sag, { baslik: true }),
  hucre("Daha önemli olan", 3 * G.yon, { baslik: true, span: 3, align: AlignmentType.CENTER }),
  hucre("Ne kadar daha önemli? (1–9)", 9 * G.deg, { baslik: true, span: 9, align: AlignmentType.CENTER })] });
const alt = new TableRow({ tableHeader: true, children: [
  hucre("", G.no, { baslik: true }), hucre("", G.sol, { baslik: true }), hucre("", G.sag, { baslik: true }),
  ...["Sol", "Eşit", "Sağ"].map(t => hucre(t, G.yon, { baslik: true, align: AlignmentType.CENTER, size: 16 })),
  ...Array.from({ length: 9 }, (_, k) => hucre(String(k + 1), G.deg, { baslik: true, align: AlignmentType.CENTER, size: 16 }))] });
const satirlar = [];
let n = 0;
for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) {
  n++;
  const fill = n % 2 === 0 ? "FAFAFA" : undefined;
  satirlar.push(new TableRow({ height: { value: 480, rule: HeightRule.ATLEAST }, cantSplit: true, children: [
    hucre(String(n), G.no, { fill }), hucre(KR[i], G.sol, { fill }), hucre(KR[j], G.sag, { fill }),
    kutu(G.yon, fill), kutu(G.yon, fill), kutu(G.yon, fill),
    ...Array.from({ length: 9 }, () => kutu(G.deg, fill))] }));
}
const s2 = [
  new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: "İkili karşılaştırmalar (15 çift)", font: FONT, size: 28, bold: true })] }),
  new Table({ width: { size: toplam, type: WidthType.DXA }, columnWidths: kolonlar, rows: [ust, alt, ...satirlar] }),
  h("Yargıç bilgisi (isim gerekmez)"),
  basitTablo([["Soru", "Cevap"], ["Görev / uzmanlık (ör. banka çalışanı, kredi analisti)", ""],
    ["Kredi değerlendirme deneyimi (yıl)", ""], ["Formu doldurma tarihi", ""]], [4800, TAM - 4800]),
  new Paragraph({ spacing: { before: 200 }, children: [new TextRun({ text: "Katılımınız için teşekkür ederim. Sorularınız için: Mehmet Egemen Kılınç (projeyi yürüten öğrenci).", font: FONT, size: 19 })] }),
];

const doc = new Document({
  creator: "Mehmet Egemen Kılınç", title: "AHP Yargı Formu: Kredi Onay Kriterlerinin Göreli Önemi",
  styles: { default: { document: { run: { font: FONT, size: 21 } } } },
  sections: [{ properties: { page: { margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      children: [new TextRun({ font: FONT, size: 16, children: ["Sayfa ", PageNumber.CURRENT, " / ", PageNumber.TOTAL_PAGES] })] })] }) },
    children: [...s1, ...s2] }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("AHP_Yargi_Formu.docx", b); console.log("ok", toplam); });
