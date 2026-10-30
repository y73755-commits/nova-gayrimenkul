# Özgün mimari konsept görselleri — üretim betikleri

Sitedeki tüm mimari görseller bu klasördeki Python betikleriyle **Blender (Cycles)** içinde sıfırdan modellenip render edilmiştir.
Dışarıdan fotoğraf, doku, 3B model veya başka bir sitenin görseli kullanılmamıştır; geometri, malzeme ve ışık tamamen koddan üretilir.

| Betik | Görsel |
|---|---|
| `villa.py -- desktop / mobile / pool` | Gün batımında havuzlu modern villa (ana görsel masaüstü + mobil kırpım, havuz açısı) |
| `garden.py` | Bahçeli, geniş cam cepheli müstakil konut |
| `penthouse.py` | Şehir manzaralı penthouse salonu |
| `residence.py` | Gün ışığı alan zarif rezidans iç mekânı |
| `plaza.py` | Akşam ışığında çağdaş plaza cephesi |
| `lobby.py` | Premium ofis lobisi |
| `homeoffice.py` | Manzaralı home ofis |
| `detail.py` | Mermer, oluklu meşe ve sıcak ışık — malzeme detayı |

Çalıştırma: `pip install bpy` → `python3 villa.py -- desktop` (çıktı: `out/`). Sonra `python3 tools/import_renders.py` görselleri siteye aktarır.

Görseller gerçek bir mülkü veya adresi temsil etmez; sitede “Görseller mimari konsept ve yaşam alanı sunumu amacıyla hazırlanmıştır.” notuyla kullanılır.
