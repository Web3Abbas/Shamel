# 08 — Questions for ISCO (أسئلة إلى شركة ISCO)

> Status: draft v1 · 2026-11-03 · Binding input: [`00-decisions.md`](00-decisions.md) §11 ("Owner confirmed they can
> contact ISCO. Design doc must include a precise question list"). Upstream reference:
> [`../upstream/shamel-api.md`](../upstream/shamel-api.md) (cited "U §x" and "Qnn").
> Sources: U §6.4 and §7, [`01-architecture.md`](01-architecture.md) §16, [`02-security.md`](02-security.md) §20.2–§20.3,
> [`03-api.md`](03-api.md) §27.3 (`I-n`), [`04-permissions-and-tokens.md`](04-permissions-and-tokens.md) §17.3,
> [`05-operations.md`](05-operations.md) §11.
>
> This document owns the **consolidated list of questions for ISCO** (Isra' Software & Computer, the vendor of Shamel
> Pro). It has 55 questions; 10 are marked **Priority**. It merges every unknown, assumption and open question that the
> design set raised about the upstream API.

---

## 0. How to use this document (internal, not for sending)

- **What to send:** §1 (cover message, Arabic then English), §2 (priority list) and §3 (questions). §0 and Appendix A
  are internal. The `Ref:` line under each question points to our own documents. It contains nothing confidential and
  may stay in or be deleted before sending.
- **Before sending:** fill the placeholders `[…]` in §1 and in ISCO-50 (our Shamel version, if known). Check ISCO's
  official Arabic company name for the salutation. Decide whether ISCO-53 (c) (possible commercial use later) should be
  asked now or in a separate, later conversation.
- **Stable ids:** questions are `ISCO-01` … `ISCO-55`. Other design documents cite them as "08 ISCO-nn". ISCO-54 and
  ISCO-55 were added later (from 01 §16.2) and sit in their topic groups (§3.13 and §3.2), so ids are not in document
  order there. Ids are never renumbered; a question added later takes the next free id, and a sub-item added later
  takes the next free letter. The older ids keep their meaning: `Qnn` (U §7), `I-n` (03 §27.3), "02 §20.2 #n",
  "04 §17.3 #n", and the retired `ISCO-1` … `ISCO-28` of an earlier draft of 01 §16.2. Appendix A maps every one of
  them to the question that now carries it.
- **Recording answers:** add `> **ISCO answer (YYYY-MM-DD):** …` under the question. Then update U §7 (mark the `Qnn`
  resolved) and the affected design document. Fields published as *(provisional)* (03 §3.4) may be renamed only before
  M1 GA.
- **What we can check without ISCO:** `bawaba upstream calibrate` against the live server measures HTTP methods, header
  casing, the effect of a second login and response sizes (01 §16, 02 §7.5). Those questions are still asked, because
  only ISCO can state the intended behaviour that stays stable across Shamel versions.
- **How the priority set was chosen:** the answer changes a design decision, protects accounting-data integrity or
  carries legal risk, and cannot be settled by observing a live server alone. It also covers the owner's examples in
  00 §11. Close runners-up: ISCO-34 (`image_path`), ISCO-51 (test database), ISCO-25 (salesman scoping).
- **Ref legend:** `Qnn` = U §7 item; `U §x` = upstream section; `I-n` = 03 §27.3; `0N §x` = design document N.

---

## 1. Cover message (رسالة التغطية)

### 1.1 Arabic (العربية)

<div dir="rtl" lang="ar">

**الموضوع: استفسارات فنية حول واجهة برمجة التطبيقات لبرنامج الشامل (Shamel Pro Web API)**

السادة شركة إسراء للبرمجيات والكمبيوتر (ISCO) المحترمين،

تحية طيبة وبعد،

نحن في [اسم الشركة] نستخدم برنامج الشامل للمحاسبة، ونعمل حالياً على بناء طبقة تكامل داخلية فوق واجهة برمجة التطبيقات الخاصة بالبرنامج (Shamel Pro Web API). تهدف هذه الطبقة إلى أن تتصل أدواتنا وأنظمتنا الداخلية بالشامل من خلال نقطة واحدة آمنة، مع صلاحيات محددة لكل أداة وسجلّ تدقيق كامل، دون أن تحتاج أي أداة إلى بيانات دخول الشامل أو إلى الاتصال بخادمه مباشرة. ولا تُجري هذه الطبقة أي تعديل على برنامج الشامل أو على قاعدة بياناته، وإنما تستخدم الواجهة البرمجية الرسمية فقط، ضمن صلاحيات المستخدمين الممنوحة لنا.

اعتمدنا في التصميم على دليل "التكامل مع برنامج الشامل للمحاسبة – API – العرض الفني"، ووجدناه واضحاً ومفيداً في معظمه. غير أن بعض النقاط لم يتطرق إليها الدليل أو تحتمل أكثر من تفسير، ونودّ التأكد منها قبل الاعتماد عليها في بيئة العمل الفعلية.

لذا نرجو التكرم بالإجابة عن الأسئلة المرفقة. وهي مرقّمة من ISCO-01 إلى ISCO-55، ومقسّمة حسب الموضوع، ومكتوبة باللغتين العربية والإنجليزية، ويرافق كل سؤال سطر قصير بالإنجليزية بعنوان "Why we ask" يوضّح سبب السؤال وأثره على عملنا. أما الأسئلة العشرة المعلّمة بكلمة "أولوية" فهي الأهم بالنسبة لنا، ونرجو البدء بها إن أمكن.

لا مانع لدينا من تلقّي الإجابات على مراحل، أو من ترتيب اجتماع فني قصير (حضورياً أو عن بُعد) إن كان ذلك أيسر لكم. كما نرجو إعلامنا إن كانت الإجابة عن بعض هذه الأسئلة تتطلب طلب خدمة أو اتفاقية دعم.

شاكرين لكم حسن تعاونكم، ومتطلعين إلى ردّكم.

وتفضلوا بقبول فائق الاحترام،

[الاسم]<br>
[المسمى الوظيفي] – [اسم الشركة]<br>
[البريد الإلكتروني / الهاتف]

</div>

### 1.2 English

**Subject: Technical questions about the Shamel Pro Web API**

Dear ISCO team,

We at [Company name] use the Shamel accounting software, and we are building an internal integration layer on top of
the Shamel Pro Web API. Its purpose is to let our internal tools and systems reach Shamel through one secure point,
with specific permissions for each tool and a complete audit log, so that no tool needs Shamel credentials or a direct
connection to the Shamel server. The layer does not modify Shamel or its database in any way. It uses only the official
Web API, within the permissions of the user accounts granted to us.

We based our design on the manual "Integration with the Shamel accounting program – API – technical presentation",
which we found clear and helpful for the most part. Some points, however, are not covered by the manual or can be read
in more than one way, and we would like to confirm them before we rely on them in production.

We would be grateful if you could answer the attached questions. They are numbered ISCO-01 to ISCO-55, grouped by topic
and written in Arabic and English. Each one has a short "Why we ask" line that explains its impact on our work. The ten
questions marked "Priority" matter most to us, so we would appreciate answers to those first.

We are happy to receive the answers in stages, or to arrange a short technical meeting (in person or online) if that is
easier for you. Please also let us know if answering some of these questions requires a service request or a support
agreement.

Thank you for your cooperation. We look forward to your reply.

Kind regards,

[Name]<br>
[Job title] – [Company name]<br>
[Email / phone]

---

## 2. Priority questions (الأسئلة ذات الأولوية)

Listed in document order.

| # | Id | Topic | الموضوع |
|---|---|---|---|
| 1 | ISCO-01 | Session token lifetime and concurrent sessions per user | مدة صلاحية رمز الجلسة والجلسات المتزامنة للمستخدم |
| 2 | ISCO-05 | HTTPS / TLS support | دعم HTTPS وTLS |
| 3 | ISCO-18 | Error response format, stable error codes, expired-token signal | صيغة استجابات الأخطاء ورموز الأخطاء الثابتة |
| 4 | ISCO-20 | Rate and concurrency limits, recommended parallel calls | حدود معدل الطلبات والطلبات المتزامنة |
| 5 | ISCO-21 | Pagination, truncation and large responses | تقسيم النتائج إلى صفحات والاستجابات الكبيرة |
| 6 | ISCO-22 | Semantics of `lastupdatedate` | دلالة المعامل `lastupdatedate` |
| 7 | ISCO-26 | Response of `/Files/GetSalesmen` | استجابة `/Files/GetSalesmen` |
| 8 | ISCO-43 | Duplicate prevention and the outcome of failed writes | منع التكرار ونتيجة عمليات الإدخال الفاشلة |
| 9 | ISCO-50 | Shamel version, API versioning and change notices | إصدار الشامل وإدارة إصدارات الواجهة البرمجية |
| 10 | ISCO-53 | Licensing: internal integration layer now, commercial use later | الترخيص: طبقة التكامل الداخلية حالياً والاستخدام التجاري مستقبلاً |

---

## 3. Questions (الأسئلة)

### 3.1 Authentication and sessions (المصادقة والجلسات)

#### ISCO-01 — Session token lifetime and concurrent sessions per user

**[Priority · أولوية]**

After a successful `/Main/Login`, how long does the returned `token` stay valid?

- (a) Is there a fixed (absolute) lifetime, an idle timeout, or both? What are the default values, and can they be
  configured?
- (b) Is the lifetime extended (sliding) each time the token is used?
- (c) If the same user logs in again (from the API, from the Shamel desktop program or from another device), does the
  earlier token stop working?
- (d) How many concurrent sessions may one user have? Can the same user be signed in to the desktop program and to the
  API at the same time?
- (e) Is a token bound to the client's IP address or to one connection, or can it be used from several machines?
- (f) Do tokens survive an IIS application-pool recycle or a server restart?

<div dir="rtl" lang="ar">

**مدة صلاحية رمز الجلسة وعدد الجلسات المتزامنة للمستخدم**

بعد نجاح طلب تسجيل الدخول `/Main/Login`، ما مدة صلاحية رمز الجلسة (`token`) الذي يُعاد؟

- أ. هل للرمز مدة صلاحية ثابتة (مطلقة)، أم مهلة تنتهي عند عدم الاستخدام، أم كلاهما؟ وما القيم الافتراضية؟ وهل يمكن تعديلها؟
- ب. هل تتجدد مدة الصلاحية تلقائياً مع كل استخدام للرمز؟
- ج. إذا سجّل المستخدم نفسه الدخول مرة أخرى (من الواجهة البرمجية، أو من برنامج الشامل المكتبي، أو من جهاز آخر)، هل يتوقف الرمز السابق عن العمل؟
- د. كم جلسة متزامنة يُسمح بها للمستخدم الواحد؟ وهل يمكن أن يكون المستخدم نفسه مسجّلاً في البرنامج المكتبي وفي الواجهة البرمجية في الوقت ذاته؟
- هـ. هل يرتبط الرمز بعنوان IP الخاص بالجهاز الطالب أو باتصال واحد، أم يمكن استخدامه من أكثر من جهاز؟
- و. هل يبقى الرمز صالحاً بعد إعادة تدوير مجمّع التطبيقات (Application Pool) في IIS أو بعد إعادة تشغيل الخادم؟

</div>

**Why we ask:** our layer shares one Shamel session per user across several servers and serialises logins; if a second
login ends the first session, or tokens are bound to an IP address, all calls for that user must go through a single
session holder, and we must avoid repeated logins.

<sub>Ref: Q14 · 02 §20.2 #3 · 02 §20.3 · 02 §7.5 · 01 §7.1 · 01 §16 · 00 §11</sub>

#### ISCO-02 — Logout and server-side revocation

- (a) Is there a logout call that invalidates a token?
- (b) Can an administrator end all active sessions of a user from inside Shamel?
- (c) Does changing a user's password, disabling the user or removing their API permission immediately invalidate the
  tokens that were already issued?

<div dir="rtl" lang="ar">

**تسجيل الخروج وإلغاء الجلسات من جهة الخادم**

- أ. هل توجد عملية لتسجيل الخروج تُبطل رمز الجلسة؟
- ب. هل يستطيع مدير النظام إنهاء جميع الجلسات النشطة لمستخدم معيّن من داخل الشامل؟
- ج. هل يؤدي تغيير كلمة مرور المستخدم، أو إيقافه، أو سحب صلاحية الواجهة البرمجية منه، إلى إبطال الرموز الصادرة سابقاً فوراً؟

</div>

**Why we ask:** if a credential is ever exposed, our incident procedure needs a reliable way to end existing Shamel
sessions, not only to change the password.

<sub>Ref: Q14 · 02 §20.2 #3 · 02 §17 (IR-3) · 01 §16</sub>

#### ISCO-03 — Login request and failure responses

- (a) On later requests, should the `username` header contain the login name sent to `/Main/Login`, or `userCode` or
  `userId` from `AuthResult`?
- (b) What exactly does `/Main/Login` return for a wrong password, an unknown user, a disabled user and a locked user:
  HTTP 200 with `success=false`, or HTTP 500?
- (c) Can a user whose `userIsDisabled` is `true` still receive a usable token?
- (d) Is there an account-lockout policy after repeated failed logins (threshold, duration, how to unlock)?

<div dir="rtl" lang="ar">

**تفاصيل طلب تسجيل الدخول واستجابات الفشل**

- أ. في الطلبات اللاحقة، هل يجب أن تحتوي الترويسة (header) `username` على اسم الدخول نفسه المرسل إلى `/Main/Login`، أم على `userCode` أو `userId` من نتيجة `AuthResult`؟
- ب. ماذا تُعيد `/Main/Login` تحديداً عند إدخال كلمة مرور خاطئة، أو اسم مستخدم غير موجود، أو مستخدم موقوف، أو مستخدم مقفل: استجابة HTTP 200 مع `success=false`، أم HTTP 500؟
- ج. هل يمكن لمستخدم قيمة `userIsDisabled` لديه `true` أن يحصل على رمز جلسة صالح للاستخدام؟
- د. هل توجد سياسة لقفل الحساب بعد عدد من محاولات الدخول الفاشلة (عدد المحاولات، ومدة القفل، وطريقة فكّه)؟

</div>

**Why we ask:** a wrong password in our configuration must not lock the service account that all our tools use; we
must tell "wrong credentials" apart from "Shamel is unavailable" and stop retrying in time.

<sub>Ref: Q15 · Q16 · 01 §16 (account lockout)</sub>

#### ISCO-04 — API users and their permissions inside Shamel

- (a) Are API users the same accounts as Shamel desktop users (same password), or a separate kind of account?
- (b) Can API access be enabled or disabled per user?
- (c) Can we create an API-only user that cannot sign in to the desktop program?
- (d) Does the API enforce the user permissions defined inside Shamel (for example read-only, allowed voucher types,
  allowed stores, hidden cost prices)? If yes, which permissions apply to which endpoints?

<div dir="rtl" lang="ar">

**مستخدمو الواجهة البرمجية وصلاحياتهم داخل الشامل**

- أ. هل مستخدمو الواجهة البرمجية هم أنفسهم مستخدمو برنامج الشامل المكتبي (بكلمة المرور نفسها)، أم هم نوع مستقل من الحسابات؟
- ب. هل يمكن تفعيل صلاحية الوصول إلى الواجهة البرمجية أو إيقافها لكل مستخدم على حدة؟
- ج. هل يمكن إنشاء مستخدم مخصص للواجهة البرمجية فقط، لا يستطيع الدخول إلى البرنامج المكتبي؟
- د. هل تطبّق الواجهة البرمجية صلاحيات المستخدم المعرّفة داخل الشامل (مثل: القراءة فقط، وأنواع السندات المسموحة، والمستودعات المسموحة، وإخفاء أسعار الكلفة)؟ وإن كان الأمر كذلك، فأيّ الصلاحيات تنطبق على أيّ نقاط النهاية (endpoints)؟

</div>

**Why we ask:** we want a least-privilege Shamel account as a second line of defence beneath our own token
permissions, and we need to know whether the API applies or ignores Shamel's own restrictions.

<sub>Ref: 02 §20.2 #5 · 04 §17.3 #7</sub>

### 3.2 Transport security and IIS hosting (أمان الاتصال واستضافة IIS)

#### ISCO-05 — HTTPS / TLS support

**[Priority · أولوية]**

- (a) Does the Shamel Web API support HTTPS?
- (b) Which certificate options are supported (a certificate from a public certificate authority, an internal or
  self-signed certificate)? Who installs and renews it?
- (c) Which TLS versions are supported (TLS 1.2, TLS 1.3)?
- (d) Can plain HTTP be disabled completely once HTTPS is enabled?

<div dir="rtl" lang="ar">

**دعم HTTPS وTLS**

- أ. هل تدعم واجهة الشامل البرمجية بروتوكول HTTPS؟
- ب. ما خيارات الشهادات المدعومة (شهادة صادرة عن جهة إصدار عامة، أو شهادة داخلية أو موقّعة ذاتياً)؟ ومن يتولى تركيبها وتجديدها؟
- ج. ما إصدارات TLS المدعومة (TLS 1.2 وTLS 1.3)؟
- د. هل يمكن تعطيل HTTP غير المشفّر بالكامل بعد تفعيل HTTPS؟

</div>

**Why we ask:** without HTTPS the Shamel password (at login) and every session token cross the office network in clear
text; the answer decides whether our connector must run on the Shamel server itself.

<sub>Ref: Q11 · 02 §20.2 #1 · 01 §16 · 00 §11</sub>

#### ISCO-06 — IIS authentication mode

Does the API site use IIS Windows Authentication (NTLM/Negotiate), Basic authentication or client certificates
anywhere? Or is it anonymous at the IIS level and protected only by Shamel's `username` and `token` headers? Does ISCO
require or recommend any of these options?

<div dir="rtl" lang="ar">

**نمط المصادقة في IIS**

هل يستخدم موقع الواجهة البرمجية في IIS مصادقة ويندوز (NTLM/Negotiate) أو المصادقة الأساسية (Basic) أو شهادات العميل في أي موضع؟ أم أنه مفتوح (Anonymous) على مستوى IIS ومحميّ فقط بالترويستين `username` و`token` الخاصتين بالشامل؟ وهل تشترطون أو توصون بأيٍّ من هذه الخيارات؟

</div>

**Why we ask:** if Windows Authentication is enabled, our client must authenticate at the IIS layer as well, otherwise
every call fails before it reaches Shamel.

<sub>Ref: 02 §20.2 #4</sub>

#### ISCO-07 — Network exposure, base address and installation layout

- (a) What is the default structure of the API's base address (port, virtual directory or base path)? Is the API a
  separate IIS site from the other Shamel components?
- (b) Can the API site be bound to the loopback interface (localhost) only, or restricted by IIS IP rules, without
  breaking anything?
- (c) Does any other component (the desktop program, mobile apps, other ISCO products) need to reach the API over the
  LAN?
- (d) Must the API run on the same server as the Shamel database?

<div dir="rtl" lang="ar">

**إتاحة الخدمة على الشبكة والعنوان الأساسي وطريقة التركيب**

- أ. ما البنية الافتراضية للعنوان الأساسي للواجهة البرمجية (المنفذ، والمجلد الافتراضي أو المسار الأساسي)؟ وهل الواجهة موقع مستقل في IIS عن مكوّنات الشامل الأخرى؟
- ب. هل يمكن ربط موقع الواجهة البرمجية بالواجهة المحلية للجهاز نفسه فقط (localhost)، أو تقييده بقواعد عناوين IP في IIS، دون أن يتعطّل أي شيء؟
- ج. هل يحتاج أي مكوّن آخر (البرنامج المكتبي، أو تطبيقات الهاتف، أو منتجات ISCO الأخرى) إلى الوصول إلى الواجهة البرمجية عبر الشبكة المحلية؟
- د. هل يجب أن تعمل الواجهة البرمجية على الخادم نفسه الذي توجد عليه قاعدة بيانات الشامل؟

</div>

**Why we ask:** we plan to install a small agent next to Shamel and, if possible, make the API reachable only from that
machine, so that it is not exposed even on the office network.

<sub>Ref: Q11 · 02 §20.2 #6 · 02 §7.9</sub>

#### ISCO-08 — Logging of requests on the Shamel side

Do Shamel or its IIS configuration log request headers or bodies (which would include the `username` and `token`
headers, and the password at login)? Where are these logs stored, for how long, and can header logging be disabled or
masked?

<div dir="rtl" lang="ar">

**تسجيل الطلبات من جهة الشامل**

هل يسجّل الشامل أو إعدادات IIS الخاصة به ترويسات الطلبات أو محتواها (بما في ذلك الترويستان `username` و`token`، وكلمة المرور عند تسجيل الدخول)؟ وأين تُحفظ هذه السجلات، وما مدة الاحتفاظ بها؟ وهل يمكن تعطيل تسجيل الترويسات أو إخفاء قيمها؟

</div>

**Why we ask:** session tokens written to log files are a credential leak; we need to know whether our IT must protect
or rotate those logs.

<sub>Ref: 02 §20.2 #7</sub>

#### ISCO-09 — Hardening of the Shamel server

Which network services must stay reachable on the Shamel server (SQL Server, file shares, remote desktop, licensing
services, desktop clients)? Must SQL Server be reachable from the LAN for the desktop program to work? Do you have a
recommended firewall configuration or a hardening guide?

<div dir="rtl" lang="ar">

**تحصين خادم الشامل**

ما خدمات الشبكة التي يجب أن تبقى متاحة على خادم الشامل (SQL Server، ومشاركة الملفات، وسطح المكتب البعيد، وخدمات الترخيص، وأجهزة البرنامج المكتبي)؟ وهل يلزم أن يكون SQL Server متاحاً عبر الشبكة المحلية لكي يعمل البرنامج المكتبي؟ وهل لديكم إعدادات جدار حماية موصى بها أو دليل لتحصين الخادم؟

</div>

**Why we ask:** our deployment guide will tell our IT what to close, and it must not block anything Shamel needs.

<sub>Ref: 02 §20.2 #10</sub>

#### ISCO-10 — Security updates and vulnerability reporting

- (a) How are security fixes for Shamel and its Web API delivered, and how often?
- (b) Is there a contact for reporting a suspected vulnerability, or a security incident that affects Shamel
  credentials?
- (c) Do you publish security advisories?

<div dir="rtl" lang="ar">

**التحديثات الأمنية والإبلاغ عن الثغرات**

- أ. كيف تُوفَّر الإصلاحات الأمنية لبرنامج الشامل وواجهته البرمجية، وما وتيرتها؟
- ب. هل توجد جهة اتصال للإبلاغ عن ثغرة أمنية محتملة، أو عن حادث أمني يمسّ بيانات الدخول إلى الشامل؟
- ج. هل تنشرون نشرات أو تنبيهات أمنية؟

</div>

**Why we ask:** our incident procedure includes notifying ISCO if Shamel credentials or the Shamel server are ever
exposed.

<sub>Ref: 02 §20.2 #8 · 02 §17 (IR-6)</sub>

#### ISCO-11 — Proxy compatibility, request size and compression

- (a) `Voucher/GetVoucher` uses a header name with an underscore (`voucher_code`), which many reverse proxies drop by
  default. Is there an alternative name or form (for example `vouchercode`, or a query-string parameter)?
- (b) `GetVouchers` and `GetExtraVouchers` send JSON in the `filters` header. Is there a size limit for header values,
  and is there an alternative (query string or form field)?
- (c) What is the maximum request size accepted for the `obj` form posts?
- (d) Does the API support gzip-compressed responses (`Accept-Encoding: gzip`)?
- (e) Are HTTP keep-alive connections supported?

<div dir="rtl" lang="ar">

**التوافق مع الخوادم الوسيطة وحجم الطلب والضغط**

- أ. تستخدم `Voucher/GetVoucher` ترويسة يحتوي اسمها على شرطة سفلية (`voucher_code`)، وكثير من الخوادم الوسيطة (reverse proxy) تحذف مثل هذه الترويسات افتراضياً. هل يوجد اسم بديل أو طريقة بديلة (مثل `vouchercode`، أو معامل في عنوان الطلب)؟
- ب. ترسل `GetVouchers` و`GetExtraVouchers` بيانات JSON داخل الترويسة `filters`. هل يوجد حدّ لحجم قيمة الترويسة؟ وهل توجد طريقة بديلة (عنوان الطلب أو حقل نموذج)؟
- ج. ما الحد الأقصى لحجم الطلب المقبول في طلبات الإدخال التي تحمل الحقل `obj`؟
- د. هل تدعم الواجهة ضغط الاستجابات بصيغة gzip (`Accept-Encoding: gzip`)؟
- هـ. هل تدعم الواجهة إبقاء الاتصال مفتوحاً (HTTP keep-alive)؟

</div>

**Why we ask:** these details decide whether a proxy or firewall in front of Shamel can silently break voucher lookups,
and how much bandwidth large lists will use.

<sub>Ref: Q6 · Q7 · 01 §16 (gzip)</sub>

#### ISCO-55 — Endpoints not described in the manual

- (a) Apart from the endpoints in the manual and `/Voucher/Post` (ISCO-50 (d)), does the API site expose other
  endpoints? For example: older versions of documented endpoints, update or delete operations, administrative or
  diagnostic endpoints, or generated help pages (ASP.NET Web API Help, Swagger). Please list them with their purpose.
- (b) Do any of them change or delete data, or answer without a valid `token`?
- (c) Can they be disabled, or blocked in IIS, without affecting the Shamel desktop program or other ISCO products?

<div dir="rtl" lang="ar">

**نقاط نهاية غير مذكورة في الدليل**

- أ. باستثناء نقاط النهاية الواردة في الدليل و`/Voucher/Post` (انظر ISCO-50، البند د)، هل يتيح موقع الواجهة البرمجية نقاط نهاية أخرى؟ ومن أمثلة ذلك: إصدارات أقدم من نقاط النهاية الموثّقة، أو عمليات تعديل أو حذف، أو نقاط نهاية إدارية أو تشخيصية، أو صفحات مساعدة مولَّدة تلقائياً (مثل ASP.NET Web API Help أو Swagger). نرجو تزويدنا بقائمة بها مع الغرض من كل منها.
- ب. هل يعدّل أيٌّ منها البيانات أو يحذفها، أو يستجيب دون رمز جلسة (`token`) صالح؟
- ج. هل يمكن تعطيلها، أو حجبها في IIS، دون التأثير على برنامج الشامل المكتبي أو على منتجات ISCO الأخرى؟

</div>

**Why we ask:** our layer forwards only the documented endpoints we have reviewed, but any other endpoint on the API
site stays reachable to whoever can reach the Shamel server; we want to block what we do not use, and to learn about
any endpoint we should use instead.

<sub>Ref: Q22 · 01 §6.5 · 01 §16</sub>

### 3.3 Request and response conventions (قواعد الطلبات والاستجابات)

#### ISCO-12 — Exact HTTP method per endpoint

The manual names the HTTP method of only a few endpoints. Please confirm or correct the method we assumed for each one
(last column), and tell us whether other methods are rejected.

| # | Endpoint | Our assumption | Correct method (ISCO) |
|---|---|---|---|
| 1 | `/Main/Login` | POST (stated in the manual) | |
| 2–9 | `/Files/GetCurrencies`, `/Files/GetCurrencyRates`, `/Files/GetBanks`, `/Files/GetBanksBranchs`, `/Files/GetCities`, `/Files/GetStores`, `/Files/GetPriceClasses`, `/Files/GetSalesmen` | GET | |
| 10 | `/Customer/GetCustomers` | GET | |
| 11 | `/Customer/GetCustomerBalances` | GET | |
| 12 | `/Customer/Post` | POST (stated) | |
| 13 | `/Customer/GetCustomerPricesAsRows` | GET | |
| 14 | `/Item/GetItems` | GET | |
| 15 | `/Item/GetItemsStores` | GET | |
| 16 | `/Item/getItemDetails` | GET | |
| 17 | `/Item/GetItemsGroups` | GET | |
| 18 | `/Item/GetItemsCatalog` | GET | |
| 19 | `/Item/GetItemsSerials` | GET | |
| 20 | `/Item/Post` | POST (stated) | |
| 21 | `/Report/GetLastPriceReport` | GET | |
| 22 | `/Report/GetAccountsheet` | POST, form field `obj` | |
| 23 | `/Voucher/Post2` | POST (stated) | |
| 24 | `/Voucher/GetDelivery` | GET | |
| 25 | `/Voucher/GetStatus` | GET | |
| 26 | `/Voucher/GetVoucher` | GET | |
| 27 | `/Voucher/GetVouchers` | GET | |
| 28 | `/Voucher/GetExtraVouchers` | GET | |
| 29 | `/CostCenter/Post` | POST (stated) | |
| 30 | `/CostCenter/GetCostCenterAccountsheet` | POST, form field `filters` | |

<div dir="rtl" lang="ar">

**طريقة HTTP الصحيحة لكل نقطة نهاية**

لا يذكر الدليل طريقة HTTP إلا لعدد قليل من نقاط النهاية. نرجو تأكيد الطريقة التي افترضناها لكل منها في الجدول أعلاه أو تصحيحها (في العمود الأخير)، وإفادتنا إن كانت الطرق الأخرى تُرفض.

</div>

**Why we ask:** our client is driven by a per-endpoint table; a wrong method makes every call to that endpoint fail, and
we will not find the right method for writes by trial and error on live data.

<sub>Ref: Q4 · 01 §16 (assumption 2)</sub>

#### ISCO-13 — Case sensitivity of header names and paths

The manual spells the same parameter in different ways: `itemCode` (GetItems, getItemDetails), `itemcode`
(GetItemsStores) and `ItemCode` (GetLastPriceReport).

- (a) Are header names matched without regard to letter case, so that any spelling works?
- (b) Are paths case-insensitive (for example `/Item/getItemDetails` and `/Item/GetItemDetails`)?
- (c) Four paths are printed without a leading slash (`Customer/GetCustomerPricesAsRows`, `Voucher/GetVoucher`,
  `Voucher/GetVouchers`, `Voucher/GetExtraVouchers`). We assume they follow the same `/Controller/Action` form as the
  others. Is that correct?

<div dir="rtl" lang="ar">

**حساسية أسماء الترويسات والمسارات لحالة الأحرف**

يكتب الدليل المعامل نفسه بأشكال مختلفة: `itemCode` (في GetItems وgetItemDetails)، و`itemcode` (في GetItemsStores)، و`ItemCode` (في GetLastPriceReport).

- أ. هل تُطابَق أسماء الترويسات دون تمييز بين الأحرف الكبيرة والصغيرة، بحيث تعمل أيّ صيغة؟
- ب. هل المسارات غير حساسة لحالة الأحرف (مثل `/Item/getItemDetails` و`/Item/GetItemDetails`)؟
- ج. طُبعت أربعة مسارات دون الشرطة المائلة في بدايتها (`Customer/GetCustomerPricesAsRows` و`Voucher/GetVoucher` و`Voucher/GetVouchers` و`Voucher/GetExtraVouchers`)، ونفترض أنها بالصيغة `/Controller/Action` نفسها كبقية المسارات. هل هذا صحيح؟

</div>

**Why we ask:** our HTTP library normalises the case of header names; if Shamel matches names case-sensitively, we
must send each name exactly as printed.

<sub>Ref: Q5 · Q10</sub>

#### ISCO-14 — Header values: booleans, empty values and Arabic text

- (a) Which values are accepted for boolean headers such as `getBalance`, `getAll` and `getCustomerBalance` (`true`,
  `True`, `1`)? Is an absent header the same as `false`?
- (b) Is an empty header value treated like an absent header (for example an empty `lastupdatedate` or
  `customerCode`)?
- (c) How should non-Latin values (Arabic codes or names) be sent in headers, for example in `filters` or `code`? Is a
  particular encoding expected (UTF-8, percent-encoding)?
- (d) Are responses always UTF-8 encoded JSON?

<div dir="rtl" lang="ar">

**قيم الترويسات: القيم المنطقية والقيم الفارغة والنصوص العربية**

- أ. ما القيم المقبولة للترويسات المنطقية مثل `getBalance` و`getAll` و`getCustomerBalance` (`true` أو `True` أو `1`)؟ وهل غياب الترويسة يعادل القيمة `false`؟
- ب. هل تُعامَل الترويسة ذات القيمة الفارغة معاملة الترويسة الغائبة (مثل `lastupdatedate` أو `customerCode` الفارغتين)؟
- ج. كيف يجب إرسال القيم غير اللاتينية (رموز أو أسماء عربية) داخل الترويسات، مثل `filters` أو `code`؟ وهل يُتوقَّع ترميز معيّن (UTF-8، أو الترميز بالنسبة المئوية)؟
- د. هل الاستجابات دائماً بصيغة JSON مرمّزة بـ UTF-8؟

</div>

**Why we ask:** a value that Shamel silently ignores would turn a filtered request into a full download, or return the
wrong records.

<sub>Ref: Q8 · Q48</sub>

#### ISCO-15 — Filter matching rules

For the filter headers `code`, `vatreg`, `customerCode`, `itemCode`, `serial`, `barcode`, `model`, `customer` and
`store`: is matching exact, by prefix, or partial (contains)? Is it case-sensitive, and are surrounding spaces trimmed?
Can a single-record filter such as `code` on `GetCustomers` ever return more than one record?

<div dir="rtl" lang="ar">

**قواعد المطابقة في معاملات التصفية**

بالنسبة لترويسات التصفية `code` و`vatreg` و`customerCode` و`itemCode` و`serial` و`barcode` و`model` و`customer` و`store`: هل المطابقة تامة، أم على بداية القيمة، أم جزئية (تحتوي على القيمة)؟ وهل هي حساسة لحالة الأحرف، وهل تُحذف المسافات الزائدة؟ وهل يمكن لمعامل مخصص لسجل واحد، مثل `code` في `GetCustomers`، أن يُعيد أكثر من سجل؟

</div>

**Why we ask:** we limit each token to specific customers, items and stores; a partial match could return records the
caller may not see, so we must know Shamel's exact behaviour.

<sub>Ref: Q19</sub>

#### ISCO-16 — Encoding of write requests

- (a) For the `obj` and `filters` form posts, is `Content-Type: application/x-www-form-urlencoded` with UTF-8 correct?
  Is `multipart/form-data`, or a raw JSON body (`application/json`), also accepted?
- (b) Are JSON property names inside `obj` matched case-sensitively?
- (c) Are unknown properties ignored or rejected?
- (d) Must numbers be JSON numbers, or are numeric strings accepted?

<div dir="rtl" lang="ar">

**ترميز طلبات الإدخال**

- أ. في الطلبات التي تحمل الحقل `obj` أو `filters`، هل الصحيح استخدام `Content-Type: application/x-www-form-urlencoded` مع ترميز UTF-8؟ وهل تُقبل أيضاً صيغة `multipart/form-data` أو إرسال JSON مباشرة (`application/json`)؟
- ب. هل تُطابَق أسماء الخصائص داخل JSON في `obj` مع مراعاة حالة الأحرف؟
- ج. هل تُتجاهَل الخصائص غير المعروفة أم تُرفض؟
- د. هل يجب أن تكون الأرقام أرقاماً في JSON، أم تُقبل الأرقام المكتوبة كنصوص؟

</div>

**Why we ask:** an encoding mistake on a voucher post can create a wrong accounting record that the API cannot update
or delete.

<sub>Ref: Q9 · 02 §11.2</sub>

#### ISCO-17 — Response JSON conventions

- (a) Are response property names exactly as in the manual's C# classes (same case, for example `VATReg`,
  `sale_parice1`), or converted (for example to camelCase)?
- (b) For empty values, do you return `null`, an empty string or `0`, or do you omit the property?
- (c) Is JSON always returned, or can the API return XML depending on the `Accept` header?
- (d) Is the field order stable, so that two identical calls return identical bodies when no data changed?
- (e) Are decimal amounts rounded to a fixed number of decimal places?
- (f) Is every JSON response, including error responses, sent with `Content-Type: application/json` (with or without
  `charset=utf-8`)? Or can JSON arrive labelled as `text/html`, `text/plain` or another type?

<div dir="rtl" lang="ar">

**قواعد صيغة JSON في الاستجابات**

- أ. هل أسماء الخصائص في الاستجابة مطابقة تماماً لأسماء الحقول في أصناف C# الواردة في الدليل (بحالة الأحرف نفسها، مثل `VATReg` و`sale_parice1`)، أم يتم تحويلها (مثلاً إلى صيغة camelCase)؟
- ب. عند خلوّ القيمة، هل تُعيدون `null` أم نصاً فارغاً أم `0`، أم تُحذف الخاصية من الاستجابة؟
- ج. هل تُعاد الاستجابة بصيغة JSON دائماً، أم قد تُعاد بصيغة XML بحسب الترويسة `Accept`؟
- د. هل ترتيب الحقول ثابت، بحيث يُعيد استدعاءان متطابقان المحتوى نفسه تماماً إذا لم تتغير البيانات؟
- هـ. هل تُقرَّب المبالغ العشرية إلى عدد ثابت من المنازل العشرية؟
- و. هل تُرسَل كل استجابة JSON، بما فيها استجابات الأخطاء، مع الترويسة `Content-Type: application/json` (مع `charset=utf-8` أو بدونها)؟ أم قد تصل بيانات JSON موسومة بنوع آخر مثل `text/html` أو `text/plain`؟

</div>

**Why we ask:** our decoders and our test server mirror your exact field names; stable output also lets us store
identical audit records only once. We treat a response that is not labelled as JSON as an error.

<sub>Ref: Q12 · Q46 · I-19 · 01 §7.4 · 05 §11 (assumption 1 and stable-serialisation question)</sub>

### 3.4 Errors (الأخطاء)

#### ISCO-18 — Format of error responses and stable error codes

**[Priority · أولوية]**

The manual says that every error returns HTTP 500 "with the error details".

- (a) What is the exact body format of an error response (JSON, plain text, HTML)? Please share an example.
- (b) Is there a stable error code or error number, or only free text? If only text, is it in Arabic, English or both,
  and does it change between versions?
- (c) Please give the exact response for an expired or invalid token, so that we can detect it reliably and log in
  again.
- (d) Can error details include internal information (stack traces, SQL statements, file paths, server names)? Can
  detailed errors be switched off in production?
- (e) Do other HTTP status codes ever occur (for example 400, 401, 404)?

<div dir="rtl" lang="ar">

**صيغة استجابات الأخطاء ورموز الأخطاء الثابتة**

يذكر الدليل أن أي خطأ يُعيد الحالة HTTP 500 "مع تفاصيل الخطأ".

- أ. ما الصيغة الدقيقة لمحتوى استجابة الخطأ (JSON، أو نص عادي، أو HTML)؟ نرجو تزويدنا بمثال.
- ب. هل يوجد رمز أو رقم خطأ ثابت، أم نص حرّ فقط؟ وإن كان نصاً فقط، فهل هو بالعربية أم بالإنجليزية أم بكلتيهما؟ وهل يتغيّر بين الإصدارات؟
- ج. نرجو تزويدنا بالاستجابة الدقيقة عند استخدام رمز جلسة منتهي الصلاحية أو غير صالح، لكي نكتشف ذلك بدقة ونعيد تسجيل الدخول.
- د. هل يمكن أن تتضمن تفاصيل الخطأ معلومات داخلية (مثل تتبّع المكدّس stack trace، أو جمل SQL، أو مسارات ملفات، أو أسماء خوادم)؟ وهل يمكن إيقاف عرض هذه التفاصيل في بيئة التشغيل الفعلية؟
- هـ. هل تظهر أحياناً رموز حالة HTTP أخرى (مثل 400 أو 401 أو 404)؟

</div>

**Why we ask:** every failure looks the same at HTTP level; to give our tools correct, safe error messages (and never
pass internal details on), we must tell an expired session, a validation error, a missing record and a server fault
apart.

<sub>Ref: Q1 · Q14 · 01 §16 · 01 §7.5 · 02 §5.6 · 00 §11</sub>

#### ISCO-19 — Business errors on writes

- (a) When does a write return HTTP 200 with `Success=false`, and when does it return HTTP 500?
- (b) In `/Voucher/Post2`, does `ErrorMessage` (a list) contain one entry per validation problem?
- (c) Could you share the list of validation messages that the write endpoints can return (for example unknown
  customer, unknown item, stopped customer, insufficient stock, duplicate code, closed period), ideally with stable
  codes?

<div dir="rtl" lang="ar">

**أخطاء العمل في عمليات الإدخال**

- أ. متى تُعيد عملية الإدخال الحالة HTTP 200 مع `Success=false`، ومتى تُعيد HTTP 500؟
- ب. في `/Voucher/Post2`، هل تحتوي `ErrorMessage` (وهي قائمة) على عنصر لكل مشكلة في التحقق من البيانات؟
- ج. هل يمكنكم تزويدنا بقائمة رسائل التحقق التي قد تُعيدها نقاط الإدخال (مثل: زبون غير موجود، صنف غير موجود، زبون موقوف، كمية غير كافية، رقم مكرر، فترة مغلقة)، ويُفضَّل أن تكون مع رموز ثابتة؟

</div>

**Why we ask:** we translate Shamel rejections into documented, bilingual error codes for our tools, and that mapping
needs the real list of messages.

<sub>Ref: Q2 · Q3 · I-6 · 03 §22.3</sub>

### 3.5 Load, limits and large responses (الأحمال والحدود والاستجابات الكبيرة)

#### ISCO-20 — Rate and concurrency limits

**[Priority · أولوية]**

- (a) Does the API enforce any rate limit or concurrency limit (per user, per IP address, global)?
- (b) What is the recommended maximum number of parallel requests, and of requests per minute, for a typical server?
- (c) Do heavy API reads (for example the full item or customer list) slow down Shamel desktop users or lock their
  tables?
- (d) Which endpoints are expensive, and should any of them be avoided during working hours?
- (e) What is the server-side request timeout?

<div dir="rtl" lang="ar">

**حدود معدل الطلبات والطلبات المتزامنة**

- أ. هل تفرض الواجهة البرمجية أي حدّ لمعدل الطلبات أو لعدد الطلبات المتزامنة (لكل مستخدم، أو لكل عنوان IP، أو بشكل عام)؟
- ب. ما الحد الأقصى الموصى به لعدد الطلبات المتوازية، ولعدد الطلبات في الدقيقة، على خادم نموذجي؟
- ج. هل تؤدي عمليات القراءة الكبيرة عبر الواجهة (مثل قائمة الأصناف أو الزبائن كاملة) إلى إبطاء عمل مستخدمي البرنامج المكتبي أو إلى قفل الجداول لديهم؟
- د. ما نقاط النهاية المكلفة من حيث الأداء؟ وهل يُفضَّل تجنّب بعضها خلال ساعات العمل؟
- هـ. ما مهلة انتهاء الطلب (timeout) من جهة الخادم؟

</div>

**Why we ask:** our layer queues requests behind a global cap (currently a conservative 8 in parallel) so that Shamel
is never overloaded; we want to size that cap from your figures, not by experimenting on the live system.

<sub>Ref: Q47 · 02 §20.2 #9 · 01 §16 · 01 §7.6 · 00 §11</sub>

#### ISCO-21 — Pagination and large responses

**[Priority · أولوية]**

The list endpoints return all records in one response.

- (a) Is there any hidden server-side limit, maximum row count or truncation for large results?
- (b) Is pagination (page and size, or offset and limit) supported, even if undocumented, or is it planned?
- (c) What response sizes should we expect from `GetItems`, `GetCustomers`, `GetItemsStores`,
  `GetCustomerPricesAsRows`, `GetItemsCatalog` and `GetItemsSerials` with tens of thousands of records, and from
  `GetVouchers` over a wide date range?
- (d) Is there a maximum date range for `GetVouchers`, `GetExtraVouchers` and the two account-statement reports?
- (e) Apart from pagination, do any list endpoints accept other undocumented parameters, for example a maximum number
  of rows, a sort order or a selection of fields?

<div dir="rtl" lang="ar">

**تقسيم النتائج إلى صفحات والاستجابات الكبيرة**

تُعيد نقاط النهاية الخاصة بالقوائم جميع السجلات في استجابة واحدة.

- أ. هل يوجد من جهة الخادم أي حدّ خفي، أو عدد أقصى للسجلات، أو اقتطاع للنتائج الكبيرة؟
- ب. هل يتوفر تقسيم النتائج إلى صفحات (رقم الصفحة وحجمها، أو الإزاحة والحد الأقصى) ولو بشكل غير موثق، أو هل هو مخطط له؟
- ج. ما أحجام الاستجابة المتوقعة من `GetItems` و`GetCustomers` و`GetItemsStores` و`GetCustomerPricesAsRows` و`GetItemsCatalog` و`GetItemsSerials` عندما يبلغ عدد السجلات عشرات الآلاف، ومن `GetVouchers` عند طلب فترة زمنية طويلة؟
- د. هل يوجد حدّ أقصى للفترة الزمنية في `GetVouchers` و`GetExtraVouchers` وفي تقريرَي كشف الحساب؟
- هـ. بالإضافة إلى تقسيم النتائج إلى صفحات، هل تقبل أيٌّ من نقاط النهاية الخاصة بالقوائم معاملات أخرى غير موثّقة، مثل حدّ أقصى لعدد السجلات، أو ترتيب النتائج، أو اختيار الحقول المطلوبة؟

</div>

**Why we ask:** silent truncation would make our data wrong without any error, and the sizes decide our timeouts and
memory limits.

<sub>Ref: Q13 · 02 §20.2 #9 · 01 §16 · I-8 · 05 §11 · 00 §11</sub>

### 3.6 Incremental sync, dates and change detection (المزامنة التدريجية والتواريخ ورصد التغييرات)

#### ISCO-22 — Semantics of `lastupdatedate`

**[Priority · أولوية]**

`GetCustomers`, `GetItems` and `GetItemsStores` accept the `lastupdatedate` header ("get all … that updated after
lastupdatedate").

- (a) Is the value date-only (`yyyy-MM-dd`), or is a date and time accepted (in which format)?
- (b) Is the comparison "after" (exclusive) or "on or after" (inclusive)? With a date-only value, are changes made
  earlier on the same day returned?
- (c) In which timezone is the last-update time stored and compared (server local time, UTC)?
- (d) Which changes update a customer's last-update time: edits to the customer card only, or also balance changes
  from new vouchers, contacts, classifications and the stopped flag?
- (e) Which changes update an item's last-update time: price changes, stopped or paused changes, new barcodes?
- (f) For `GetItemsStores`: do stock movements from vouchers (sales, purchases, transfers, stock-taking) update it, so
  that it returns only the rows whose quantity changed?
- (g) Are deleted records ever reported?

<div dir="rtl" lang="ar">

**دلالة المعامل `lastupdatedate`**

تقبل نقاط النهاية `GetCustomers` و`GetItems` و`GetItemsStores` الترويسة `lastupdatedate` (أي إرجاع السجلات "التي عُدّلت بعد lastupdatedate").

- أ. هل القيمة تاريخ فقط (`yyyy-MM-dd`)، أم يُقبل التاريخ مع الوقت (وبأي صيغة)؟
- ب. هل المقارنة "بعد" التاريخ (غير شاملة) أم "في التاريخ نفسه أو بعده" (شاملة)؟ وعند إرسال تاريخ فقط، هل تُعاد التعديلات التي تمّت في وقت سابق من اليوم نفسه؟
- ج. بأي منطقة زمنية يُخزَّن وقت آخر تعديل وتتم المقارنة (التوقيت المحلي للخادم، أم UTC)؟
- د. ما التغييرات التي تُحدِّث وقت آخر تعديل للزبون: تعديل بطاقة الزبون فقط، أم أيضاً تغيّر الرصيد بسبب سندات جديدة، وجهات الاتصال، والتصنيفات، وحالة الإيقاف؟
- هـ. ما التغييرات التي تُحدِّث وقت آخر تعديل للصنف: تغيير الأسعار، أو حالة الإيقاف أو التجميد، أو إضافة باركود جديد؟
- و. بالنسبة لـ `GetItemsStores`: هل تُحدِّث حركات المخزون الناتجة عن السندات (المبيعات، والمشتريات، والتحويلات، والجرد) هذا الوقت، بحيث تُعاد فقط الصفوف التي تغيّرت كميتها؟
- ز. هل يتم الإبلاغ عن السجلات المحذوفة بأي شكل؟

</div>

**Why we ask:** our change notifications (webhooks) and incremental sync depend on this; today we must download the
full stock list every 5 minutes because we cannot rely on it.

<sub>Ref: Q18 · I-11 · 05 §11 · 05 §2.4.1–2.4.2 · 03 §5.7 · 00 §11</sub>

#### ISCO-23 — Edits and deletions of records

- (a) Can customers, items and vouchers be deleted in Shamel (by desktop users)? If yes, is there any way to detect
  deletions through the API?
- (b) Can a voucher be edited after it is saved or posted (header, lines, amounts, date)?
- (c) Does `VoucherHeader.update_date` change on every edit, and what is its format (date or date and time, timezone)?
- (d) Does `GetVouchers` filter by voucher date or by entry or update date?

<div dir="rtl" lang="ar">

**تعديل السجلات وحذفها**

- أ. هل يمكن حذف الزبائن والأصناف والسندات في الشامل (من قبل مستخدمي البرنامج المكتبي)؟ وإن كان ذلك ممكناً، فهل توجد طريقة لاكتشاف عمليات الحذف عبر الواجهة البرمجية؟
- ب. هل يمكن تعديل السند بعد حفظه أو ترحيله (الرأس، أو البنود، أو المبالغ، أو التاريخ)؟
- ج. هل تتغير قيمة `VoucherHeader.update_date` مع كل تعديل؟ وما صيغتها (تاريخ فقط أم تاريخ ووقت، وبأي منطقة زمنية)؟
- د. هل تُصفّي `GetVouchers` النتائج حسب تاريخ السند، أم حسب تاريخ إدخاله أو تعديله؟

</div>

**Why we ask:** to notify our tools about changed or removed vouchers we currently re-scan the last 35 days every
night; knowing how edits and deletions behave lets us do this correctly and at lower cost.

<sub>Ref: Q43 · 05 §11 · 05 §2.4.4</sub>

#### ISCO-24 — Dates, times and timezone

- (a) Which timezone do the server and the database use for business dates and times (we assume local Palestine
  time)?
- (b) Are `fromDate` and `toDate` inclusive in `GetVouchers`, `GetExtraVouchers` and both account-statement reports?
- (c) Is `VoucherHeader.time` (`hhmmss`) in 24-hour format?
- (d) Do all date fields in responses use `yyyy-MM-dd`, or do some include a time part (for example the guarantee
  dates of serials)?

<div dir="rtl" lang="ar">

**التواريخ والأوقات والمنطقة الزمنية**

- أ. ما المنطقة الزمنية التي يستخدمها الخادم وقاعدة البيانات للتواريخ والأوقات (نفترض التوقيت المحلي لفلسطين)؟
- ب. هل التاريخان `fromDate` و`toDate` شاملان في `GetVouchers` و`GetExtraVouchers` وفي تقريرَي كشف الحساب؟
- ج. هل الوقت `VoucherHeader.time` (`hhmmss`) بنظام 24 ساعة؟
- د. هل تستخدم جميع حقول التاريخ في الاستجابات الصيغة `yyyy-MM-dd`، أم أن بعضها يتضمن الوقت أيضاً (مثل تواريخ الكفالة للأرقام التسلسلية)؟

</div>

**Why we ask:** off-by-one-day errors in date ranges cause missing or double-counted vouchers in reports built on our
API.

<sub>Ref: I-8 · Q41 · 03 §4.5 · 00 §11</sub>

### 3.7 Salesman scoping (نطاق صلاحيات المندوب)

#### ISCO-25 — Salesman scoping across endpoints

A user linked to a salesman (`AuthResult.salesmanCode`) sees only that salesman's customers in `GetCustomers` unless
`getAll=true` is sent, and `GetDelivery` depends on the salesman.

- (a) Which other endpoints are limited to the salesman's data: `GetCustomerBalances`, `GetCustomerPricesAsRows`,
  `GetItems`, `GetItemsStores`, `GetItemsSerials`, `GetVouchers`, `GetExtraVouchers`, `GetVoucher`, `GetAccountsheet`,
  `GetLastPriceReport`?
- (b) For a user with no salesman link, does `GetCustomers` without `getAll` return all customers?
- (c) Can any user send `getAll=true`, or does it require a permission in Shamel?
- (d) Is salesman scoping enforced on writes? Can a salesman user post a voucher for another salesman's customer, or
  create a customer for another salesman?

<div dir="rtl" lang="ar">

**تطبيق نطاق المندوب على نقاط النهاية**

المستخدم المرتبط بمندوب مبيعات (`AuthResult.salesmanCode`) لا يرى في `GetCustomers` إلا زبائن ذلك المندوب ما لم تُرسَل الترويسة `getAll=true`، كما أن `GetDelivery` تعتمد على المندوب.

- أ. ما نقاط النهاية الأخرى التي تقتصر على بيانات المندوب: `GetCustomerBalances`، `GetCustomerPricesAsRows`، `GetItems`، `GetItemsStores`، `GetItemsSerials`، `GetVouchers`، `GetExtraVouchers`، `GetVoucher`، `GetAccountsheet`، `GetLastPriceReport`؟
- ب. بالنسبة لمستخدم غير مرتبط بأي مندوب، هل تُعيد `GetCustomers` جميع الزبائن دون إرسال `getAll`؟
- ج. هل يستطيع أي مستخدم إرسال `getAll=true`، أم يتطلب ذلك صلاحية في الشامل؟
- د. هل يُطبَّق نطاق المندوب على عمليات الإدخال؟ أي هل يستطيع مستخدم مرتبط بمندوب إدخال سند لزبون تابع لمندوب آخر، أو إنشاء زبون لمندوب آخر؟

</div>

**Why we ask:** tokens that act as a salesman's Shamel user rely on Shamel's own scoping; we must know exactly where it
applies so that our permission layer covers the gaps.

<sub>Ref: Q17 · I-16 · 04 §17.3 #1–#3 · 05 §11</sub>

### 3.8 Master data (البيانات الأساسية)

#### ISCO-26 — Response of `/Files/GetSalesmen`

**[Priority · أولوية]**

The manual prints only the heading of `/Files/GetSalesmen`.

- (a) Does it take any input headers?
- (b) Please give the response model: field names, types and meanings (for example code, name, linked user, linked
  store or van, stopped flag).
- (c) Does it return all salesmen, or only the logged-in user's salesman? A sample response would help.

<div dir="rtl" lang="ar">

**استجابة `/Files/GetSalesmen`**

يذكر الدليل عنوان `/Files/GetSalesmen` فقط دون أي تفاصيل.

- أ. هل تقبل أي ترويسات كمدخلات؟
- ب. نرجو تزويدنا بنموذج الاستجابة: أسماء الحقول وأنواعها ومعانيها (مثل الرمز، والاسم، والمستخدم المرتبط، والمستودع أو السيارة المرتبطة، وحالة الإيقاف).
- ج. هل تُعيد جميع المندوبين، أم مندوب المستخدم الحالي فقط؟ وسيكون من المفيد تزويدنا بمثال على الاستجابة.

</div>

**Why we ask:** the salesmen list is part of our first release, and per-salesman permissions are validated against it;
without a model we can only publish it as provisional.

<sub>Ref: Q24 · I-1 · 04 §17.3 #6 · 00 §11</sub>

#### ISCO-27 — Stores

The manual documents `GetStores` with the class name `City`. Please confirm the store fields (`id`, `name`, `type`,
`car_code`, `orgnization_code`) and explain:

- (a) the values of `type`;
- (b) whether a non-empty `car_code` means the store is a salesman's van;
- (c) what `orgnization_code` refers to (a branch, a company).

<div dir="rtl" lang="ar">

**المستودعات**

وثّق الدليل `GetStores` باسم الصنف `City`. نرجو تأكيد حقول المستودع (`id` و`name` و`type` و`car_code` و`orgnization_code`) وتوضيح ما يلي:

- أ. قيم الحقل `type`؛
- ب. هل يعني وجود قيمة في `car_code` أن المستودع هو سيارة مندوب (مبيعات متنقلة)؟
- ج. إلامَ يشير `orgnization_code` (فرع، أم شركة)؟

</div>

**Why we ask:** stores are a permission dimension in our layer (a token can be limited to certain stores and vans), so
their meaning must be exact.

<sub>Ref: Q27 · U §6.4</sub>

#### ISCO-28 — Currencies and exchange rates

- (a) What do `Currency.units` and `Currency.division` contain?
- (b) Is `Currency.code` (for example `NIS`, `$`) a stable key that never changes, and is it the value expected in
  every currency field of vouchers, items and prices?
- (c) Does `GetCurrencyRates` return the latest 10 rates in total or per currency? Is there a way to get historical
  rates, or the rate on a given date?
- (d) What exactly does `is_base` mean?

<div dir="rtl" lang="ar">

**العملات وأسعار الصرف**

- أ. ماذا يحتوي الحقلان `Currency.units` و`Currency.division`؟
- ب. هل `Currency.code` (مثل `NIS` و`$`) مفتاح ثابت لا يتغير؟ وهل هو القيمة المتوقعة في جميع حقول العملة في السندات والأصناف والأسعار؟
- ج. هل تُعيد `GetCurrencyRates` آخر 10 أسعار إجمالاً، أم آخر 10 لكل عملة؟ وهل توجد طريقة للحصول على الأسعار التاريخية أو على سعر الصرف في تاريخ معيّن؟
- د. ما المعنى الدقيق للحقل `is_base`؟

</div>

**Why we ask:** currency codes join vouchers, prices and balances; the wrong key or a stale rate gives wrong totals.

<sub>Ref: Q31 · Q36 · I-21 · I-22</sub>

#### ISCO-29 — Price classes and item prices

- (a) Are there always exactly 6 price classes, and does class N correspond to `Item.sale_pariceN`?
- (b) What is the difference between `sale_pariceN` and `unit_price_N`? Is the currency field `currN` linked to price
  class N or to unit N?
- (c) Why is `Customer.price_class` a decimal (`double`)? Can it hold values other than 1 to 6?
- (d) What does `purchase_price` represent (last purchase price, average cost)?

<div dir="rtl" lang="ar">

**فئات الأسعار وأسعار الأصناف**

- أ. هل عدد فئات الأسعار 6 دائماً؟ وهل تقابل الفئة رقم N الحقل `Item.sale_pariceN`؟
- ب. ما الفرق بين `sale_pariceN` و`unit_price_N`؟ وهل يرتبط حقل العملة `currN` بفئة السعر رقم N أم بالوحدة رقم N؟
- ج. لماذا نوع الحقل `Customer.price_class` عدد عشري (`double`)؟ وهل يمكن أن يحمل قيماً غير الأرقام من 1 إلى 6؟
- د. ماذا يمثّل `purchase_price` (آخر سعر شراء، أم متوسط التكلفة)؟

</div>

**Why we ask:** we expose prices per class and unit, and can hide cost prices from some tokens; a misread field would
show the wrong price in a customer-facing tool.

<sub>Ref: Q33 · U §5.15</sub>

### 3.9 Customers (الزبائن)

#### ISCO-30 — Stopped customers by default

`getStopped="true"` returns only stopped customers. When the header is absent, does `GetCustomers` return active and
stopped customers, or active customers only? How can we get all customers (active and stopped) in one call?

<div dir="rtl" lang="ar">

**الزبائن الموقوفون في الوضع الافتراضي**

تُعيد الترويسة `getStopped="true"` الزبائن الموقوفين فقط. فعند عدم إرسالها، هل تُعيد `GetCustomers` الزبائن النشطين والموقوفين معاً، أم النشطين فقط؟ وكيف يمكننا الحصول على جميع الزبائن (النشطين والموقوفين) في استدعاء واحد؟

</div>

**Why we ask:** our customer filter (`stopped=true|false`) and our change detection depend on knowing which set the
default call returns.

<sub>Ref: Q34</sub>

#### ISCO-31 — Customer balance semantics

- (a) Without `getBalance`, are `balance`, `notPayedCheqsBalance` and `returnedCheqsBalance` always 0?
- (b) In `GetCustomerBalances`, is there one row per customer per currency? What do `pos`, `date` and `rate` mean?
- (c) Do balances include unposted vouchers and uncleared cheques?
- (d) For `getCustomerBalance` on vouchers, `GetVoucher` says the balance is "at the invoice time", while `GetVouchers`
  and `GetExtraVouchers` say "excluding the invoice itself". Does the balance from `GetVoucher` include the voucher
  itself? In which currency is it expressed?

<div dir="rtl" lang="ar">

**دلالة أرصدة الزبائن**

- أ. عند عدم إرسال `getBalance`، هل تكون الحقول `balance` و`notPayedCheqsBalance` و`returnedCheqsBalance` صفراً دائماً؟
- ب. في `GetCustomerBalances`، هل يوجد صف واحد لكل زبون لكل عملة؟ وما معنى الحقول `pos` و`date` و`rate`؟
- ج. هل تشمل الأرصدة السندات غير المرحّلة والشيكات غير المحصّلة؟
- د. بالنسبة للترويسة `getCustomerBalance` في السندات: يذكر الدليل في `GetVoucher` أن الرصيد "وقت الفاتورة"، بينما يذكر في `GetVouchers` و`GetExtraVouchers` أنه "باستثناء الفاتورة نفسها". فهل يشمل الرصيد في `GetVoucher` السند نفسه؟ وبأي عملة يُعبَّر عنه؟

</div>

**Why we ask:** balances are sensitive and shown in the owner's tools; a 0 that means "not requested" must never be
displayed as a real zero balance.

<sub>Ref: Q37 · U §5.12</sub>

#### ISCO-32 — Customer fields and read/write mapping

- (a) Please explain these fields of the customer read model: `citizen_code`, `attr`, `man_name`,
  `trans_permissions`, `level`, `creditType`, `discount` (percentage or amount?), `referee1`, `referee2`, `id_number`.
- (b) Please confirm how the write model of `/Customer/Post` maps to the read model: `Address` → `street`, `Street` →
  `street2`, `PhoneNumber` → `phone`, `Referee` → `referee1`, `RefereeMobile` → `referee2`, `Salesman` →
  `salesman_code`, `CustomerLevel` → `level`, `VatReg` → `VATReg`.
- (c) The manual comments `MobileNumber` as "fax". Is it the mobile number or the fax number, and where does it appear
  in the read model?

<div dir="rtl" lang="ar">

**حقول الزبون والمطابقة بين نموذجَي القراءة والإدخال**

- أ. نرجو توضيح معنى حقول الزبون التالية في نموذج القراءة: `citizen_code`، `attr`، `man_name`، `trans_permissions`، `level`، `creditType`، `discount` (نسبة أم مبلغ؟)، `referee1`، `referee2`، `id_number`.
- ب. نرجو تأكيد المطابقة بين حقول نموذج الإدخال في `/Customer/Post` وحقول نموذج القراءة: `Address` يقابل `street`، و`Street` يقابل `street2`، و`PhoneNumber` يقابل `phone`، و`Referee` يقابل `referee1`، و`RefereeMobile` يقابل `referee2`، و`Salesman` يقابل `salesman_code`، و`CustomerLevel` يقابل `level`، و`VatReg` يقابل `VATReg`.
- ج. وُصف الحقل `MobileNumber` في الدليل بأنه "فاكس". فهل هو رقم الهاتف المحمول أم رقم الفاكس؟ وأين يظهر في نموذج القراءة؟

</div>

**Why we ask:** several of these fields are published as provisional in our API until you confirm them, and their names
are frozen at our first stable release.

<sub>Ref: Q29 · Q30 · I-18 · 03 §3.4</sub>

#### ISCO-33 — `Customer/GetCustomerPricesAsRows`

- (a) Which inputs does it accept (customer, item, price class)?
- (b) Does one call return the special prices of all customers?
- (c) What do `code`, `discount_type` (which values?) and `tax` (rate or amount?) mean?
- (d) Is `stock_code` the item code?
- (e) Are rows without a `customer_code` price-class prices?

<div dir="rtl" lang="ar">

**نقطة النهاية `Customer/GetCustomerPricesAsRows`**

- أ. ما المدخلات التي تقبلها (الزبون، أو الصنف، أو فئة السعر)؟
- ب. هل يُعيد استدعاء واحد الأسعار الخاصة لجميع الزبائن؟
- ج. ما معنى `code` و`discount_type` (وما قيمه؟) و`tax` (نسبة أم مبلغ؟)؟
- د. هل `stock_code` هو رمز الصنف؟
- هـ. هل الصفوف التي لا تحتوي على `customer_code` هي أسعار خاصة بفئة سعر؟

</div>

**Why we ask:** without filters every request downloads the whole price table; knowing the inputs lets us ask Shamel for
one customer only.

<sub>Ref: Q25 · I-2 · 04 §17.4 #3</sub>

### 3.10 Items, stock and catalog (الأصناف والمخزون والكتالوج)

#### ISCO-34 — Format of `image_path` in the item catalog

- (a) What exactly does `ItemCatalog.image_path` contain: a URL (absolute or relative), a local file path, or a
  network (UNC) path?
- (b) If it is a URL, which server serves the images, and does it require the same `username` and `token` headers?
- (c) Is there an endpoint that returns the image bytes of an item?
- (d) Which image formats and typical file sizes should we expect?

<div dir="rtl" lang="ar">

**صيغة `image_path` في كتالوج الأصناف**

- أ. ماذا يحتوي الحقل `ItemCatalog.image_path` تحديداً: رابط URL (كامل أم نسبي)، أم مسار ملف محلي، أم مسار على الشبكة (UNC)؟
- ب. إن كان رابطاً، فما الخادم الذي يقدّم الصور؟ وهل يتطلب الترويستين `username` و`token` نفسيهما؟
- ج. هل توجد نقطة نهاية تُعيد محتوى صورة الصنف مباشرة؟
- د. ما صيغ الصور وأحجامها المعتادة؟

</div>

**Why we ask:** we never pass internal paths or server addresses on to our tools; item images stay disabled in our API
until we know how to fetch them safely.

<sub>Ref: Q26 · 02 §20.2 #2 · 02 §5.4 · 01 §16 · 01 §8.4</sub>

#### ISCO-35 — Item list filters and item details

- (a) On `GetItems`, what does the `store` header select: items that have stock in that store, or items linked to it?
  What do `model` and `serial` match (the read model has no `model` field)?
- (b) Does `getItemDetails` return one object (`{itm, itmStores}`) or a list?
- (c) `ItemGroup.code` says "Item has itemGroupCode field". We assume the item field is `item_group_code`, and that the
  group's `parentCode` corresponds to the item's `item_group_father_code`. Is that correct?

<div dir="rtl" lang="ar">

**معاملات تصفية الأصناف وتفاصيل الصنف**

- أ. في `GetItems`، ماذا تحدد الترويسة `store`: الأصناف التي لها كمية في ذلك المستودع، أم الأصناف المرتبطة به؟ وبماذا تُطابَق الترويستان `model` و`serial` (علماً بأن نموذج القراءة لا يحتوي على حقل `model`)؟
- ب. هل تُعيد `getItemDetails` كائناً واحداً (`{itm, itmStores}`) أم قائمة؟
- ج. يذكر الدليل في `ItemGroup.code` أن "للصنف حقل itemGroupCode يشير إلى هذا الحقل"، ونفترض أن الحقل في الصنف هو `item_group_code`، وأن `parentCode` في المجموعة يقابل `item_group_father_code` في الصنف. هل هذا صحيح؟

</div>

**Why we ask:** we pass these filters to Shamel to avoid full downloads; a wrong assumption would silently return the
wrong items.

<sub>Ref: I-16 · Q28 · Q29 · Q32</sub>

#### ISCO-36 — Stock quantities

For `GetItemsStores`:

- (a) Is `qnty` expressed in the item's main unit?
- (b) Are rows with zero quantity returned, and can quantities be negative?
- (c) Does `qnty` include quantities reserved by open orders or pending deliveries?
- (d) Is there a way to filter by store?

<div dir="rtl" lang="ar">

**كميات المخزون**

بالنسبة لـ `GetItemsStores`:

- أ. هل الكمية `qnty` معبَّر عنها بالوحدة الرئيسية للصنف؟
- ب. هل تُعاد الصفوف ذات الكمية صفر؟ وهل يمكن أن تكون الكميات سالبة؟
- ج. هل تشمل `qnty` الكميات المحجوزة لطلبيات مفتوحة أو لإرساليات معلّقة؟
- د. هل توجد طريقة للتصفية حسب المستودع؟

</div>

**Why we ask:** stock across stores is a core screen in the owner's tools, and quantities must carry the right unit and
meaning.

<sub>Ref: U §5.16 · 05 §2.4.2</sub>

### 3.11 Reports (التقارير)

#### ISCO-37 — Last price report

For `/Report/GetLastPriceReport`:

- (a) The manual says "ItemCode is mandatory" and, after `barcode`, "ItemCode is optional". We read this as: `ItemCode`
  is required and `barcode` is optional. Is that correct? If both are sent, which one wins?
- (b) Is the report global (the last prices to any customer) or per customer? Can it be filtered by customer?
- (c) Does `customer` contain the customer code or the customer name?
- (d) Is `code` the voucher code? How many rows are returned, and which voucher types are included (sales invoices
  only)?

<div dir="rtl" lang="ar">

**تقرير آخر الأسعار**

بالنسبة لتقرير آخر الأسعار `/Report/GetLastPriceReport`:

- أ. يذكر الدليل أن "ItemCode is mandatory"، ثم يذكر بعد `barcode` أن "ItemCode is optional". فهمنا من ذلك أن `ItemCode` إلزامي وأن `barcode` اختياري. هل هذا صحيح؟ وإذا أُرسل الاثنان معاً، فأيّهما يُعتمد؟
- ب. هل التقرير عام (آخر الأسعار لأي زبون) أم خاص بزبون معيّن؟ وهل يمكن تصفيته حسب الزبون؟
- ج. هل يحتوي الحقل `customer` على رمز الزبون أم على اسمه؟
- د. هل الحقل `code` هو رقم السند؟ وكم عدد الصفوف التي تُعاد، وما أنواع السندات المشمولة (فواتير المبيعات فقط)؟

</div>

**Why we ask:** tokens limited to certain customers may only see those customers' last prices; if `customer` is a name,
we must hide the report from such tokens.

<sub>Ref: Q21 · I-13 · 04 §17.3 #4 · 04 §17.2</sub>

#### ISCO-38 — Customer account statement (`/Report/GetAccountsheet`)

- (a) Does `customerCode` accept only customer codes, or any account code from the chart of accounts?
- (b) The amounts `credit`, `debit` and `balance` are strings. What is their number format (decimal separator,
  thousands separator, negative sign, empty for zero)?
- (c) What does `start_date` mean in each row?
- (d) What does the `type` column contain (an Arabic voucher-type name, a code, the voucher-type number)?
- (e) Is the opening balance returned as a separate first row?

<div dir="rtl" lang="ar">

**كشف حساب الزبون (`/Report/GetAccountsheet`)**

- أ. هل يقبل الحقل `customerCode` رموز الزبائن فقط، أم أي رمز حساب من دليل الحسابات؟
- ب. تُعاد المبالغ `credit` و`debit` و`balance` كنصوص: فما صيغة الأرقام فيها (الفاصلة العشرية، وفاصل الآلاف، وإشارة السالب، وهل تكون فارغة عند الصفر)؟
- ج. ما معنى الحقل `start_date` في كل صف؟
- د. ماذا يحتوي العمود `type` (اسم نوع السند بالعربية، أم رمزاً، أم رقم نوع السند)؟
- هـ. هل يُعاد الرصيد الافتتاحي كصف مستقل في بداية الكشف؟

</div>

**Why we ask:** we convert these strings into exact decimal amounts; an unknown format must fail safely rather than
produce a wrong balance.

<sub>Ref: I-12 · I-15 · Q35 · 04 §17.3 #5 · 04 §17.4 #2</sub>

#### ISCO-39 — Cost centers

- (a) For `/CostCenter/GetCostCenterAccountsheet`, what are the values of the `type` filter, and what does `account`
  accept?
- (b) Is there a way to list the existing cost centers?
- (c) The manual describes `/CostCenter/Post` as "Insert new customer". We assume it inserts a cost center. Please
  confirm, and explain `father`, `type` (which values?) and `date`.
- (d) `/CostCenter/Post` returns no identifier. Is the created cost center's code always the `code` we send? What
  happens if that code already exists?

<div dir="rtl" lang="ar">

**مراكز التكلفة**

- أ. في تقرير كشف حساب مركز التكلفة `/CostCenter/GetCostCenterAccountsheet`، ما قيم معامل التصفية `type`؟ وماذا يقبل الحقل `account`؟
- ب. هل توجد طريقة لاستعراض مراكز التكلفة الموجودة؟
- ج. وُصفت `/CostCenter/Post` في الدليل بعبارة "Insert new customer"، ونفترض أنها تُدخل مركز تكلفة جديداً. نرجو التأكيد، وتوضيح معنى الحقول `father` و`type` (وما قيمه؟) و`date`.
- د. لا تُعيد `/CostCenter/Post` أي معرّف. فهل يكون رمز المركز المُنشأ دائماً هو قيمة `code` التي نرسلها؟ وماذا يحدث إذا كان الرمز موجوداً مسبقاً؟

</div>

**Why we ask:** cost-center reports are in our first release; cost-center inserts come later and must never create
duplicates.

<sub>Ref: Q20 · Q3 · Q42 · U §6.4</sub>

### 3.12 Vouchers: reading (السندات: القراءة)

#### ISCO-40 — `GetVoucher`, `GetVouchers` and `GetExtraVouchers`

- (a) Does `GetVouchers` return the full voucher (header, items, cheques and accounts), like `GetVoucher`?
- (b) What is the purpose of `GetExtraVouchers` (what does "extra" mean), and which voucher types does it include? Does
  it include stock-only types such as goods issue (12) and internal delivery (16)?
- (c) Can `GetVouchers` filter by voucher type? Are `fromDate` and `toDate` both required?
- (d) Must the `voucher_code` header of `GetVoucher` include the prefix letter (for example `I1234`)?

<div dir="rtl" lang="ar">

**نقاط النهاية `GetVoucher` و`GetVouchers` و`GetExtraVouchers`**

- أ. هل تُعيد `GetVouchers` السند كاملاً (الرأس والبنود والشيكات والحسابات) كما في `GetVoucher`؟
- ب. ما الغرض من `GetExtraVouchers` (وما المقصود بكلمة "Extra")؟ وما أنواع السندات التي تشملها؟ وهل تشمل الأنواع المخزنية فقط، مثل إخراج البضاعة (12) والإرسالية الداخلية (16)؟
- ج. هل يمكن تصفية `GetVouchers` حسب نوع السند؟ وهل التاريخان `fromDate` و`toDate` إلزاميان كلاهما؟
- د. هل يجب أن تتضمن الترويسة `voucher_code` في `GetVoucher` الحرف البادئ (مثل `I1234`)؟

</div>

**Why we ask:** we scan recent vouchers to detect changes for webhooks; knowing what each endpoint returns lets us use
the cheapest call.

<sub>Ref: Q23 · 05 §11 · 05 §2.4.4</sub>

#### ISCO-41 — `GetDelivery`

`GetDelivery` returns "the delivery that is prepared to the salesman" as a single object.

- (a) What is returned when there is no prepared delivery, or when there are several?
- (b) Which voucher type is returned (sales delivery 10, internal delivery 16)?
- (c) Does it take any input, or does it always use the logged-in user's salesman?
- (d) Does calling it change any state in Shamel (for example, mark the delivery as received)?

<div dir="rtl" lang="ar">

**نقطة النهاية `GetDelivery`**

تُعيد `GetDelivery` "الإرسالية المجهّزة للمندوب" ككائن واحد.

- أ. ماذا يُعاد عند عدم وجود إرسالية مجهّزة، أو عند وجود أكثر من واحدة؟
- ب. ما نوع السند المُعاد (إرسالية مبيعات 10، أم إرسالية داخلية 16)؟
- ج. هل تقبل أي مدخلات، أم أنها تعتمد دائماً على مندوب المستخدم الحالي؟
- د. هل يؤدي استدعاؤها إلى تغيير أي حالة في الشامل (مثل اعتبار الإرسالية مستلَمة)؟

</div>

**Why we ask:** we expose this as a read-only list, and a read must never change data in Shamel.

<sub>Ref: Q23 · I-10</sub>

#### ISCO-42 — `GetStatus`

- (a) Is the `manual` header the order's `manual_code` (paper reference) or its voucher code?
- (b) What is the exact response (a bare number, JSON)?
- (c) What is returned for an unknown value?
- (d) Can several orders share the same `manual_code`?
- (e) Is there a way to get an order's status by voucher code, for orders that have no `manual_code`?
- (f) Does it apply only to orders (type 0)?

<div dir="rtl" lang="ar">

**نقطة النهاية `GetStatus`**

- أ. هل الترويسة `manual` هي `manual_code` الخاص بالطلبية (الرقم المرجعي الورقي)، أم رقم السند؟
- ب. ما الصيغة الدقيقة للاستجابة (رقم مجرد، أم JSON)؟
- ج. ماذا يُعاد عند إرسال قيمة غير موجودة؟
- د. هل يمكن أن تشترك أكثر من طلبية في قيمة `manual_code` نفسها؟
- هـ. هل توجد طريقة لمعرفة حالة الطلبية برقم السند، للطلبيات التي لا تحتوي على `manual_code`؟
- و. هل تقتصر هذه النقطة على الطلبيات (النوع 0)؟

</div>

**Why we ask:** we notify tools when an order becomes ready or sent; orders without a manual code currently cannot be
tracked.

<sub>Ref: I-9 · 05 §11 · 05 §2.4.5</sub>

### 3.13 Writes (عمليات الإدخال)

#### ISCO-43 — Duplicate prevention and the outcome of failed writes

**[Priority · أولوية]**

The API has no idempotency mechanism, and its writes are insert-only.

- (a) If `/Voucher/Post2`, `/Customer/Post` or `/Item/Post` returns HTTP 500, or the connection times out, can the
  record still have been saved? Is each write a single database transaction (all or nothing)?
- (b) Does Shamel reject a voucher whose `code` already exists? Does it reject a duplicate `manual_code` (for the same
  voucher type, for the same customer, or at all)?
- (c) What is your recommended way to make a retry safe? For example, could we send our own unique reference in
  `manual_code` (or another field) and look for it before retrying? Which read endpoint can find a voucher by
  `manual_code`?
- (d) Does `/Item/Post` reject an item `code` that already exists? Does `/Customer/Post` detect duplicate customers
  (for example the same VAT registration number)?

<div dir="rtl" lang="ar">

**منع التكرار ونتيجة عمليات الإدخال الفاشلة**

لا توفّر الواجهة البرمجية آلية لمنع تكرار التنفيذ، وعمليات الكتابة فيها إدخال فقط (دون تعديل أو حذف).

- أ. إذا أعادت `/Voucher/Post2` أو `/Customer/Post` أو `/Item/Post` الحالة HTTP 500، أو انقطع الاتصال بسبب انتهاء المهلة، فهل يُحتمل أن يكون السجل قد حُفظ فعلاً؟ وهل تتم كل عملية إدخال ضمن معاملة واحدة في قاعدة البيانات (إمّا أن تتم كاملة أو لا تتم إطلاقاً)؟
- ب. هل يرفض الشامل سنداً رقمه (`code`) موجود مسبقاً؟ وهل يرفض تكرار `manual_code` (لنفس نوع السند، أو لنفس الزبون، أو بشكل مطلق)؟
- ج. ما الطريقة التي توصون بها لجعل إعادة المحاولة آمنة؟ مثلاً: هل يمكننا إرسال مرجع فريد خاص بنا في `manual_code` (أو في حقل آخر) والبحث عنه قبل إعادة المحاولة؟ وما نقطة النهاية التي يمكن من خلالها البحث عن سند بواسطة `manual_code`؟
- د. هل ترفض `/Item/Post` رمز صنف موجوداً مسبقاً؟ وهل تكتشف `/Customer/Post` الزبائن المكررين (مثلاً بنفس رقم المشتغل المرخص)؟

</div>

**Why we ask:** a duplicated invoice or receipt is a real accounting error that cannot be deleted through the API; we
never retry a write automatically until we know how to tell whether the first attempt succeeded.

<sub>Ref: Q39 · Q2 · I-6 · 03 §15.2</sub>

#### ISCO-44 — Meaning and range of `system_id`

`VoucherHeader.system_id` "must be between 1000 and 2000".

- (a) What is it used for? Does it identify the external system that created the voucher? Is it visible inside Shamel
  (for example in reports or filters)?
- (b) Are the values 1000 and 2000 themselves allowed?
- (c) Should each integrating system use its own value? Does ISCO assign or register these values?
- (d) Is it returned by `GetVoucher` and `GetVouchers`?

<div dir="rtl" lang="ar">

**معنى الحقل `system_id` ونطاقه**

يجب أن تكون قيمة `VoucherHeader.system_id` "بين 1000 و2000".

- أ. ما الغرض منه؟ هل يُعرّف النظام الخارجي الذي أنشأ السند؟ وهل يظهر داخل الشامل (مثلاً في التقارير أو في عوامل التصفية)؟
- ب. هل القيمتان 1000 و2000 نفساهما مسموحتان؟
- ج. هل يجب أن يستخدم كل نظام متكامل قيمة خاصة به؟ وهل تقوم ISCO بتخصيص هذه القيم أو بتسجيلها؟
- د. هل يُعاد هذا الحقل في `GetVoucher` و`GetVouchers`؟

</div>

**Why we ask:** we currently send a fixed 1500; if the value identifies the source system, it would also let your
support team and our accountants recognise vouchers created through our layer.

<sub>Ref: Q38 · I-17 · 03 §15.7</sub>

#### ISCO-45 — Voucher codes and prefix letters

- (a) The manual lists no prefix letter for `PurchaseDelivery` (2). Which letter should it use, or must its code always
  be left to Shamel?
- (b) After the prefix letter, what format is allowed (digits only, maximum length, leading zeros)?
- (c) Are codes unique per voucher type, per year, or across the whole database?
- (d) When `code` is left empty, how does Shamel number the voucher (the next number in a series per type, per
  branch)? Can codes that we send collide with Shamel's own series?

<div dir="rtl" lang="ar">

**أرقام السندات والأحرف البادئة**

- أ. لم يذكر الدليل حرفاً بادئاً لنوع `PurchaseDelivery` (2). فما الحرف الذي يجب استخدامه، أم يجب دائماً ترك ترقيمه للشامل؟
- ب. ما الصيغة المسموحة بعد الحرف البادئ (أرقام فقط، والطول الأقصى، والأصفار في البداية)؟
- ج. هل الأرقام فريدة لكل نوع سند، أم لكل سنة، أم على مستوى قاعدة البيانات كاملة؟
- د. عند ترك `code` فارغاً، كيف يرقّم الشامل السند (الرقم التالي في سلسلة لكل نوع أو لكل فرع)؟ وهل يمكن أن تتعارض الأرقام التي نرسلها مع تسلسل الترقيم في الشامل نفسه؟

</div>

**Why we ask:** we validate codes before sending them; a code that clashes with Shamel's numbering could be rejected or
disturb desktop users.

<sub>Ref: Q40 · I-5 · 03 §15.7</sub>

#### ISCO-46 — Voucher amounts, discounts, tax and posting state

- (a) Is `VoucherHeader.balance` the total after the header discount? Does it include VAT?
- (b) Is `VoucherHeader.discount` an amount (while `VoucherItems.discount` is a percentage from 0 to 100)?
- (c) Is `VoucherItems.vat` the tax for one unit of quantity, and `VoucherHeader.vat` the voucher total? On insert,
  does Shamel calculate tax and totals itself, or does it keep the values we send?
- (d) Must `balance`, `vat` and `cheq_balance` be sent on insert, or are they computed?
- (e) On insert, what is the effect of `is_posted` and `is_printed`? Should we send `is_posted=false` so that an
  accountant reviews the voucher before it is posted?

<div dir="rtl" lang="ar">

**مبالغ السندات والخصومات والضريبة وحالة الترحيل**

- أ. هل `VoucherHeader.balance` هو الإجمالي بعد خصم الفاتورة؟ وهل يشمل ضريبة القيمة المضافة؟
- ب. هل `VoucherHeader.discount` مبلغ (بينما `VoucherItems.discount` نسبة من 0 إلى 100)؟
- ج. هل `VoucherItems.vat` هي ضريبة الوحدة الواحدة من الكمية، و`VoucherHeader.vat` إجمالي ضريبة السند؟ وعند الإدخال، هل يحسب الشامل الضريبة والإجماليات بنفسه، أم يعتمد القيم المرسلة؟
- د. هل يجب إرسال `balance` و`vat` و`cheq_balance` عند الإدخال، أم تُحسب تلقائياً؟
- هـ. ما أثر الحقلين `is_posted` و`is_printed` عند الإدخال؟ وهل يُنصح بإرسال `is_posted=false` ليتمكن المحاسب من مراجعة السند قبل ترحيله؟

</div>

**Why we ask:** wrong assumptions here produce invoices with wrong totals or tax, which are costly to correct because the
API cannot edit them.

<sub>Ref: Q41 · I-7</sub>

#### ISCO-47 — Rules per voucher type

- (a) Is `accounts` allowed (not only required) in vouchers other than journal vouchers?
- (b) In receipts (24) and payments (27), how is the cash amount expressed: in `balance`, as an `accounts` line, or
  otherwise? How are cheques (`cheqs`) linked?
- (c) "Invoice from a delivery" has no voucher type. Is it a sales invoice (9) with `delivery_id` and
  `VoucherItems.delivery_pos` filled?
- (d) For an internal delivery (16), how is the destination store specified?
- (e) Which header and line fields are required for each voucher type?
- (f) Does Shamel check stock availability, credit limits, stopped customers or stopped items on insert?
- (g) What is `ReturnedPendingSalesDelivery` (5) used for?

<div dir="rtl" lang="ar">

**قواعد كل نوع من أنواع السندات**

- أ. هل يُسمح بإرسال `accounts` (وليس فقط يُشترط) في السندات الأخرى غير سندات القيد؟
- ب. في سندات القبض (24) والصرف (27)، كيف يُعبَّر عن المبلغ النقدي: من خلال `balance`، أم كبند في `accounts`، أم بطريقة أخرى؟ وكيف تُربط الشيكات (`cheqs`)؟
- ج. لا يوجد نوع سند مخصص لـ"فاتورة من إرسالية". فهل هي فاتورة مبيعات (9) مع تعبئة `delivery_id` و`VoucherItems.delivery_pos`؟
- د. في الإرسالية الداخلية (16)، كيف يُحدَّد المستودع المُستلِم؟
- هـ. ما حقول الرأس والبنود المطلوبة لكل نوع سند؟
- و. هل يتحقق الشامل عند الإدخال من توفّر الكمية، أو من حدّ الائتمان، أو من إيقاف الزبون أو الصنف؟
- ز. ما استخدام النوع `ReturnedPendingSalesDelivery` (5)؟

</div>

**Why we ask:** our API validates each voucher type before it reaches Shamel, using rules we inferred from the manual;
please correct them before we enable writes.

<sub>Ref: I-4 · I-14 · Q40 · Q41 · 03 §15.7 · 03 §27.2</sub>

#### ISCO-48 — Customer and item inserts

- (a) `/Customer/Post`: is the new customer code always generated by Shamel? The write model has no currency, credit
  limit or discount. Which defaults apply to these?
- (b) `/Item/Post`: does `value` contain the item code? Which item `type` values are allowed? Which values are expected
  in `currency` and `group`?
- (c) The item fields `trademark`, `producing_company`, `style` and `model` are numbers. Where can we read their valid
  values?

<div dir="rtl" lang="ar">

**إدخال الزبائن والأصناف**

- أ. `/Customer/Post`: هل يُولّد الشامل رمز الزبون الجديد دائماً؟ لا يتضمن نموذج الإدخال العملة وحدّ الائتمان والخصم، فما القيم الافتراضية التي تُطبَّق عليها؟
- ب. `/Item/Post`: هل يحتوي الحقل `value` على رمز الصنف؟ وما قيم `type` المسموحة؟ وما القيم المتوقعة في `currency` و`group`؟
- ج. حقول الصنف `trademark` و`producing_company` و`style` و`model` أرقام، فمن أين يمكننا قراءة القيم الصحيحة لها؟

</div>

**Why we ask:** these inserts are planned for our second phase, and any default Shamel applies silently must be shown to
whoever approves the write.

<sub>Ref: Q29 · Q42 · U §4.3 · U §4.4</sub>

#### ISCO-54 — Authentication check before a write is executed

Suppose a write (`/Voucher/Post2`, `/Customer/Post`, `/Item/Post` or `/CostCenter/Post`) is sent with a `token` that
has expired or is invalid.

- (a) Does the API always check the `username` and `token` headers before it executes anything, so that an
  authentication failure guarantees that nothing was saved?
- (b) Can an authentication-failure response ever follow a write that was partly or fully executed (for example, if
  the session expires while a long voucher is being saved)?
- (c) Is the response for an expired token on a write the same as on a read (ISCO-18 (c))?

<div dir="rtl" lang="ar">

**التحقق من المصادقة قبل تنفيذ عملية الإدخال**

لنفترض أن عملية إدخال (`/Voucher/Post2` أو `/Customer/Post` أو `/Item/Post` أو `/CostCenter/Post`) أُرسلت برمز جلسة (`token`) منتهي الصلاحية أو غير صالح.

- أ. هل تتحقق الواجهة البرمجية دائماً من الترويستين `username` و`token` قبل تنفيذ أي شيء، بحيث يعني فشل المصادقة يقيناً أنه لم يُحفظ أي شيء؟
- ب. هل يمكن أن تُعاد استجابة فشل المصادقة بعد تنفيذ عملية الإدخال جزئياً أو كلياً (مثلاً إذا انتهت صلاحية الجلسة أثناء حفظ سند طويل)؟
- ج. هل الاستجابة عند استخدام رمز منتهي الصلاحية في عملية إدخال هي نفسها الاستجابة في عملية القراءة (انظر ISCO-18، البند ج)؟

</div>

**Why we ask:** when a write fails with an authentication error, we must know whether it is safe to log in again and
resend it. Until then we report the outcome as unknown and ask a person to check in Shamel; a guarantee that
authentication comes first lets us resend such a write safely.

<sub>Ref: Q14 · Q39 · 01 §6.4 (step 6) · 01 §7.5</sub>

### 3.14 Enumerations (القيم المرمّزة)

#### ISCO-49 — Values of undocumented enumerations

Please give the possible values and their meanings (Arabic labels as shown in the program are welcome) for these fields:

| Field(s) | Where |
|---|---|
| `type` | Store (`/Files/GetStores`) |
| `creditType`, `attr`, `trans_permissions`, `level` | Customer (`/Customer/GetCustomers`) |
| `type` | CustomerContact (`getContacts`) |
| `type`, `eval_unit` | Item (`/Item/GetItems`, `/Item/Post`) |
| `stopped`, `paused`, `has_serial`, `has_measure`, `has_color`, `has_expiry` (only 0 and 1?) | Item (`/Item/GetItems`) |
| `status` | ItemSerial (`/Item/GetItemsSerials`) |
| `payment_type` | VoucherHeader |
| `unit` (an index 1–6 into `unit1` … `unit6`?) | VoucherItems |
| `debit_credit` | VoucherAccounts |
| `cr_dr` | `/Voucher/GetExtraVouchers` |
| `discount_type` | `/Customer/GetCustomerPricesAsRows` |
| `type` (text) | AccountsheetColumns (both account-statement reports) |
| `type` (number) | Filter of `/CostCenter/GetCostCenterAccountsheet` |
| `type` (text) | CostCenterDTO (`/CostCenter/Post`) |

Also: the voucher-type numbers that the manual does not list (1, 3, 6–8, 11, 13–15, 17–21). Do they exist, and can
vouchers of those types be read through the API?

<div dir="rtl" lang="ar">

**قيم الحقول المرمّزة غير الموثّقة**

نرجو تزويدنا بالقيم الممكنة لكل حقل من الحقول الواردة في الجدول أعلاه ومعنى كل قيمة (ويُفضَّل ذكر التسميات العربية كما تظهر في البرنامج). كما نرجو إفادتنا بشأن أرقام أنواع السندات غير المذكورة في الدليل (1، 3، 6–8، 11، 13–15، 17–21): هل هي موجودة، وهل يمكن قراءة سندات هذه الأنواع عبر الواجهة البرمجية؟

</div>

**Why we ask:** we publish these fields as raw numbers marked provisional; your answers let us name them before our
API's first stable release.

<sub>Ref: I-20 · I-3 · Q44 · U §6.1 · U §6.4 · 03 §3.4</sub>

### 3.15 Versions, test environment and roadmap (الإصدارات وبيئة الاختبار وخطة التطوير)

#### ISCO-50 — Shamel version, API versioning and change notices

**[Priority · أولوية]**

- (a) Which versions of Shamel and of its Web API are installed at our company [our version, if known: …]? How can we
  read the version (from the API or from the program)?
- (b) Does the manual we have match that version? Is there a newer manual?
- (c) How is the API versioned? Is there a changelog, and how much notice is given before a breaking change (a renamed
  field, a removed endpoint, changed behaviour)? Can a Shamel update change the API's behaviour?
- (d) The name `/Voucher/Post2` implies an older `/Voucher/Post`. Is the old one deprecated, and should we use `Post2`
  only?
- (e) Which IIS and .NET versions does the API require?

<div dir="rtl" lang="ar">

**إصدار الشامل وإدارة إصدارات الواجهة البرمجية والإبلاغ عن التغييرات**

- أ. ما إصدار برنامج الشامل وإصدار واجهته البرمجية المثبّتان لدى شركتنا [إصدارنا إن كان معروفاً: …]؟ وكيف يمكن معرفة رقم الإصدار (من الواجهة البرمجية أو من البرنامج)؟
- ب. هل يتوافق الدليل الذي لدينا مع هذا الإصدار؟ وهل يوجد دليل أحدث؟
- ج. كيف تُدار إصدارات الواجهة البرمجية؟ هل يوجد سجل للتغييرات؟ وما مدة الإشعار المسبق قبل أي تغيير غير متوافق (إعادة تسمية حقل، أو إزالة نقطة نهاية، أو تغيير في السلوك)؟ وهل يمكن أن تؤدي تحديثات الشامل إلى تغيير سلوك الواجهة البرمجية؟
- د. يوحي اسم `/Voucher/Post2` بوجود نسخة أقدم باسم `/Voucher/Post`. فهل النسخة القديمة متوقفة، وهل يجب أن نستخدم `Post2` فقط؟
- هـ. ما إصدارات IIS و.NET التي تتطلبها الواجهة البرمجية؟

</div>

**Why we ask:** our client mirrors your API's exact behaviour; we need to know when a Shamel update could break the
integration, so that we can test before upgrading.

<sub>Ref: Q22 · 02 §20.2 #8 · 00 §11</sub>

#### ISCO-51 — Test or staging environment

- (a) Can you provide a test company, a copy of our database or a demo database where we can test the API, especially
  writes, without affecting real accounting data?
- (b) Can a second API instance point to that test database on the same server?
- (c) Is there a licence cost for a test environment?

<div dir="rtl" lang="ar">

**بيئة اختبار أو قاعدة بيانات تجريبية**

- أ. هل يمكنكم توفير شركة تجريبية، أو نسخة من قاعدة بياناتنا، أو قاعدة بيانات للعرض التوضيحي، نختبر عليها الواجهة البرمجية، وخاصة عمليات الإدخال، دون التأثير على البيانات المحاسبية الحقيقية؟
- ب. هل يمكن تشغيل نسخة ثانية من الواجهة البرمجية مرتبطة بقاعدة البيانات التجريبية على الخادم نفسه؟
- ج. هل توجد تكلفة ترخيص لبيئة الاختبار؟

</div>

**Why we ask:** our own simulator covers development, but every write type must be verified against real Shamel before
we enable it, and we will not test writes on live data.

<sub>Ref: 03 §27.2 · 00 §6</sub>

#### ISCO-52 — Requesting new endpoints or changes

- (a) Can we request new endpoints or changes? What are the process, cost and typical timeline?
- (b) These would help us most. Please tell us if any of them already exist:
  - pagination (page and size) and a total count on large lists;
  - lookup lists for codes that the API uses but cannot list: GL accounts, cost centers, towns and villages, payment
    terms, customer classifications and contact types, item types, trademarks, producing companies, styles, models,
    organizations and payment types;
  - a change feed that includes deletions, or a date-and-time `lastupdatedate` on more entities (vouchers, balances);
  - endpoints to update or cancel vouchers, customers and items;
  - a voucher-type filter on `GetVouchers`, and a voucher lookup by `manual_code`;
  - an endpoint that returns item image bytes.
- (c) Who is our technical contact for API questions, and what is the support channel?

<div dir="rtl" lang="ar">

**طلب نقاط نهاية جديدة أو تعديلات**

- أ. هل يمكننا طلب نقاط نهاية جديدة أو تعديلات؟ وما الإجراءات والتكلفة والمدة المعتادة؟
- ب. فيما يلي أكثر ما نراه مفيداً، ونرجو إعلامنا إن كان بعضه متوفراً أصلاً:
  - تقسيم القوائم الكبيرة إلى صفحات (رقم الصفحة وحجمها) مع العدد الإجمالي للسجلات؛
  - قوائم مرجعية للرموز التي تستخدمها الواجهة دون إمكانية استعراضها: الحسابات العامة، ومراكز التكلفة، والبلدات والقرى، وشروط الدفع، وتصنيفات الزبائن وأنواع جهات الاتصال، وأنواع الأصناف، والعلامات التجارية، والشركات المنتجة، والطرازات، والموديلات، والمؤسسات، وأنواع الدفع؛
  - سجلّ تغييرات يشمل عمليات الحذف، أو دعم `lastupdatedate` بالتاريخ والوقت لكيانات أكثر (السندات والأرصدة)؛
  - نقاط نهاية لتعديل السندات والزبائن والأصناف أو إلغائها؛
  - تصفية `GetVouchers` حسب نوع السند، والبحث عن سند بواسطة `manual_code`؛
  - نقطة نهاية تُعيد محتوى صور الأصناف.
- ج. من هو مسؤول التواصل الفني لأسئلة الواجهة البرمجية، وما قناة الدعم المعتمدة؟

</div>

**Why we ask:** each item removes a workaround in our layer (full downloads, partial validation, manual corrections in
Shamel).

<sub>Ref: Q13 · Q42 · Q43 · 00 §9</sub>

### 3.16 Licensing and commercial use (الترخيص والاستخدام التجاري)

#### ISCO-53 — Permission to build the integration layer, and possible commercial use later

**[Priority · أولوية]**

- (a) Do the Shamel licence terms allow us to build and operate an internal integration layer (gateway) that calls the
  Shamel Web API on behalf of our own internal tools? Are there conditions we must follow?
- (b) Is the API licensed per user or per connection? Does the one Shamel service account that our layer uses need a
  specific licence, and are there additional fees?
- (c) Later, not now, we may wish to offer this layer to other Shamel customers, as a hosted service or as software they
  install themselves. Would ISCO allow this, and under what conditions (partnership, certification, revenue share,
  written agreement)?
- (d) May product documentation say that it works with Shamel? Are there rules for using the Shamel or ISCO name?

<div dir="rtl" lang="ar">

**الإذن ببناء طبقة التكامل والاستخدام التجاري المحتمل مستقبلاً**

- أ. هل تسمح شروط ترخيص الشامل لنا ببناء وتشغيل طبقة تكامل داخلية (بوابة) تستدعي واجهة الشامل البرمجية لصالح أدواتنا الداخلية؟ وهل توجد شروط يجب علينا الالتزام بها؟
- ب. هل يُحتسب ترخيص الواجهة البرمجية بعدد المستخدمين أم بعدد الاتصالات؟ وهل يحتاج حساب الخدمة الواحد الذي تستخدمه طبقتنا إلى ترخيص خاص؟ وهل توجد رسوم إضافية؟
- ج. قد نرغب مستقبلاً، وليس في الوقت الحالي، في تقديم هذه الطبقة لعملاء آخرين يستخدمون الشامل، كخدمة مستضافة أو كبرنامج يثبّتونه لديهم. فهل تسمح ISCO بذلك، وبأي شروط (شراكة، أو اعتماد، أو تقاسم إيرادات، أو اتفاقية مكتوبة)؟
- د. هل يجوز أن تذكر وثائق المنتج أنه يعمل مع برنامج الشامل؟ وهل توجد قواعد لاستخدام اسم الشامل أو اسم ISCO؟

</div>

**Why we ask:** we want to build on a clear, written understanding with ISCO from the start, both for internal use now
and for any commercial step later.

<sub>Ref: 00 §2 · 00 §11 · 02 §5.3 (LV-13)</sub>

---

## Appendix A — Traceability index (internal)

Each older reference and the question(s) that now carry it. "–" = no question needed.

### A.1 Upstream reference, U §7 (`Qnn`)

| Ref | Question | Ref | Question | Ref | Question | Ref | Question |
|---|---|---|---|---|---|---|---|
| Q1 | ISCO-18 | Q2 | ISCO-19, ISCO-43 | Q3 | ISCO-19, ISCO-39 | Q4 | ISCO-12 |
| Q5 | ISCO-13 | Q6 | ISCO-11 | Q7 | ISCO-11 | Q8 | ISCO-14 |
| Q9 | ISCO-16 | Q10 | ISCO-13 | Q11 | ISCO-05, ISCO-07 | Q12 | ISCO-17 |
| Q13 | ISCO-21, ISCO-52 | Q14 | ISCO-01, ISCO-02, ISCO-18, ISCO-54 | Q15 | ISCO-03 | Q16 | ISCO-03 |
| Q17 | ISCO-25 | Q18 | ISCO-22 | Q19 | ISCO-15 | Q20 | ISCO-39 |
| Q21 | ISCO-37 | Q22 | ISCO-50, ISCO-55 | Q23 | ISCO-40, ISCO-41 | Q24 | ISCO-26 |
| Q25 | ISCO-33 | Q26 | ISCO-34 | Q27 | ISCO-27 | Q28 | ISCO-35 |
| Q29 | ISCO-32, ISCO-35, ISCO-48 | Q30 | ISCO-32 | Q31 | ISCO-28 | Q32 | ISCO-35 |
| Q33 | ISCO-29 | Q34 | ISCO-30 | Q35 | ISCO-38 | Q36 | ISCO-28 |
| Q37 | ISCO-31 | Q38 | ISCO-44 | Q39 | ISCO-43, ISCO-54 | Q40 | ISCO-45, ISCO-47 |
| Q41 | ISCO-24, ISCO-46, ISCO-47 | Q42 | ISCO-39, ISCO-48, ISCO-52 | Q43 | ISCO-23, ISCO-52 | Q44 | ISCO-49 |
| Q45 | – (naming only; `/v1` renames regardless) | Q46 | ISCO-17 | Q47 | ISCO-20 | Q48 | ISCO-14 |

U §6.4 (undocumented enum values) → ISCO-49, plus ISCO-27, ISCO-33 and ISCO-39 for context.

### A.2 API design, 03 §27.3 (`I-n`)

| Ref | Question | Ref | Question | Ref | Question | Ref | Question |
|---|---|---|---|---|---|---|---|
| I-1 | ISCO-26 | I-2 | ISCO-33 | I-3 | ISCO-49 | I-4 | ISCO-47 |
| I-5 | ISCO-45 | I-6 | ISCO-43, ISCO-19 | I-7 | ISCO-46 | I-8 | ISCO-24, ISCO-21 |
| I-9 | ISCO-42 | I-10 | ISCO-41 | I-11 | ISCO-22 | I-12 | ISCO-38 |
| I-13 | ISCO-37 | I-14 | ISCO-47 | I-15 | ISCO-38 | I-16 | ISCO-35, ISCO-25 |
| I-17 | ISCO-44 | I-18 | ISCO-32 | I-19 | ISCO-17 | I-20 | ISCO-49 |
| I-21 | ISCO-28 | I-22 | ISCO-28 | | | | |

### A.3 Security, 02 §20.2 (#n) and §20.3

| Ref | Question | Ref | Question |
|---|---|---|---|
| #1 HTTPS | ISCO-05 | #6 Bind to localhost | ISCO-07 |
| #2 `image_path` | ISCO-34 | #7 Header logging | ISCO-08 |
| #3 Session lifetime, second login, revocation | ISCO-01, ISCO-02 | #8 Versions, patch cadence, vulnerability reports | ISCO-10, ISCO-50 |
| #4 IIS Windows authentication | ISCO-06 | #9 Rate/concurrency limits, response sizes | ISCO-20, ISCO-21 |
| #5 API users, password reuse, API-only user | ISCO-04 | #10 SQL Server and other exposed services | ISCO-09 |

02 §20.3 (session holder protocol for connector-held credentials) depends on ISCO-01 (c)–(e).

### A.4 Permissions, 04 §17.3 (#n) and §17.4

| Ref | Question | Ref | Question |
|---|---|---|---|
| #1 Salesman scoping per endpoint | ISCO-25 (a) | #5 `AccountsheetColumns.type` | ISCO-38 (d) |
| #2 `GetCustomers` without salesman | ISCO-25 (b) | #6 `GetSalesmen` shape | ISCO-26 |
| #3 Scoping on writes | ISCO-25 (d) | #7 Restricted API-only user | ISCO-04 |
| #4 Last-price `customer` | ISCO-37 (c) | §17.4 #2, #3 (assumptions) | ISCO-38 (a), ISCO-33 (e) |

### A.5 Architecture, 01 §16

| Item | Question |
|---|---|
| Session lifetime; new login invalidates; logout; error body for an invalid token | ISCO-01, ISCO-02, ISCO-18 (c) |
| Account lockout policy | ISCO-03 (d) |
| Recommended concurrency / requests per second / throttling (assumption 3: `max_concurrency = 8`) | ISCO-20 |
| HTTP methods (assumption 2), HTTPS (assumption 1), gzip, maximum response sizes | ISCO-12, ISCO-05, ISCO-11, ISCO-21 |
| `image_path` format (assumption 4) | ISCO-34 |
| Stack traces / SQL in errors | ISCO-18 (d) |
| Authentication checked before a write executes (01 §6.4 step 6) | ISCO-54 |
| Response `Content-Type` other than `application/json` (01 §7.4) | ISCO-17 (f) |
| Undocumented endpoints to know about or block (01 §6.5) | ISCO-50 (d), ISCO-55 |

**Retired ids of an earlier 01 §16.2 (`ISCO-1` … `ISCO-28`, without a leading zero).** That draft numbered its own
list; 01 §16.2 now only maps its topics to this document. An old id must never be read as the `ISCO-0n` of the same
digit (old `ISCO-8` is ISCO-01, not ISCO-08).

| Old id | Topic | Question(s) here |
|---|---|---|
| ISCO-1 | Permission to wrap the API; offering Bawaba to other Shamel customers later; licence terms, fees | ISCO-53 |
| ISCO-2 | API versioning, change notices, changelog, test server; deployed versions; patch cadence, vulnerability reports | ISCO-50, ISCO-51, ISCO-10 |
| ISCO-3 | HTTPS and certificates; base URL and scheme; HTTP method per endpoint; gzip; response `Content-Type` | ISCO-05, ISCO-07 (a), ISCO-12, ISCO-11 (d), ISCO-17 (c), (f) |
| ISCO-4 | Undocumented paging, limit, sort or field-selection parameters; largest response sizes | ISCO-21 (b), (c), (e) |
| ISCO-5 | Recommended concurrency and requests per second; throttling; server-side timeouts | ISCO-20 |
| ISCO-6 | IIS Windows authentication; binding the API site to `127.0.0.1` | ISCO-06, ISCO-07 (b) |
| ISCO-7 | Stable serialization; wire JSON casing; `null` versus empty string | ISCO-17 (a), (b), (d) |
| ISCO-8 | Session lifetime; second login invalidates the first; server-side revocation, logout | ISCO-01, ISCO-02 |
| ISCO-9 | Error bodies for an invalid token and for failed logins; lockout policy; content of the `username` header | ISCO-18 (c), ISCO-03 |
| ISCO-10 | Authentication checked before a write executes | ISCO-54 |
| ISCO-11 | API users versus desktop users; API access per user; restricted API-only user | ISCO-04 |
| ISCO-12 | Logging of request headers by Shamel or IIS | ISCO-08 |
| ISCO-13 | Stack traces or SQL in errors; `ErrorMessage` shapes; rejection messages for duplicates and validation | ISCO-18 (a), (d), ISCO-19, ISCO-43 (b) |
| ISCO-14 | Salesman scoping per endpoint; `store` header on `GetItems` | ISCO-25 (a), ISCO-35 (a) |
| ISCO-15 | `GetCustomers` for a user without salesman binding; salesman scoping on writes | ISCO-25 (b), (d) |
| ISCO-16 | `/Files/GetSalesmen` response | ISCO-26 |
| ISCO-17 | `lastupdatedate` semantics | ISCO-22 |
| ISCO-18 | Date-range inclusivity, maximum range, timezone; `GetVouchers` date basis; `update_date` | ISCO-24, ISCO-21 (d), ISCO-23 (c), (d) |
| ISCO-19 | Deletions and how to observe them | ISCO-23 (a), ISCO-22 (g) |
| ISCO-20 | `ItemCatalog.image_path` format; image endpoint | ISCO-34 |
| ISCO-21 | `GetCustomerPricesAsRows` filters and fields | ISCO-33 |
| ISCO-22 | `GetLastPriceReport`: `customer` code or name; global or per customer | ISCO-37 (b), (c) |
| ISCO-23 | `GetAccountsheet`: accounts accepted, number format, `start_date`, `type` | ISCO-38 |
| ISCO-24 | `GetDelivery`; voucher types of `GetExtraVouchers`; `GetStatus` | ISCO-41 (a), ISCO-40 (b), ISCO-42 |
| ISCO-25 | Voucher-write semantics (`debit_credit`/`cr_dr`, `accounts`, cash amount, totals and VAT, prefixes, destination store, `system_id`) | ISCO-49, ISCO-47 (a), (b), (d), ISCO-46 (a), ISCO-45 (a), ISCO-44 |
| ISCO-26 | Currency fields and rates; customer fields; undocumented enumerations | ISCO-28, ISCO-32, ISCO-49 |
| ISCO-27 | `/Voucher/Post` still active; other undocumented endpoints | ISCO-50 (d), ISCO-55 |
| ISCO-28 | SQL Server reachable from the LAN; other exposed services | ISCO-09 |

### A.6 Operations, 05 §11

| Item | Question |
|---|---|
| `lastupdatedate` comparison, granularity, timezone, what updates it | ISCO-22 |
| `GetVouchers` date basis, maximum range and size, `update_date` | ISCO-23 (c)–(d), ISCO-21 (d) |
| Voucher types in `GetExtraVouchers` | ISCO-40 (b) |
| `GetStatus` (`manual` meaning, representation, unknown values, shared manual codes) | ISCO-42 |
| Deletions | ISCO-23 (a) |
| Salesman scoping of balances, stock, vouchers | ISCO-25 (a) |
| Stable serialisation (also assumption 1) | ISCO-17 (d) |

### A.7 Owner's examples, 00 §11

GetSalesmen response shape → ISCO-26 · token lifetime and expiry → ISCO-01 · HTTPS → ISCO-05 · rate and concurrency
limits → ISCO-20 · pagination → ISCO-21 · error format → ISCO-18 · `lastupdatedate` semantics and timezone → ISCO-22,
ISCO-24 · permission to wrap and resell later → ISCO-53 · versioning → ISCO-50.
