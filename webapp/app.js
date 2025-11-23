// === ИНИЦИАЛИЗАЦИЯ ===
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// === КОНФИГУРАЦИЯ И СОСТОЯНИЕ ===
const STEP = {
  NAME: 'step-name',
  TYPE: 'step-type',
  CHAR: 'step-character',
  FORM: 'step-form',
  PROB: 'step-problem',
  RES: 'step-result'
};

let state = {
  name: "",
  answerType: "single", // 'single' | 'group'
  characters: ["usagi"],
  form: "human",
  problem: "",
  chatHistory: [] // История переписки
};

// ДАННЫЕ (Должны совпадать с сервером)
const CHARACTERS = {
  "usagi": { label: "Усаги", forms: { "human": { title: "Усаги Цукино 👧", img: "https://i.pinimg.com/736x/a4/47/c4/a447c423d530b9cac4612a9f71c96ddc.jpg" }, "sailor": { title: "Сейлор Мун 🌙", img: "https://i.pinimg.com/736x/55/ff/32/55ff32a1d1a2e86ff41d76068672e108.jpg" }, "super": { title: "Супер Сейлор Мун 💫", img: "https://i.pinimg.com/736x/56/7b/38/567b38a7e0d7729573f997ded2448d5e.jpg" }, "eternal": { title: "Вечная Сейлор Мун ✨", img: "https://i.pinimg.com/1200x/a1/e5/52/a1e552f9276025313b66b8f3a36a3c44.jpg" } } },
  "ami": { label: "Ами", forms: { "human": { title: "Ами Мидзуно 📚", img: "https://i.pinimg.com/736x/0b/07/f9/0b07f95abbceecf7922c44ac333a48f2.jpg" }, "sailor": { title: "Сейлор Меркурий 💧", img: "https://i.pinimg.com/736x/b1/61/1a/b1611addcf1190d311218c22614e1e36.jpg" } } },
  "rei": { label: "Рей", forms: { "human": { title: "Рей Хино 🔥", img: "https://i.pinimg.com/736x/d7/9c/61/d79c617912ae0e4d510660c32c971227.jpg" }, "sailor": { title: "Сейлор Марс 🔥", img: "https://i.pinimg.com/736x/7f/e6/e8/7fe6e8b47812f4778d229903c1776744.jpg" } } },
  "minako": { label: "Минако", forms: { "human": { title: "Минако Айно 💛", img: "https://i.pinimg.com/736x/68/68/52/6868521a4cf61d75b40772b6f13c0504.jpg" }, "sailor": { title: "Сейлор Венера 💖", img: "https://i.pinimg.com/1200x/bb/e9/6e/bbe96e1b50292f72dab46e16dfd5f632.jpg" } } },
  "makoto": { label: "Макото", forms: { "human": { title: "Макото Кино 🌿", img: "https://i.pinimg.com/736x/49/27/8d/49278da7f93a6028a0a3d05bbd43fd22.jpg" }, "sailor": { title: "Сейлор Юпитер ⚡", img: "https://i.pinimg.com/736x/84/f8/c0/84f8c01989fa310f2ca46bd8bcd58af3.jpg" } } },
  "hotaru": { label: "Хотару", forms: { "human": { title: "Хотару Томоэ 🌙", img: "https://i.pinimg.com/736x/62/e8/61/62e861ea332c0bf8dafd00fd4e9571d9.jpg" }, "sailor": { title: "Сейлор Сатурн 🌑", img: "https://i.pinimg.com/736x/65/e3/95/65e3950cb55aaffbfd443ef8d5f3ae2a.jpg" } } },
  "setsuna": { label: "Сецуна", forms: { "human": { title: "Сецуна Мейо ⏳", img: "https://i.pinimg.com/736x/89/bf/f4/89bff47fee6011a503b18c274a0370a5.jpg" }, "sailor": { title: "Сейлор Плутон 🕰️", img: "https://i.pinimg.com/736x/d4/8b/89/d48b8992dfac715b928af9d974d4c37c.jpg" } } },
  "haruka": { label: "Харука", forms: { "human": { title: "Харука Тэнно 🌟", img: "https://i.pinimg.com/736x/a8/c9/9e/a8c99e3558ea0caf592cb06c1339f720.jpg" }, "sailor": { title: "Сейлор Уран 🌪️", img: "https://i.pinimg.com/1200x/ec/bd/fd/ecbdfd6392394b2d66fa68729eeb5948.jpg" } } },
  "michiru": { label: "Мичиру", forms: { "human": { title: "Мичиру Кайо 🌊", img: "https://i.pinimg.com/736x/a4/fe/e9/a4fee98a8f01e8a377a70759edbfc5df.jpg" }, "sailor": { title: "Сейлор Нептун 🎻", img: "https://i.pinimg.com/736x/ef/a9/72/efa97290c250e97924777c4551120f60.jpg" } } },
  "chibiusa": { label: "Чибиуса", forms: { "human": { title: "Чибиуса ✨", img: "https://i.pinimg.com/736x/40/74/49/4074490084d46e4d173179fe03427d2b.jpg" }, "sailor": { title: "Сейлор Чиби-Мун 💕", img: "https://i.pinimg.com/736x/09/89/00/098900bcc276be04da9e30b7cf3a6007.jpg" } } },
  "mamoru": { label: "Мамору", forms: { "human": { title: "Мамору Чиба 🌹", img: "https://i.pinimg.com/736x/68/f4/07/68f4077d2f6944bad32604a96a62f310.jpg" }, "sailor": { title: "Такседо Маск 🥶", img: "https://i.pinimg.com/736x/62/c0/97/62c0978a24a049425d9895a159ca3104.jpg" } } },
  "seiya": { label: "Сейя", forms: { "human": { title: "Сейя Кое ♂️⭐", img: "https://i.pinimg.com/736x/fa/44/48/fa4448c6b3b4d06e33e905e34256199b.jpg" }, "sailor": { title: "Сейлор Стар Файтер ⭐", img: "https://i.pinimg.com/736x/7c/f6/11/7cf6111d7e826a5e8008310206683b1e.jpg" } } },
  "taiki": { label: "Тайки", forms: { "human": { title: "Тайки Кое ♂️📚", img: "https://i.pinimg.com/736x/9d/cf/05/9dcf05f2328100ef411b710d30ffc465.jpg" }, "sailor": { title: "Сейлор Стар Хилер 📚", img: "https://i.pinimg.com/736x/32/1f/c6/321fc67961d968c73c972616e53721af.jpg" } } },
  "yaten": { label: "Ятен", forms: { "human": { title: "Ятен ♂️🎭", img: "https://i.pinimg.com/736x/68/b2/00/68b2006277d4c56dde09e0eb1cce61e0.jpg" }, "sailor": { title: "Сейлор Стар Мейкер 🎭", img: "https://i.pinimg.com/736x/90/42/a3/9042a33ae40ccc635e909c2ba00449fb.jpg" } } }
};

// === ЗВУКИ ===
const music = document.getElementById('bg-music');
const clickSound = document.getElementById('click-sound');
const magicSound = document.getElementById('magic-sound');
const selectSound = document.getElementById('select-sound');
let isMusicPlaying = false;

function playSound(el) { if(el) { el.currentTime=0; el.play().catch(()=>{}); } }

function initMusic() {
  const btn = document.getElementById('music-toggle');
  const startAudio = () => {
    if (!isMusicPlaying) {
      music.volume = 0.3; music.play().catch(()=>{});
      isMusicPlaying = true; btn.textContent = '🔊';
    }
    document.removeEventListener('click', startAudio);
  };
  document.addEventListener('click', startAudio);
  
  btn.onclick = (e) => {
    e.stopPropagation(); playSound(clickSound);
    if(isMusicPlaying) { music.pause(); btn.textContent = '🔇'; } 
    else { music.play(); btn.textContent = '🔊'; }
    isMusicPlaying = !isMusicPlaying;
  };
}

// === УТИЛИТЫ ===
function parseMarkdown(text) {
  if (!text) return "";
  let html = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  html = html.replace(/\n/g, '<br>');
  return html;
}

function updateProgressBar(stepName) {
  const map = { 'step-name': 1, 'step-type': 2, 'step-character': 3, 'step-form': 3.5, 'step-problem': 4, 'step-result': 5 };
  let n = map[stepName] || 1;
  if (n === 3.5) n = 3;
  
  document.querySelector('.progress-fill').style.width = `${((n-1)/4)*100}%`;
  document.getElementById('current-step').textContent = Math.ceil(n);
  document.querySelectorAll('.step-dot').forEach((dot, i) => {
    dot.classList.remove('active', 'completed');
    if (i+1 === Math.ceil(n)) dot.classList.add('active');
    else if (i+1 < Math.ceil(n)) dot.classList.add('completed');
  });
}

// === НАВИГАЦИЯ ===
function show(stepId, dir = 'next') {
  playSound(clickSound);
  const cur = document.querySelector('.card.active');
  const next = document.getElementById(stepId);
  
  if (cur && next) {
    cur.classList.remove('active');
    if (dir === 'next') { cur.classList.add('slide-in-prev'); next.classList.add('slide-in-next'); }
    else if (dir === 'prev') { cur.classList.add('slide-in-next'); next.classList.add('slide-in-prev'); }
    else if (dir === 'zoom') { next.classList.add('zoom-in'); }
    
    setTimeout(() => {
      next.classList.add('active');
      updateProgressBar(stepId);
      if (stepId === STEP.FORM) renderForms();
      if (stepId === STEP.CHAR) renderChars();
      setTimeout(() => {
        cur.classList.remove('slide-in-prev', 'slide-in-next', 'zoom-in');
        next.classList.remove('slide-in-prev', 'slide-in-next', 'zoom-in');
      }, 400);
    }, 50);
  } else if (next) {
    document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
    next.classList.add('active');
    updateProgressBar(stepId);
  }
}

// === РЕНДЕР ПЕРСОНАЖЕЙ ===
function renderChars() {
  const container = document.getElementById('characters');
  container.innerHTML = '';
  const title = document.getElementById('character-title');
  
  if (state.answerType === 'group') title.innerHTML = `Выбери команду <span style="color:var(--accent-2)">${state.characters.length}/4</span>`;
  else title.textContent = 'Выбери персонажа';

  for (const key in CHARACTERS) {
    const char = CHARACTERS[key];
    const div = document.createElement('div');
    div.className = 'char-card';
    if (state.answerType === 'group') {
      div.classList.add('multiple');
      if (state.characters.includes(key)) div.classList.add('selected');
    } else {
      if (state.characters[0] === key) div.classList.add('selected');
    }
    
    div.innerHTML = `<img src="${Object.values(char.forms)[0].img}" /><div class="label">${char.label}</div>`;
    div.onclick = () => handleCharClick(key);
    container.appendChild(div);
  }
}

function handleCharClick(key) {
  playSound(selectSound);
  if (state.answerType === 'single') {
    state.characters = [key];
    renderChars();
    const forms = Object.keys(CHARACTERS[key].forms);
    if (forms.length > 1) show(STEP.FORM, 'next');
    else { state.form = forms[0]; show(STEP.PROB, 'next'); }
  } else {
    const idx = state.characters.indexOf(key);
    if (idx > -1) state.characters.splice(idx, 1);
    else if (state.characters.length < 4) state.characters.push(key);
    else tg.showAlert('Максимум 4 персонажа');
    renderChars();
  }
}

function renderForms() {
  const container = document.getElementById('form-options');
  container.innerHTML = '';
  const char = CHARACTERS[state.characters[0]];
  
  for (const fKey in char.forms) {
    const form = char.forms[fKey];
    const div = document.createElement('div');
    div.className = 'form-card';
    if (state.form === fKey) div.classList.add('selected');
    div.innerHTML = `<img src="${form.img}" /><div class="label">${form.title}</div>`;
    div.onclick = () => {
      playSound(selectSound); state.form = fKey;
      document.querySelectorAll('.form-card').forEach(c => c.classList.remove('selected'));
      div.classList.add('selected');
    };
    container.appendChild(div);
  }
  if (!state.form && container.firstChild) container.firstChild.click();
}

// === ЛОГИКА ЧАТА ===
function addMessage(role, text) {
  const container = document.getElementById('chat-container');
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.innerHTML = parseMarkdown(text);
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

async function sendToBackend() {
  const loader = document.getElementById('loading');
  const controls = document.getElementById('chat-controls');
  
  loader.classList.remove('hidden');
  controls.classList.add('hidden');
  
  try {
    const isLocal = window.location.hostname === 'localhost';
    const backend = isLocal ? 'http://127.0.0.1:5000' : 'https://sailormoonpsychohelp-7bkw.onrender.com';
    
    const resp = await fetch(`${backend}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: state.name,
        answer_type: state.answerType,
        character: state.answerType === 'single' ? state.characters[0] : state.characters.join(','),
        form: state.form,
        history: state.chatHistory
      })
    });
    
    const data = await resp.json();
    loader.classList.add('hidden');
    
    if (data.ok) {
      tg.HapticFeedback.notificationOccurred('success');
      state.chatHistory.push({ role: "assistant", content: data.advice });
      addMessage('bot', data.advice);
      controls.classList.remove('hidden');
      if(window.innerWidth > 600) document.getElementById('chat-input').focus();
    } else {
      throw new Error(data.error);
    }
  } catch (e) {
    loader.classList.add('hidden');
    controls.classList.remove('hidden');
    addMessage('bot', "**Ошибка лунной связи 🌑**\nПопробуй нажать кнопку отправки еще раз.");
  }
}

// === INIT ===
document.addEventListener('DOMContentLoaded', () => {
  initMusic();
  if (tg.initDataUnsafe?.user?.first_name) document.getElementById('input-name').value = tg.initDataUnsafe.user.first_name;
  
  // STEP 1: Name
  document.getElementById('btn-name-next').onclick = () => {
    const val = document.getElementById('input-name').value.trim();
    if (val.length < 2) return tg.showAlert('Введи имя!');
    state.name = val; show(STEP.TYPE);
  };
  
  // STEP 2: Type
  document.querySelectorAll('.type-option').forEach(opt => {
    opt.onclick = () => {
      playSound(selectSound);
      document.querySelectorAll('.type-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      state.answerType = opt.dataset.type;
      state.characters = state.answerType === 'group' ? [] : ['usagi'];
    };
  });
  document.getElementById('btn-type-back').onclick = () => show(STEP.NAME, 'prev');
  document.getElementById('btn-type-next').onclick = () => { renderChars(); show(STEP.CHAR); };
  
  // STEP 3: Char
  document.getElementById('btn-char-back').onclick = () => show(STEP.TYPE, 'prev');
  document.getElementById('btn-char-next').onclick = () => {
    if (state.answerType === 'group' && state.characters.length === 0) return tg.showAlert('Выбери персонажа!');
    if (state.answerType === 'single') handleCharClick(state.characters[0]);
    else show(STEP.PROB);
  };
  
  // STEP 3.5: Form
  document.getElementById('btn-form-back').onclick = () => show(STEP.CHAR, 'prev');
  document.getElementById('btn-form-next').onclick = () => show(STEP.PROB);
  
  // STEP 4: Problem
  document.getElementById('btn-problem-back').onclick = () => {
    if (state.answerType === 'group') show(STEP.CHAR, 'prev');
    else {
      if (Object.keys(CHARACTERS[state.characters[0]].forms).length > 1) show(STEP.FORM, 'prev');
      else show(STEP.CHAR, 'prev');
    }
  };
  
  // SEND (START CHAT)
  document.getElementById('btn-problem-send').onclick = () => {
    playSound(magicSound);
    const text = document.getElementById('input-problem').value.trim();
    if (!text) return tg.showAlert('Напиши проблему!');
    
    state.problem = text;
    state.chatHistory = [{ role: "user", content: text }];
    document.getElementById('chat-container').innerHTML = '';
    
    addMessage('user', text);
    show(STEP.RES, 'zoom');
    sendToBackend();
  };
  
  // CHAT SEND
  const handleChatSend = () => {
    const input = document.getElementById('chat-input');
    const text = input.value.trim();
    if (!text) return;
    playSound(clickSound);
    state.chatHistory.push({ role: "user", content: text });
    addMessage('user', text);
    input.value = '';
    sendToBackend();
  };
  document.getElementById('btn-chat-send').onclick = handleChatSend;
  document.getElementById('chat-input').onkeypress = (e) => { if(e.key === 'Enter') handleChatSend(); };
  
  // RESULT CONTROLS
  document.getElementById('btn-result-again').onclick = () => {
    document.getElementById('input-problem').value = '';
    show(STEP.PROB, 'prev');
  };
  document.getElementById('btn-result-close').onclick = () => tg.close();
  
  // PARALLAX
  document.addEventListener('mousemove', e => {
    const x = (e.clientX/window.innerWidth-0.5)*15;
    const y = (e.clientY/window.innerHeight-0.5)*15;
    const m = document.getElementById('moon');
    if(m) m.style.transform = `translate(${x}px, ${y}px)`;
  });
  
  show(STEP.NAME);
});
