//app.js
const tg = window.Telegram.WebApp;
tg.expand();
const STEP = {
  NAME: 'step-name',
  TYPE: 'step-type',
  CHAR: 'step-character',
  FORM: 'step-form',
  PROB: 'step-problem'
};
let state = {
  name: "",
  answerType: "single",
  characters: ["usagi"],
  form: "human",
  problem: ""
};

// === CHARACTER DATA (убраны лишние пробелы в URL) ===
const CHARACTERS = {
  "usagi": {
    label: "Усаги",
    forms: {
      "human": { title: "Усаги Цукино 👧", img: "https://i.pinimg.com/736x/a4/47/c4/a447c423d530b9cac4612a9f71c96ddc.jpg" },
      "sailor": { title: "Сейлор Мун 🌙", img: "https://i.pinimg.com/736x/55/ff/32/55ff32a1d1a2e86ff41d76068672e108.jpg" },
      "super": { title: "Супер Сейлор Мун 💫", img: "https://i.pinimg.com/736x/56/7b/38/567b38a7e0d7729573f997ded2448d5e.jpg" },
      "eternal": { title: "Вечная Сейлор Мун ✨", img: "https://i.pinimg.com/1200x/a1/e5/52/a1e552f9276025313b66b8f3a36a3c44.jpg" }
    }
  },
  "ami": {
    label: "Ами",
    forms: {
      "human": { title: "Ами Мидзуно 📚", img: "https://i.pinimg.com/736x/0b/07/f9/0b07f95abbceecf7922c44ac333a48f2.jpg" },
      "sailor": { title: "Сейлор Меркурий 💧", img: "https://i.pinimg.com/736x/b1/61/1a/b1611addcf1190d311218c22614e1e36.jpg" }
    }
  },
  "rei": {
    label: "Рей",
    forms: {
      "human": { title: "Рей Хино 🔥", img: "https://i.pinimg.com/736x/d7/9c/61/d79c617912ae0e4d510660c32c971227.jpg" },
      "sailor": { title: "Сейлор Марс 🔥", img: "https://i.pinimg.com/736x/7f/e6/e8/7fe6e8b47812f4778d229903c1776744.jpg" }
    }
  },
  "minako": {
    label: "Минако",
    forms: {
      "human": { title: "Минако Айно 💛", img: "https://i.pinimg.com/736x/68/68/52/6868521a4cf61d75b40772b6f13c0504.jpg" },
      "sailor": { title: "Сейлор Венера 💖", img: "https://i.pinimg.com/1200x/bb/e9/6e/bbe96e1b50292f72dab46e16dfd5f632.jpg" }
    }
  },
  "makoto": {
    label: "Макото",
    forms: {
      "human": { title: "Макото Кино 🌿", img: "https://i.pinimg.com/736x/49/27/8d/49278da7f93a6028a0a3d05bbd43fd22.jpg" },
      "sailor": { title: "Сейлор Юпитер ⚡", img: "https://i.pinimg.com/736x/84/f8/c0/84f8c01989fa310f2ca46bd8bcd58af3.jpg" }
    }
  },
  "hotaru": {
    label: "Хотару",
    forms: {
      "human": { title: "Хотару Томоэ 🌙", img: "https://i.pinimg.com/736x/62/e8/61/62e861ea332c0bf8dafd00fd4e9571d9.jpg" },
      "sailor": { title: "Сейлор Сатурн 🌑", img: "https://i.pinimg.com/736x/65/e3/95/65e3950cb55aaffbfd443ef8d5f3ae2a.jpg" }
    }
  },
  "setsuna": {
    label: "Сецуна",
    forms: {
      "human": { title: "Сецуна Мейо ⏳", img: "https://i.pinimg.com/736x/89/bf/f4/89bff47fee6011a503b18c274a0370a5.jpg" },
      "sailor": { title: "Сейлор Плутон 🕰️", img: "https://i.pinimg.com/736x/d4/8b/89/d48b8992dfac715b928af9d974d4c37c.jpg" }
    }
  },
  "haruka": {
    label: "Харука",
    forms: {
      "human": { title: "Харука Тэнно 🌟", img: "https://i.pinimg.com/736x/a8/c9/9e/a8c99e3558ea0caf592cb06c1339f720.jpg" },
      "sailor": { title: "Сейлор Уран 🌪️", img: "https://i.pinimg.com/1200x/ec/bd/fd/ecbdfd6392394b2d66fa68729eeb5948.jpg" }
    }
  },
  "michiru": {
    label: "Мичиру",
    forms: {
      "human": { title: "Мичиру Кайо 🌊", img: "https://i.pinimg.com/736x/a4/fe/e9/a4fee98a8f01e8a377a70759edbfc5df.jpg" },
      "sailor": { title: "Сейлор Нептун 🎻", img: "https://i.pinimg.com/736x/ef/a9/72/efa97290c250e97924777c4551120f60.jpg" }
    }
  },
  "chibiusa": {
    label: "Чибиуса",
    forms: {
      "human": { title: "Чибиуса ✨", img: "https://i.pinimg.com/736x/40/74/49/4074490084d46e4d173179fe03427d2b.jpg" },
      "sailor": { title: "Сейлор Чиби-Мун 💕", img: "https://i.pinimg.com/736x/09/89/00/098900bcc276be04da9e30b7cf3a6007.jpg" }
    }
  },
  "seiya": {
    label: "Сейя",
    forms: {
      "human": { title: "Сейя Кое ♂️⭐", img: "https://i.pinimg.com/736x/fa/44/48/fa4448c6b3b4d06e33e905e34256199b.jpg" },
      "sailor": { title: "Сейлор Стар Файтер ⭐", img: "https://i.pinimg.com/736x/7c/f6/11/7cf6111d7e826a5e8008310206683b1e.jpg" }
    }
  },
  "taiki": {
    label: "Тайки",
    forms: {
      "human": { title: "Тайки Кое ♂️📚", img: "https://i.pinimg.com/736x/9d/cf/05/9dcf05f2328100ef411b710d30ffc465.jpg" },
      "sailor": { title: "Сейлор Стар Хилер 📚", img: "https://i.pinimg.com/736x/32/1f/c6/321fc67961d968c73c972616e53721af.jpg" }
    }
  },
  "yaten": {
    label: "Ятен",
    forms: {
      "human": { title: "Ятен ♂️🎭", img: "https://i.pinimg.com/736x/68/b2/00/68b2006277d4c56dde09e0eb1cce61e0.jpg" },
      "sailor": { title: "Сейлор Стар Мейкер 🎭", img: "https://i.pinimg.com/736x/90/42/a3/9042a33ae40ccc635e909c2ba00449fb.jpg" }
    }
  }
};

// === Звуки ===
const CHARACTER_SOUNDS = {
  "usagi": "./music/characters/usagi (1).mp3",
  "ami": "./music/characters/ami (1).mp3", 
  "rei": "./music/characters/rei (1).mp3",
  "minako": "./music/characters/minako (1).mp3",
  "makoto": "./music/characters/makoto (1).mp3",
  "hotaru": "./music/characters/hotaru (1).mp3",
  "setsuna": "./music/characters/setsuna (1).mp3",
  "haruka": "./music/characters/haruka (1).mp3",
  "michiru": "./music/characters/michiru (1).mp3",
  "chibiusa": "./music/characters/chibiusa (1).mp3"
};
let characterSound = null;

// === Аудио ===
const music = document.getElementById('bg-music');
const clickSound = document.getElementById('click-sound');
const magicSound = document.getElementById('magic-sound');
const selectSound = document.getElementById('select-sound');
const DEFAULT_MUSIC_VOLUME = 0.3;
const QUIET_MUSIC_VOLUME = 0.1;

// === Фейд ===
let fadeInterval;
let isFading = false;
const FADE_DURATION = 1000;
const FADE_STEPS = 20;
const FADE_INTERVAL = FADE_DURATION / FADE_STEPS;

// === Функция добавления сообщения в чат ===
function addMessage(text, isUser = false) {
  const container = document.getElementById('chat-messages');
  const el = document.createElement('div');
  el.classList.add('chat-message', isUser ? 'user' : 'bot');
  el.textContent = text;
  container.appendChild(el);
  container.scrollTop = container.scrollHeight;
}

// === Обновление заголовка чата ===
function updateChatHeader() {
  const avatar = document.getElementById('chat-avatar');
  const name = document.getElementById('chat-character-name');

  if (state.answerType === 'group') {
    avatar.src = 'https://i.pinimg.com/120x120/55/ff/32/55ff32a1d1a2e86ff41d76068672e108.jpg';
    name.textContent = 'Команда Сейлор Воинов 💫';
  } else {
    const charKey = state.characters[0];
    const char = CHARACTERS[charKey];
    const form = char.forms[state.form];
    avatar.src = form.img;
    name.textContent = form.title;
  }
}

// === Прогресс ===
function updateProgressBar(step) {
  const map = {
    'step-name': 1,
    'step-type': 2,
    'step-character': 3,
    'step-form': 3,
    'step-problem': 4
  };
  const n = map[step] || 1;
  document.getElementById('current-step').textContent = n;
  document.querySelector('.progress-fill').style.width = `${((n - 1) / 4) * 100}%`;
  document.querySelectorAll('.step-dot').forEach((dot, i) => {
    dot.classList.toggle('active', i + 1 === n);
    dot.classList.toggle('completed', i + 1 < n);
  });
}

// === СOUNDS ===
function playClickSound() { if (clickSound) { clickSound.currentTime = 0; clickSound.play().catch(() => {}); } }
function playMagicSound() { if (magicSound) { magicSound.currentTime = 0; magicSound.play().catch(() => {}); } }
function playSelectSound() { if (selectSound) { selectSound.currentTime = 0; selectSound.play().catch(() => {}); } }

// === SHOW STEP ===
function show(step, direction = 'next') {
  const current = document.querySelector('.card.active');
  const next = document.getElementById(step);
  current?.classList.remove('active');
  next.classList.add('active');
  updateProgressBar(step);
  if (step === STEP.FORM) renderFormStep();
  if (step === STEP.PROB) updateChatHeader();
}

// === Персонажи и формы ===
function handleCharacterClick(charKey) {
  playSelectSound();
  if (state.answerType === 'group') {
    const i = state.characters.indexOf(charKey);
    if (i > -1) state.characters.splice(i, 1);
    else if (state.characters.length < 4) state.characters.push(charKey);
    if (state.characters.length === 0) state.characters = ['usagi'];
    updateCharacterSelectionUI();
  } else {
    state.characters = [charKey];
    updateCharacterSelectionUI();
    if (Object.keys(CHARACTERS[charKey].forms).length > 1) {
      show(STEP.FORM);
    } else {
      state.form = Object.keys(CHARACTERS[charKey].forms)[0];
      show(STEP.PROB);
    }
  }
}
function updateCharacterSelectionUI() {
  const title = document.getElementById('character-title');
  if (state.answerType === 'group') {
    title.innerHTML = `Выбери персонажей <span class="selected-count">${state.characters.length}</span>`;
    document.querySelectorAll('.char-card').forEach(c => {
      c.classList.add('multiple');
      const k = c.dataset.key;
      if (state.characters.includes(k)) c.classList.add('selected');
      else c.classList.remove('selected');
    });
  } else {
    title.textContent = 'Выбери персонажа';
    document.querySelectorAll('.char-card').forEach(c => {
      c.classList.remove('multiple');
      const k = c.dataset.key;
      if (state.characters[0] === k) c.classList.add('selected');
    });
  }
}
function renderFormStep() {
  const key = state.characters[0];
  const container = document.getElementById('form-options');
  container.innerHTML = '';
  const char = CHARACTERS[key];
  for (const f in char.forms) {
    const form = char.forms[f];
    const div = document.createElement('div');
    div.className = 'form-card';
    div.dataset.form = f;
    div.innerHTML = `<img src="${form.img}" /><div class="label">${form.title}</div>`;
    div.onclick = () => {
      state.form = f;
      document.querySelectorAll('.form-card').forEach(c => c.classList.remove('selected'));
      div.classList.add('selected');
      playSelectSound();
    };
    container.appendChild(div);
  }
  const first = container.querySelector('.form-card');
  if (first) {
    first.classList.add('selected');
    state.form = first.dataset.form;
  }
}

// === Музыка ===
let musicInitialized = false;
let isMusicPlaying = false;
function initMusic() {
  if (musicInitialized) return;
  music.volume = 0;
  document.addEventListener('click', () => {
    if (!musicInitialized) {
      music.play().then(() => {
        musicInitialized = true;
        isMusicPlaying = true;
        document.getElementById('music-toggle').textContent = '🔊';
      });
    }
  }, { once: true });
}
document.getElementById('music-toggle').onclick = () => {
  playClickSound();
  if (isMusicPlaying) {
    music.pause();
    document.getElementById('music-toggle').textContent = '🔇';
    isMusicPlaying = false;
  } else {
    music.play();
    document.getElementById('music-toggle').textContent = '🔊';
    isMusicPlaying = true;
  }
};

// === Звёзды и параллакс (минимум для совместимости) ===
document.addEventListener('mousemove', e => {
  const x = (e.clientX / window.innerWidth - 0.5) * 15;
  const y = (e.clientY / window.innerHeight - 0.5) * 15;
  document.querySelectorAll('.parallax-layer').forEach((l, i) => {
    l.style.transform = `translate(${x * (1 + i * 0.2)}px, ${y * (1 + i * 0.2)}px)`;
  });
});
const stars = document.querySelector('.stars');
for (let i = 0; i < 100; i++) {
  const s = document.createElement('div');
  s.classList.add('star');
  s.style.top = Math.random() * 100 + '%';
  s.style.left = Math.random() * 100 + '%';
  s.style.width = s.style.height = Math.random() * 2 + 1 + 'px';
  stars.appendChild(s);
}

// === Инициализация ===
document.addEventListener('DOMContentLoaded', () => {
  initMusic();

  // Выбор типа
  document.querySelectorAll('.type-option').forEach(opt => {
    opt.onclick = () => {
      playSelectSound();
      document.querySelectorAll('.type-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      state.answerType = opt.dataset.type;
    };
  });
  document.querySelector('.type-option[data-type="single"]').classList.add('selected');

  // Генерация персонажей
  const charContainer = document.getElementById('characters');
  for (const key in CHARACTERS) {
    const char = CHARACTERS[key];
    const div = document.createElement('div');
    div.className = 'char-card';
    div.dataset.key = key;
    div.innerHTML = `<img src="${Object.values(char.forms)[0].img}" alt="${char.label}" /><div class="label">${char.label}</div>`;
    div.onclick = () => handleCharacterClick(key);
    charContainer.appendChild(div);
  }
  charContainer.firstElementChild.classList.add('selected');

  // Кнопки навигации
  document.getElementById('btn-name-next').onclick = () => {
    const name = document.getElementById('input-name').value.trim();
    if (name.length < 2) return alert('Имя должно быть от 2 символов');
    state.name = name;
    show(STEP.TYPE);
  };
  document.getElementById('btn-type-back').onclick = () => show(STEP.NAME);
  document.getElementById('btn-type-next').onclick = () => show(STEP.CHAR);
  document.getElementById('btn-char-back').onclick = () => show(STEP.TYPE);
  document.getElementById('btn-char-next').onclick = () => {
    if (state.answerType === 'single') return alert('Выбери персонажа!');
    show(STEP.PROB);
  };
  document.getElementById('btn-form-back').onclick = () => show(STEP.CHAR);
  document.getElementById('btn-form-next').onclick = () => show(STEP.PROB);
  document.getElementById('btn-problem-back').onclick = () => {
    if (state.answerType === 'group') show(STEP.CHAR);
    else show(STEP.FORM);
  };

  // Новый чат
  document.getElementById('btn-new-chat').onclick = () => {
    document.getElementById('chat-messages').innerHTML = '';
    document.getElementById('input-problem').value = '';
    show(STEP.NAME);
  };

  // Отправка в чат
  document.getElementById('btn-problem-send').onclick = async () => {
    const input = document.getElementById('input-problem');
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, true);
    input.value = '';
    input.disabled = true;
    document.getElementById('btn-problem-send').disabled = true;

    const init = tg.initDataUnsafe || {};
    const user = init.user || {};
    const chat_id = user.id || null;
    const username = state.name || user.first_name || "друг";

    addMessage('Собирает мысли... 💫', false);
    const thinkingEl = document.querySelector('.chat-message:last-child');

    try {
      const resp = await fetch('https://sailormoonpsychohelp-7bkw.onrender.com/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id,
          username,
          character: state.answerType === 'single' ? state.characters[0] : state.characters.join(','),
          form: state.answerType === 'single' ? state.form : undefined,
          answer_type: state.answerType,
          problem: text
        })
      });
      const data = await resp.json();
      thinkingEl.remove();
      if (data.ok && data.advice) {
        addMessage(data.advice, false);
      } else {
        addMessage("🌙 Что-то пошло не так... Попробуй позже!", false);
      }
    } catch (e) {
      console.error(e);
      thinkingEl.remove();
      addMessage("💔 Не удалось связаться с Луной. Проверь соединение.", false);
    } finally {
      input.disabled = false;
      document.getElementById('btn-problem-send').disabled = false;
    }
  };

  show(STEP.NAME);
});
