// app.js — логика мини-аппа
const tg = window.Telegram.WebApp;
tg.expand();

const STEP = {
  NAME: 'step-name',
  CHAR: 'step-character',
  PROB: 'step-problem',
  RES: 'step-result'
};

let state = {
  name: "",
  character: "usagi",
  problem: ""
};

// Персонажи, имена и изображения (совпадают с backend keys)
const CHARACTERS = {
  "usagi": { label: "Усаги", img: "https://i.pinimg.com/736x/a4/47/c4/a447c423d530b9cac4612a9f71c96ddc.jpg" },
  "ami": { label: "Ами", img: "https://i.pinimg.com/736x/b1/61/1a/b1611addcf1190d311218c22614e1e36.jpg" },
  "rei": { label: "Рей", img: "https://i.pinimg.com/736x/d7/9c/61/d79c617912ae0e4d510660c32c971227.jpg" },
  "minako": { label: "Минако", img: "https://i.pinimg.com/736x/68/68/52/6868521a4cf61d75b40772b6f13c0504.jpg" },
  "makoto": { label: "Макото", img: "https://i.pinimg.com/736x/49/27/8d/49278da7f93a6028a0a3d05bbd43fd22.jpg" }
  // Добавь остальные ключи если хочешь
};

function show(step) {
  document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
  document.getElementById(step).classList.add('active');
}

// init UI
document.addEventListener('DOMContentLoaded', () => {
  // render character cards
  const container = document.getElementById('characters');
  for (const key in CHARACTERS) {
    const ch = CHARACTERS[key];
    const div = document.createElement('div');
    div.className = 'char-card';
    div.dataset.key = key;
    div.innerHTML = `<img src="${ch.img}" alt="${ch.label}" /><div class="label">${ch.label}</div>`;
    div.onclick = () => {
      document.querySelectorAll('.char-card').forEach(el => el.classList.remove('selected'));
      div.classList.add('selected');
      state.character = key;
    };
    container.appendChild(div);
  }
  // select default
  const first = container.querySelector('.char-card');
  if (first) { first.classList.add('selected'); state.character = first.dataset.key; }

  // buttons
  document.getElementById('btn-name-next').onclick = () => {
    const name = document.getElementById('input-name').value.trim();
    if (!name || name.length < 2) {
      alert('Введите имя минимум из 2 символов');
      return;
    }
    state.name = name;
    show(STEP.CHAR);
  };
  document.getElementById('btn-char-back').onclick = () => show(STEP.NAME);
  document.getElementById('btn-char-next').onclick = () => show(STEP.PROB);
  document.getElementById('btn-problem-back').onclick = () => show(STEP.CHAR);

  document.getElementById('btn-problem-send').onclick = async () => {
    const problem = document.getElementById('input-problem').value.trim();
    if (!problem) { alert('Опиши проблему, пожалуйста'); return; }
    state.problem = problem;
    // Получаем chat_id и имя из Telegram WebApp initDataUnsafe (если возможно)
    const init = tg.initDataUnsafe || {};
    const user = init.user || {};
    const chat_id = user.id || null;
    const username = state.name || (user.first_name || "друг");

    // Постим на backend /ask
    try {
      // Замените <YOUR_RENDER_BACKEND> на домен где у тебя бот (Render)
      const backend = 'https://sailormoonpsychohelp-7bkw.onrender.com'; // <-- Поменяй на свой render hostname
      const resp = await fetch(`${backend}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: chat_id,
          username: username,
          character: state.character,
          problem: state.problem
        })
      });
      const data = await resp.json();
      if (!data.ok) {
        document.getElementById('result-box').innerText = "Ошибка: " + (data.error || JSON.stringify(data));
      } else {
        document.getElementById('result-box').innerText = data.advice || "Пустой ответ";
      }
      show(STEP.RES);
    } catch (err) {
      console.error(err);
      document.getElementById('result-box').innerText = "Ошибка связи с сервером. Попробуй позже.";
      show(STEP.RES);
    }
  };

  document.getElementById('btn-result-again').onclick = () => {
    // очистим поле проблемы и вернемся на шаг
    document.getElementById('input-problem').value = '';
    show(STEP.PROB);
  };
  document.getElementById('btn-result-close').onclick = () => {
    tg.close();
  };

  // show first step by default
  show(STEP.NAME);

  // Auto-fill name from Telegram if available
  try {
    const init = tg.initDataUnsafe || {};
    if (init.user && init.user.first_name) {
      document.getElementById('input-name').value = init.user.first_name;
    }
  } catch(e){/* ignore */}
});
