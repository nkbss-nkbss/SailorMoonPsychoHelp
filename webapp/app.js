//app.js
const tg = window.Telegram.WebApp;
tg.expand();

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
  answerType: "single",
  characters: ["usagi"],
  form: "human",
  problem: ""
};

// === CHARACTER DATA WITH FORMS (без лишних пробелов в URL) ===
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

// === Character sounds ===
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
  "chibiusa": "./music/characters/chibiusa (1).mp3",
  "mamoru": "./music/characters/mamoru (1).mp3"
};

let characterSound = null;

// === Audio elements ===
const music = document.getElementById('bg-music');
const clickSound = document.getElementById('click-sound');
const magicSound = document.getElementById('magic-sound');
const selectSound = document.getElementById('select-sound');

// === Music fade variables ===
let fadeInterval;
let isFading = false;
const FADE_DURATION = 1000;
const FADE_STEPS = 20;
const FADE_INTERVAL = FADE_DURATION / FADE_STEPS;

// === Character sound functions ===
function playCharacterSound(characterKey) {
  if (characterSound && !characterSound.paused) {
    characterSound.pause();
    characterSound.currentTime = 0;
  }
  const soundFile = CHARACTER_SOUNDS[characterKey];
  if (!soundFile) {
    playSelectSound();
    return;
  }
  characterSound = new Audio(soundFile);
  characterSound.volume = 0.4;
  characterSound.play().catch(e => {
    console.log('Character sound error:', e);
    playSelectSound();
  });
}

// === Progress bar ===
function updateProgressBar(step) {
  const stepMap = {
    'step-name': 1,
    'step-type': 2,
    'step-character': 3,
    'step-form': 3.5,
    'step-problem': 4,
    'step-result': 5
  };
  let currentStep = stepMap[step] || 1;
  if (currentStep === 3.5) currentStep = 3;
  const progressPercentage = ((currentStep - 1) / 4) * 100;
  document.getElementById('current-step').textContent = Math.min(5, Math.ceil(currentStep));
  document.querySelector('.progress-fill').style.width = `${progressPercentage}%`;
  updateStepDots(Math.min(5, Math.ceil(currentStep)));
}

function updateStepDots(currentStep) {
  const dots = document.querySelectorAll('.step-dot');
  dots.forEach((dot, index) => {
    const n = index + 1;
    dot.classList.remove('active', 'completed');
    if (n === currentStep) dot.classList.add('active');
    else if (n < currentStep) dot.classList.add('completed');
  });
}

// === Sound functions ===
function playClickSound() {
  if (clickSound) {
    clickSound.volume = 0.3;
    clickSound.currentTime = 0;
    clickSound.play().catch(e => console.log('Click sound error:', e));
  }
}
function playMagicSound() {
  if (magicSound) {
    magicSound.volume = 0.4;
    magicSound.currentTime = 0;
    magicSound.play().catch(e => console.log('Magic sound error:', e));
  }
}
function playSelectSound() {
  if (selectSound) {
    selectSound.volume = 0.3;
    selectSound.currentTime = 0;
    selectSound.play().catch(e => console.log('Select sound error:', e));
  }
}

// === Fade functions ===
function fadeIn(audio, vol = 0.3) {
  if (isFading) clearInterval(fadeInterval);
  isFading = true;
  audio.volume = 0;
  audio.play().catch(e => console.log('Fade in error:', e));
  let s = 0;
  fadeInterval = setInterval(() => {
    s++;
    audio.volume = (s / FADE_STEPS) * vol;
    if (s >= FADE_STEPS) {
      clearInterval(fadeInterval);
      audio.volume = vol;
      isFading = false;
    }
  }, FADE_INTERVAL);
}
function fadeOut(audio) {
  if (isFading) clearInterval(fadeInterval);
  isFading = true;
  const v = audio.volume;
  let s = 0;
  fadeInterval = setInterval(() => {
    s++;
    audio.volume = v * (1 - s / FADE_STEPS);
    if (s >= FADE_STEPS) {
      clearInterval(fadeInterval);
      audio.pause();
      audio.volume = 0.3;
      isFading = false;
    }
  }, FADE_INTERVAL);
}

// === Show step (С КЛЮЧЕВЫМ ИСПРАВЛЕНИЕМ) ===
function show(step, direction = 'next') {
  playClickSound();
  const current = document.querySelector('.card.active');
  const next = document.getElementById(step);
  if (current && next) {
    current.classList.remove('active');
    if (direction === 'next') {
      current.classList.add('slide-in-prev');
      next.classList.add('slide-in-next');
    } else if (direction === 'prev') {
      current.classList.add('slide-in-next');
      next.classList.add('slide-in-prev');
    } else if (direction === 'zoom') {
      next.classList.add('zoom-in');
    }
    setTimeout(() => {
      next.classList.add('active');
      updateProgressBar(step);

      // 🔥 КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: рендерим формы при входе на шаг
      if (step === STEP.FORM) {
        renderFormStep();
      }

      setTimeout(() => {
        current.classList.remove('slide-in-prev', 'slide-in-next', 'zoom-in');
        next.classList.remove('slide-in-prev', 'slide-in-next', 'zoom-in');
      }, 400);
    }, 50);
  } else {
    document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
    next.classList.add('active');
    updateProgressBar(step);

    if (step === STEP.FORM) {
      renderFormStep();
    }
  }
}

// === Handle character click ===
function handleCharacterClick(charKey) {
  playSelectSound();
  playCharacterSound(charKey);
  if (state.answerType === 'group') {
    const i = state.characters.indexOf(charKey);
    if (i > -1) {
      state.characters.splice(i, 1);
      if (state.characters.length === 0) state.characters.push('usagi');
    } else {
      if (state.characters.length < 4) state.characters.push(charKey);
      else { alert('Можно выбрать до 4 персонажей'); return; }
    }
    updateCharacterSelectionUI();
  } else {
    state.characters = [charKey];
    updateCharacterSelectionUI();
    if (Object.keys(CHARACTERS[charKey].forms).length > 1) {
      show(STEP.FORM, 'next');
    } else {
      state.form = Object.keys(CHARACTERS[charKey].forms)[0];
      show(STEP.PROB, 'next');
    }
  }
}

function updateCharacterSelectionUI() {
  const title = document.getElementById('character-title');
  const container = document.getElementById('characters');
  if (state.answerType === 'group') {
    title.innerHTML = `Выбери персонажей <span class="selected-count">${state.characters.length}</span>`;
    document.querySelectorAll('.char-card').forEach(card => {
      card.classList.add('multiple');
      const k = card.dataset.key;
      if (state.characters.includes(k)) card.classList.add('selected');
      else card.classList.remove('selected');
    });
  } else {
    title.textContent = 'Выбери персонажа';
    document.querySelectorAll('.char-card').forEach(card => {
      card.classList.remove('multiple');
      const k = card.dataset.key;
      if (state.characters[0] === k) card.classList.add('selected');
      else card.classList.remove('selected');
    });
  }
}

// === FORM STEP UI ===
function renderFormStep() {
  const charKey = state.characters[0];
  const container = document.getElementById('form-options');
  container.innerHTML = '';
  const char = CHARACTERS[charKey];
  for (const formKey in char.forms) {
    const form = char.forms[formKey];
    const div = document.createElement('div');
    div.className = 'form-card';
    div.dataset.form = formKey;
    div.innerHTML = `<img src="${form.img}" alt="${form.title}" /><div class="label">${form.title}</div>`;
    div.onclick = () => {
      state.form = formKey;
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

// === Music ===
const musicBtn = document.getElementById('music-toggle');
let musicInitialized = false;
let isMusicPlaying = false;

function initMusic() {
  if (musicInitialized) return;
  music.volume = 0;
  musicBtn.addEventListener('click', () => { playClickSound(); toggleMusic(); });
  document.addEventListener('click', () => {
    if (!musicInitialized) {
      fadeIn(music, 0.3);
      musicBtn.textContent = '🔊';
      musicInitialized = true;
      isMusicPlaying = true;
    }
  }, { once: true });
}
function toggleMusic() {
  if (isFading) return;
  if (isMusicPlaying) {
    fadeOut(music);
    musicBtn.textContent = '🔇';
    isMusicPlaying = false;
  } else {
    fadeIn(music, 0.3);
    musicBtn.textContent = '🔊';
    isMusicPlaying = true;
  }
}
window.addEventListener('beforeunload', () => {
  if (!music.paused) { music.volume = 0; music.pause(); }
});

// === Parallax & Stars ===
document.addEventListener('mousemove', e => {
  const x = (e.clientX / window.innerWidth - 0.5) * 25;
  const y = (e.clientY / window.innerHeight - 0.5) * 25;
  document.querySelectorAll('.parallax-layer').forEach((layer, i) => {
    const f = 1 + i*0.2;
    layer.style.transform = `translate(${x*f}px, ${y*f}px)`;
  });
});
const starsContainer = document.querySelector('.stars');
for (let i = 0; i < 150; i++) {
  const star = document.createElement('div');
  star.classList.add('star');
  star.style.top = Math.random() * 100 + '%';
  star.style.left = Math.random() * 100 + '%';
  star.style.width = star.style.height = Math.random() * 2 + 1 + 'px';
  star.style.animationDelay = Math.random() * 5 + 's';
  starsContainer.appendChild(star);
  star.style.animation = `twinkle ${2 + Math.random()*3}s infinite ease-in-out, fall ${5 + Math.random()*5}s linear ${Math.random()*5}s infinite`;
}
const moonLayer = document.getElementById('moon');
if(moonLayer){
  moonLayer.style.animation = "pulse 4s infinite ease-in-out alternate";
}

// === DOMContentLoaded ===
document.addEventListener('DOMContentLoaded', () => {
  initMusic();

  document.querySelectorAll('.type-option').forEach(opt => {
    opt.addEventListener('click', () => {
      playSelectSound();
      document.querySelectorAll('.type-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      state.answerType = opt.dataset.type;
    });
  });
  document.querySelector('.type-option[data-type="single"]').classList.add('selected');

  const charContainer = document.getElementById('characters');
  for (const key in CHARACTERS) {
    const ch = CHARACTERS[key];
    const div = document.createElement('div');
    div.className = 'char-card';
    div.dataset.key = key;
    div.innerHTML = `<img src="${Object.values(ch.forms)[0].img}" alt="${ch.label}" /><div class="label">${ch.label}</div>`;
    div.onclick = () => handleCharacterClick(key);
    charContainer.appendChild(div);
  }
  charContainer.querySelector('.char-card').classList.add('selected');

  document.getElementById('btn-form-back').onclick = () => {
    show(STEP.CHAR, 'prev');
  };
  document.getElementById('btn-form-next').onclick = () => {
    show(STEP.PROB, 'next');
  };

  document.getElementById('btn-name-next').onclick = () => {
    const name = document.getElementById('input-name').value.trim();
    if (!name || name.length < 2) {
      const input = document.getElementById('input-name');
      input.style.animation = 'shake 0.5s ease-in-out';
      setTimeout(() => input.style.animation = '', 500);
      alert('Введите имя минимум из 2 символов');
      return;
    }
    state.name = name;
    show(STEP.TYPE, 'next');
  };
  document.getElementById('btn-type-back').onclick = () => show(STEP.NAME, 'prev');
  document.getElementById('btn-type-next').onclick = () => show(STEP.CHAR, 'next');
  document.getElementById('btn-char-back').onclick = () => show(STEP.TYPE, 'prev');
  document.getElementById('btn-char-next').onclick = () => {
    if (state.answerType === 'group') {
      show(STEP.PROB, 'next');
    } else {
      alert('Выбери персонажа выше');
    }
  };
  document.getElementById('btn-problem-back').onclick = () => {
    if (state.answerType === 'group') {
      show(STEP.CHAR, 'prev');
    } else {
      show(STEP.FORM, 'prev');
    }
  };
  document.getElementById('btn-problem-send').onclick = async () => {
    playMagicSound();
    const problem = document.getElementById('input-problem').value.trim();
    if (!problem) {
      const textarea = document.getElementById('input-problem');
      textarea.style.animation = 'shake 0.5s ease-in-out';
      setTimeout(() => textarea.style.animation = '', 500);
      alert('Опиши проблему, пожалуйста');
      return;
    }
    state.problem = problem;

    const init = tg.initDataUnsafe || {};
    const user = init.user || {};
    const chat_id = user.id || null;
    const username = state.name || user.first_name || "друг";

    const resultBox = document.getElementById('result-box');
    const loader = document.getElementById('loading');
    resultBox.innerText = "";
    loader.classList.remove('hidden');
    show(STEP.RES, 'zoom');

    try {
      // ⚠️ Замените на ваш настоящий URL!
      const backend = 'https://sailor-moon-psycho-help.vercel.app';
      const resp = await fetch(`${backend}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id,
          username,
          character: state.answerType === 'single' ? state.characters[0] : state.characters.join(','),
          form: state.answerType === 'single' ? state.form : undefined,
          answer_type: state.answerType,
          problem: state.problem
        })
      });
      const data = await resp.json();
      loader.classList.add('hidden');
      resultBox.classList.add('fade-in');
      resultBox.innerText = data.ok ? (data.advice || "Пустой ответ") : "Ошибка: " + (data.error || JSON.stringify(data));
      setTimeout(() => resultBox.classList.remove('fade-in'), 600);
    } catch (err) {
      console.error(err);
      loader.classList.add('hidden');
      resultBox.innerText = "Ошибка связи с сервером. Попробуй позже.";
    }
  };
  document.getElementById('btn-result-again').onclick = () => {
    document.getElementById('input-problem').value = '';
    show(STEP.PROB, 'prev');
  };
  document.getElementById('btn-result-close').onclick = () => tg.close();

  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', playClickSound);
  });

  show(STEP.NAME);

  try {
    const init = tg.initDataUnsafe || {};
    if (init.user && init.user.first_name) {
      document.getElementById('input-name').value = init.user.first_name;
    }
  } catch (e) { /* ignore */ }
});

document.addEventListener('touchstart', () => {
  if (!musicInitialized) {
    music.play().then(() => {
      musicBtn.textContent = '🔊';
      musicInitialized = true;
      isMusicPlaying = true;
    }).catch(() => {
      musicBtn.textContent = '🔇';
      musicInitialized = true;
    });
  }
}, { once: true });



