"""Render M1_RESULTS_TR.md from saved, validated aggregate outputs (tables are generated, not transcribed)."""
import csv, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
M1 = HERE.parent
CFG = json.loads((M1 / 'config.json').read_text(encoding='utf-8'))
ROLE_TR = {'primary': 'birincil', 'control_source_binned': 'KONTROL (kaynak-binli)'}


def rows(name):
    with (M1 / name).open(encoding='utf-8') as f:
        return list(csv.DictReader(f))


def n(v, d=3):
    v = float(v)
    s = f'{v:+.{d}f}' if abs(v) >= 0.5 * 10 ** -d else f'{0:.{d}f}'
    return s.replace('+', '+')


def u(v, d=3):
    return f'{float(v):.{d}f}'


def ci(lo, hi, d=3):
    return f'[{float(lo):+.{d}f}, {float(hi):+.{d}f}]'


def main():
    summary = rows('REAL_SELECTION_SUMMARY.csv')
    contrasts = rows('POLICY_CONTRASTS.csv')
    controls = json.loads((M1 / 'FIXED_WEIGHT_CONTROLS.json').read_text(encoding='utf-8'))
    audit = json.loads((M1 / 'AUDIT_SUMMARY.json').read_text(encoding='utf-8'))
    prov = json.loads((M1 / 'PROVENANCE.json').read_text(encoding='utf-8'))
    timing = json.loads((M1 / 'RUN_TIMING.json').read_text(encoding='utf-8'))
    check = json.loads((HERE / 'CHECK_REPORT.json').read_text(encoding='utf-8'))
    freeze = (M1 / 'FREEZE_DIGEST.txt').read_text(encoding='utf-8').strip()
    S = {(r['dataset'], r['family'], r['policy']): r for r in summary}
    C = {(r['dataset'], r['family'], r['policy_minus_qwk']): r for r in contrasts}
    out = []
    w = out.append
    w('# Y1 M1 — Gerçek ordinal veri genişletmesi: sonuçlar')
    w('')
    w('2026-11-24. Dal `research/ordinal-y1-m1-extension` (taban `research/ordinal-selection-y1` e5380b5). Durum: **keşifsel genişletme**; dış ön-kayıt veya dokunulmamış doğrulama değildir. '
      f'Protokol, uygunluk kriterleri, hazır tablolar ve ayrımlar hiçbir model fitinden önce donduruldu (FREEZE digest `{freeze}`, ön-fit commit `2f5533e`). '
      'gate_v2 tasarımı değiştirilmeden kullanıldı; v1/gate_v2 dosyaları, freeze\'leri ve sonuçları değiştirilmedi veya yeniden eğitilmedi. '
      'Bu rapor görevler arası anlamlılık iddiası içermez; görevler arası çıkarım makale oturumuna aittir.')
    w('')
    w('## Özet')
    w('')
    w(f'- 11 aday birincil sayfalarında incelendi: **7 uygun** (4 birincil doğal ordinal: CTG, HCV, Cirrhosis, SUPPORT2; 3 kaynak-binli KONTROL: Diabetes130, Student-por, NPHA), **4 BLOCKED** (Maternal Health Risk, CDC Diabetes Health Indicators, Higher Education Students Performance, Heart Disease). Hazırlık aşamasında hiçbir uygun kaynak düşmedi.')
    w(f'- {timing["total_fits"]} gerçek model fiti (7 × 144), ilk fit hatası yok; paralel 7 süreç, fit başına 1 iş parçacığı, toplu duvar süresi {timing["batch_wall_seconds"]:.1f} sn (süreç sürelerinin toplamı {timing["summed_run_wall_seconds"]:.1f} sn).')
    w(f'- Yeniden fit olmadan doğrulama: **{check["status"]}**, {check["totals"]["pass"]} kontrol geçti / {check["totals"]["fail"]} başarısız (588 seçici replay, 126 bootstrap replay, 308 bağımsız QWK ve uç-recall yeniden hesabı dahil). Ön-fit birim testleri 15/15 geçti.')
    signs = [float(C[(d, f, 'amae')]['recall_extreme_delta']) for d in CFG['datasets'] for f in ['po', 'rf']]
    w(f'- AMAE eksi QWK ortalama uç recall: 14 veri seti × aile hücresinin {sum(s > 0 for s in signs)} tanesinde pozitif, {sum(s < 0 for s in signs)} tanesinde negatif, {sum(s == 0 for s in signs)} tanesinde sıfır (aynı seçim). Yön görevden göreve değişiyor; **evrensel bir "AMAE uçları korur" sonucu yok**. En büyük olumsuz farklar NPHA (KONTROL) ve SUPPORT2 RF\'de; olumlu farklar CTG ve Cirrhosis\'te küçük.')
    w('- Uç sınıf her zaman azınlık sınıf değil: SUPPORT2\'de iki uç, HCV ve CTG\'de düşük uç çoğunluk sınıfı. SUPPORT2 ve HCV PO\'da `balanced` ağırlık (sabit h) ve AMAE seçimi uç ortalamasını düşürüyor; uçların azınlık olduğu Student/NPHA\'da ve azınlık düşük uçlu Cirrhosis\'te sabit-h `balanced` uç ortalamasını artırıyor; CTG\'de bir uç düşerken diğeri artıyor.')
    w('- Endpoint-recall kısıtlı QWK, 14 hücrenin 11\'inde QWK ile aynı adayı seçti (null); farklı seçtiği 3 hücrede (Cirrhosis PO/RF, NPHA PO) uç recall arttı.')
    w('')
    w('## Uygun ve engellenen veri setleri')
    w('')
    w('| Veri seti | Rol | Kaynak / lisans | Satır | Grup (tanım) | Sınıf sayıları (rank 0..K-1) | Uç grup sayısı |')
    w('|---|---|---|---|---|---|---|')
    for name in CFG['datasets']:
        a = audit['datasets'][name]; p = prov['sources'][name]
        w(f'| {name} | {ROLE_TR[CFG["roles"][name]]} | UCI {p["uci_id"]}, {p["license"]} | {a["rows"]} | {a["groups"]} ({p["group"]}) | {a["class_counts"]} | {a["endpoint_groups"]} |')
    w('')
    w('Hedef ve kapsam kararları (fit öncesi PROTOCOL.md\'de donduruldu):')
    w('')
    w('- **ctg**: NSP normal < şüpheli < patolojik (üç uzman obstetrisyenin konsensüsü). CTG.xls\'deki 2.126 segment 352 muayene dosyasından geliyor; grup = muayene dosyası (`FileName`). Uzman taban değeri (LBE) ve A..SUSP/CLASS morfolojik etiketleri özellik değil.')
    w('- **hcv**: donör < hepatit < fibroz < siroz (kaynak: "progress"). `0s=suspect Blood Donor` (7 satır) sıralı ölçekte belgelenmiş bir düzey olmadığı için fit öncesi dışlandı; donörlerle birleştirilmedi.')
    w('- **cirrhosis**: histolojik evre 1–4; evresi eksik 6 hasta etiketsiz olarak dışlandı. N_Days/Status (kayıt sonrası izlem sonuçları) ve Drug (randomize atama) özellik değil.')
    w('- **support2**: sfdm2 1–5, hbiostat\'ın belgelediği sırayla (5 = 2 ay içinde ölüm). UCI lisans belirtmiyor; dağıtıcı hbiostat.org/data açık kullanım izni veriyor ("Permission is granted to anyone wishing to use the data sets provided here"), yeniden dağıtım hakkı iddia edilmiyor. 7.705 etiketli hastadan sonuçtan bağımsız hash ile 5.000 hasta. hbiostat\'ın önerisiyle aps/sps/surv2m/surv6m, prg2m/prg6m/dnr/dnrday ve izlem/maliyet değişkenleri dışlandı.')
    w('- **diabetes130 (KONTROL)**: NO < >30 < <30, kaynak tarafından binlenmiş "yeniden yatışa kadar geçen gün". Sıra yalnızca "yeniden yatış zamanı" olarak savunulabilir; veri çekim sınırındaki sansürleme NO ile >30\'u bulanıklaştırır. Ölüm/hospis taburculukları (kaynak makaledeki gibi, yalnız tahminci kuralı) dışlandı; hasta hash\'iyle ≤5.000 karşılaşma (3.471 hasta).')
    w('- **student_por (KONTROL)**: Cortez & Silva (2008) Tablo 2 beş düzeyi (V 0–9 < IV 10–11 < III 12–13 < II 14–15 < I 16–20), birincil makaleden doğrulandı. Yalnız Portekizce tablosu (Matematik tablosuyla 382 öğrenci örtüşüyor), G1/G2 yok.')
    w('- **npha (KONTROL)**: görülen doktor sayısı 0–1 < 2–3 < 4+ (kaynak-binli sayım); tüm 14 anket değişkeni kategorik, ret kodları ayrı kategori.')
    w('')
    w('| BLOCKED | Neden (fit öncesi kayıt) |')
    w('|---|---|')
    for name, reason in audit['blocked_before_preparation'].items():
        w(f'| {name} | {reason} |')
    w('')
    w('Kullanılmayan varyantlar: Student ham G3 (0–20) birincil olarak kullanılmadı; Student-mat kişi örtüşmesi nedeniyle dışarıda. Hiçbir engelli kaynak başka bir kaynakla ikame edilmedi.')
    w('')
    w('## Tasarım (gate_v2 ile aynı)')
    w('')
    w('8 aday (PO C=0.1/1, RF derinlik 4/None; her biri none/balanced), 7 aile-içi seçici (QWK, MAE, AMAE, MMAE, macro-F1, RPS, uç-recall ≥0.2 kısıtlı QWK; AMAE fallback; tie toleransı 1e-12), 3 dış × 2 iç gruplu nested CV, tohumlar 20261124/20261125 (100 destek-geçerli deneme; tüm veri setlerinde etkin tohum = istenen tohum), seçim yalnız havuzlanmış iç OOF skorlarından, ön-işleme yalnız eğitim bölümünde. Aralıklar: sabit tahminler üzerinde grup-yeniden-örnekleme bootstrap (1.000 çekim), **eğitilmiş modellere koşullu**; fold/tekrarlar bağımsız n değildir.')
    w('')
    w('## QWK ve AMAE: uç sınıf recall\'ları ve maliyetler')
    w('')
    w('Değerler iki tekrarın ortalaması (dış OOF). "Uç" = en düşük ve en yüksek rank; Δ = AMAE-seçimi eksi QWK-seçimi; köşeli parantez koşullu %95 grup-bootstrap aralığı. Konfig/ağırlık/h = 6 seçim kararında QWK\'dan farklı aday / farklı ağırlık / farklı hiperparametre oranı.')
    w('')
    w('| Veri seti | Aile | QWK-seçimi QWK | QWK-seçimi recall düşük/yüksek | AMAE-seçimi recall düşük/yüksek | Δ düşük | Δ yüksek | Δ uç ort. [%95] | Δ QWK | Δ norm. MAE | Δ RPS | Konfig/ağırlık/h |')
    w('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for d in CFG['datasets']:
        for f in ['po', 'rf']:
            q = S[(d, f, 'qwk')]; a = S[(d, f, 'amae')]; c = C[(d, f, 'amae')]
            w(f'| {d} | {f.upper()} | {u(q["qwk"])} | {u(q["recall_low"])} / {u(q["recall_high"])} | {u(a["recall_low"])} / {u(a["recall_high"])} | '
              f'{n(c["recall_low_delta"])} | {n(c["recall_high_delta"])} | {n(c["recall_extreme_delta"])} {ci(c["recall_extreme_conditional_lower"], c["recall_extreme_conditional_upper"])} | '
              f'{n(c["qwk_delta"])} | {n(c["normalized_mae_delta"])} | {n(c["rps_delta"])} | {u(c["config_change_vs_qwk"], 2)}/{u(c["weight_changed_fraction"], 2)}/{u(c["hyperparameter_changed_fraction"], 2)} |')
    w('')
    w('Okuma: birincil görevlerde işaretler karışık. CTG\'de AMAE yüksek uç (patolojik) recall\'ını artırıp düşük uç (normal) recall\'ını düşürüyor; ortalama uç farkı küçük ve koşullu aralık sıfırı içeriyor, QWK maliyeti PO\'da −0.026, RF\'de −0.041. HCV\'de AMAE her iki ailede uç ortalamasını düşürüyor (PO\'da donör recall\'ı −0.335; QWK maliyeti −0.106). Cirrhosis\'te küçük pozitif farklar (QWK maliyeti ~0). SUPPORT2\'de iki uç da çoğunluk sınıfı; AMAE nadir orta sınıflara yöneliyor ve iki ucu da düşürüyor (RF: −0.264, QWK maliyeti −0.123). SUPPORT2 PO\'da tekrarlar ayrışıyor (tekrar 0: −0.188, tekrar 1: +0.003). KONTROL görevlerde AMAE hiçbir hücrede uç ortalamasını artırmadı; Diabetes130 PO\'da AMAE ve QWK 6/6 kararda aynı adayı seçti (tam null).')
    w('')
    w('## Macro-F1 ve kısıtlı QWK (politika eksi QWK)')
    w('')
    w('| Veri seti | Aile | macro-F1: Δ uç ort. [%95] | macro-F1: Δ QWK | kısıtlı QWK: Δ uç ort. [%95] | kısıtlı QWK: Δ QWK | kısıtlı QWK fallback |')
    w('|---|---|---|---|---|---|---|')
    for d in CFG['datasets']:
        for f in ['po', 'rf']:
            m = C[(d, f, 'macro_f1')]; k = C[(d, f, 'qwk_recall')]
            w(f'| {d} | {f.upper()} | {n(m["recall_extreme_delta"])} {ci(m["recall_extreme_conditional_lower"], m["recall_extreme_conditional_upper"])} | {n(m["qwk_delta"])} | '
              f'{n(k["recall_extreme_delta"])} {ci(k["recall_extreme_conditional_lower"], k["recall_extreme_conditional_upper"])} | {n(k["qwk_delta"])} | {k["fallback"]}/6 |')
    w('')
    w('Macro-F1 aileye göre yön değiştirebiliyor: SUPPORT2 PO\'da uç ortalamasını artırırken (+0.095) RF\'de düşürüyor (−0.097). Kısıtlı QWK yalnızca QWK-seçiminin iç uç recall\'ı 0.2 tabanının altında kaldığında farklılaşıyor; Cirrhosis RF\'de bir kararda kısıt karşılanamadı ve AMAE fallback kullanıldı (işaretli).')
    w('')
    w('## Sabit hiperparametrede balanced − none kontrolleri')
    w('')
    w('Aynı mimari, hiperparametre, ayrım ve tohumda yalnız eğitim ağırlığı değişiyor (h=0: PO C=0.1 / RF derinlik 4; h=1: PO C=1 / RF derinlik None).')
    w('')
    w('| Veri seti | Aile | h | Δ QWK | Δ recall düşük | Δ recall yüksek | Δ uç ort. [%95] | Δ norm. AMAE | Δ macro-F1 |')
    w('|---|---|---|---|---|---|---|---|---|')
    for c in controls:
        b = c['balanced_minus_none']; e = c['endpoint_ci']
        w(f'| {c["dataset"]} | {c["family"].upper()} | {c["fixed_h"]} | {n(b["qwk"])} | {n(b["recall_low"])} | {n(b["recall_high"])} | {n(b["recall_extreme"])} {ci(*e["mean_ci"])} | {n(b["normalized_amae"])} | {n(b["macro_f1"])} |')
    w('')
    w('Okuma: azınlık-uçlu görevlerde (Cirrhosis düşük uç, Student, NPHA, Diabetes130 yüksek uç) `balanced` uç ortalamasını artırıyor (Diabetes130\'da çoğunluk düşük uç NO düşerken). SUPPORT2\'nin dört hücresinde ve HCV PO\'da düşürüyor (çoğunluk uçlar). CTG\'de tüm hücrelerde düşük uç azalıp yüksek uç artıyor; ortalama farkın aralığı sıfırı içeriyor. HCV RF ve Diabetes130 RF h=1\'de aralık sıfırı içeriyor. Ağırlıklandırma uç-recall\'ı doğrudan "korumuyor"; etki, uçların azınlık mı çoğunluk mu olduğuna bağlı.')
    w('')
    w('## Null\'lar ve tersine dönmeler (kaydedilmiş çıktılardan otomatik listelendi)')
    w('')
    cells = [(d, f) for d in CFG['datasets'] for f in ['po', 'rf']]
    lab = lambda d, f: d + ' ' + f.upper()
    for policy in ['mae', 'amae', 'mmae', 'macro_f1', 'rps', 'qwk_recall']:
        same = [lab(d, f) for d, f in cells if float(S[(d, f, policy)]['config_change_vs_qwk']) == 0]
        w(f'- **Tam null, {policy} = QWK** (6/6 kararda aynı aday; {len(same)}/14): ' + (', '.join(same) if same else 'yok') + '.')
    zero_ci = []
    for d, f in cells:
        for policy in ['amae', 'macro_f1', 'qwk_recall']:
            c = C[(d, f, policy)]
            if float(c['config_change_vs_qwk']) > 0 and float(c['recall_extreme_conditional_lower']) <= 0 <= float(c['recall_extreme_conditional_upper']):
                zero_ci.append(f'{lab(d, f)} {policy} ({n(c["recall_extreme_delta"])} {ci(c["recall_extreme_conditional_lower"], c["recall_extreme_conditional_upper"])})')
    w('- **Seçim değişti ama uç-ortalama farkının koşullu aralığı 0\'ı içeriyor**: ' + '; '.join(zero_ci) + '.')
    rev = []
    for d, f in cells:
        for policy in ['amae', 'macro_f1', 'qwk_recall']:
            c = C[(d, f, policy)]; lo, hi = float(c['recall_low_delta']), float(c['recall_high_delta'])
            if lo * hi < 0:
                rev.append(f'{lab(d, f)} {policy} (düşük {n(lo)}, yüksek {n(hi)})')
    w('- **Uç içi tersine dönme** (bir uç artar, diğeri azalır; ortalama bunu gizler): ' + '; '.join(rev) + '.')
    fam = []
    for d in CFG['datasets']:
        for policy in ['amae', 'macro_f1', 'qwk_recall']:
            a, b = float(C[(d, 'po', policy)]['recall_extreme_delta']), float(C[(d, 'rf', policy)]['recall_extreme_delta'])
            if a * b < 0:
                fam.append(f'{d} {policy} (PO {n(a)}, RF {n(b)})')
    w('- **Aile tersine dönmesi** (uç ortalaması PO ve RF\'de zıt işaretli): ' + ('; '.join(fam) if fam else 'yok') + '.')
    rep = []
    for d, f in cells:
        for policy in ['amae', 'macro_f1', 'qwk_recall']:
            c = C[(d, f, policy)]; r0, r1 = float(c['recall_extreme_delta_repeat_0']), float(c['recall_extreme_delta_repeat_1'])
            if r0 * r1 < 0:
                rep.append(f'{lab(d, f)} {policy} (tekrar 0 {n(r0)}, tekrar 1 {n(r1)})')
    w('- **Tekrarlar arası işaret değişimi**: ' + ('; '.join(rep) if rep else 'yok') + '.')
    w('- **gate_v2 ile yön karşılaştırması (betimsel)**: gate_v2\'de MovieLens PO −0.403 ve SkillCraft-survey RF +0.187 idi; M1\'de de her iki yön görülüyor (örn. NPHA RF −0.335, Cirrhosis RF +0.029). Bu bir test değildir.')
    w('')
    w('## Mekanizma gözlemi (betimsel, test edilmedi)')
    w('')
    w('QWK sabit tahmine 0 verir; AMAE ise K=3\'te "hep orta sınıf" tahminine normalize 1/3 verir. Zayıf sinyalli NPHA\'da (QWK-seçimi QWK ≈ 0.07–0.10) AMAE seçimi ağırlıksız, büyük ölçüde orta sınıfı tahmin eden modelleri seçti (düşük uç recall 0.000, yüksek uç 0.06–0.13), QWK ise çoğunlukla `balanced` adayları seçti. SUPPORT2\'de uçlar çoğunluk olduğundan AMAE\'nin sınıf-eşit ağırlığı nadir orta düzeylere kayıyor. Yani "QWK uçları ezer, AMAE korur" genellemesi bu görevlerde desteklenmiyor; seçicinin etkisi sınıf marjinallerine ve sinyal gücüne bağlı görünüyor. Bu yorum ileride önceden tanımlı bir simülasyonla sınanmalı.')
    w('')
    w('## Doğrulama, süre ve fit sayısı')
    w('')
    w('| Veri seti | Fit | Süreç duvar süresi (sn) | Fit+tahmin toplamı (sn) | Medyan fit (sn) |')
    w('|---|---|---|---|---|')
    for d, r in timing['runs'].items():
        w(f'| {d} | {r["fits"]} | {r["wall_seconds"]:.1f} | {r["fit_predict_seconds"]:.1f} | {r["fit_predict_median_seconds"]:.3f} |')
    w('')
    w(f'Toplam {timing["total_fits"]} fit; 7 süreç paralel ({timing["logical_cpus"]} mantıksal CPU), toplu duvar süresi {timing["batch_wall_seconds"]:.1f} sn ({timing["batch_start_utc"]} → {timing["batch_end_utc"]}). '
      f'Doğrulayıcı {check["elapsed_seconds"]:.1f} sn. Ortam: Python {timing["versions"]["python"]}, numpy {timing["versions"]["numpy"]}, pandas {timing["versions"]["pandas"]}, scikit-learn {timing["versions"]["scikit-learn"]}. İnsan/ajan saatleri ölçülmedi.')
    w('')
    w('Doğrulama sınırı: modeller ve iç OOF tahminleri bağımsız yeniden üretilmedi; seçici replay kaydedilmiş iç metriklerle yapıldı. Hash\'ler fit sonrası alındı; fit öncesi kanıt olan yalnız ön-fit commit\'teki freeze digest\'idir.')
    w('')
    w('## Sınırlılıklar')
    w('')
    w('- Keşifsel: aynı yazarlar v1/gate_v2 sonuçlarını görmüştü; aday listesi lisans/hedef/grup/destek ölçütleriyle seçildi, model sonuçlarıyla değil. Bu bağımsız doğrulama örneklemi değildir.')
    w('- 3 görev KONTROL (kaynak-binli); birincil kanıt olarak havuzlanmamalı. Birincil görev sayısı M1\'de 4.')
    w('- Klinik görevler (CTG, HCV, Cirrhosis, SUPPORT2) yalnız metodolojik testtir; klinik karar desteği veya kişi düzeyi iddia yok. HCV vaka-kontrol örnekleme taşıyor (donörler farklı popülasyon). CTG etiketleri aynı kayıtların uzman okuması; muayene dosyası doğrulanmış hasta kimliği değil.')
    w('- Küçük destekler: Cirrhosis evre 1 = 21 hasta, HCV fibroz 21 / hepatit 24, SUPPORT2 düzey 4 = 28 hasta; uç recall aralıkları geniş ve koşullu.')
    w('- SUPPORT2 ve Diabetes130 hash alt-örneklemi (≤5.000 satır); tam veri sonuçları farklı olabilir. Diabetes130\'da hastane düzeyi bağımlılık ve tanı kodları kullanılmadı; NPHA ve Student\'ta gruplar yalnızca birebir tahminci kopyaları.')
    w('- Aralıklar eğitilmiş modellere koşullu sabit-tahmin bootstrap\'ıdır; tam eğitim belirsizliğini veya görevler arası çıkarımı vermez. Burada görevler arası anlamlılık iddiası yok.')
    w('- Lisans yorumları birincil sayfalardaki ifadelere dayanır; kurum etik/hukuk kararı değildir. Ham veri, satırlar, kimlikler ve tahminler yayımlanmadı (yalnız ignored `local/`).')
    w('')
    w('## Makale oturumu için birleştirme notu')
    w('')
    w('`REAL_SELECTION_SUMMARY.csv`, `POLICY_CONTRASTS.csv` ve `FIXED_WEIGHT_CONTROLS.json` gate_v2 ile birebir aynı şemada (gate_v2 `real_tables` fonksiyonu doğrudan kullanıldı); 7 veri seti × 14 / 6 / 4 satır. Rol bilgisi (birincil/KONTROL) `Y1_DATASET_AUDIT_M1.csv` `eligibility` sütununda ve `config.json` `roles` alanında. KONTROL görevleri birincil havuzdan ayrı tutulmalı.')
    w('')
    w('## Dosyalar')
    w('')
    w('PROTOCOL.md, config.json, data.py, run.py, provenance.py, tests/ (fit öncesi donduruldu); PROVENANCE.json, AUDIT_SUMMARY.json, Y1_DATASET_AUDIT_M1.csv, FREEZE.json, FREEZE_DIGEST.txt, TEST_LOG.txt; REAL_SELECTION_SUMMARY.csv, POLICY_CONTRASTS.csv, FIXED_WEIGHT_CONTROLS.json, RUN_TIMING.json; validation/check_results.py, CHECK_REPORT.json, RUN_HASH_RECEIPT.json, build_report.py, render_report_tr.py.')
    (M1 / 'M1_RESULTS_TR.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
    print('wrote M1_RESULTS_TR.md', len(out), 'lines')


if __name__ == '__main__':
    main()
