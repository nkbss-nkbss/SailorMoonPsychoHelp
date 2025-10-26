const tg = window.Telegram.WebApp;
tg.expand();

let state = {
  name: "",
  character: "usagi"
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

// Показ шага
function show(step){
  document.querySelectorAll('.card').forEach(c=>c.classList.remove('active'));
  const el = document.getElementById(step);
  el.classList.add('active');
  el.style.opacity = 0;
  setTimeout(()=>el.style.opacity = 1,10);
}

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('characters');
  for(const key in CHARACTERS){
    const ch = CHARACTERS[key];
    const div = document.createElement('div');
    div.className = 'char-card';
    div.dataset.key = key;
    div.innerHTML = `
      <img src="${ch.img}" alt="${ch.label}" />
      <div class="label">${ch.label}</div>
    `;
    div.onclick = ()=>{
      document.querySelectorAll('.char-card').forEach(el=>el.classList.remove('selected'));
      div.classList.add('selected');
      state.character = key;
    };
    container.appendChild(div);
  }

  const first = container.querySelector('.char-card');
  if(first){ first.classList.add('selected'); state.character = first.dataset.key; }

  // шаг 1 — ввод имени
  document.getElementById('btn-name-next').onclick = ()=>{
    const name = document.getElementById('input-name').value.trim();
    if(!name || name.length<2){ alert('Введите имя минимум из 2 символов'); return; }
    state.name = name;
    show('step-chat');
  };

  // кнопка "назад" из выбора персонажа
  document.getElementById('btn-char-back').onclick = ()=>show('step-name');

  // обработчик отправки сообщения
  document.getElementById('btn-send').onclick = async ()=>{
    const input = document.getElementById('input-problem');
    const problem = input.value.trim();
    if(!problem){ alert('Опиши проблему, пожалуйста'); return; }
    input.value = '';

    const chatBox = document.getElementById('chat-box');
    const userMsg = document.createElement('div');
    userMsg.className = 'msg user';
    userMsg.innerText = problem;
    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    const loader = document.createElement('div');
    loader.className = 'msg bot loading';
    loader.innerText = '💫 Думает...';
    chatBox.appendChild(loader);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
      const backend = 'https://sailormoonpsychohelp-7bkw.onrender.com';
      const resp = await fetch(`${backend}/ask`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          chat_id: tg.initDataUnsafe?.user?.id || null,
          username: state.name,
          character: state.character,
          problem
        })
      });
      const data = await resp.json();
      loader.remove();

      const botMsg = document.createElement('div');
      botMsg.className = 'msg bot';
      botMsg.innerText = data.ok ? (data.advice || "Пустой ответ") : "Ошибка: " + (data.error || JSON.stringify(data));
      chatBox.appendChild(botMsg);
      chatBox.scrollTop = chatBox.scrollHeight;
    } catch(err) {
      console.error(err);
      loader.remove();
      const errorMsg = document.createElement('div');
      errorMsg.className = 'msg bot error';
      errorMsg.innerText = "Ошибка связи с сервером. Попробуй позже.";
      chatBox.appendChild(errorMsg);
    }
  };

  show('step-name');

  try {
    const init = tg.initDataUnsafe || {};
    if(init.user && init.user.first_name){
      document.getElementById('input-name').value = init.user.first_name;
    }
  } catch(e) { /* ignore */ }
});
