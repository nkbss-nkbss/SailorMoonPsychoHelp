// === INIT TELEGRAM ===
const tg = window.Telegram.WebApp;
tg.ready(); // Сообщаем, что приложение инициализировалось
tg.expand(); // Разворачиваем на весь экран

// === CONFIG & STATE ===
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
  problem: ""
};

// === DATA ===
// Данные должны совпадать с ключами на сервере (Python)
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
  "mamoru": {
    label: "Мамору",
    forms: {
      "human": { title: "Мамору Чиба 🌹", img: "https://i.pinimg.com/736x/68/f4/07/68f4077d2f6944bad32604a96a62f310.jpg" },
      "sailor": { title: "Такседо Маск 🥶", img: "https://i.pinimg.com/736x/62/c0/97/62c0978a24a049425d9895a159ca3104.jpg" }
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

// === AUDIO SYSTEM ===
const music = document.getElementById('bg-music');
const clickSound = document.getElementById('click-sound');
const magicSound = document.getElementById('magic-sound');
const selectSound = document.getElementById('select-sound');

let isMusicPlaying = false;
let isFading = false;
let fadeInterval;
const DEFAULT_MUSIC_VOLUME = 0.3;

// Воспроизведение коротких звуков
function playSound(audioEl, vol = 0.4) {
  if (audioEl) {
    audioEl.volume = vol;
    audioEl.currentTime = 0;
    audioEl.play().catch(e => console.log('Sound error:', e));
  }
}

// Плавное появление музыки
function fadeIn(audio, maxVol = 0.3) {
  if (isFading) clearInterval(fadeInterval);
  isFading = true;
  audio.volume = 0;
  audio.play().catch(e => console.log('Autoplay blocked:', e));
  
  let vol = 0;
  fadeInterval = setInterval(() => {
    vol += 0.02;
    if (vol >= maxVol) {
      vol = maxVol;
      clearInterval(fadeInterval);
      isFading = false;
    }
    audio.volume = vol;
  }, 100);
}

// Плавное затухание
function fadeOut(audio) {
  if (isFading) clearInterval(fadeInterval);
  isFading = true;
  
  let vol = audio.volume;
  fadeInterval = setInterval(() => {
    vol -= 0.02;
    if (vol <= 0) {
      vol = 0;
      clearInterval(fadeInterval);
      audio.pause();
      isFading = false;
    }
    audio.volume = vol;
  }, 100);
}

function initMusic() {
  const btn = document.getElementById('music-toggle');
  
  // Пытаемся запустить музыку при первом взаимодействии
  const startAudio = () => {
    if (!isMusicPlaying) {
      fadeIn(music, DEFAULT_MUSIC_VOLUME);
      isMusicPlaying = true;
      btn.textContent = '🔊';
    }
    document.removeEventListener('click', startAudio);
    document.removeEventListener('touchstart', startAudio);
  };

  document.addEventListener('click', startAudio);
  document.addEventListener('touchstart', startAudio);

  btn.onclick = (e) => {
    e.stopPropagation(); // Чтобы не триггерить startAudio дважды
    playSound(clickSound);
    if (isMusicPlaying) {
      fadeOut(music);
      btn.textContent = '🔇';
    } else {
      fadeIn(music, DEFAULT_MUSIC_VOLUME);
      btn.textContent = '🔊';
    }
    isMusicPlaying = !isMusicPlaying;
  };
}

// === UTILS ===

// Преобразование Markdown (жирный, курсив) в HTML
function parseMarkdown(text) {
  if (!text) return "";
  let html = text;
  // Жирный: **text** -> <strong>text</strong>
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Курсив: *text* -> <em>text</em>
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  // Переносы строк
  html = html.replace(/\n/g, '<br>');
  return html;
}

// Обновление прогресс-бара
function updateProgressBar(stepName) {
  const map = {
    'step-name': 1,
    'step-type': 2,
    'step-character': 3,
    'step-form': 3.5,
    'step-problem': 4,
    'step-result': 5
  };
  
  let stepNum = map[stepName] || 1;
  // Шаг 3.5 (выбор формы) визуально показываем как 3
  if (stepNum === 3.5) stepNum = 3; 

  const percentage = ((stepNum - 1) / 4) * 100;
  
  document.querySelector('.progress-fill').style.width = `${percentage}%`;
  document.getElementById('current-step').textContent = Math.ceil(stepNum);
  
  document.querySelectorAll('.step-dot').forEach((dot, index) => {
    const n = index + 1;
    dot.classList.remove('active', 'completed');
    if (n === Math.ceil(stepNum)) dot.classList.add('active');
    else if (n < Math.ceil(stepNum)) dot.classList.add('completed');
  });
}

// Навигация между карточками
function show(stepId, direction = 'next') {
  playSound(clickSound);
  
  const currentCard = document.querySelector('.card.active');
  const nextCard = document.getElementById(stepId);
  
  if (currentCard && nextCard) {
    currentCard.classList.remove('active');
    
    // Анимации
    if (direction === 'next') {
      currentCard.classList.add('slide-in-prev');
      nextCard.classList.add('slide-in-next');
    } else if (direction === 'prev') {
      currentCard.classList.add('slide-in-next');
      nextCard.classList.add('slide-in-prev');
    } else if (direction === 'zoom') {
      nextCard.classList.add('zoom-in');
    }
    
    setTimeout(() => {
      nextCard.classList.add('active');
      updateProgressBar(stepId);
      
      // Если перешли к выбору формы, нужно отрисовать их
      if (stepId === STEP.FORM) renderForms();
      // Если перешли к выбору персонажа, обновляем список (особенно для галочек в группе)
      if (stepId === STEP.CHAR) renderChars();

      // Очистка классов анимации
      setTimeout(() => {
        currentCard.classList.remove('slide-in-prev', 'slide-in-next', 'zoom-in');
        nextCard.classList.remove('slide-in-prev', 'slide-in-next', 'zoom-in');
      }, 400);
    }, 50);
  } else {
    // Первый запуск
    if (nextCard) {
      document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
      nextCard.classList.add('active');
      updateProgressBar(stepId);
    }
  }
}

// === RENDER LOGIC ===

// Отрисовка списка персонажей
function renderChars() {
  const container = document.getElementById('characters');
  container.innerHTML = '';
  
  const title = document.getElementById('character-title');
  if (state.answerType === 'group') {
    title.innerHTML = `Выбери команду <span class="selected-count">${state.characters.length}/4</span>`;
  } else {
    title.textContent = 'Выбери персонажа';
  }

  for (const key in CHARACTERS) {
    const char = CHARACTERS[key];
    const div = document.createElement('div');
    div.className = 'char-card';
    div.dataset.key = key;

    // Режим множественного выбора
    if (state.answerType === 'group') {
      div.classList.add('multiple');
      if (state.characters.includes(key)) div.classList.add('selected');
    } else {
      // Одиночный режим
      if (state.characters[0] === key) div.classList.add('selected');
    }

    // Берем первую форму для превью
    const previewImg = Object.values(char.forms)[0].img;
    div.innerHTML = `<img src="${previewImg}" alt="${char.label}" /><div class="label">${char.label}</div>`;
    
    div.onclick = () => handleCharacterClick(key);
    container.appendChild(div);
  }
}

// Отрисовка форм персонажа (Step 3.5)
function renderForms() {
  const container = document.getElementById('form-options');
  container.innerHTML = '';
  
  const charKey = state.characters[0];
  const char = CHARACTERS[charKey];
  
  if (!char) return;

  for (const formKey in char.forms) {
    const form = char.forms[formKey];
    const div = document.createElement('div');
    div.className = 'form-card';
    if (state.form === formKey) div.classList.add('selected');
    
    div.innerHTML = `<img src="${form.img}" alt="${form.title}" /><div class="label">${form.title}</div>`;
    div.onclick = () => {
      playSound(selectSound);
      state.form = formKey;
      document.querySelectorAll('.form-card').forEach(c => c.classList.remove('selected'));
      div.classList.add('selected');
    };
    container.appendChild(div);
  }
  
  // Выбираем первую форму по умолчанию, если ничего не выбрано
  if (!state.form && container.firstChild) {
    container.firstChild.click();
  }
}

// Обработка клика по персонажу
function handleCharacterClick(key) {
  playSound(selectSound);

  if (state.answerType === 'single') {
    state.characters = [key];
    renderChars(); // Обновить визуал выделения
    
    const forms = Object.keys(CHARACTERS[key].forms);
    // Если форм больше одной, идем выбирать форму
    if (forms.length > 1) {
      show(STEP.FORM, 'next');
    } else {
      // Иначе сразу к проблеме
      state.form = forms[0];
      show(STEP.PROB, 'next');
    }
  } else {
    // Групповой режим
    const index = state.characters.indexOf(key);
    if (index > -1) {
      state.characters.splice(index, 1);
    } else {
      if (state.characters.length < 4) {
        state.characters.push(key);
      } else {
        tg.showAlert('Максимум 4 персонажа в команде!');
        return;
      }
    }
    renderChars();
  }
}

// === MAIN EVENT LISTENERS ===
document.addEventListener('DOMContentLoaded', () => {
  initMusic();
  
  // Автозаполнение имени из Телеграм
  const user = tg.initDataUnsafe?.user;
  if (user?.first_name) {
    document.getElementById('input-name').value = user.first_name;
  }

  // 1. Кнопка имени
  document.getElementById('btn-name-next').onclick = () => {
    const val = document.getElementById('input-name').value.trim();
    if (val.length < 2) {
      const input = document.getElementById('input-name');
      input.style.animation = 'shake 0.5s ease-in-out';
      setTimeout(() => input.style.animation = '', 500);
      tg.showAlert('Пожалуйста, введи имя (минимум 2 буквы)');
      return;
    }
    state.name = val;
    show(STEP.TYPE, 'next');
  };

  // 2. Выбор типа ответа
  document.querySelectorAll('.type-option').forEach(opt => {
    opt.addEventListener('click', () => {
      playSound(selectSound);
      document.querySelectorAll('.type-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      state.answerType = opt.dataset.type;
      
      // Сброс выбора персонажей при смене режима
      state.characters = state.answerType === 'group' ? [] : ['usagi'];
    });
  });

  document.getElementById('btn-type-back').onclick = () => show(STEP.NAME, 'prev');
  document.getElementById('btn-type-next').onclick = () => {
    renderChars();
    show(STEP.CHAR, 'next');
  };

  // 3. Выбор персонажа (кнопки навигации)
  document.getElementById('btn-char-back').onclick = () => show(STEP.TYPE, 'prev');
  document.getElementById('btn-char-next').onclick = () => {
    if (state.answerType === 'group') {
      if (state.characters.length === 0) {
        tg.showAlert('Выбери хотя бы одного воина!');
        return;
      }
      show(STEP.PROB, 'next');
    } else {
      // В одиночном режиме клик по карточке сам переводит дальше,
      // но если пользователь нажал кнопку "Дальше" без выбора:
      if (state.characters.length === 1) handleCharacterClick(state.characters[0]);
    }
  };

  // 3.5. Выбор формы
  document.getElementById('btn-form-back').onclick = () => show(STEP.CHAR, 'prev');
  document.getElementById('btn-form-next').onclick = () => show(STEP.PROB, 'next');

  // 4. Описание проблемы
  document.getElementById('btn-problem-back').onclick = () => {
    if (state.answerType === 'group') {
      show(STEP.CHAR, 'prev');
    } else {
      // Если у одиночного чара было несколько форм -> назад к формам, иначе -> к чарам
      const forms = Object.keys(CHARACTERS[state.characters[0]].forms);
      if (forms.length > 1) show(STEP.FORM, 'prev');
      else show(STEP.CHAR, 'prev');
    }
  };

  // === ОТПРАВКА ЗАПРОСА ===
  document.getElementById('btn-problem-send').onclick = async () => {
    playSound(magicSound);
    const problem = document.getElementById('input-problem').value.trim();
    
    if (!problem) {
      tg.HapticFeedback.notificationOccurred('error');
      tg.showAlert('Напиши, что тебя беспокоит, чтобы получить совет.');
      return;
    }
    state.problem = problem;

    const resultBox = document.getElementById('result-box');
    const loader = document.getElementById('loading');
    
    // 1. Скрываем старый результат и саму рамку
    resultBox.classList.add('hidden'); 
    resultBox.innerHTML = "";
    
    // 2. Показываем лоадер
    loader.classList.remove('hidden');
    
    // Переход к слайду результата
    show(STEP.RES, 'zoom');

    try {
      // Определение URL (Локальный тест или Продакшн)
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const backend = isLocal 
        ? 'http://127.0.0.1:5000' 
        : 'https://sailormoonpsychohelp-7bkw.onrender.com';

      // Подготовка данных
      const payload = {
        chat_id: tg.initDataUnsafe?.user?.id,
        username: state.name,
        problem: state.problem,
        answer_type: state.answerType,
        character: state.answerType === 'single' ? state.characters[0] : state.characters.join(','),
        form: state.form
      };

      const resp = await fetch(`${backend}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await resp.json();
      
      // 3. Данные пришли: скрываем лоадер, показываем рамку
      loader.classList.add('hidden');
      resultBox.classList.remove('hidden'); // <--- ВОЗВРАЩАЕМ РАМКУ
      resultBox.classList.add('fade-in');

      if (data.ok) {
        tg.HapticFeedback.notificationOccurred('success');
        resultBox.innerHTML = parseMarkdown(data.advice);
      } else {
        throw new Error(data.error || "Неизвестная ошибка");
      }
    } catch (e) {
      console.error(e);
      // При ошибке тоже нужно вернуть рамку, чтобы показать текст ошибки
      loader.classList.add('hidden');
      resultBox.classList.remove('hidden'); 
      
      tg.HapticFeedback.notificationOccurred('error');
      resultBox.innerHTML = "<strong>Ошибка связи с Луной 🌑</strong><br>Сервер спит или интернет пропал. Попробуй еще раз через минуту.";
    }
  };

  // 5. Результат
  document.getElementById('btn-result-again').onclick = () => {
    document.getElementById('input-problem').value = '';
    show(STEP.PROB, 'prev');
  };
  
  document.getElementById('btn-result-close').onclick = () => tg.close();

  // Параллакс эффект для фона
  document.addEventListener('mousemove', e => {
    const x = (e.clientX / window.innerWidth - 0.5) * 20;
    const y = (e.clientY / window.innerHeight - 0.5) * 20;
    const moon = document.getElementById('moon');
    if(moon) moon.style.transform = `translate(${x}px, ${y}px)`;
  });

  // Генерация звезд
  const starsContainer = document.querySelector('.stars');
  for (let i = 0; i < 100; i++) {
    const star = document.createElement('div');
    star.classList.add('star');
    star.style.top = Math.random() * 100 + '%';
    star.style.left = Math.random() * 100 + '%';
    star.style.animationDelay = Math.random() * 5 + 's';
    starsContainer.appendChild(star);
  }

  // Запуск первого экрана
  show(STEP.NAME);
});

