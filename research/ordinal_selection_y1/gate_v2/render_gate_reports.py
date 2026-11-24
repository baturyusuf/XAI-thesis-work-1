"""Render descriptive reports from saved aggregates; no fitting or data download."""
import csv
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def csvrows(name):
    with (ROOT / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def js(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def main():
    rows = csvrows('REAL_SELECTION_SUMMARY.csv')
    contrasts = csvrows('POLICY_CONTRASTS.csv')
    sim = csvrows('MECHANISM_CONTRASTS.csv')
    assert len(rows) == 56 and len(contrasts) == 24 and len(sim) == 24
    index = {(r['dataset'], r['family'], r['policy']): r for r in rows}
    names = ['restaurant', 'sushi', 'movielens100k', 'skillcraft_survey']
    lines = ['# Y1 Gate-v2: gerçek sonuçlar ve sınırları', '',
      'Astra, 2026-11-23. Kaynak: kaydedilmiş OOF sonuçlarından üretilen aggregate CSV/JSON. Bu betik model eğitmez; sabit protokolleri değiştirmez. İki tekrarın pooled-OOF metrik ortalaması kullanılır. Fold/tekrar bağımsız bilimsel örnek sayılmaz.', '',
      '## QWK ile AMAE seçimi', '',
      'Alt/üst recall tam sınıf isabetidir; endpoint ortalaması bu ikisinin ortalamasıdır. Normalize uzaklıklar K-1 ile bölünür. Her ailede aynı dört aday, iki hiperparametre × iki eğitim ağırlığı karşılaştırılır.', '',
      '| Görev | Model | QWK seçiminin QWK / AMAE seçiminin QWK | Alt recall Q / A | Üst recall Q / A | Uç ortalama Q / A | Değişen karar |',
      '|---|---|---:|---:|---:|---:|---:|']
    def pair(a, b, key):
        return format(float(a[key]), '.4f') + ' / ' + format(float(b[key]), '.4f')
    for name in names:
        for family in ['po', 'rf']:
            a, b = index[name, family, 'qwk'], index[name, family, 'amae']
            cells = [name, family] + [pair(a, b, m) for m in ['qwk','recall_low','recall_high','recall_extreme']]
            cells += [str(round(float(b['config_change_vs_qwk'])*6)) + '/6']
            lines += ['| ' + ' | '.join(cells) + ' |']
    lines += ['', '## AMAE eksi QWK seçim politikasının maliyetleri', '',
      'Eksi uzaklık/RPS daha iyidir; eksi recall/QWK daha kötüdür. Güven aralıkları sabit model tahminlerine koşullu, gruplu bootstrap aralıklarıdır; tüm eğitim belirsizliği değildir. Kişi/item/pilot-seçim belirsizliğini kapatmaz.', '',
      '| Görev | Model | Uç farkı [koşullu %95] | İki tekrardaki uç farkı | nMAE farkı | nAMAE farkı | nMMAE farkı | RPS farkı |',
      '|---|---|---:|---:|---:|---:|---:|---:|']
    for r in contrasts:
        if r['policy_minus_qwk'] != 'amae':
            continue
        interval = format(float(r['recall_extreme_delta']), '.4f') + ' [' + format(float(r['recall_extreme_conditional_lower']), '.4f') + ', ' + format(float(r['recall_extreme_conditional_upper']), '.4f') + ']'
        repeats = format(float(r['recall_extreme_delta_repeat_0']), '.4f') + ' / ' + format(float(r['recall_extreme_delta_repeat_1']), '.4f')
        cells = [r['dataset'],r['family'],interval,repeats] + [format(float(r[m+'_delta']),'.4f') for m in ['normalized_mae','normalized_amae','normalized_mmae','rps']]
        lines += ['| ' + ' | '.join(cells) + ' |']
    lines += ['', '## Sabit hiperparametrede balanced eksi none', '',
      'Bu kontrol, mimari/hiperparametre/seed/split sabitken eğitim ağırlığı değişimidir. Politika değişimi ile aynı deney değildir; insanlar üzerinde nedensellik iddiası oluşturmaz.', '',
      '| Görev | Aile/h | Alt recall | Üst recall | Uç ortalama | QWK | nMAE | nAMAE |',
      '|---|---|---:|---:|---:|---:|---:|---:|']
    for c in js('FIXED_WEIGHT_CONTROLS.json'):
        d = c['balanced_minus_none']
        cells = [c['dataset'],c['family']+'/'+str(c['fixed_h'])] + [format(d[m],'.4f') for m in ['recall_low','recall_high','recall_extreme','qwk','normalized_mae','normalized_amae']]
        lines += ['| ' + ' | '.join(cells) + ' |']
    lines += ['', '## Kontrollü latent simülasyon: AMAE eksi QWK', '',
      '3 sınıf-öncül dağılımı ×2 sinyal düzeyi ×10 seed ×8 aday =480 fit. Beş ordinal sınıf; ayrı train1000/validation1000/test4000. Aynı seedin hücreleri eşlenmiştir. Aşağıdaki t95 aralıkları yalnız belirtilen DGP altında 10-seed Monte Carlo değişkenliğidir, gerçek veri bootstrap aralığıyla karşılaştırılamaz. Çoklu karşılaştırma düzeltilmemiş betimsel sonuçlar; sıfır genişlik eşdeğerlik kanıtı değildir.', '',
      '| Hücre | Aile | Alt recall farkı | Üst recall farkı | Uç ortalama [MC t95] |',
      '|---|---|---:|---:|---:|']
    for r in sim:
        if r['policy_minus_qwk'] != 'amae':
            continue
        effect = format(float(r['recall_extreme_delta']),'.4f') + ' [' + format(float(r['recall_extreme_mc_lower']),'.4f') + ', ' + format(float(r['recall_extreme_mc_upper']),'.4f') + ']'
        cells = [r['cell'],r['family'],format(float(r['recall_low_delta']),'.4f'),format(float(r['recall_high_delta']),'.4f'),effect]
        lines += ['| ' + ' | '.join(cells) + ' |']
    lines += ['', '## Bilimsel yorum ve olumsuz sonuçlar', '',
      '- MovieLens PO: AMAE altında alt recall sıfır. Ortalama uzaklık/RPS iyileşirken en kötü sınıf hatası ve uç recall kötüleşiyor. Bu, AMAE genel çözüm iddiasına karşı örnektir; sonuç çıkarılmadı.',
      '- SkillCraft RF: AMAE uç recall kazancı iki tekrarda da 0.05 üzerinde. QWK kaybı 0.0203408 ile önceden belirlenmiş 0.02 toleransını aşıyor. Dış AMAE az miktarda kötüleşiyor. Başarılı ve ücretsiz iyileştirme denemez.',
      '- SkillCraft RF QWK/AMAE iki politikada da balanced6/6. Konfigürasyon farkı ağırlık değişimi değil hiperparametre değişimidir. MovieLens PO ise ağırlıkla birlikte bazı hiperparametreleri de değiştiriyor. Ayrı kontrol tablosu bu karışıklığı önler.',
      '- Sushi PO özdeş AMAE/QWK seçimi; Restaurant iki uçta farklı yönler; hiçbiri başarısız diye elenmedi. Makro-F1 ve kısıtlı-QWK dahil tüm yedi politika REAL_SELECTION_SUMMARY.csv içinde.',
      '- İç recall kısıtı yalnız validation üzerinde tanımlı; dış garanti yok. İnfeasible/fallback sayıları CSV içinde, başarı yerine geçirilmez. SkillCraft RF macro-F1 etkisi bir tekrarda sıfır: iki-tekrar kararlılık kanıtı diye gösterilemez.',
      '- Simülasyon dengesiz/denge ve sinyal koşullarında yön değiştiriyor; belirli argmax decoder ve dar havuza koşullu. QWK merkez tahminini evrensel olarak ödüllendirmez. ECE tanı amaçlı; RPS yalnız kalibrasyon değildir.',
      '- Model sonuçları düşük sinyalli/sade özellikli rating görevleri ve bir oyun-league göreviyle sınırlı. Kaynak aileleri bilimsel birimdir; binlerce puan bağımsız dataset sayılmaz. Dört kaynakla genel üstünlük p-değeri verilmedi.', '',
      '## Çalıştırma ve doğrulama', '',
      'Gate-v2 gerçek fit576 + simülasyon480 =1.056. Önceki v1 gerçek fit576 tekrar edilmedi; tüm aşamalar toplam1.152 gerçek +480 simülasyon =1.632 bilimsel fit. Unit test içindeki küçük estimator kontrolleri bu sayılara dahil değil. Gerçek runner süreleri toplam104.924s, simülasyon48.794s. Bu aktif insan/ajan zamanı, CPU çekirdek-saati veya tüm oturum süresi değildir.',
      '61 birleşik test geçti. No-refit kontroller1292+448=1740 PASS;840 simülasyon seçim kararı validation skorlarından replay edildi. Kontroller hash/split/OOF/selector/metric bağıntılarını sınar; fiilen yapılan her model eğitimini bağımsız yeniden üretmez. Bazı sayısal kontroller aynı donmuş helper fonksiyonunu kullanır; QWK ayrıca bağımsız formülle kontrol edilmiştir.',
      'Simülasyon kodu test metriklerini seçim kaydı öncesinde de hesaplar; selector yalnız validation skorlarını alır. İşlemsel test-körlüğü veya bağımsız dış preregistration iddia edilmez. Post-run hash makbuzları önceden dondurmanın dış zaman damgası değildir.', '',
      '## Yeniden üretim', '',
      'Yetkili worktree kökünde yerel venv python ile research/ordinal_selection_y1/gate_v2/build_report.py ve ardından render_gate_reports.py çalıştırılır. Bu iki betik yeniden eğitim yapmaz. İlgili local/ veri ve tahmin arşivleri olmadan tam replay mümkün değildir; kamuya dağıtım hakları ayrıca kapatılmalıdır.',
      'Kaynaklar: SESSION_EVIDENCE.json; POLICY_CONTRASTS.csv; FIXED_WEIGHT_CONTROLS.json; MECHANISM_CONTRASTS.csv; validation/CHECK_REPORT.json ve CHECK_SKILLCRAFT.json; üç aktif FREEZE.json; ilgili ajan denetimleri.']
    (ROOT/'Y1_GATE_V2_RESULTS.md').write_text(chr(10).join(lines)+chr(10),encoding='utf-8')
    audits = js('real_extension/AUDIT_SUMMARY.json')['datasets']
    audits['skillcraft_survey'] = js('skillcraft_survey/AUDIT_SUMMARY.json')
    sources = {
      'restaurant': ('https://archive.ics.uci.edu/dataset/232/restaurant+consumer+data','CC-BY-4.0','permitted with attribution','user','source-paper counts differ; same-item historical ratings'),
      'sushi': ('https://www.kamishima.net/sushi/','research-use terms','permission required','user','500 hash-selected users; same items; 2016 corrected score direction'),
      'movielens100k': ('https://grouplens.org/datasets/movielens/100k/','research-use terms with attribution/nonendorsement','permission required','user','400 hash-selected users; historical selected ratings; same-item pool'),
      'skillcraft_survey': ('https://archive.ics.uci.edu/dataset/272/skillcraft1+master+table+dataset','CC-BY-4.0','permitted with attribution','exact predictor group; person independence assumed','post-v1 source narrowing; original cohort mapping unverified; highclass35')}
    output=[]
    for name in names:
        a=audits[name];url,licence,redistribution,unit,risks=sources[name]
        output.append({'dataset':name,'source_url':url,'real_not_synthetic':True,'rows_analyzed':a['rows'],'group_count':a['groups'],'group_definition':unit,'feature_count':len(a['features']),'class_count':len(a['class_counts']),'class_counts':json.dumps(a['class_counts']),'endpoint_group_counts':json.dumps(a['endpoint_groups']),'license_or_terms':licence,'research_use':'primary terms permit local research; not institutional ethics decision','redistribution':redistribution,'missing_counts':json.dumps(a['missing']),'split':'2 repeats; 3 outer x2 inner group-disjoint; all classes per partition','eligibility':'bounded exploratory pilot; not unrestricted confirmation','remaining_risks':risks,'archive_or_table_sha256':a.get('archive_sha256',a.get('source_sha256')),'provenance_path':'skillcraft_survey/PROVENANCE.json' if name=='skillcraft_survey' else 'real_extension/PROVENANCE.json'})
    with (ROOT/'Y1_DATASET_AUDIT_V2.csv').open('w',encoding='utf-8',newline='') as out:
        w=csv.DictWriter(out,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
    print('Rendered results and 4-row audit; no training')

if __name__ == '__main__':
    main()
