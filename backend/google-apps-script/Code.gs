/**
 * NOVA GAYRİMENKUL — TALEP KAYIT SERVİSİ (Google Apps Script web uygulaması)
 * -------------------------------------------------------------------------
 * - Sitedeki formlardan gelen talepleri sunucu tarafında doğrular ve bu E-Tablo'ya kaydeder.
 * - Spam önleme (gizli alan + süre kontrolü), gönderim sınırı, tekrar gönderim engeli uygular.
 * - Yeni talepte e-posta bildirimi gönderir (isteğe bağlı).
 * - "Talepler" sayfası yönetim alanıdır: Durum (Yeni / Görüşüldü / Takip / Tamamlandı) ve Not sütunları.
 * - Erişim yalnızca bu E-Tablo'yu paylaştığınız Google hesaplarıyla sınırlıdır.
 *
 * Kurulum: KURULUM.md
 */

var AYAR = {
  SAYFA: 'Talepler',
  KAYIT_SAYFASI: 'Hata kayıtları',
  // Bildirim e-postası. Boş bırakılırsa betiği dağıtan hesabın e-postası kullanılır; '-' yazılırsa bildirim kapanır.
  BILDIRIM_EPOSTA: '',
  KISI_BASI_SINIR: 3,        // aynı telefondan 10 dakikada en fazla talep
  GENEL_SINIR: 40,           // tüm siteden 10 dakikada en fazla talep
  MIN_DOLDURMA_MS: 2500,     // formun bundan kısa sürede doldurulması bot işaretidir
  TEKRAR_PENCERESI_SN: 600,  // aynı telefon + form için tekrar gönderim engeli (saniye)
};

var DURUMLAR = ['Yeni', 'Görüşüldü', 'Takip', 'Tamamlandı'];
var BASLIKLAR = ['Talep no', 'Tarih', 'Form', 'Ad soyad', 'Telefon', 'Konu / amaç', 'Mülk türü', 'Konum', 'm²', 'Bütçe', 'İletişim tercihi', 'Mesaj / ek bilgi', 'Pazarlama izni', 'Kaynak sayfa', 'Kampanya', 'Reklam tıklama kimliği', 'Durum', 'Not'];

var KONULAR = { 'villa': 'Villa ve lüks konut', 'daire-rezidans': 'Daire ve rezidans', 'plaza-ofis': 'Plaza ve ofis', 'home-ofis': 'Home ofis', 'alim': 'Alım danışmanlığı', 'satis': 'Satış danışmanlığı', 'kiralama': 'Kiralama danışmanlığı', 'ticari': 'Ticari gayrimenkul danışmanlığı', 'diger': 'Diğer' };
var TURLER = { 'villa': 'Villa', 'daire': 'Daire', 'rezidans': 'Rezidans', 'plaza-ofis': 'Plaza ve Ofis', 'home-ofis': 'Home Ofis', 'diger': 'Diğer' };
var ISLEMLER = { 'satin-al': 'Satın almak', 'kirala': 'Kiralamak', 'sat': 'Satmak', 'kiraya-ver': 'Kiraya vermek' };
var BUTCELER = { b1: '15 milyon TL’ye kadar', b2: '15 – 30 milyon TL', b3: '30 – 60 milyon TL', b4: '60 milyon TL ve üzeri', k1: 'Aylık 75.000 TL’ye kadar', k2: 'Aylık 75.000 – 150.000 TL', k3: 'Aylık 150.000 – 300.000 TL', k4: 'Aylık 300.000 TL ve üzeri' };
var ILCELER = { 'adalar': 'Adalar', 'arnavutkoy': 'Arnavutköy', 'atasehir': 'Ataşehir', 'avcilar': 'Avcılar', 'bagcilar': 'Bağcılar', 'bahcelievler': 'Bahçelievler', 'bakirkoy': 'Bakırköy', 'basaksehir': 'Başakşehir', 'bayrampasa': 'Bayrampaşa', 'besiktas': 'Beşiktaş', 'beykoz': 'Beykoz', 'beylikduzu': 'Beylikdüzü', 'beyoglu': 'Beyoğlu', 'buyukcekmece': 'Büyükçekmece', 'catalca': 'Çatalca', 'cekmekoy': 'Çekmeköy', 'esenler': 'Esenler', 'esenyurt': 'Esenyurt', 'eyupsultan': 'Eyüpsultan', 'fatih': 'Fatih', 'gaziosmanpasa': 'Gaziosmanpaşa', 'gungoren': 'Güngören', 'kadikoy': 'Kadıköy', 'kagithane': 'Kağıthane', 'kartal': 'Kartal', 'kucukcekmece': 'Küçükçekmece', 'maltepe': 'Maltepe', 'pendik': 'Pendik', 'sancaktepe': 'Sancaktepe', 'sariyer': 'Sarıyer', 'silivri': 'Silivri', 'sultanbeyli': 'Sultanbeyli', 'sultangazi': 'Sultangazi', 'sile': 'Şile', 'sisli': 'Şişli', 'tuzla': 'Tuzla', 'umraniye': 'Ümraniye', 'uskudar': 'Üsküdar', 'zeytinburnu': 'Zeytinburnu' };

/* ---------------------------------------------------------------- giriş noktaları */

function doGet() {
  return yanit_({ ok: true, servis: 'nova-talep', zaman: new Date().toISOString() });
}

function doPost(e) {
  try {
    var ham = e && e.postData && e.postData.contents;
    if (!ham || ham.length > 20000) return yanit_({ ok: false, error: 'invalid' });
    var d;
    try { d = JSON.parse(ham); } catch (err) { return yanit_({ ok: false, error: 'invalid' }); }

    // 1) spam: gizli alan dolu ya da form insan için imkânsız hızda doldurulmuş
    if (d.website || (typeof d.sureMs === 'number' && d.sureMs < AYAR.MIN_DOLDURMA_MS)) {
      hataKaydet_('spam', { form: d.form, sureMs: d.sureMs });
      return yanit_({ ok: false, error: 'spam' });
    }

    // 2) doğrulama
    var v = dogrula_(d);
    if (!v.ok) return yanit_({ ok: false, error: 'invalid', fields: v.alanlar });
    var t = v.temiz;

    var onbellek = CacheService.getScriptCache();

    // Tekrar kontrolleri ile kayıt aynı kilit altında: eşzamanlı iki istek
    // (çift tıklama, ağ tekrarı) önbellekte birbirini göremeden iki satır açamaz.
    var kilit = LockService.getScriptLock();
    kilit.waitLock(15000);
    var no;
    try {
      // 3) aynı istek numarası tekrar geldiyse (ağ tekrarı) önceki talep numarasını döndür
      var oncekiNo = d.istekNo ? onbellek.get('istek:' + d.istekNo) : null;
      if (oncekiNo) return yanit_({ ok: true, id: oncekiNo, tekrar: true });

      // 4) aynı telefon + form için kısa sürede ikinci talep
      var tekrarAnahtar = 'tekrar:' + t.form + ':' + t.telefon;
      if (onbellek.get(tekrarAnahtar)) return yanit_({ ok: false, error: 'duplicate' });

      // 5) gönderim sınırları
      if (!sinirKontrol_(onbellek, 'kisi:' + t.telefon, AYAR.KISI_BASI_SINIR) || !sinirKontrol_(onbellek, 'genel', AYAR.GENEL_SINIR)) {
        hataKaydet_('rate_limited', { form: t.form });
        return yanit_({ ok: false, error: 'rate_limited' });
      }

      // 6) kayıt
      var sayfa = sayfaGetir_();
      no = talepNo_();
      sayfa.appendRow([
        no, new Date(), t.formEtiket, t.adSoyad, t.telefonGoster, t.konu, t.tur, t.konum, t.metrekare, t.butce,
        t.kanal, t.mesaj, t.pazarlamaIzni ? 'Evet' : 'Hayır', t.sayfa, t.kampanya, t.tiklama, 'Yeni', '',
      ]);
      SpreadsheetApp.flush();

      // kilit bırakılmadan önce işaretle ki bekleyen istek bu kaydı görsün
      onbellek.put(tekrarAnahtar, '1', AYAR.TEKRAR_PENCERESI_SN);
      if (d.istekNo) onbellek.put('istek:' + d.istekNo, no, 21600);
    } finally {
      kilit.releaseLock();
    }

    bildir_(no, t);
    return yanit_({ ok: true, id: no });
  } catch (err) {
    hataKaydet_('server', { mesaj: String(err && err.message || err) });
    return yanit_({ ok: false, error: 'server' });
  }
}

/* ---------------------------------------------------------------- doğrulama */

function dogrula_(d) {
  var alanlar = [];
  var form = d.form === 'gorusme' || d.form === 'degerlendirme' ? d.form : null;
  if (!form) return { ok: false, alanlar: ['form'] };

  var ad = metin_(d.adSoyad, 80);
  if (ad.length < 3) alanlar.push('adSoyad');
  var tel = telefonNormalle_(d.telefon);
  if (!tel) alanlar.push('telefon');

  var t = {
    form: form,
    formEtiket: form === 'gorusme' ? 'Görüşme' : 'Mülk değerlendirme',
    adSoyad: ad,
    telefon: tel,
    telefonGoster: tel ? telefonGoster_(tel) : '',
    pazarlamaIzni: d.pazarlamaIzni === true,
    sayfa: metin_(d.sayfa, 120),
    kampanya: d.kaynak ? metin_(Object.keys(d.kaynak).map(function (k) { return k + '=' + d.kaynak[k]; }).join('; '), 400) : '',
    tiklama: d.tiklamaKimligi ? metin_(Object.keys(d.tiklamaKimligi).map(function (k) { return k + '=' + d.tiklamaKimligi[k]; }).join('; '), 400) : '',
    konu: '', tur: '', konum: '', metrekare: '', butce: '', kanal: '', mesaj: '',
  };

  if (form === 'gorusme') {
    if (!KONULAR[d.konu]) alanlar.push('konu');
    t.konu = KONULAR[d.konu] || '';
    t.kanal = d.kanal === 'whatsapp' ? 'WhatsApp' : 'Telefon';
    t.mesaj = metin_(d.mesaj, 1200);
    var p = d.tercih || {};
    var parcalar = [];
    if (ISLEMLER[p.islem]) parcalar.push('İşlem: ' + ISLEMLER[p.islem]);
    t.tur = TURLER[p.tur] || '';
    t.konum = konum_(p.il, p.ilce, p.ilText);
    t.butce = BUTCELER[p.butce] || '';
    if (parcalar.length) t.konu = t.konu + ' (' + parcalar.join(', ') + ')';
  } else {
    if (d.amac !== 'sat' && d.amac !== 'kiraya-ver') alanlar.push('amac');
    t.konu = d.amac === 'kiraya-ver' ? 'Kiraya vermek' : 'Satmak';
    if (!TURLER[d.tur]) alanlar.push('tur');
    t.tur = TURLER[d.tur] || '';
    var m2 = Number(d.metrekare);
    if (!(m2 >= 10 && m2 <= 100000)) alanlar.push('metrekare');
    t.metrekare = m2 >= 10 ? Math.round(m2) : '';
    t.konum = konum_(d.il, d.ilce, d.ilText);
    if (!t.konum || (d.il === 'istanbul' && !ILCELER[d.ilce])) alanlar.push('konum');
    t.mesaj = metin_(d.ekBilgi, 1200);
  }
  return alanlar.length ? { ok: false, alanlar: alanlar } : { ok: true, temiz: t };
}

function konum_(il, ilce, ilText) {
  if (il === 'istanbul') return ILCELER[ilce] ? ILCELER[ilce] + ', İstanbul' : 'İstanbul';
  if (il === 'diger') return metin_(ilText, 60);
  return '';
}

function metin_(v, max) {
  // E-Tablo formül enjeksiyonunu önle (=, +, -, @ ile başlayan değerler)
  var s = String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function telefonNormalle_(raw) {
  var s = String(raw || '').trim();
  var r = s.replace(/\D/g, '');
  if (/^\+/.test(s) && !/^\+90/.test(s)) return r.length >= 8 && r.length <= 15 ? '+' + r : null;
  if (r.indexOf('90') === 0 && r.length === 12) r = r.slice(2);
  if (r.indexOf('0') === 0 && r.length === 11) r = r.slice(1);
  return /^[2-5]\d{9}$/.test(r) ? '+90' + r : null;
}

function telefonGoster_(e164) {
  if (e164.indexOf('+90') !== 0) return e164;
  var d = e164.slice(3);
  return '0' + d.slice(0, 3) + ' ' + d.slice(3, 6) + ' ' + d.slice(6, 8) + ' ' + d.slice(8);
}

/* ---------------------------------------------------------------- yardımcılar */

function sinirKontrol_(onbellek, anahtar, sinir) {
  var k = 'sinir:' + anahtar;
  var n = Number(onbellek.get(k) || 0);
  if (n >= sinir) return false;
  onbellek.put(k, String(n + 1), 600);
  return true;
}

function talepNo_() {
  var tz = Session.getScriptTimeZone() || 'Europe/Istanbul';
  var gun = Utilities.formatDate(new Date(), tz, 'yyMMdd');
  var rastgele = Math.floor(Math.random() * 1679616).toString(36).toUpperCase();
  while (rastgele.length < 4) rastgele = '0' + rastgele;
  return 'NV-' + gun + '-' + rastgele;
}

function sayfaGetir_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sayfa = ss.getSheetByName(AYAR.SAYFA);
  if (!sayfa) { kurulum(); sayfa = ss.getSheetByName(AYAR.SAYFA); }
  return sayfa;
}

function bildir_(no, t) {
  try {
    var alici = AYAR.BILDIRIM_EPOSTA === '-' ? '' : (AYAR.BILDIRIM_EPOSTA || Session.getEffectiveUser().getEmail());
    if (!alici) return;
    var satirlar = [
      'Yeni talep: ' + no,
      'Form: ' + t.formEtiket,
      'Ad soyad: ' + t.adSoyad,
      'Telefon: ' + t.telefonGoster,
      'Konu / amaç: ' + t.konu,
      t.tur ? 'Mülk türü: ' + t.tur : '',
      t.konum ? 'Konum: ' + t.konum : '',
      t.metrekare ? 'm²: ' + t.metrekare : '',
      t.butce ? 'Bütçe: ' + t.butce : '',
      t.kanal ? 'İletişim tercihi: ' + t.kanal : '',
      t.mesaj ? 'Mesaj: ' + t.mesaj : '',
      '',
      'Tüm talepler: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl(),
    ].filter(function (x) { return x !== ''; });
    MailApp.sendEmail({ to: alici, subject: 'Nova Gayrimenkul — yeni ' + t.formEtiket.toLowerCase() + ' talebi (' + no + ')', body: satirlar.join('\n') });
  } catch (err) {
    hataKaydet_('bildirim', { mesaj: String(err && err.message || err) });
  }
}

function hataKaydet_(tur, ayrinti) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var s = ss.getSheetByName(AYAR.KAYIT_SAYFASI) || ss.insertSheet(AYAR.KAYIT_SAYFASI);
    if (s.getLastRow() === 0) s.appendRow(['Tarih', 'Tür', 'Ayrıntı']);
    s.appendRow([new Date(), tur, JSON.stringify(ayrinti || {}).slice(0, 500)]);
  } catch (err) { /* kayıt da başarısızsa sessiz geç */ }
}

function yanit_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

/* ---------------------------------------------------------------- kurulum ve bakım (elle çalıştırılır) */

/** İlk kurulumda bir kez çalıştırın: sayfaları, başlıkları, durum seçeneklerini ve görünümü hazırlar. */
function kurulum() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var s = ss.getSheetByName(AYAR.SAYFA) || ss.insertSheet(AYAR.SAYFA, 0);
  if (s.getLastRow() === 0) s.appendRow(BASLIKLAR);
  s.setFrozenRows(1);
  s.getRange(1, 1, 1, BASLIKLAR.length).setFontWeight('bold').setBackground('#101114').setFontColor('#F5F1E8');
  var durumSutun = BASLIKLAR.indexOf('Durum') + 1;
  var kural = SpreadsheetApp.newDataValidation().requireValueInList(DURUMLAR, true).setAllowInvalid(false).build();
  s.getRange(2, durumSutun, 5000, 1).setDataValidation(kural);
  var renkler = { 'Yeni': '#F6E7C8', 'Görüşüldü': '#DDE8F3', 'Takip': '#F3E0D8', 'Tamamlandı': '#DCEBDD' };
  var kurallar = DURUMLAR.map(function (d) {
    return SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo(d).setBackground(renkler[d]).setRanges([s.getRange(2, durumSutun, 5000, 1)]).build();
  });
  s.setConditionalFormatRules(kurallar);
  s.setColumnWidths(1, BASLIKLAR.length, 140);
  s.setColumnWidth(BASLIKLAR.indexOf('Mesaj / ek bilgi') + 1, 320);
  s.setColumnWidth(BASLIKLAR.indexOf('Not') + 1, 280);
  s.getRange(2, 2, 5000, 1).setNumberFormat('dd.mm.yyyy hh:mm');
  if (!ss.getSheetByName(AYAR.KAYIT_SAYFASI)) ss.insertSheet(AYAR.KAYIT_SAYFASI).appendRow(['Tarih', 'Tür', 'Ayrıntı']);
  var varsayilan = ss.getSheetByName('Sayfa1') || ss.getSheetByName('Sheet1');
  if (varsayilan && varsayilan.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(varsayilan);
}

/** Yedek: E-Tablo'nun tarihli bir kopyasını Drive'daki "Nova Talep Yedekleri" klasörüne alır. Haftalık tetikleyiciye bağlanabilir. */
function yedekAl() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var klasorler = DriveApp.getFoldersByName('Nova Talep Yedekleri');
  var klasor = klasorler.hasNext() ? klasorler.next() : DriveApp.createFolder('Nova Talep Yedekleri');
  var ad = 'Nova Talepler yedek ' + Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'Europe/Istanbul', 'yyyy-MM-dd');
  DriveApp.getFileById(ss.getId()).makeCopy(ad, klasor);
}

/** Haftalık yedek tetikleyicisini bir kez kurar (pazartesi 07:00). */
function haftalikYedekKur() {
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === 'yedekAl') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('yedekAl').timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(7).create();
}
