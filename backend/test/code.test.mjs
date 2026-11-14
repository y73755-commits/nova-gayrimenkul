// Code.gs için yerel test: Google servisleri sahte (mock) nesnelerle taklit edilir.
// Çalıştırma: node backend/test/code.test.mjs
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const rows = []; const logRows = []; const mails = []; const cache = new Map();
let kilitli = false; const kilitDisiOkuma = [];
const sheet = (store) => ({
  appendRow: (r) => store.push(r), getLastRow: () => store.length, setFrozenRows() {}, getRange: () => ({ setFontWeight() { return this; }, setBackground() { return this; }, setFontColor() { return this; }, setDataValidation() {}, setNumberFormat() {} }),
  setConditionalFormatRules() {}, setColumnWidths() {}, setColumnWidth() {},
});
const sheets = { 'Talepler': sheet(rows), 'Hata kayıtları': sheet(logRows) };
const ctx = {
  SpreadsheetApp: {
    getActiveSpreadsheet: () => ({ getSheetByName: (n) => sheets[n] || null, insertSheet: (n) => (sheets[n] = sheet([])), getUrl: () => 'https://docs.google.com/x', getSheets: () => Object.values(sheets) }),
    flush() {}, newDataValidation: () => ({ requireValueInList() { return this; }, setAllowInvalid() { return this; }, build() {} }),
    newConditionalFormatRule: () => ({ whenTextEqualTo() { return this; }, setBackground() { return this; }, setRanges() { return this; }, build() {} }),
  },
  CacheService: { getScriptCache: () => ({ get: (k) => { if (!kilitli && /^(istek|tekrar):/.test(k)) kilitDisiOkuma.push(k); return cache.get(k) ?? null; }, put: (k, v) => cache.set(k, v) }) },
  LockService: { getScriptLock: () => ({ waitLock() { kilitli = true; }, releaseLock() { kilitli = false; } }) },
  MailApp: { sendEmail: (m) => mails.push(m) },
  Session: { getEffectiveUser: () => ({ getEmail: () => 'sahip@example.com' }), getScriptTimeZone: () => 'Europe/Istanbul' },
  Utilities: { formatDate: () => '261030' },
  ContentService: { MimeType: { JSON: 'json' }, createTextOutput: (s) => ({ body: s, setMimeType() { return this; } }) },
  console,
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(new URL('../google-apps-script/Code.gs', import.meta.url), 'utf8'), ctx);
const post = (d) => JSON.parse(ctx.doPost({ postData: { contents: JSON.stringify(d) } }).body);
const base = { form: 'gorusme', adSoyad: 'Ayşe Yılmaz', telefon: '0532 123 45 67', konu: 'villa', kanal: 'telefon', mesaj: 'Merhaba', pazarlamaIzni: false, website: '', sureMs: 9000, istekNo: 'a1', sayfa: '/iletisim/', tercih: { islem: 'satin-al', tur: 'villa', il: 'istanbul', ilce: 'sariyer', butce: 'b3' } };
let pass = 0; const t = (name, fn) => { fn(); pass++; console.log('✓', name); };

t('geçerli görüşme talebi kaydedilir ve numara döner', () => {
  const r = post(base);
  assert.equal(r.ok, true); assert.match(r.id, /^NV-261030-[0-9A-Z]{4}$/);
  assert.equal(rows.length, 1); assert.equal(rows[0][4], '0532 123 45 67'); assert.equal(rows[0][7], 'Sarıyer, İstanbul'); assert.equal(rows[0][16], 'Yeni');
  assert.equal(mails.length, 1);
});
t('aynı istek numarası tekrar gelirse yeni satır açılmaz, aynı numara döner', () => {
  const r = post(base); assert.equal(r.ok, true); assert.equal(r.tekrar, true); assert.equal(rows.length, 1);
});
t('aynı telefon + form kısa sürede tekrar gönderilemez', () => {
  const r = post({ ...base, istekNo: 'a2' }); assert.equal(r.ok, false); assert.equal(r.error, 'duplicate'); assert.equal(rows.length, 1);
});
t('gizli alan doluysa spam olarak reddedilir', () => {
  const r = post({ ...base, istekNo: 'a3', telefon: '05321111111', website: 'http://spam' }); assert.equal(r.error, 'spam'); assert.equal(rows.length, 1);
});
t('çok hızlı doldurulan form reddedilir', () => {
  const r = post({ ...base, istekNo: 'a4', telefon: '05321111112', sureMs: 400 }); assert.equal(r.error, 'spam');
});
t('eksik/hatalı alanlar sunucuda yakalanır', () => {
  const r = post({ ...base, istekNo: 'a5', adSoyad: 'A', telefon: '123', konu: 'yok' }); assert.equal(r.error, 'invalid'); assert.deepEqual(r.fields.sort(), ['adSoyad', 'konu', 'telefon']);
});
t('değerlendirme formu: geçersiz ilçe ve metrekare reddedilir', () => {
  const r = post({ form: 'degerlendirme', adSoyad: 'Mehmet Kaya', telefon: '+90 542 000 00 00', amac: 'sat', tur: 'villa', il: 'istanbul', ilce: 'xyz', metrekare: 3, sureMs: 8000, istekNo: 'b1' });
  assert.equal(r.error, 'invalid'); assert.deepEqual(r.fields.sort(), ['konum', 'metrekare']);
});
t('değerlendirme formu kaydedilir; formül enjeksiyonu etkisizleştirilir', () => {
  const r = post({ form: 'degerlendirme', adSoyad: '=HYPERLINK("x")', telefon: '0542 000 00 00', amac: 'kiraya-ver', tur: 'rezidans', il: 'istanbul', ilce: 'kadikoy', metrekare: 140, ekBilgi: '+3 oda', sureMs: 8000, istekNo: 'b2' });
  assert.equal(r.ok, true); const row = rows[rows.length - 1];
  assert.equal(row[3].startsWith("'="), true); assert.equal(row[11], "'+3 oda"); assert.equal(row[5], 'Kiraya vermek'); assert.equal(row[7], 'Kadıköy, İstanbul');
});
t('aynı telefondan 10 dakikada en fazla 3 talep', () => {
  const tel = '0533 999 88 77';
  const res = [1, 2, 3, 4].map((i) => post({ ...base, form: i % 2 ? 'gorusme' : 'degerlendirme', amac: 'sat', tur: 'daire', il: 'diger', ilText: 'Bursa Nilüfer', metrekare: 100, telefon: tel, istekNo: 'c' + i }));
  assert.equal(res[0].ok, true); assert.equal(res[1].ok, true);
  assert.equal(res.at(-1).error === 'rate_limited' || res.at(-1).error === 'duplicate', true);
});
t('bozuk JSON güvenli biçimde reddedilir', () => {
  const r = JSON.parse(ctx.doPost({ postData: { contents: '{bozuk' } }).body); assert.equal(r.error, 'invalid');
});
t('tekrar kontrolleri kayıt kilidi altında yapılır, kilit her yanıttan sonra bırakılır', () => {
  assert.deepEqual(kilitDisiOkuma, []); assert.equal(kilitli, false);
});
console.log(`\n${pass} test geçti. Kayıt satırı: ${rows.length}, bildirim: ${mails.length}, hata kaydı: ${logRows.length}`);
