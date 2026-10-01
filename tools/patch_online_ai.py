from pathlib import Path

root = Path('buildsrc/GoalRiderV3')
manifest = root / 'app/src/main/AndroidManifest.xml'
html = root / 'app/src/main/assets/index.html'

# INTERNET permission
m = manifest.read_text(encoding='utf-8')
perm = '<uses-permission android:name="android.permission.INTERNET" />'
if perm not in m:
    m = m.replace('<manifest xmlns:android="http://schemas.android.com/apk/res/android">', '<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n    ' + perm)
manifest.write_text(m, encoding='utf-8')

s = html.read_text(encoding='utf-8')

# Expand bottom nav to five buttons.
s = s.replace('grid-template-columns:repeat(4,1fr)', 'grid-template-columns:repeat(5,1fr)')
old_nav = "<nav class=\"nav\"><button class=\"active\" onclick=\"closeSheet()\"><span>🏁</span>السباق</button><button onclick=\"openSheet('missions')\"><span>🎯</span>المهمات</button><button onclick=\"openSheet('rewards')\"><span>🎁</span>الجوائز</button><button onclick=\"openSheet('parents')\"><span>🔐</span>الوالدان</button></nav>"
new_nav = "<nav class=\"nav\"><button class=\"active\" onclick=\"closeSheet()\"><span>🏁</span>السباق</button><button onclick=\"openSheet('missions')\"><span>🎯</span>المهمات</button><button onclick=\"openNur()\"><span>🤖</span>المرافق</button><button onclick=\"openSheet('rewards')\"><span>🎁</span>الجوائز</button><button onclick=\"openSheet('parents')\"><span>🔐</span>الوالدان</button></nav>"
if old_nav in s:
    s = s.replace(old_nav, new_nav)

css = r'''
<style id="nur-online-style">
#nurOverlay{position:absolute;z-index:80;inset:0;background:#eef7ff;color:#14304c;display:none;flex-direction:column;direction:rtl}
#nurOverlay.show{display:flex}.nurHead{padding:max(16px,env(safe-area-inset-top)) 16px 12px;background:#fff;border-bottom:1px solid #dce8f3;display:flex;align-items:center;gap:10px}.nurHead .bot{width:50px;height:50px;border-radius:17px;background:linear-gradient(145deg,#74e0d5,#b6f4dc);display:grid;place-items:center;font-size:28px;border:2px solid #fff;box-shadow:0 5px 15px #245b6d26}.nurHeadText{flex:1}.nurHeadText b{font-size:20px;display:block}.nurHeadText small{color:#7890a6}.nurBack{border:0;width:44px;height:44px;border-radius:15px;background:#e6f0fa;font-size:22px}
.nurBody{flex:1;overflow:auto;padding:14px 14px 100px}.nurHello{background:linear-gradient(135deg,#d9f7fb,#edfbe5);border:1px solid #ccebf0;border-radius:22px;padding:14px;margin-bottom:12px}.nurModes{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:12px}.nurMode{border:2px solid #d8e8f5;background:#fff;border-radius:18px;padding:12px;text-align:right;color:#17324d}.nurMode.on{border-color:#26a9e8;box-shadow:0 0 0 3px #26a9e818}.nurMode span{font-size:26px}.nurMode b{display:block;font-size:16px;margin-top:3px}.nurMode small{color:#748ca3}.nurContext{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}.nurInput{width:100%;border:1px solid #c8d8e7;background:#fff;border-radius:14px;padding:10px;color:#17324d}.nurChat{display:flex;flex-direction:column;gap:8px}.nurMsg{max-width:88%;padding:11px 13px;border-radius:17px;line-height:1.55;white-space:pre-wrap}.nurMsg.user{align-self:flex-start;background:#176fe8;color:white;border-bottom-right-radius:5px}.nurMsg.bot{align-self:flex-end;background:white;border:1px solid #dbe7f2;border-bottom-left-radius:5px}.nurMeta{font-size:11px;color:#71869b;margin-top:3px}.nurComposer{position:absolute;left:0;right:0;bottom:0;background:#fff;border-top:1px solid #dbe6ef;padding:9px 10px calc(9px + env(safe-area-inset-bottom));display:flex;gap:8px}.nurComposer textarea{flex:1;resize:none;min-height:46px;max-height:100px;border:1px solid #c9d8e6;border-radius:15px;padding:11px}.nurSend{width:52px;border:0;border-radius:15px;background:#17aee8;color:white;font-size:22px}.nurSetup{background:#fff6d7;border:1px solid #f2d77a;border-radius:17px;padding:12px;margin:10px 0}.nurSetup button{border:0;border-radius:12px;background:#ff9e17;color:#223149;padding:9px 12px;font-weight:900}.nurThinking{opacity:.7;font-style:italic}.nurXp{display:inline-flex;gap:5px;align-items:center;background:#f0e6ff;color:#7043a8;border-radius:999px;padding:5px 9px;font-size:12px;font-weight:900}
</style>
'''
if 'id="nur-online-style"' not in s:
    s = s.replace('</head>', css + '</head>')

panel = r'''
<div id="nurOverlay">
  <div class="nurHead"><button class="nurBack" onclick="closeNur()">‹</button><div class="bot">🤖</div><div class="nurHeadText"><b>نُور · المرافق الذكي</b><small>متصل بالإنترنت · يتعلّم مع يوسف</small></div><div class="nurXp">🌱 <span id="nurTeacherXp">0</span> XP</div></div>
  <div class="nurBody" id="nurBody">
    <div class="nurHello"><b>مرحباً يوسف 👋</b><div>اسألني، دعني أشرح لك درساً، أو كن أنت المعلّم وأنا التلميذ.</div></div>
    <div class="nurModes">
      <button class="nurMode on" data-mode="ask" onclick="setNurMode('ask',this)"><span>💬</span><b>اسأل نُور</b><small>أي سؤال أو معلومة</small></button>
      <button class="nurMode" data-mode="teach" onclick="setNurMode('teach',this)"><span>📚</span><b>علّمني</b><small>شرح درس خطوة بخطوة</small></button>
      <button class="nurMode" data-mode="teacher" onclick="setNurMode('teacher',this)"><span>🧑‍🏫</span><b>أنا المعلّم</b><small>يوسف يشرح ونُور يسأل</small></button>
      <button class="nurMode" data-mode="quiz" onclick="setNurMode('quiz',this)"><span>🧠</span><b>اختبرني</b><small>سؤال واحد في كل مرة</small></button>
    </div>
    <div class="nurContext"><input id="nurSubject" class="nurInput" placeholder="المادة: الفرنسية، الرياضيات..."><input id="nurLesson" class="nurInput" placeholder="الدرس الحالي"></div>
    <div id="nurSetup" class="nurSetup" style="display:none"><b>إعداد الذكاء مطلوب</b><div style="font-size:12px;margin:5px 0 8px">يُدخل أحد الوالدين مفتاح Gemini مرة واحدة. يبقى محفوظاً على هذا الهاتف.</div><button onclick="setupGeminiKey()">إعداد الوالدين</button></div>
    <div id="nurChat" class="nurChat"></div>
  </div>
  <div class="nurComposer"><textarea id="nurMessage" rows="1" placeholder="اكتب رسالتك إلى نُور..."></textarea><button id="nurSend" class="nurSend" onclick="sendNur()">➤</button></div>
</div>
'''
if 'id="nurOverlay"' not in s:
    s = s.replace('</main>', panel + '</main>')

js = r'''
<script id="nur-online-js">
const NUR_ENDPOINT='https://euccllpmhrxeagayvsgw.supabase.co/functions/v1/goal-rider-ai';
const NUR_APP_TOKEN='goal-rider-mobile-v1-2026';
let nurMode='ask', nurBusy=false;
let nurHistory=JSON.parse(localStorage.getItem('GoalRiderNurHistory')||'[]');
let nurLearning=JSON.parse(localStorage.getItem('GoalRiderNurLearning')||'{"understood":[],"needsReview":[],"teacherXp":0}');
function openNur(){document.getElementById('nurOverlay').classList.add('show');renderNurChat();refreshNurSetup();document.getElementById('nurTeacherXp').textContent=nurLearning.teacherXp||0}
function closeNur(){document.getElementById('nurOverlay').classList.remove('show')}
function setNurMode(mode,btn){nurMode=mode;document.querySelectorAll('.nurMode').forEach(x=>x.classList.remove('on'));btn.classList.add('on');const p={ask:'اسأل أي سؤال يا يوسف…',teach:'ما الدرس الذي تريد أن أشرحه لك؟',teacher:'اشرح لي ما تعلمته، وأنا سأكون تلميذك.',quiz:'اكتب المادة أو الدرس وسأبدأ الاختبار.'};document.getElementById('nurMessage').placeholder=p[mode]||p.ask}
function refreshNurSetup(){document.getElementById('nurSetup').style.display=localStorage.getItem('GoalRiderGeminiKey')?'none':'block'}
function setupGeminiKey(){let pin=prompt('أدخل رمز الوالدين');if(pin!==String((window.s&&s.pin)||'1234')){alert('رمز الوالدين غير صحيح');return}let key=prompt('ألصق مفتاح Gemini API');if(key&&key.trim().length>20){localStorage.setItem('GoalRiderGeminiKey',key.trim());refreshNurSetup();alert('تم حفظ مفتاح الذكاء على هذا الهاتف')}else if(key!==null)alert('المفتاح غير صالح')}
function escNur(x){return String(x||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function renderNurChat(){let c=document.getElementById('nurChat');c.innerHTML=nurHistory.slice(-20).map(x=>`<div class="nurMsg ${x.role==='assistant'?'bot':'user'}">${escNur(x.text)}${x.sources&&x.sources.length?`<div class="nurMeta">المصادر: ${escNur(x.sources.join(' · '))}</div>`:''}</div>`).join('');setTimeout(()=>{document.getElementById('nurBody').scrollTop=999999},40)}
function learningSummary(){let u=(nurLearning.understood||[]).slice(-8).join('، '),r=(nurLearning.needsReview||[]).slice(-8).join('، ');return `يفهم: ${u||'لا بيانات بعد'}. يحتاج مراجعة: ${r||'لا بيانات بعد'}.`}
function mergeSignals(sig){if(!sig)return;let u=Array.isArray(sig.understood)?sig.understood:[],r=Array.isArray(sig.needsReview)?sig.needsReview:[];nurLearning.understood=[...(nurLearning.understood||[]),...u].slice(-30);nurLearning.needsReview=[...(nurLearning.needsReview||[]),...r].slice(-30);if(nurMode==='teacher'&&u.length){nurLearning.teacherXp=(nurLearning.teacherXp||0)+Math.min(5,u.length*2)}localStorage.setItem('GoalRiderNurLearning',JSON.stringify(nurLearning));document.getElementById('nurTeacherXp').textContent=nurLearning.teacherXp||0}
async function sendNur(){if(nurBusy)return;let box=document.getElementById('nurMessage'),msg=box.value.trim();if(!msg)return;let key=localStorage.getItem('GoalRiderGeminiKey');if(!key){refreshNurSetup();setupGeminiKey();key=localStorage.getItem('GoalRiderGeminiKey');if(!key)return}nurHistory.push({role:'user',text:msg});nurHistory=nurHistory.slice(-16);localStorage.setItem('GoalRiderNurHistory',JSON.stringify(nurHistory));box.value='';renderNurChat();nurBusy=true;document.getElementById('nurSend').disabled=true;let wait={role:'assistant',text:'نُور يفكر…',temp:true};nurHistory.push(wait);renderNurChat();try{let hist=nurHistory.filter(x=>!x.temp).slice(-8);let r=await fetch(NUR_ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json','x-goalrider-app':NUR_APP_TOKEN,'x-gemini-key':key},body:JSON.stringify({message:msg,mode:nurMode,subject:document.getElementById('nurSubject').value.trim(),lesson:document.getElementById('nurLesson').value.trim(),language:/[\u0600-\u06ff]/.test(msg)?'ar':'fr',history:hist,learningSummary:learningSummary(),allowSearch:true})});let d=await r.json();nurHistory=nurHistory.filter(x=>!x.temp);if(!r.ok){throw new Error(d.message||d.details||d.error||'تعذر الاتصال بالمرافق')}nurHistory.push({role:'assistant',text:d.reply||'لم يصلني جواب.',sources:d.sources||[]});mergeSignals(d.learningSignals);localStorage.setItem('GoalRiderNurHistory',JSON.stringify(nurHistory.slice(-16)));renderNurChat()}catch(e){nurHistory=nurHistory.filter(x=>!x.temp);nurHistory.push({role:'assistant',text:'تعذر الاتصال الآن: '+(e.message||e)});renderNurChat()}finally{nurBusy=false;document.getElementById('nurSend').disabled=false}}
document.addEventListener('keydown',e=>{if(document.getElementById('nurOverlay')?.classList.contains('show')&&e.key==='Enter'&&!e.shiftKey&&document.activeElement?.id==='nurMessage'){e.preventDefault();sendNur()}})
</script>
'''
if 'id="nur-online-js"' not in s:
    s = s.replace('</body>', js + '</body>')

html.write_text(s, encoding='utf-8')
print('Goal Rider Online AI patch applied')
