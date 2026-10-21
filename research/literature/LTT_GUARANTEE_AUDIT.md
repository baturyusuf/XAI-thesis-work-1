# LTT — Koşullu risk ve garanti nicemleyicileri

2026-10-21. D019 kapsamında dar yeniden kontrol; yeni literatür taraması veya deney yok. Kaynak: [Learn then Test, arXiv2110.01052v5](https://arxiv.org/html/2110.01052v5), §§1.1,2.1–2.3,3.2–3.3,5; Appendix B/C. Parent tam metin pasajlarını okudu; S8 extraction yardımcı kontrol. Paper sonuçları REPORTED, H2 uyarlaması koşullu matematiksel çıkarım.

## Executive Summary
LTT, kabul edilenler üzerindeki koşullu population riskini kontrol etmek için kullanılabilir. Garanti calibration-sample rastgeleliği üzerinden yüksek olasılıklıdır; her birey, alt grup veya keyfî distribution shift için koşullu doğruluk değildir. Bounded-loss sonlu-örneklem yolu ile unbounded-MSE/CLT yolu ayrılmalı. Bu mevcut mekanizma H2 için güçlü null; yeni algoritma değil.

## Evidence
### Teorem ve iki farklı koşullama
Sabit/pretrained predictor ve calibration verisinden bağımsız öğrenilmiş açıklayıcı/score ailesi için sonlu Lambda grid; H_lambda: R(lambda)>alpha. Doğru null altında her p_lambda super-uniform ve prosedür FWER<=delta ise Thm1:

P_calibration(sup_{lambda in Lambda_hat} R(lambda)<=alpha)>=1-delta.

Bu olayda Lambda_hat içinden veriye bakarak seçim yapılabilir. Test edilen aile/score veya test graphını aynı calibration verisiyle serbestçe öğrenmek bu izinle eşdeğer değildir. Boş Lambda_hat sertifikalı policy bulunamadı demektir; başarılı sıfır-risk politika diye raporlanmaz.

§3.2 Eq7–8: R(lambda)=P(error | accepted). §3.3 Eq9–10: R(lambda)=E[squared error | accepted]. Buradaki conditioning kabul olayıdır. Dış olasılık calibration sample üzerindedir; R ilgili deployment popülasyonunda kalan accepted örnekler üzerinde ortalamadır. §5te marginal uyarısı subgroup/instance koşullu güvence olmadığını açıklar. E[A*L] ile E[L|A=1] aynı değildir: ilki coverage ile küçülür.

### H2 için doğrudan uygulanabilir bounded-null sözleşmesi
E(x) explanation; A_lambda(x) accepted indicator; 0<=L(x,E)<=1, C(lambda)=P(A_lambda=1)>0 olsun. Parent analitik indirgeme:

L_tilde_lambda = alpha + A_lambda*(L-alpha),  0<=L_tilde<=1.
E[L_tilde]-alpha = C(lambda)*(E[L|A_lambda=1]-alpha).

Dolayısıyla E[L_tilde]>alpha nullı conditional explanation-risk>alpha nullına eşdeğerdir. Sabit her lambda için observation-level iid bounded loss ve HB/başka geçerli p-değeri + FWER, LTT Thm1e bir uygulamadır. Bu indirgeme yeni yöntem katkısı değildir. Alternatif: kabul edilen calibration altkümesinde geçerli binomial/bounded-loss test; seçilen sayıya koşullamanın varsayımları yazılmalı.

Somut bounded loss: probability çıktısı için bağımsız completionlarda abs(output difference) veya violation indicator. Bunlar universal explanation truth değil; önceden belirtilmiş Q/output/object hedefini ölçer. Signed margin veya sınırsız local-MSE için sabit bir bound gerekçesi olmadan HB kullanmayın. Clip etmek yeni bir loss hedefidir; clipped-risk garantisini ham-loss garantisi diye sunmayın.

### MC loss ve bağımsızlık
Z_i aynı base observation için ayrık eval probes olsun. Bounded L_hat ve E[L_hat | observation,E,A]=L_exact ise E[A*L_hat]=E[A*L_exact]; böylece above nullın latent expected-loss hedefi korunabilir. Score/acceptance aynı probe noiseuna bakıyorsa bu conditional-unbiasedness kendiliğinden geçmez. Probes bağımsız calibration birimi değil, observation-level loss içindeki ölçümlerdir. Sequential/adaptive probing farklı koşul gerektirir; bu handoff keyfî adaptive test garantisi vermez.

## Competing Approaches
§2.2 Prop1 HB bounded [0,1] loss için finite-sample p-değerleri; Appendix B finite mean/variance CLT p-değeri ASİMPTOTİK. §3.3 finite-sample MSE ifadesi sınırsız square-loss için varsayımsız HB izni olarak okunamaz. CRC Thm1in exchangeable monotone bounded-loss marginal expected-risk garantisi, LTTnin high-probability accepted-risk hedefiyle aynı değildir; R02 CRC dossier referansı korunur.

## Reviewer Findings
P0: population conditional target ile per-instance/subgroup guarantee karıştırılmamalı. P0: aynı calibration üzerinde score-fit veya yeni policy search, Thm1in certified kümeden seçim izni değildir. P1: zero/low coverage; çok sayıda policy/metric için multiplicity. §3.2de kabul sayısı<25 eşiğini dışlamak paper deney kararıdır, evrensel sample-size kuralı değil.

### Pinned MEPS artifact — dar statik kontrol
Repo [aangelopoulos/ltt](https://github.com/aangelopoulos/ltt), commit 3ad7a64adad9f356e29f40e73935a6114f896396. Parent [MEPS source](https://github.com/aangelopoulos/ltt/blob/3ad7a64adad9f356e29f40e73935a6114f896396/experiments/meps/experiment.py) lines159–190 ve [concentration.py](https://github.com/aangelopoulos/ltt/blob/3ad7a64adad9f356e29f40e73935a6114f896396/core/concentration.py) lines127–131 okudu:
- line166 alpha+A*(squared_error-alpha) dönüşümü kullanılıyor. Bu dönüşüm, uygun loss koşullarında conditional risk nullına yukarıdaki eşdeğerliği sağlar; sırf ratio yazılmadı diye yanlış değildir. S8in dönüşümü koşullu hedefle ilişkilendiremediği yorumu bu analitik gerekçeyle sınırlandı.
- lines176–179 tüm tablonun observed maximumuna bölme, ardından cal/val ayırma; line189 test çağrısında alpha aynı. Sabit population bound/threshold-scaling ve split bağımsızlığını bunun sağladığı doğrulanmadı. Current artifact paper sürümü eşdeğerliği de UNVERIFIED.
- concentration.py HB p-değerini core.bounds içinden import ediyor; parent bound implementationının tümünü audit etmedi. Native MEPS deneyinin sonlu-örneklem geçerliliği bu kısa incelemeyle kabul veya reddedilmedi.
Bu nedenle MEPS scripti aynen explanation-risk benchmarkına kopyalanmayacak. Genel teorem için açık fixed bounded-loss contractı esas alınacak. Artifact gözlemleri LTT teoremini çürütmez. Kaynak hash/line snippets evidence/r03_ltt_code_check.json içinde; native kod çalıştırılmadı.

## Research Implications
H2 yeni-score+threshold veya generic LTT uygulamasından ibaret olamaz. Önce bağımsız bounded functional-loss, sabit policy family ve açık total-budget altında Bayes/learned-loss/direct-probe score + LTT nullı sınanmalı. Noisy loss sözcüğü otomatik gap değildir. Calibration randomness üstü violation frequency ile within-dataset risk CI ayrı raporlanmalı; finite test estimate ile oracle truth aynı değil.

## Open Questions
A3/A5 seçilen functional loss için hangi valid p-değeri, iid birimi, family/FWER ve positive-coverage sözleşmesini kullanacak? A4 pinned native artifact ile theorem-faithful adaptationı nasıl ayrı adlandıracak? Adaptive probing gerekmiyorsa bunun literatürünü genişletmeye gerek yok.

## Recommended Decision
Bounded independent-loss koşullarında güçlü generic nullı handoffa koy. Ham unbounded MSE, arbitrary subgroup/shift ve shared-probe selection için garanti iddia etme. Bu karar D019 kapsamında gereksinimdir; final deney dondurma veya novelty kararı değil.

## Next Actions
Agent3 contractı risk-event/quantifier/p-value tablosuyla tamamlasın; Agent4 native artifacti wrapperdan ayırsın ve split/probe tests önerisini sunsun. Bu belgede yeni benchmark veya algoritma çalıştırılmadı.
