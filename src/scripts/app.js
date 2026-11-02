/**
 * Nova Gayrimenkul — istemci tarafı davranışlar
 *  - tercih seçimi (işlem / mülk türü / konum / bütçe) + kalıcılık
 *  - sayfaya göre WhatsApp mesajı, telefon / WhatsApp / yol tarifi ölçümü
 *  - formlar (sunucu kaydı veya açıkça belirtilen WhatsApp akışı)
 *  - çerez tercihleri + Consent Mode v2 + GTM yükleme
 *  - menü, başlık, mobil klavye uyumu, ölçülü kaydırma animasyonu
 *
 * Kişisel veriler (ad, telefon, mesaj, adres) hiçbir ölçüm olayına veya URL'ye eklenmez.
 */
import { ISLEMLER, MULK_TURLERI, BUTCELER, ISTANBUL_ILCELERI, KONULAR } from '../data/talep.mjs';

const CFG = (() => {
  try { return JSON.parse(document.getElementById('nova-config')?.textContent || '{}'); } catch { return {}; }
})();

const store = (area) => ({
  get(k) { try { return JSON.parse(area.getItem(k)); } catch { return null; } },
  set(k, v) { try { area.setItem(k, JSON.stringify(v)); } catch { /* depolama kapalı olabilir */ } },
  del(k) { try { area.removeItem(k); } catch { /* yok say */ } },
});
const LS = store(window.localStorage);
const SS = store(window.sessionStorage);

/* ------------------------------------------------------------------ ölçüm */
function track(event, params = {}) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event, page_path: location.pathname, ...params });
}

/* ------------------------------------------------------------------ toast */
let toastTimer;
function toast(msg, ms = 5200) {
  const el = document.getElementById('toast');
  if (!el) return;
  el.textContent = msg;
  el.classList.add('is-on');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('is-on'), ms);
}

/* ------------------------------------------------------------------ tercihler */
const PREF_KEY = 'nova.prefs.v1';
const byId = (list, id) => list.find((x) => x.id === id);
const islemOf = (id) => byId(ISLEMLER, id);
const turOf = (id) => byId(MULK_TURLERI, id);
const ilceOf = (id) => byId(ISTANBUL_ILCELERI, id);

function getPrefs() {
  const p = LS.get(PREF_KEY);
  return p && typeof p === 'object' ? p : null;
}
function setPrefs(p) {
  const clean = {
    islem: p.islem || '', tur: p.tur || '', il: p.il || '', ilce: p.il === 'istanbul' ? p.ilce || '' : '',
    ilText: p.il === 'diger' ? (p.ilText || '').slice(0, 60) : '', butce: p.butce || '', t: Date.now(),
  };
  LS.set(PREF_KEY, clean);
  document.dispatchEvent(new CustomEvent('nova:prefs', { detail: clean }));
  return clean;
}
function clearPrefs() {
  LS.del(PREF_KEY);
  document.dispatchEvent(new CustomEvent('nova:prefs', { detail: null }));
}
function hasPrefs(p) { return !!(p && (p.islem || p.tur || p.il)); }
function konumText(p) {
  if (!p) return '';
  if (p.il === 'istanbul') return p.ilce ? `${ilceOf(p.ilce)?.ad || ''}, İstanbul` : 'İstanbul';
  if (p.il === 'diger') return p.ilText || 'İstanbul dışı';
  return '';
}
function butceText(p) {
  if (!p?.butce) return '';
  const all = [...BUTCELER.alici, ...BUTCELER.kiraci];
  return byId(all, p.butce)?.label || '';
}
function prefLines(p) {
  if (!hasPrefs(p)) return [];
  const out = [];
  if (p.islem) out.push(['İşlem', islemOf(p.islem)?.label]);
  if (p.tur) out.push(['Mülk türü', turOf(p.tur)?.label]);
  const k = konumText(p);
  if (k) out.push(['Talep konumu', k]);
  const b = butceText(p);
  if (b) out.push(['Bütçe aralığı', b]);
  return out.filter((x) => x[1]);
}

/* ------------------------------------------------------------------ WhatsApp */
const pageTopic = () => document.body.dataset.waTopic || 'gayrimenkul danışmanlığı';
function waHref(text) { return `https://wa.me/${CFG.whatsappNumber}?text=${encodeURIComponent(text)}`; }
function waText(topic, p = getPrefs()) {
  let t = `Merhaba Nova Gayrimenkul, ${topic} hakkında görüşmek istiyorum.`;
  const lines = prefLines(p);
  if (lines.length) t += '\n' + lines.map(([k, v]) => `${k}: ${v}`).join('\n');
  return t;
}
function refreshWaLinks() {
  document.querySelectorAll('a[data-wa]').forEach((a) => {
    a.href = waHref(waText(a.dataset.waTopic || pageTopic()));
  });
}

/* ------------------------------------------------------------------ tıklama ölçümü */
document.addEventListener('click', (e) => {
  const a = e.target.closest('a[href]');
  if (!a) return;
  const loc = a.dataset.loc || 'content';
  const href = a.getAttribute('href') || '';
  if (href.startsWith('tel:')) {
    track('phone_click', { link_location: loc });
  } else if (a.hasAttribute('data-wa') || /^https:\/\/wa\.me\//.test(href)) {
    if (a.hasAttribute('data-wa')) a.href = waHref(waText(a.dataset.waTopic || pageTopic()));
    track('whatsapp_click', { link_location: loc });
    toast('WhatsApp açılıyor. Mesajınız, WhatsApp’ta “Gönder”e bastığınızda bize ulaşır.');
  } else if (a.hasAttribute('data-directions')) {
    track('directions_click', { link_location: loc });
  }
});

/* ------------------------------------------------------------------ konum alanları (il → ilçe bağımlılığı) */
function bindLocation(root, onChange) {
  const il = root.querySelector('select[name="il"]');
  const ilce = root.querySelector('select[name="ilce"]');
  const ilText = root.querySelector('input[name="ilText"]');
  if (!il || !ilce) return { set() {}, get: () => ({}) };
  const sync = (clear) => {
    const v = il.value;
    if (clear) { ilce.value = ''; if (ilText) ilText.value = ''; }
    ilce.disabled = v !== 'istanbul';
    ilce.hidden = v === 'diger';
    if (ilText) ilText.hidden = v !== 'diger';
    if (v === '') { ilce.hidden = false; }
  };
  il.addEventListener('change', () => { sync(true); onChange?.(); });
  ilce.addEventListener('change', () => onChange?.());
  ilText?.addEventListener('input', () => onChange?.());
  sync(false);
  return {
    set(p) {
      il.value = p?.il || '';
      sync(false);
      ilce.value = p?.il === 'istanbul' ? p.ilce || '' : '';
      if (ilText) ilText.value = p?.il === 'diger' ? p.ilText || '' : '';
    },
    get: () => ({ il: il.value, ilce: il.value === 'istanbul' ? ilce.value : '', ilText: il.value === 'diger' ? (ilText?.value || '').trim() : '' }),
  };
}

/* ------------------------------------------------------------------ tercih seçim formu */
function initPrefs(form) {
  const loc = bindLocation(form, update);
  const tur = form.querySelector('select[name="tur"]');
  const butce = form.querySelector('select[name="butce"]');
  const summary = form.querySelector('[data-prefs-summary]');
  const radios = [...form.querySelectorAll('input[name="islem"]')];

  function fillBudget(group, keep) {
    const prev = keep ? butce.value : '';
    butce.innerHTML = '';
    if (!group || group === 'sahip') {
      butce.append(new Option(group === 'sahip' ? 'Mülk sahipleri için gerekmez' : 'Önce işlemi seçin', ''));
      butce.disabled = true;
      return;
    }
    butce.append(new Option('Belirtmek istemiyorum', ''));
    BUTCELER[group].forEach((b) => butce.append(new Option(b.label, b.id)));
    butce.disabled = false;
    if (prev && BUTCELER[group].some((b) => b.id === prev)) butce.value = prev;
  }
  const current = () => ({ islem: radios.find((r) => r.checked)?.value || '', tur: tur.value, ...loc.get(), butce: butce.disabled ? '' : butce.value });
  function update() {
    const lines = prefLines(current());
    summary.textContent = lines.length ? 'Seçiminiz — ' + lines.map(([k, v]) => `${k}: ${v}`).join('; ') : '';
  }
  radios.forEach((r) => r.addEventListener('change', () => {
    const g = islemOf(r.value)?.grup;
    fillBudget(g, false); // üst seçim değişince bağlı bütçe seçimi temizlenir
    update();
  }));
  tur.addEventListener('change', update);
  butce.addEventListener('change', update);

  // geri dönüldüğünde seçimler kaybolmasın
  const saved = getPrefs();
  if (saved) {
    const r = radios.find((x) => x.value === saved.islem);
    if (r) r.checked = true;
    tur.value = saved.tur || '';
    loc.set(saved);
    fillBudget(islemOf(saved.islem)?.grup, false);
    if (saved.butce && !butce.disabled) butce.value = saved.butce;
  } else {
    fillBudget(null);
  }
  update();

  // bölge sayfasındaki ilçe düğmeleri
  form.setLocation = (ilceId) => {
    loc.set({ il: 'istanbul', ilce: ilceId });
    update();
  };

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const p = current();
    if (!p.islem) {
      summary.textContent = 'Devam etmek için önce işlem türünü seçin.';
      radios[0].focus();
      return;
    }
    const saved2 = setPrefs(p);
    track('preferences_set', {
      islem: saved2.islem, mulk_turu: saved2.tur || '(seçilmedi)',
      konum_ili: saved2.il || '(seçilmedi)', konum_ilcesi: saved2.ilce || '', butce_secildi: !!saved2.butce,
    });
    const sahip = islemOf(p.islem)?.grup === 'sahip';
    location.href = sahip ? '/mulkumu-degerlendir/#degerlendirme' : '/iletisim/#gorusme';
  });
}

/* ------------------------------------------------------------------ bölge düğmeleri */
function initRegionChips() {
  const chips = document.querySelectorAll('[data-ilce-chip]');
  if (!chips.length) return;
  const form = document.querySelector('form[data-prefs]');
  const mark = (id) => chips.forEach((c) => c.setAttribute('aria-pressed', String(c.dataset.ilceChip === id)));
  const saved = getPrefs();
  if (saved?.il === 'istanbul' && saved.ilce) mark(saved.ilce);
  chips.forEach((c) => c.addEventListener('click', () => {
    const id = c.dataset.ilceChip;
    mark(id);
    form?.setLocation?.(id);
    const p = getPrefs() || {};
    setPrefs({ ...p, il: 'istanbul', ilce: id });
    toast(`${c.textContent.trim()} talep konumu olarak seçildi. Seçiminiz formlara ve WhatsApp mesajına eklenir.`);
    form?.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
  }));
}

/* ------------------------------------------------------------------ kampanya kaynağı */
const UTM_KEY = 'nova.utm';
const CLICK_KEY = 'nova.clickid';
let pendingClick = null;
(function captureCampaign() {
  const q = new URLSearchParams(location.search);
  const utm = {};
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'].forEach((k) => { const v = q.get(k); if (v) utm[k] = v.slice(0, 100); });
  if (Object.keys(utm).length && !SS.get(UTM_KEY)) SS.set(UTM_KEY, { ...utm, landing: location.pathname });
  const click = {};
  ['gclid', 'gbraid', 'wbraid'].forEach((k) => { const v = q.get(k); if (v) click[k] = v.slice(0, 200); });
  if (Object.keys(click).length) pendingClick = click;
})();
function storeClickIfAllowed() {
  const c = LS.get('nova.consent.v1');
  if (c?.ads && pendingClick) { SS.set(CLICK_KEY, pendingClick); pendingClick = null; }
  if (c && !c.ads) { SS.del(CLICK_KEY); pendingClick = null; }
}

/* ------------------------------------------------------------------ formlar */
const normPhone = (raw) => {
  const s = String(raw || '').trim();
  const digits = s.replace(/\D/g, '');
  if (/^\+/.test(s) && !/^\+90/.test(s)) return digits.length >= 8 && digits.length <= 15 ? '+' + digits : null;
  let d = digits;
  if (d.startsWith('90') && d.length === 12) d = d.slice(2);
  if (d.startsWith('0') && d.length === 11) d = d.slice(1);
  return /^[2-5]\d{9}$/.test(d) ? '+90' + d : null;
};
const fmtPhone = (e164) => (e164?.startsWith('+90') ? `0${e164.slice(3, 6)} ${e164.slice(6, 9)} ${e164.slice(9, 11)} ${e164.slice(11)}` : e164 || '');

function mapKonuFromPrefs(p) {
  if (!p) return '';
  const fromTur = { villa: 'villa', daire: 'daire-rezidans', rezidans: 'daire-rezidans', 'plaza-ofis': 'plaza-ofis', 'home-ofis': 'home-ofis' }[p.tur];
  if (fromTur) return fromTur;
  return { 'satin-al': 'alim', kirala: 'kiralama', sat: 'satis', 'kiraya-ver': 'kiralama' }[p.islem] || '';
}

function initForm(form) {
  const type = form.dataset.form;
  const live = form.dataset.live === '1' && !!CFG.formEndpoint;
  const statusEl = form.querySelector('[data-status]');
  const submit = form.querySelector('[data-submit]');
  const chip = form.querySelector('[data-prefchip]');
  const chipText = form.querySelector('[data-prefchip-text]');
  const loc = form.querySelector('[data-locgroup]') ? bindLocation(form.querySelector('[data-locgroup]')) : null;
  const renderedAt = Date.now();
  let started = false;

  const q = new URLSearchParams(location.search);
  function applyPrefs() {
    const p = getPrefs();
    const lines = prefLines(p);
    if (chip) {
      chip.hidden = !lines.length;
      if (lines.length) chipText.innerHTML = lines.map(([k, v]) => `${k}: <strong>${escapeHtml(v)}</strong>`).join('; ');
    }
    if (type === 'gorusme') {
      const konu = form.querySelector('select[name="konu"]');
      const fromUrl = KONULAR.some((k) => k.id === q.get('konu')) ? q.get('konu') : '';
      if (konu && !konu.dataset.touched) konu.value = fromUrl || konu.dataset.default || mapKonuFromPrefs(p) || konu.value;
    } else {
      const tur = form.querySelector('select[name="tur"]');
      const urlTur = MULK_TURLERI.some((t) => t.id === q.get('tur')) ? q.get('tur') : '';
      if (tur && !tur.dataset.touched && (urlTur || p?.tur)) tur.value = urlTur || p.tur;
      if (p?.islem === 'kiraya-ver' || p?.islem === 'sat') {
        const r = form.querySelector(`input[name="amac"][value="${p.islem}"]`);
        if (r && !form.dataset.amacTouched) r.checked = true;
      }
      if (loc && p?.il && !form.dataset.locTouched) loc.set(p);
    }
  }
  applyPrefs();
  document.addEventListener('nova:prefs', applyPrefs);
  form.querySelectorAll('select').forEach((s) => s.addEventListener('change', () => { s.dataset.touched = '1'; }));
  form.querySelectorAll('input[name="amac"]').forEach((r) => r.addEventListener('change', () => { form.dataset.amacTouched = '1'; }));
  form.querySelector('[data-locgroup]')?.addEventListener('change', () => { form.dataset.locTouched = '1'; });
  form.querySelector('[data-prefs-clear]')?.addEventListener('click', () => { clearPrefs(); refreshWaLinks(); toast('Seçimleriniz temizlendi.'); });

  form.addEventListener('input', () => {
    if (!started) { started = true; track('form_start', { form_name: type }); }
  });

  const setError = (name, msg) => {
    const el = form.querySelector(`[data-error-for="${name}"]`);
    if (el) el.textContent = msg || '';
    const ctrl = name === 'konum' ? form.querySelector('select[name="il"]') : form.querySelector(`[name="${name}"]`);
    if (ctrl && ctrl.type !== 'radio') ctrl.setAttribute('aria-invalid', msg ? 'true' : 'false');
    return msg ? ctrl : null;
  };
  const showStatus = (kind, html) => {
    statusEl.className = `form-status form-status--${kind}`;
    statusEl.innerHTML = html;
    statusEl.hidden = false;
  };

  function validate() {
    const errs = [];
    const fd = new FormData(form);
    const ad = String(fd.get('adSoyad') || '').trim();
    errs.push(setError('adSoyad', ad.length < 3 ? 'Adınızı ve soyadınızı yazın.' : ''));
    const tel = normPhone(fd.get('telefon'));
    errs.push(setError('telefon', !tel ? 'Telefon numaranızı 05xx xxx xx xx biçiminde yazın.' : ''));
    if (type === 'gorusme') {
      errs.push(setError('konu', !fd.get('konu') ? 'İlgilendiğiniz konuyu seçin.' : ''));
    } else {
      errs.push(setError('amac', !fd.get('amac') ? 'Satış veya kiralama amacını seçin.' : ''));
      errs.push(setError('tur', !fd.get('tur') ? 'Mülk türünü seçin.' : ''));
      const m2 = Number(fd.get('metrekare'));
      errs.push(setError('metrekare', !(m2 >= 10 && m2 <= 100000) ? 'Yaklaşık metrekareyi rakamla yazın (örn. 180).' : ''));
      const l = loc?.get() || {};
      const okLoc = (l.il === 'istanbul' && l.ilce) || (l.il === 'diger' && l.ilText?.length >= 2);
      errs.push(setError('konum', !okLoc ? (l.il === 'istanbul' ? 'İlçeyi seçin.' : l.il === 'diger' ? 'İl ve ilçeyi yazın.' : 'Mülkün bulunduğu ili seçin.') : ''));
    }
    const first = errs.find(Boolean);
    return { ok: !first, first, tel };
  }

  function collect(tel) {
    const fd = new FormData(form);
    const p = getPrefs();
    const base = {
      form: type,
      adSoyad: String(fd.get('adSoyad') || '').trim(),
      telefon: tel,
      pazarlamaIzni: fd.get('pazarlamaIzni') === '1',
      website: String(fd.get('website') || ''),
      sayfa: location.pathname,
      sureMs: Date.now() - renderedAt,
      istekNo: '',
      kaynak: SS.get(UTM_KEY) || null,
      tiklamaKimligi: SS.get(CLICK_KEY) || null,
    };
    if (type === 'gorusme') {
      return {
        ...base,
        konu: String(fd.get('konu') || ''),
        mesaj: String(fd.get('mesaj') || '').trim(),
        kanal: String(fd.get('kanal') || 'telefon'),
        tercih: hasPrefs(p) ? { islem: p.islem, tur: p.tur, il: p.il, ilce: p.ilce, ilText: p.ilText, butce: p.butce } : null,
      };
    }
    const l = loc.get();
    return {
      ...base,
      amac: String(fd.get('amac') || ''),
      tur: String(fd.get('tur') || ''),
      il: l.il, ilce: l.ilce, ilText: l.ilText,
      metrekare: Number(fd.get('metrekare')),
      ekBilgi: String(fd.get('ekBilgi') || '').trim(),
    };
  }

  function waFormText(d) {
    const parts = [];
    if (type === 'gorusme') {
      const konu = KONULAR.find((k) => k.id === d.konu)?.label || '';
      parts.push(`Merhaba Nova Gayrimenkul, ${konu ? konu.toLocaleLowerCase('tr-TR') + ' konusunda' : ''} görüşmek istiyorum.`.replace('  ', ' '));
      parts.push(`Ad soyad: ${d.adSoyad}`);
      parts.push(`Geri dönüş numarası: ${fmtPhone(d.telefon)}`);
      parts.push(`Tercih edilen iletişim: ${d.kanal === 'whatsapp' ? 'WhatsApp' : 'Telefon'}`);
      prefLines(getPrefs()).forEach(([k, v]) => parts.push(`${k}: ${v}`));
      if (d.mesaj) parts.push(`Not: ${d.mesaj}`);
    } else {
      const tur = turOf(d.tur)?.label || '';
      const konum = d.il === 'istanbul' ? `${ilceOf(d.ilce)?.ad || ''}, İstanbul` : d.ilText;
      parts.push(`Merhaba Nova Gayrimenkul, mülkümü ${d.amac === 'kiraya-ver' ? 'kiraya vermek' : 'satmak'} için değerlendirme talep ediyorum.`);
      parts.push(`Ad soyad: ${d.adSoyad}`);
      parts.push(`Geri dönüş numarası: ${fmtPhone(d.telefon)}`);
      parts.push(`Mülk türü: ${tur}`);
      parts.push(`Konum: ${konum}`);
      parts.push(`Yaklaşık metrekare: ${d.metrekare}`);
      if (d.ekBilgi) parts.push(`Ek bilgi: ${d.ekBilgi}`);
    }
    return parts.join('\n');
  }

  const ERRORS = {
    invalid: 'Bazı bilgiler eksik veya hatalı görünüyor. Alanları kontrol edip tekrar deneyin.',
    rate_limited: 'Kısa sürede çok sayıda talep gönderildi. Lütfen birkaç dakika sonra tekrar deneyin ya da bizi arayın.',
    duplicate: 'Bu talebi az önce aldık; tekrar göndermenize gerek yok. Kısa süre içinde size dönüş yapacağız.',
    spam: 'Talebiniz otomatik güvenlik kontrolünden geçemedi. Lütfen bizi telefonla arayın.',
    server: 'Talebiniz şu anda kaydedilemedi. Lütfen tekrar deneyin ya da bizi telefonla arayın.',
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (form.dataset.busy === '1') return;
    statusEl.hidden = true;
    const v = validate();
    if (!v.ok) {
      track('form_submit_attempt', { form_name: type, valid: false, error_field: v.first?.name || '' });
      showStatus('error', 'Formu göndermek için işaretli alanları tamamlayın.');
      v.first?.focus?.();
      return;
    }
    track('form_submit_attempt', { form_name: type, valid: true });
    const data = collect(v.tel);
    // Aynı içerik yeniden gönderilirse (ör. zaman aşımından sonra) aynı istek numarası kullanılır;
    // sunucu ilk kayıt olduysa aynı talep numarasını döndürür, ikinci satır oluşmaz.
    const icerik = JSON.stringify({ ...data, sureMs: 0, istekNo: '', kaynak: null, tiklamaKimligi: null });
    if (form.dataset.sonIcerik !== icerik || !form.dataset.istekNo) {
      form.dataset.sonIcerik = icerik;
      form.dataset.istekNo = crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2);
    }
    data.istekNo = form.dataset.istekNo;

    if (!live) {
      // Yalnızca WhatsApp akışı: talep sunucuya kaydedilmez, bu nedenle başarı mesajı gösterilmez.
      const url = waHref(waFormText(data));
      // 'noopener' özelliği window.open'ın null dönmesine yol açar; bu yüzden opener'ı elle kesiyoruz
      const w = window.open(url, '_blank');
      if (w) { try { w.opener = null; } catch { /* yok say */ } } else { location.href = url; }
      // WhatsApp'ta hazırlanan mesaj "talep" sayılmaz; gönderim ziyaretçinin elindedir
      track('whatsapp_message_prepared', { form_name: type, method: 'whatsapp' });
      showStatus('info', `WhatsApp açıldı. Talebiniz, mesajı WhatsApp’ta gönderdiğinizde bize ulaşır. WhatsApp açılmadıysa <a href="${url}" target="_blank" rel="noopener">buraya dokunun</a> ya da <a href="${CFG.phoneHref}">bizi arayın</a>.`);
      return;
    }

    const fp = `${type}:${data.telefon}`;
    const done = SS.get('nova.sent') || {};
    if (done[fp] && Date.now() - done[fp] < 10 * 60 * 1000) {
      showStatus('ok', ERRORS.duplicate);
      return;
    }
    form.dataset.busy = '1';
    submit.setAttribute('aria-disabled', 'true');
    submit.disabled = true;
    const label = submit.textContent;
    submit.textContent = 'Gönderiliyor…';
    // Apps Script yanıt vermezse düğme sonsuza dek "Gönderiliyor…" kalmasın
    const ZAMAN_ASIMI_MS = 20000;
    const ac = 'AbortController' in window ? new AbortController() : null;
    const zamanlayici = ac ? setTimeout(() => ac.abort(), ZAMAN_ASIMI_MS) : 0;
    try {
      const res = await fetch(CFG.formEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify(data),
        redirect: 'follow',
        signal: ac ? ac.signal : undefined,
      });
      let json = null;
      try { json = await res.json(); } catch { json = null; }
      if (json && json.ok === true && json.id) {
        done[fp] = Date.now();
        SS.set('nova.sent', done);
        delete form.dataset.istekNo;
        delete form.dataset.sonIcerik;
        form.querySelectorAll('input:not([type=hidden]):not([type=radio]):not([type=checkbox]), textarea').forEach((i) => { i.value = ''; });
        showStatus('ok', `Talebiniz kaydedildi (talep no: <strong>${escapeHtml(json.id)}</strong>). ${data.kanal === 'whatsapp' ? 'WhatsApp üzerinden' : 'Telefonla'} size dönüş yapacağız.`);
        track('generate_lead', { form_name: type, lead_id: json.id });
        if (type === 'gorusme') track('appointment_request', { form_name: type, lead_id: json.id });
        statusEl.focus?.();
      } else {
        const code = json?.error && ERRORS[json.error] ? json.error : 'server';
        track('form_error', { form_name: type, error_type: code, http_status: res.status });
        showStatus(code === 'duplicate' ? 'ok' : 'error', `${ERRORS[code]} <a href="${CFG.phoneHref}">Hemen arayın</a>.`);
        if (code === 'invalid' && json?.fields) json.fields.forEach((f) => setError(f, 'Bu alanı kontrol edin.'));
      }
    } catch (err) {
      const zamanAsimi = err && err.name === 'AbortError';
      track('form_error', { form_name: type, error_type: zamanAsimi ? 'timeout' : (navigator.onLine === false ? 'offline' : 'network') });
      if (zamanAsimi) {
        showStatus('error', `Sunucudan zamanında yanıt alınamadı; talebinizin kaydedilip kaydedilmediğini doğrulayamadık. Tekrar gönderebilirsiniz — kaydedildiyse ikinci kez kaydedilmez ve aynı talep numarasını görürsünüz. Dilerseniz <a href="${CFG.phoneHref}">bizi arayın</a>.`);
      } else {
        showStatus('error', `Bağlantı kurulamadı ve talebiniz kaydedilmedi. İnternet bağlantınızı kontrol edip tekrar deneyin ya da <a href="${CFG.phoneHref}">bizi arayın</a>.`);
      }
    } finally {
      clearTimeout(zamanlayici);
      form.dataset.busy = '0';
      submit.disabled = false;
      submit.removeAttribute('aria-disabled');
      submit.textContent = label;
    }
  });
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

/* ------------------------------------------------------------------ çerez tercihleri */
const CKEY = 'nova.consent.v1';
/** İzin geri alındığında daha önce yazılmış Google çerezlerini siler (alan adı ve üst alan adı için). */
function deleteCookies(prefixes) {
  const host = location.hostname;
  const parts = host.split('.');
  const domains = ['', host, '.' + host];
  if (parts.length > 2) domains.push('.' + parts.slice(-2).join('.'));
  document.cookie.split(';').forEach((c) => {
    const name = c.split('=')[0].trim();
    if (!prefixes.some((p) => name.indexOf(p) === 0)) return;
    domains.forEach((d) => { document.cookie = `${name}=; Max-Age=0; path=/${d ? '; domain=' + d : ''}`; });
  });
}
function applyConsent(c, source) {
  const v = { analytics: !!c.analytics, ads: !!c.ads, v: 1, t: Date.now() };
  const prev = LS.get(CKEY);
  LS.set(CKEY, v);
  if (prev && prev.analytics && !v.analytics) deleteCookies(['_ga', '_gid']);
  if (prev && prev.ads && !v.ads) deleteCookies(['_gcl', '_gac', 'FPGCL']);
  window.gtag?.('consent', 'update', {
    analytics_storage: v.analytics ? 'granted' : 'denied',
    ad_storage: v.ads ? 'granted' : 'denied',
    ad_user_data: v.ads ? 'granted' : 'denied',
    ad_personalization: v.ads ? 'granted' : 'denied',
  });
  window.dataLayer.push({ event: 'consent_update', consent_analytics: v.analytics, consent_ads: v.ads, consent_source: source });
  if (v.analytics || v.ads) window.__novaLoadGTM?.();
  storeClickIfAllowed();
  document.getElementById('cc').hidden = true;
  document.body.classList.remove('cc-open');
}
function initConsent() {
  const banner = document.getElementById('cc');
  const dlg = document.getElementById('ccd');
  if (!banner || !dlg) return;
  const stored = LS.get(CKEY);
  // Analiz/reklam etiketi (GTM) kurulu değilse izin istenecek çerez yok → bant kendiliğinden açılmaz.
  // "Çerez tercihleri" bağlantısı her zaman çalışır.
  if (!stored && CFG.gtmId) { banner.hidden = false; document.body.classList.add('cc-open'); }
  storeClickIfAllowed();
  const openPrefs = () => {
    const c = LS.get(CKEY) || { analytics: false, ads: false };
    dlg.querySelector('[name="analytics"]').checked = !!c.analytics;
    dlg.querySelector('[name="ads"]').checked = !!c.ads;
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
  };
  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-cc], [data-cc-open]');
    if (!t) return;
    if (t.hasAttribute('data-cc-open')) { e.preventDefault(); openPrefs(); return; }
    const act = t.dataset.cc;
    if (act === 'accept') applyConsent({ analytics: true, ads: true }, 'banner');
    if (act === 'reject') applyConsent({ analytics: false, ads: false }, t.closest('dialog') ? 'dialog' : 'banner');
    if (act === 'save') applyConsent({ analytics: dlg.querySelector('[name="analytics"]').checked, ads: dlg.querySelector('[name="ads"]').checked }, 'dialog');
  });
}

/* ------------------------------------------------------------------ başlık ve menü */
function initHeader() {
  const header = document.getElementById('site-header');
  const toggle = header?.querySelector('.menu-toggle');
  const nav = document.getElementById('site-nav');
  if (!header) return;
  const onScroll = () => header.classList.toggle('is-solid', window.scrollY > 40);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  const closeSubs = (except) => header.querySelectorAll('.has-sub > button[aria-expanded="true"]').forEach((b) => {
    if (b !== except) { b.setAttribute('aria-expanded', 'false'); b.nextElementSibling.classList.remove('is-open'); }
  });
  header.querySelectorAll('.has-sub > button').forEach((b) => {
    b.addEventListener('click', () => {
      const open = b.getAttribute('aria-expanded') !== 'true';
      closeSubs(b);
      b.setAttribute('aria-expanded', String(open));
      b.nextElementSibling.classList.toggle('is-open', open);
    });
  });
  const setMenu = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Menüyü aç');
    nav.classList.toggle('is-open', open);
    header.classList.toggle('is-open', open);
    document.documentElement.style.overflow = open ? 'hidden' : '';
  };
  toggle?.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    closeSubs();
    if (toggle?.getAttribute('aria-expanded') === 'true') { setMenu(false); toggle.focus(); }
  });
  document.addEventListener('click', (e) => { if (!e.target.closest('.has-sub')) closeSubs(); });
  nav?.addEventListener('click', (e) => { if (e.target.closest('a') && toggle?.getAttribute('aria-expanded') === 'true') setMenu(false); });
  window.matchMedia('(min-width: 961px)').addEventListener('change', (m) => { if (m.matches) setMenu(false); });
}

/* ------------------------------------------------------------------ mobil klavye: alt çubuk alanları kapatmasın */
function initKeyboardGuard() {
  const isField = (el) => el && el.matches?.('input:not([type=checkbox]):not([type=radio]), textarea, select');
  document.addEventListener('focusin', (e) => { if (isField(e.target)) document.body.classList.add('kb-open'); });
  document.addEventListener('focusout', () => setTimeout(() => { if (!isField(document.activeElement)) document.body.classList.remove('kb-open'); }, 120));
}

/* ------------------------------------------------------------------ ölçülü kaydırma animasyonu */
function initReveal() {
  // Yalnızca masaüstünde (fare + geniş ekran) ve hareket azaltma kapalıysa. Telefon ve tabletlerde
  // içerik hiç gizlenmez; böylece hızlı kaydırmada veya uygulama içi tarayıcılarda boş alan kalmaz.
  const desktop = matchMedia('(hover: hover) and (pointer: fine) and (min-width: 861px)').matches;
  if (!desktop || matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  const els = [...document.querySelectorAll('.reveal')];
  const io = new IntersectionObserver((entries) => entries.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
  }), { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  els.forEach((el) => io.observe(el));
  document.documentElement.classList.add('reveal-on');
  // Güvenlik ağı: ekranda veya ekranın üstünde kalmış her öğe, gözlemci gecikse bile görünür olur.
  const sweep = () => els.forEach((el) => { if (!el.classList.contains('is-in') && el.getBoundingClientRect().top < innerHeight) { el.classList.add('is-in'); io.unobserve(el); } });
  let t = 0;
  window.addEventListener('scroll', () => { clearTimeout(t); t = setTimeout(sweep, 150); }, { passive: true });
  setTimeout(sweep, 1200);
}

/* ------------------------------------------------------------------ başlat */
// Her bölüm ayrı çalışır: birinde hata olursa diğerleri (menü, formlar, görünürlük) etkilenmez.
const safe = (fn) => { try { fn(); } catch (err) { if (window.console) console.error('[nova]', err); } };
safe(initReveal);
safe(initHeader);
safe(initConsent);
safe(initKeyboardGuard);
document.querySelectorAll('form[data-prefs]').forEach((f) => safe(() => initPrefs(f)));
document.querySelectorAll('form[data-form]').forEach((f) => safe(() => initForm(f)));
safe(initRegionChips);
safe(refreshWaLinks);
document.addEventListener('nova:prefs', () => safe(refreshWaLinks));
