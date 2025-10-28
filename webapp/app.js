const tg = window.Telegram.WebApp;
tg.expand();

const STEP = {
  NAME: 'step-name',
  TYPE: 'step-type',
  CHAR: 'step-character',
  PROB: 'step-problem',
  RES: 'step-result'
};

let state = {
  name: "",
  answerType: "single", // "single" или "group"
  characters: ["usagi"], // массив выбранных персонажей
  problem: ""
};

const CHARACTERS = {
  "usagi": { label: "Усаги", img: "https://i.pinimg.com/736x/a4/47/c4/a447c423d530b9cac4612a9f71c96ddc.jpg" },
  "ami": { label: "Ами", img: "https://i.pinimg.com/736x/b1/61/1a/b1611addcf1190d311218c22614e1e36.jpg" },
  "rei": { label: "Рей", img: "https://i.pinimg.com/736x/d7/9c/61/d79c617912ae0e4d510660c32c971227.jpg" },
  "minako": { label: "Минако", img: "https://i.pinimg.com/736x/68/68/52/6868521a4cf61d75b40772b6f13c0504.jpg" },
  "makoto": { label: "Макото", img: "https://i.pinimg.com/736x/49/27/8d/49278da7f93a6028a0a3d05bbd43fd22.jpg" },
  "hotaru": { label: "Хотару", img: "https://i.pinimg.com/736x/62/e8/61/62e861ea332c0bf8dafd00fd4e9571d9.jpg" },
  "setsuna": { label: "Сецуна", img: "https://i.pinimg.com/736x/89/bf/f4/89bff47fee6011a503b18c274a0370a5.jpg" },
  "haruka": { label: "Харука", img: "https://i.pinimg.com/736x/a8/c9/9e/a8c99e3558ea0caf592cb06c1339f720.jpg" },
  "michiru": { label: "Мичиру", img: "https://i.pinimg.com/736x/a4/fe/e9/a4fee98a8f01e8a377a70759edbfc5df.jpg" },
  "chibiusa": { label: "Чибиуса", img: "https://i.pinimg.com/736x/40/74/49/4074490084d46e4d173179fe03427d2b.jpg" },
  "mamoru": { label: "Мамору", img: "https://i.pinimg.com/736x/62/c0/97/62c0978a24a049425d9895a159ca3104.jpg" }
};

// === Audio elements ===
const music = document.getElementById('bg-music');
const clickSound = document.getElementById('click-sound');
const magicSound = document.getElementById('magic-sound');
const selectSound = document.getElementById('select-sound');

// === Music fade variables ===
let fadeInterval;
let isFading = false;
const FADE_DURATION = 1000; // 1 second fade
const FADE_STEPS = 20;
const FADE_INTERVAL = FADE_DURATION / FADE_STEPS;

// === Progress bar functions ===
function updateProgressBar(step) {
  const stepMap = {
    'step-name': 1,
    'step-type': 2,
    'step-character': 3, 
    'step-problem': 4,
    'step-result': 5
  };
  
  const currentStep = stepMap[step] || 1;
  const progressPercentage = ((currentStep - 1) / 4) * 100;
  
  console.log('Updating progress bar:', step, '-> step', currentStep, '(', progressPercentage, '%)');
  
  // Обновляем текст
  document.getElementById('current-step').textContent = currentStep;
  
  // Обновляем прогресс-бар
  const progressFill = document.querySelector('.progress-fill');
  if (progressFill) {
    progressFill.style.width = `${progressPercentage}%`;
  }
  
  // Обновляем точки шагов
  updateStepDots(currentStep);
}

function updateStepDots(currentStep) {
  const dots = document.querySelectorAll('.step-dot');
  
  dots.forEach((dot, index) => {
    const stepNumber = index + 1;
    
    // Убираем все классы
    dot.classList.remove('active', 'completed');
    
    // Добавляем соответствующие классы
    if (stepNumber === currentStep) {
      dot.classList.add('active');
    } else if (stepNumber < currentStep) {
      dot.classList.add('completed');
    }
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
function fadeIn(audioElement, targetVolume = 0.3) {
  if (isFading) {
    clearInterval(fadeInterval);
  }
  
  isFading = true;
  audioElement.volume = 0;
  audioElement.play().catch(e => console.log('Fade in play error:', e));
  
  let currentStep = 0;
  
  fadeInterval = setInterval(() => {
    currentStep++;
    const newVolume = (currentStep / FADE_STEPS) * targetVolume;
    audioElement.volume = newVolume;
    
    if (currentStep >= FADE_STEPS) {
      clearInterval(fadeInterval);
      audioElement.volume = targetVolume;
      isFading = false;
    }
  }, FADE_INTERVAL);
}

function fadeOut(audioElement) {
  if (isFading) {
    clearInterval(fadeInterval);
  }
  
  isFading = true;
  const startVolume = audioElement.volume;
  let currentStep = 0;
  
  fadeInterval = setInterval(() => {
    currentStep++;
    const newVolume = startVolume * (1 - currentStep / FADE_STEPS);
    audioElement.volume = newVolume;
    
    if (currentStep >= FADE_STEPS) {
      clearInterval(fadeInterval);
      audioElement.pause();
      audioElement.volume = 0.3; // Reset to default volume
      isFading = false;
    }
  }, FADE_INTERVAL);
}

// === Updated show function with animations and progress bar ===
function show(step, direction = 'next') {
  playClickSound();
  
  const currentStep = document.querySelector('.card.active');
  const nextStep = document.getElementById(step);
  
  if (currentStep && nextStep) {
    // Убираем текущий шаг с анимацией
    currentStep.classList.remove('active');
    
    // Добавляем классы анимации в зависимости от направления
    if (direction === 'next') {
      currentStep.classList.add('slide-in-prev');
      nextStep.classList.add('slide-in-next');
    } else if (direction === 'prev') {
      currentStep.classList.add('slide-in-next');
      nextStep.classList.add('slide-in-prev');
    } else if (direction === 'zoom') {
      nextStep.classList.add('zoom-in');
    }
    
    // Показываем следующий шаг
    setTimeout(() => {
      nextStep.classList.add('active');
      
      // Обновляем прогресс-бар
      updateProgressBar(step);
      
      // Убираем классы анимации после завершения
      setTimeout(() => {
        currentStep.classList.remove('slide-in-prev', 'slide-in-next', 'zoom-in');
        nextStep.classList.remove('slide-in-prev', 'slide-in-next', 'zoom-in');
      }, 400);
    }, 50);
  } else {
    // Первый запуск или fallback
    document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
    nextStep.classList.add('active');
    updateProgressBar(step);
  }
}

// === Character selection functions ===
function updateCharacterSelectionUI() {
  const title = document.getElementById('character-title');
  const charactersContainer = document.getElementById('characters');
  
  if (state.answerType === 'group') {
    title.innerHTML = `Выбери персонажей <span class="selected-count">${state.characters.length}</span>`;
    
    // Обновляем все карточки для множественного выбора
    document.querySelectorAll('.char-card').forEach(card => {
      card.classList.add('multiple');
      const charKey = card.dataset.key;
      
      if (state.characters.includes(charKey)) {
        card.classList.add('selected');
      } else {
        card.classList.remove('selected');
      }
    });
  } else {
    title.textContent = 'Выбери персонажа';
    
    // Обновляем все карточки для одиночного выбора
    document.querySelectorAll('.char-card').forEach(card => {
      card.classList.remove('multiple');
      const charKey = card.dataset.key;
      
      if (state.characters[0] === charKey) {
        card.classList.add('selected');
      } else {
        card.classList.remove('selected');
      }
    });
  }
}

function handleCharacterClick(charKey) {
  playSelectSound();
  
  if (state.answerType === 'group') {
    // Множественный выбор
    const index = state.characters.indexOf(charKey);
    
    if (index > -1) {
      // Убираем из выбранных
      state.characters.splice(index, 1);
      // Если ничего не выбрано, добавляем обратно
      if (state.characters.length === 0) {
        state.characters.push('usagi');
      }
    } else {
      // Добавляем в выбранные (максимум 4 персонажа)
      if (state.characters.length < 4) {
        state.characters.push(charKey);
      } else {
        // Можно показать уведомление о максимальном количестве
        alert('Можно выбрать до 4 персонажей для группового ответа');
        return;
      }
    }
  } else {
    // Одиночный выбор
    state.characters = [charKey];
  }
  
  updateCharacterSelectionUI();
}

// === Improved Music control ===
const musicBtn = document.getElementById('music-toggle');
let musicInitialized = false;
let isMusicPlaying = false;

function initMusic() {
  if (musicInitialized) return;
  
  // Устанавливаем начальную громкость
  music.volume = 0;
  
  musicBtn.addEventListener('click', function() {
    playClickSound();
    toggleMusic();
  });
  
  // Автозапуск с плавным появлением
  document.addEventListener('click', function initMusicOnInteraction() {
    if (!musicInitialized) {
      fadeIn(music, 0.3);
      musicBtn.textContent = '🔊';
      musicInitialized = true;
      isMusicPlaying = true;
      document.removeEventListener('click', initMusicOnInteraction);
    }
  }, { once: true });
}

function toggleMusic() {
  if (isFading) return; // Предотвращаем множественные нажатия во время фейда
  
  if (isMusicPlaying) {
    // Плавное затухание и пауза
    fadeOut(music);
    musicBtn.textContent = '🔇';
    isMusicPlaying = false;
  } else {
    // Плавное появление
    fadeIn(music, 0.3);
    musicBtn.textContent = '🔊';
    isMusicPlaying = true;
  }
}

// Обработчик для плавной остановки при закрытии страницы
window.addEventListener('beforeunload', () => {
  if (!music.paused) {
    // Быстрое затухание при закрытии
    music.volume = 0;
    music.pause();
  }
});

// === Parallax effect ===
document.addEventListener('mousemove', e => {
  const x = (e.clientX / window.innerWidth - 0.5) * 25;
  const y = (e.clientY / window.innerHeight - 0.5) * 25;
  document.querySelectorAll('.parallax-layer').forEach((layer, i) => {
    const factor = 1 + i*0.2;
    layer.style.transform = `translate(${x*factor}px, ${y*factor}px)`;
  });
});

// === Stars animation ===
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

// === Moon pulse animation ===
const moonLayer = document.getElementById('moon');
if(moonLayer){
  moonLayer.style.animation = "pulse 4s infinite ease-in-out alternate";
}

// === DOMContentLoaded ===
document.addEventListener('DOMContentLoaded', () => {
  // Инициализируем музыку
  initMusic();
  
  // Добавляем анимацию тряски для ошибок
  const style = document.createElement('style');
  style.textContent = `
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      25% { transform: translateX(-5px); }
      75% { transform: translateX(5px); }
    }
  `;
  document.head.appendChild(style);
  
  // Инициализируем выбор типа ответа
  document.querySelectorAll('.type-option').forEach(option => {
    option.addEventListener('click', function() {
      playSelectSound();
      document.querySelectorAll('.type-option').forEach(opt => opt.classList.remove('selected'));
      this.classList.add('selected');
      state.answerType = this.dataset.type;
    });
  });
  
  // Устанавливаем выбранный тип по умолчанию
  document.querySelector('.type-option[data-type="single"]').classList.add('selected');
  
  // Инициализируем персонажей
  const container = document.getElementById('characters');
  for(const key in CHARACTERS){
    const ch = CHARACTERS[key];
    const div = document.createElement('div');
    div.className='char-card';
    div.dataset.key=key;
    div.innerHTML=`<img src="${ch.img}" alt="${ch.label}" /><div class="label">${ch.label}</div>`;
    div.onclick = () => handleCharacterClick(key);
    container.appendChild(div);
  }
  
  // Устанавливаем первого персонажа по умолчанию
  const first = container.querySelector('.char-card');
  if(first){ 
    first.classList.add('selected'); 
  }
  updateCharacterSelectionUI();

  // Обработчики кнопок с анимациями
  document.getElementById('btn-name-next').onclick = ()=>{
    playClickSound();
    const name = document.getElementById('input-name').value.trim();
    if(!name || name.length<2){ 
      // Анимация "тряски" для инпута при ошибке
      const input = document.getElementById('input-name');
      input.style.animation = 'shake 0.5s ease-in-out';
      setTimeout(() => input.style.animation = '', 500);
      alert('Введите имя минимум из 2 символов'); 
      return; 
    }
    state.name=name;
    show(STEP.TYPE, 'next');
  };

  document.getElementById('btn-type-back').onclick = ()=>{
    show(STEP.NAME, 'prev');
  };
  
  document.getElementById('btn-type-next').onclick = ()=>{
    show(STEP.CHAR, 'next');
  };

  document.getElementById('btn-char-back').onclick = ()=>{
    show(STEP.TYPE, 'prev');
  };
  
  document.getElementById('btn-char-next').onclick = ()=>{
    show(STEP.PROB, 'next');
  };
  
  document.getElementById('btn-problem-back').onclick = ()=>{
    show(STEP.CHAR, 'prev');
  };

  document.getElementById('btn-problem-send').onclick = async ()=>{
    playMagicSound();
    
    const problem=document.getElementById('input-problem').value.trim();
    if(!problem){ 
      const textarea = document.getElementById('input-problem');
      textarea.style.animation = 'shake 0.5s ease-in-out';
      setTimeout(() => textarea.style.animation = '', 500);
      alert('Опиши проблему, пожалуйста'); 
      return; 
    }
    state.problem=problem;
    
    const init=tg.initDataUnsafe||{};
    const user=init.user||{};
    const chat_id=user.id||null;
    const username=state.name || user.first_name || "друг";

    const resultBox = document.getElementById('result-box');
    const loader = document.getElementById('loading');

    resultBox.innerText = "";
    loader.classList.remove('hidden');
    
    // Показываем экран результата с особой анимацией
    show(STEP.RES, 'zoom');

    try{
      const backend=''; // вставь свой бэкенд
      const resp = await fetch(`${backend}/ask`,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
          chat_id, 
          username, 
          character: state.answerType === 'single' ? state.characters[0] : state.characters.join(','),
          answer_type: state.answerType,
          problem: state.problem
        })
      });
      const data = await resp.json();
      loader.classList.add('hidden');
      
      // Анимация появления результата
      resultBox.classList.add('fade-in');
      resultBox.innerText = data.ok ? (data.advice || "Пустой ответ") : "Ошибка: " + (data.error || JSON.stringify(data));
      
      setTimeout(() => {
        resultBox.classList.remove('fade-in');
      }, 600);
      
    }catch(err){
      console.error(err);
      loader.classList.add('hidden');
      resultBox.innerText = "Ошибка связи с сервером. Попробуй позже.";
    }
  };

  document.getElementById('btn-result-again').onclick = ()=>{
    playClickSound();
    document.getElementById('input-problem').value='';
    show(STEP.PROB, 'prev');
  };
  
  document.getElementById('btn-result-close').onclick = ()=>{
    playClickSound();
    tg.close();
  };

  // Добавляем звуки для всех кнопок при клике
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', playClickSound);
  });

  // Показываем первый экран и инициализируем прогресс-бар
  show(STEP.NAME);

  // Автозаполнение имени из Telegram
  try{
    const init=tg.initDataUnsafe||{};
    if(init.user && init.user.first_name){
      document.getElementById('input-name').value=init.user.first_name;
    }
  }catch(e){/* ignore */}
});

// === Touch device support ===
document.addEventListener('touchstart', function() {
  // Активируем музыку на тач-устройствах при первом касании
  if (!musicInitialized) {
    music.play().then(() => {
      musicBtn.textContent = '🔊';
      musicInitialized = true;
      isMusicPlaying = true;
    }).catch(error => {
      console.log('Автозапуск музыки на тач-устройстве заблокирован');
      musicBtn.textContent = '🔇';
      musicInitialized = true;
    });
  }
}, { once: true });
