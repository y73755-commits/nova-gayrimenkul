"""Generates docs/REKLAM-TASLAKLARI.md and validates Google Ads character limits."""
ads = {
 "Villa ve lüks konut danışmanlığı": {
  "lp": "https://nova-gayrimenkul.com/lp/villa-luks-konut/",
  "basliklar": ["Villa Danışmanlığı İstanbul","Lüks Konut Danışmanlığı","Nova Gayrimenkul","Villa Arayışınızı Netleştirin","Görüşme Planlayın","Kurucu Broker Yusuf Sezmiş","Konum ve Mahremiyet Odaklı","Villa Seçiminde Doğru Adımlar","Ofisimiz Sarıyer’de","Alım ve Kiralama Danışmanlığı","İhtiyacınızı Konuşalım","WhatsApp’tan Yazın","Lüks Konutta Doğru Karar","Mahremiyet, Bahçe ve Konum","Seçenekleri Birlikte Görelim"],
  "aciklamalar": ["Villa arayışınızda konum, mahremiyet ve bakım yükünü birlikte değerlendirelim.","İhtiyacınızı dinliyor, uygun seçenekleri aynı ölçütlerle karşılaştırıyoruz.","Kurucu Broker Yusuf Sezmiş ile alım ve kiralama sürecinizi adım adım planlayın.","Formu doldurun ya da WhatsApp’tan yazın; talebinize kısa sürede dönüş yapalım."],
  "temalar": ["villa danışmanlığı", "lüks konut danışmanlığı", "satılık villa istanbul", "kiralık villa istanbul (uzun dönem)", "müstakil ev danışmanlığı", "havuzlu villa sarıyer", "lüks konut emlak danışmanı"],
 },
 "Plaza, ofis ve home ofis danışmanlığı": {
  "lp": "https://nova-gayrimenkul.com/lp/plaza-ofis/",
  "basliklar": ["Ofis Kiralama Danışmanlığı","Plaza ve Ofis Danışmanlığı","Nova Gayrimenkul","Ekibinize Uygun Ofis","Kullanım Planıyla Başlayalım","Görüşme Planlayın","Ticari Gayrimenkul Desteği","Home Ofis Danışmanlığı","Ulaşım ve Bina Hizmetleri","Ofisimiz Sarıyer’de","Kurucu Broker Yusuf Sezmiş","Sözleşme Öncesi Kontrol","Ofis Seçiminde Doğru Adımlar","WhatsApp’tan Yazın","İhtiyacınızı Konuşalım"],
  "aciklamalar": ["Ekip yapısı, ulaşım ve bina hizmetlerine göre ofis seçeneklerini değerlendirelim.","Plaza, ofis ve home ofis arayışınızı metrekareden değil, kullanım planından başlatıyoruz.","Kira süresi, artış koşulları ve teslim durumunu baştan konuşarak ilerleyelim.","Formu doldurun ya da WhatsApp’tan yazın; talebinize kısa sürede dönüş yapalım."],
  "temalar": ["ofis kiralama danışmanlığı", "kiralık ofis maslak / levent / şişli", "plaza ofis kiralama", "satılık ofis istanbul", "ticari gayrimenkul danışmanı", "home ofis daire", "kurumsal ofis arayışı"],
 },
 "Mülk satış ve kiralama danışmanlığı": {
  "lp": "https://nova-gayrimenkul.com/lp/mulk-satis-kiralama/",
  "basliklar": ["Mülkünüzü Değerlendirelim","Evimi Satmak İstiyorum","Mülkümü Kiraya Vermek","Satış Danışmanlığı","Kiralama Danışmanlığı","Doğru Fiyat Stratejisi","Nova Gayrimenkul","Değerlendirme Talep Edin","Kurucu Broker Yusuf Sezmiş","Hazırlık ve Sunum Desteği","Tapu İstemiyoruz, Kısa Form","Ofisimiz Sarıyer’de","WhatsApp’tan Yazın","EİDS Yetki Süreci Desteği","Satışa Hazırlık Planı"],
  "aciklamalar": ["Mülkünüzü değerlendirip fiyat stratejisini hedeflerinize göre birlikte kuralım.","Hazırlık, fotoğraf, sunum ve yayın sürecini planlıyor, görüşmeleri düzenli takip ediyoruz.","Kısa form yeterli: mülk türü, konum ve yaklaşık metrekare. İlk aşamada belge istemiyoruz.","Satmak ya da kiraya vermek için Kurucu Broker Yusuf Sezmiş ile görüşme planlayın."],
  "temalar": ["evimi satmak istiyorum", "mülkümü kiraya vermek istiyorum", "emlak danışmanı satış", "ev değerleme talebi", "daire satış danışmanlığı", "villa satış danışmanlığı", "kiraya verme danışmanlığı"],
 },
}
neg_ortak = ["ücretsiz","bedava","iş ilanı","kariyer","staj","maaş","emlakçı olmak","emlak kursu","emlak sertifikası","sahibinden com","hepsiemlak","emlakjet","zingat","dilekçe","sözleşme örneği","örnek","nasıl yapılır","vergi hesaplama","tapu harcı hesaplama","kredi hesaplama","dekorasyon","mobilya","tadilat","inşaat malzemesi","oyun","çizim","maket","3d model","proje çizimi","the sims","minecraft"]
neg_ozel = {
 "Villa ve lüks konut danışmanlığı": ["günlük kiralık","haftalık kiralık","tatil","otel","airbnb","yazlık","balayı","bodrum","fethiye","kaş","kalkan","antalya","bungalov"],
 "Plaza, ofis ve home ofis danışmanlığı": ["sanal ofis","ofis mobilyası","ofis malzemeleri","kırtasiye","microsoft office","office 365","ofis programı","ofis temizliği","çay ocağı","coworking günlük"],
 "Mülk satış ve kiralama danışmanlığı": ["kiralık ev arıyorum","satılık ev arıyorum","öğrenci evi","apart","ev arkadaşı","kira artış oranı","tahliye","icra","kira sözleşmesi örneği"],
}
out = ["# Google Ads — reklam metni taslakları ve anahtar kelime önerileri", "",
"Bu taslaklar **yayına alınmadı**: bütçe, faturalandırma ve hesap erişimi verilmediği için hiçbir kampanya başlatılmadı.",
"Tüm metinler Google Ads sınırlarına göre otomatik kontrol edildi (başlık ≤ 30, açıklama ≤ 90 karakter; parantez içinde karakter sayısı). Garantili kazanç, “en iyi”, sahte kıtlık veya ücretsiz hizmet vaadi yoktur.", "",
"**Öneri:** Daha önce reklamlarda mülk sahiplerine (portföy kazanımı) öncelik vermek istediğinizi belirtmiştiniz; bütçe sınırlıysa önce *Mülk satış ve kiralama* kampanyasıyla başlayın.", "",
"**Dönüşüm yapısı:** Ana dönüşüm = sunucunun doğruladığı talep (`generate_lead`). WhatsApp ve telefon tıklamaları yalnızca *ikincil* (gözlem) dönüşümdür. Ayrıntı: `docs/OLCUM-VE-ETIKETLER.md`.", ""]
for name, d in ads.items():
    out += [f"## {name}", "", f"Açılış sayfası: {d['lp']}", "", "### Başlıklar (15)", ""]
    for h in d["basliklar"]:
        assert len(h) <= 30, (h, len(h)); out.append(f"- {h} ({len(h)})")
    out += ["", "### Açıklamalar (4)", ""]
    for a in d["aciklamalar"]:
        assert len(a) <= 90, (a, len(a)); out.append(f"- {a} ({len(a)})")
    out += ["", "### Anahtar kelime temaları (öbek veya tam eşleme önerilir)", ""] + [f"- {t}" for t in d["temalar"]]
    out += ["", "### Bu kampanyaya özel negatif kelimeler", "", ", ".join(neg_ozel[name]), ""]
out += ["## Tüm kampanyalar için ortak negatif kelimeler", "", ", ".join(neg_ortak), "",
"## Kampanya ayarları için notlar", "",
"- Konum: İstanbul, “bu konumda bulunan veya düzenli olarak bulunan kişiler”. Daha önce belirlediğiniz bölge tercihlerini kampanya düzeyinde uygulayın.",
"- Yaş: daha önceki tercihinize göre 25 yaş ve üzeri.",
"- Uzantılar: arama uzantısı 0501 701 79 08; site bağlantıları: Hizmetler, Mülkümü Değerlendir, Bölgeye Göre Talep, İletişim.",
"- Teklif stratejisi: ilk 30–40 doğrulanmış talebe kadar “Dönüşümleri artır”; veri biriktikten sonra hedef talep başı maliyet değerlendirilebilir.",
"- Açılış sayfaları `noindex` durumdadır ve site haritasında yer almaz; organik aramada ana sayfalarla rekabet etmez.",
"- Otomatik etiketleme açık olsun (gclid). Reklam tıklama kimliği yalnızca ziyaretçi reklam çerezine izin verirse saklanır.", ""]
open("docs/REKLAM-TASLAKLARI.md", "w").write("\n".join(out))
print("docs/REKLAM-TASLAKLARI.md yazıldı")
