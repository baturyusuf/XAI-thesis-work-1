# Validation and reproducibility ledger

## Ortam
Windows/MINGW64 sh;Python3.13,ayrılinked-worktree `.venv-dataset-audit`. Exact bağımlılıklar `../requirements-audit.txt`;script metadata versiyonları JSONda. Global environment değiştirilmedi. Scriptlere kişisel mutlak yol gömülmedi;`XAI_DATA_ROOT` veya açık `--data-root` gerekir. İlk ortam değişkeni kontrolünde XAI_DATA_ROOT yoktu;denetim gerçek bulunan kökü açık argümanla kullandı.

Komutlar aşağıda **kendi worktree kökünden**,XAI_DATA_ROOT doğru private köke ayarlı bir terminal içindir. Bu oturumda Zedterminal dışworktree `cd`yi reddettiği için aynı scriptler mutlak script yolu ve açık data-root ile ana kökten çalıştırıldı;ana kökte araştırma dosyası üretilmedi.

```sh
python -m venv .venv-dataset-audit
.venv-dataset-audit/Scripts/python.exe -m pip install -r research/datasets/requirements-audit.txt
.venv-dataset-audit/Scripts/python.exe research/datasets/scripts/audit_local.py --public-output research/datasets/evidence
.venv-dataset-audit/Scripts/python.exe research/datasets/scripts/audit_torres_identity.py --output research/datasets/evidence/torres_identity_summary.json
.venv-dataset-audit/Scripts/python.exe research/datasets/scripts/audit_uci.py --output research/datasets/evidence/uci_aggregate.json
.venv-dataset-audit/Scripts/python.exe research/datasets/scripts/capture_sources.py --output research/datasets/DATASET_SOURCE_REGISTRY.csv
.venv-dataset-audit/Scripts/python.exe research/datasets/scripts/validate_evidence.py
```

UCI scripti default mevcut cache'i okur;ilk cache için açık `--download` parametresi gerekir. Bu option yalnız resmi üç UCIURL'yi indirir;network/content hash değişimleri receipt'e yansır. Sourcecapturemetadata bağlantılarını yeniler;değişenviewcounts gibi alanlar snapshot hashini değiştirebilir. Sonuçlar admission/approval veyaotomatik dataset preprocessing değildir. Yerel source permissionlar kapanmadan başka kullanım amacı için scriptleri genişletmeyin.

## Phase 0 sırasında gerçekte çalıştırılan kontroller
- `audit_local.py`:başarılı;780raw dosya SHA256/byte,600Parquetfooter,4fulltrainingprofile,BGHCSV/DTA/codebook karşılaştırması. Null/empty-string ayrımı eklendikten sonra yeniden başarılı çalıştı.
- `audit_torres_identity.py`:başarılı;3projectedtrainingdosyada ID/date/target integrity veoverlap;hiçbirID veyarowhash dışarı yazılmaz.
- `audit_uci.py`:resmi cachedrawdan yeniden başarılı;Student resmi13-key reçetesi veGarment department key doğrulandı. Hiçbirmodel çalışmadı.
- `capture_sources.py`:18metadata kaynak kaydı;17HTTP200snapshot,1publisherurllib403. Aynıpublisherfetch aracında okundu ama403silinmedi;HTTP200varlığı codebook scientific suitability demek değildir.
- `validate_evidence.py`:**5test geçti**.30alan/dataset tutarlılığı;raw distribution/key invariants;Student/Torres/Garment düzeltmeleri;780rawdosyanın audit sonrası aynıbyte/hash kalması;metadata/UCIcache hashlerinin receipt ile eşliği.
- Tüm5Python script `ast.parse` ile başarılı parse edildi;scriptlerde kişisel yol kontrolü geçti.17zorunlu belge nonempty;15card×30alan450auditfield tutarlı. Bu yapısal kontroller bilimsel geçerlilik ispatı değildir.
- `git diff --check`hatasız;ancak yeni dosyalaruntracked olduğu için bu komut onların içeriğini denetlemez. Ayrı full-tree text whitespace/extension veprivatebinary kontrolü tamamlandı:sıfırtrailingwhitespace,araştırma ağacında sıfırprivatebinary;FINAL_CHECKS.json kaydı var.
- main/ownHEAD hâlâ`1b71d4c45ae1aba771e7c499f87f197f44b3112c`;Agent1worktree korunuyor. Commit/push/merge yok;yalnızownworktree `research/` untracked. main'de baştan varolan private klasör untracked.

## Düzeltildi / kalan sınırlamalar
Uzun Windows shell komutları aktarımda kesildi;daha küçük mutlak-yol yazmalarıyla çözüldü. pandas3StataReader `.close()` çağrısı çalışmadı;contextmanager ile düzeltildi veaudit tekrar geçti. Alt ajan H/metric veoverlap yorumları parent review ile düzeltildi. Hiçbiri ham dosya değişikliği veyaeksik sonucu başarılı gösterme ile çözülmedi.

Kaynak erişim sınırlamaları:yukarıdakipublisher403;INXraw/lisans belirsiz;TOCUCO/hiddenraw bilerek açılmadı;Trip/Fresh/TILES/Parkinson yalnızmetadata. Nihai bilimsel onay,ground-truth evaluation,power analizi,benchmark veyaheld-out test yapılmadı.

## Belge yayımı kapsamı
Araştırmacının yalnız belge ve kayıt yayımı talimatı nedeniyle `scripts/` altındaki beş denetim betiği bu commit’e dahil değildir; komutlar Phase 0 sırasında yerelde çalıştırılan işlemlerin tarihsel kaydıdır. `requirements-audit.txt` yalnız ortam sürüm kaydı olarak yayımlanır. Bu belge sürümü tek başına GitHub’dan eksiksiz yeniden yürütme paketi iddiası taşımaz. Yayım görevi sırasında yeni veri analizi veya ham dosya denetimi çalıştırılmadı; yalnız mevcut belgeler/kayıtlar ve staged Git içeriği incelendi.
