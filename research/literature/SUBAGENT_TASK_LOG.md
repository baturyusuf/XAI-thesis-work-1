# Alt ajan görev ve karar kaydı

2026-10-20. Protokol v0.1 görevlendirmeden önce yazıldı. spawn_agent ayrı bağlamlarla çalıştı; çıktı dosyası yazma yetkisi verilmedi. Bütün sonuçlar parent tarafından scope/kimlik kontrolünden geçirildi. Alt ajan nihai bilimsel karar vermez.

| Görev | Oturum | Gerçek model | Görev bazlı routing gerekçesi | Reasoning | Durum |
|---|---|---|---|---|---|
| A1-S1 | 4237e817-326e-483a-9912-61f525ce5eb2 | openai-subscribed/gpt-6-luna | Teknik sufficient/robust extraction; güçlü novelty muhakemesi parentta, Luna yeterli | BİLİNMİYOR; araçta ayrı parametre yok | İlk kapsam dışı çıktı reddedildi; aynı oturumda daraltıldı |
| A1-S2 | 206cc129-a8f3-459d-9d48-d4fa6777707f | openai-subscribed/gpt-6-luna | Selective/conformal garanti olayını çıkarma; teknik iş, karar yetkisi yok | BİLİNMİYOR | Kısmi kabul; temporal/direct-rival kapsam açığı |
| A1-S3 | 343154bb-b724-4477-8428-2df19b7d4759 | openai-subscribed/gpt-6-luna | Dört toolkitin teknik kapsam/lisans ayrımı; salt metadata değil | BİLİNMİYOR | Kısmi kabul; Quantus lisansı parentça düzeltildi |

Üç yeni görevin her biri için model yeterliliği/maliyeti ayrı değerlendirildi; sonuçta aynı erişilebilir bulut Luna uygun bulundu. Low/Medium seçildiği iddia edilmez. Basit bulk metadata işi yeni ajanla değil deterministik API collector ile yapıldı. Yerel/Rumeli/company-coder kullanılmadı. Ana model reasoning seviyesi de araçla değiştirilmedi.

## Sözleşmeler
S1: 2024–2026 tabular sufficient/robust/conditional, en fazla 5 primary identity; mechanism/type/assumptions/datasets/metrics/baselines/results/code/limitations ve query log; E1/E2 ayrımı; novelty/deney yok. İlk çıktı CF üretim yöntemleriydi; eşdeğer olmadığından reddedildi. Takip aynı oturumda PAXp/minimal reasons/conditional ile en fazla 2 kaynağa daraltıldı. Dönüş: LmPAXp2024 + SST2025.
S2: 2024–2026 selective/conformal/uncertainty feature explanations ve shift/transfer, en fazla5; guarantee event/exchangeability; prediction vs explanation coverage ayrımı; novelty/deney yok. Dönüş: Selective2024, DFI, XtrAIn, AttEXplore++. Son üçü scope açısından komşu veya yanlış terim eşleşmesi; transfer/adversarial ile temporal transfer eşitlenmedi.
S3: Tam dört kaynak OpenXAI/Quantus/MetaQuantus/BEExAI; primary paper, tabular applicability, metrics, pinned code/license; experiment/novelty yok. Dört kayıt + teknik özet döndü. Parent, paper kimliklerini Atom; repo/commitleri GitHub API; BEExAI tam metnini doğrudan kontrol etti.

## Kabul ve kalan belirsizlik
- Parent tam metin: LmPAXp, Selective, BEExAI. Kaynak yazar sonuçları REPORTED; replikasyon yok.
- SST/DFI/XtrAIn: parent kimlik/abstract kontrolü; alt ajan E2 dese de matriste parent E1 bırakıldı.
- AttEXplore++ doğrudan temporal/transfer baseline olarak kabul edilmedi, matrise alınmadı.
- S1 ilk CF listesi sadece komşu leads; parent doğrulanmış kaynak envanterine alınmadı.
- Quantus API NOASSERTION belirsizliğini pinned LICENSE çözerek LGPLv3-or-later kaydettik. OpenXAI alternatif başlık/önerilen proceedings hash ve Quantus DOI bağımsız doğrulanmadığından kullanılmadı.
- Tam sonuçların kalıcı bilimsel özeti SUBAGENT_FINDINGS.md; sorgu sayıları parent kontrolü yoksa REPORTED. Oturumlar kapanmış/silinmiş varsayılmıyor.

## REVIEW02 — 2026-10-21
Protokol v0.2 ve D012 onayı görevlendirmeden önce kaydedildi. Dört bağımsız extraction görevi; max3 eşzamanlı. Bütün görevlerde dosya yazmak, benchmark/algoritma yapmak ve nihai novelty kararı yasaktı. Reasoning seçimi parametresi yok; gerçek seviye BİLİNMİYOR. Yerel model yok.

| ID | Session | Gerçek model | Bağımsız routing gerekçesi | Sözleşme / çıktı / kabul |
|---|---|---|---|---|
| S4 | 6c388a1d-9282-45d4-b5f9-4d4f8f497a4b | openai-subscribed/gpt-6-luna | Formal sufficient/robust technical extraction; karar parentta | Max4 paper,2fulltext hedefi,2024–2026; PAXp/SST/abstraction-refinement; parent primary kontrol; conditional kabul |
| S5 | be78bda7-b3af-4f06-8aba-37158b364c12 | openai-subscribed/gpt-6-luna | Uncertainty/garanti olayı ayrımı için teknik extraction | Max4 paper,2fulltext; Selective/ReCalX/FCE/CE; parent kontrol; global gap çıkarımı reddedildi |
| S6 | eef37a26-6c8c-46ad-af76-14c6cefbb7da | openai-subscribed/gpt-5.6-luna | Daha basit ordinal metadata ve kısa method kapsamı; daha ucuz yeterli model | Max3 kaynak,1fulltext deneme; FRI/Shapley review; parent DOI kimliği; query URLleri aynı sessionda tamamlandı |
| S7 | f9abf274-a08f-4a13-a08a-7d9511821f4f | openai-subscribed/gpt-5.6-luna | Dar immutable source-path/function extraction; proof/novelty yok |2repo,max2source-file/repo; ReCalX/FCE; reject-policy lead için max2ek dosya takip; parent kritik snippets doğrulaması |

S4 takip: parent exact counterexampleı çürütmesini istedi; printed Alg1 minimality claimini sınırladı. Bu bağımsız matematik kontrolüdür, paper kodunun replikasyonu değil. S7 takip: reject_policy varlığından açıklama-risk garantisi çıkarmak yerine event ve validity metadata incelendi. Yapılan kontroller SUBAGENT_FINDINGS_R02 ve source snapshots içinde. Alt ajanların theorem/venue iddiaları otomatik VERIFIED olmadı.

## D019 handoff — S8/S9 / 2026-10-21
| Görev | Session | Exact model / routing | Reasoning | Sonuç ve parent kontrolü |
|---|---|---|---|---|
| S8 LTT | 893eea07-59e2-49b0-9a70-853b47c8b089 | openai-subscribed/gpt-6-luna; dar teknik theorem/risk extraction | BİLİNMİYOR; ayrı parametre yok | Thm1, selective risk ve CLT ayrımı kabul; parent cached fulltext hash/pasaj kontrolü. Takip max1tree+2raw MEPS/HB. Parent source lines159–190 ve concentration127–131 doğruladı. |
| S9 PAXp | d230a1dd-6319-4e2b-b776-0dccef0ca1b3 | openai-subscribed/gpt-6-luna; teknik pseudocode/assumption audit | BİLİNMİYOR | Alg1/Eq4/6/Hoeffding scope kabul; official main artifact bulunamadı. Parent printed source ve exact audit yeniden kontrolü. |

Sözleşmeler: iki paper identity/pinned source ile sınırlı; yeni tarama/novelty/deney/dosya yazma yasak. S8 fulltext Theorem1/§§3.2–3.3 + max2 paper; CRC gerekmedi. S9 max6targeted URL, 3 raporladı. Parent ek PAXp+explanations repo query0, yokluk kanıtı değil. Tamamlanma: formül/nicemleyici/varsayım + scope + source/unknowns dönmesi. Yerel model kullanılmadı.
Parent düzeltmesi: S8 centered lossu koşullu hedefle ilişkilendiremedi; alpha+A*(L-alpha) eşdeğerliği pozitif coverage altında analitik olarak gösterildi. Bu dönüşümün kendisi hata değil. Observed-max scaling, fixed population bound/p-value/threshold ve code-paper equivalence ayrı UNVERIFIED. Bütün code veya theorem invalidliği çıkarılmadı. Görevlerin salt extraction çıktıları nihai bilimsel karar sayılmadı.
