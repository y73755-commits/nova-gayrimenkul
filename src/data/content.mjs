/** Site metinlerinin tekrar kullanılan bölümleri. Metinler buradan düzenlenebilir. */

export const NAV = [
  {
    label: 'Hizmetler',
    href: '/hizmetler/',
    children: [
      { label: 'Tüm hizmetler', href: '/hizmetler/' },
      { label: 'Yaşam alanları', href: '/yasam-alanlari/' },
      { label: 'Mülkümü değerlendir', href: '/mulkumu-degerlendir/' },
    ],
  },
  { label: 'Bölgeye göre talep', href: '/bolgeye-gore-talep/' },
  {
    label: 'Kurumsal',
    href: '/hakkimizda/',
    children: [
      { label: 'Hakkımızda', href: '/hakkimizda/' },
      { label: 'Yusuf Sezmiş', href: '/yusuf-sezmis/' },
      { label: 'Bilgi merkezi', href: '/bilgi-merkezi/' },
    ],
  },
  { label: 'İletişim', href: '/iletisim/' },
];

/** Yaşam alanı kategorileri — gerçek ilan değil, danışmanlık alanı anlatımı. */
export const ALANLAR = [
  {
    id: 'villa',
    tur: 'villa',
    baslik: 'Villa',
    kisa: 'Mahremiyet, bahçe ve manzara dengesinin önemli olduğu müstakil yaşam.',
    uzun: 'Villa seçiminde konumun sessizliği kadar ulaşım süresi, arazinin eğimi, bahçe ve havuzun bakım yükü ve komşu yapılarla mesafe de kararı belirler. Görüşmede yaşam düzeninizi dinler, bu ölçütlere göre değerlendirmeye uygun seçenekleri birlikte ele alırız.',
    maddeler: ['Konum, erişim ve mahremiyet', 'Bahçe, havuz ve teknik bakım yükü', 'Yapı ve belge durumunun kontrolü'],
    gorsel: 'villa-havuz',
    alt: 'Gün batımında sonsuzluk havuzu ve denize bakan modern villa konsepti',
    waKonu: 'villa danışmanlığı',
  },
  {
    id: 'daire-rezidans',
    tur: 'rezidans',
    baslik: 'Daire ve Rezidans',
    kisa: 'Şehir merkezine yakın, hizmetleri ve manzarasıyla öne çıkan konutlar.',
    uzun: 'Rezidans ve dairelerde kat, cephe, manzara sürekliliği, aidat ve ortak alan hizmetleri günlük yaşamın kalitesini doğrudan etkiler. Kısa listeyi bu ayrıntılar üzerinden kurar, karşılaştırmayı birlikte yaparız.',
    maddeler: ['Kat, cephe ve manzara', 'Aidat ve site hizmetleri', 'Ulaşım ve günlük ihtiyaçlar'],
    gorsel: 'penthouse-salon',
    alt: 'Akşam şehir manzarasına açılan geniş camlı penthouse salonu konsepti',
    waKonu: 'daire ve rezidans danışmanlığı',
  },
  {
    id: 'plaza-ofis',
    tur: 'plaza-ofis',
    baslik: 'Plaza ve Ofis',
    kisa: 'Ekibin büyüklüğüne, çalışma biçimine ve ulaşım ihtiyaçlarına uygun iş alanları.',
    uzun: 'Ofis seçimi metrekareden önce kullanım planıyla başlar: ekip büyüklüğü, toplantı ihtiyacı, ziyaretçi akışı, otopark ve bina hizmetleri. İhtiyacınızı netleştirir, değerlendirmeyi bu çerçevede sürdürürüz.',
    maddeler: ['Kullanım planı ve verimli metrekare', 'Bina hizmetleri ve otopark', 'Kira süresi ve sözleşme koşulları'],
    gorsel: 'plaza-aksam',
    alt: 'Akşam ışığında aydınlık katlarıyla çağdaş plaza cephesi konsepti',
    waKonu: 'plaza ve ofis danışmanlığı',
  },
  {
    id: 'home-ofis',
    tur: 'home-ofis',
    baslik: 'Home Ofis',
    kisa: 'Evde çalışmayı kolaylaştıran, ışığı ve sessizliği düşünülmüş alanlar.',
    uzun: 'Evden çalışanlar için ayrı bir çalışma odası, gün ışığı, ses yalıtımı ve internet altyapısı en az oda sayısı kadar önemlidir. Bu ihtiyaçları baştan konuşur, seçenekleri bu gözle değerlendiririz.',
    maddeler: ['Ayrı çalışma alanı ve gün ışığı', 'Ses yalıtımı ve altyapı', 'Konut ve ofis kullanımının dengesi'],
    gorsel: 'home-ofis',
    alt: 'Su ve tepelere bakan geniş pencereli home ofis konsepti',
    waKonu: 'home ofis danışmanlığı',
  },
];

export const HIZMETLER = [
  {
    id: 'alim',
    baslik: 'Alım danışmanlığı',
    ozet: 'İhtiyacınızı netleştirir, uygun seçenekleri birlikte değerlendirir, görüşme ve evrak sürecinde yanınızda oluruz.',
    maddeler: ['İhtiyaç ve bütçe çerçevesinin belirlenmesi', 'Seçeneklerin karşılaştırmalı değerlendirilmesi', 'Yerinde görme ve süreç takibi'],
    konu: 'alim',
  },
  {
    id: 'satis',
    baslik: 'Satış danışmanlığı',
    ozet: 'Mülkünüzü doğru konumlandırmak için fiyat stratejisi, hazırlık ve tanıtım planını birlikte kurarız.',
    maddeler: ['Mülk değerlendirmesi ve fiyat stratejisi', 'Satışa hazırlık önerileri', 'Alıcı görüşmelerinin yönetimi'],
    konu: 'satis',
  },
  {
    id: 'kiralama',
    baslik: 'Kiralama danışmanlığı',
    ozet: 'Kiraya verirken veya kiralarken beklentileri, koşulları ve süreci açık biçimde yönetiriz.',
    maddeler: ['Kira beklentisinin piyasa ile karşılaştırılması', 'Kiracı veya mülk seçeneklerinin ön değerlendirmesi', 'Sözleşme öncesi kontrol listesi'],
    konu: 'kiralama',
  },
  {
    id: 'ticari',
    baslik: 'Ticari gayrimenkul danışmanlığı',
    ozet: 'Plaza, ofis ve iş alanı ihtiyaçlarında kullanım planından sözleşme aşamasına kadar destek veririz.',
    maddeler: ['Kullanım ve kapasite analizi', 'Bina ve lokasyon karşılaştırması', 'Kira ve devir koşullarının değerlendirilmesi'],
    konu: 'ticari',
  },
  {
    id: 'pazarlama',
    baslik: 'Mülkün pazarlama süreci',
    ozet: 'Mülkünüzün doğru kitleye doğru anlatımla ulaşması için sunum, yayın ve geri bildirim akışını planlarız.',
    maddeler: ['Fotoğraf ve sunum hazırlığı', 'Yetkilendirme ve yayın süreci', 'Düzenli geri bildirim ve raporlama'],
    konu: 'satis',
  },
];

export const SUREC = [
  { baslik: 'İhtiyacı anlama', metin: 'İlk görüşmede amacınızı, zamanlamanızı, konum ve bütçe çerçevenizi dinleriz.' },
  { baslik: 'Değerlendirme', metin: 'Mülkü veya ihtiyacı yerinde ve belgeler üzerinden değerlendirir, öncelikleri netleştiririz.' },
  { baslik: 'Strateji ve seçenekler', metin: 'Satış, kiralama ya da alım için izlenecek yolu ve uygun seçenekleri birlikte belirleriz.' },
  { baslik: 'Görüşme ve süreç takibi', metin: 'Görüşmeleri planlar, gelişmeleri düzenli paylaşır, süreci sonuçlanana kadar takip ederiz.' },
];

export const SSS = [
  {
    s: 'Hangi konularda danışmanlık veriyorsunuz?',
    c: 'Villa, daire, rezidans, plaza, ofis ve home ofis konularında alım, satış ve kiralama danışmanlığı veriyoruz. Mülkünü satmak veya kiraya vermek isteyen sahiplerle değerlendirme ve pazarlama sürecini birlikte yürütüyoruz.',
  },
  {
    s: 'İlk görüşme nasıl ilerliyor?',
    c: 'Formu doldurduğunuzda, aradığınızda veya WhatsApp’tan yazdığınızda size dönüş yaparız. İlk görüşmede amacınızı, zamanlamanızı ve önceliklerinizi konuşur; sonraki adımı birlikte belirleriz.',
  },
  {
    s: 'Mülk değerlendirmesi için neler gerekiyor?',
    c: 'Başlangıçta mülkün türü, konumu, yaklaşık metrekaresi ve amacınız (satış veya kiralama) yeterlidir. İlk aşamada tapu veya kimlik belgesi istemiyoruz; belgeler süreç ilerledikçe ve gerektiği ölçüde konuşulur.',
  },
  {
    s: 'Mülkümü satışa veya kiralamaya nasıl hazırlamalıyım?',
    c: 'Belgelerin güncel olması, küçük onarımların tamamlanması, mekânın sade ve aydınlık sunulması ve gerçekçi bir fiyat beklentisi en önemli adımlardır. Bilgi merkezimizdeki hazırlık rehberinde ayrıntıları bulabilirsiniz.',
  },
  {
    s: 'Size hangi kanallardan ulaşabilirim?',
    c: 'Telefonla arayabilir, WhatsApp’tan yazabilir veya sitedeki formları kullanabilirsiniz. Ofisimiz Reşitpaşa, Eski Büyükdere Cd. No:2, Sarıyer/İstanbul adresindedir; görüşme için önceden randevu almanızı öneririz.',
  },
  {
    s: 'Sitede ilanlarınız neden yok?',
    c: 'Bu site, danışmanlık talebinizi doğrudan bize iletmeniz için hazırlandı. Size uygun seçenekleri, ihtiyacınızı dinledikten sonra güncel durumlarıyla birlikte paylaşıyoruz.',
  },
];
