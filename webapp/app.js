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

function show(step){
  document.querySelectorAll('.card').forEach(c=>c.classList.remove('active'));
  const el = document.getElementById(step);
  el.classList.add('active');
  // плавная анимация
  el.style.opacity=0;
  setTimeout(()=>el.style.opacity=1,10);
}

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('characters');
  for(const key in CHARACTERS){
    const ch = CHARACTERS[key];
    const div = document.createElement('div');
    div.className='char-card';
    div.dataset.key=key;
    div.innerHTML=`<img src="${ch.img}" alt="${ch.label}" /><div class="label">${ch.label}</div>`;
    div.onclick = ()=>{
      document.querySelectorAll('.char-card').forEach(el=>el.classList.remove('selected'));
      div.classList.add('selected');
      state.character=key;
    }
    container.appendChild(div);
  }
  const first = container.querySelector('.char-card');
  if(first){ first.classList.add('selected'); state.character=first.dataset.key; }

  document.getElementById('btn-name-next').onclick = ()=>{
    const name = document.getElementById('input-name').value.trim();
    if(!name || name.length<2){ alert('Введите имя минимум из 2 символов'); return; }
    state.name=name;
    show(STEP.CHAR);
  };
  document.getElementById('btn-char-back').onclick = ()=>show(STEP.NAME);
  document.getElementById('btn-char-next').onclick = ()=>show(STEP.PROB);
  document.getElementById('btn-problem-back').onclick = ()=>show(STEP.CHAR);

  document.getElementById('btn-problem-send').onclick = async ()=>{
    const problem=document.getElementById('input-problem').value.trim();
    if(!problem){ alert('Опиши проблему, пожалуйста'); return; }
    state.problem=problem;
    const init=tg.initDataUnsafe||{};
    const user=init.user||{};
    const chat_id=user.id||null;
    const username=state.name||(user.first_name||"друг");
  
    const resultBox = document.getElementById('result-box');
    const loader = document.getElementById('loading');
  
    // показать анимацию ожидания
    resultBox.innerText = "";
    loader.classList.remove('hidden');
    show(STEP.RES);
  
    try{
      const backend=''; // вставь свой бэкенд
      const resp=await fetch(`${backend}/ask`,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({chat_id, username, character:state.character, problem:state.problem})
      });
      const data=await resp.json();
      loader.classList.add('hidden');
      resultBox.innerText = data.ok ? (data.advice || "Пустой ответ") : "Ошибка: " + (data.error || JSON.stringify(data));
    }catch(err){
      console.error(err);
      loader.classList.add('hidden');
      resultBox.innerText = "Ошибка связи с сервером. Попробуй позже.";
    }
  };


    try{
      const backend=''; // вставь свой бэкенд
      const resp=await fetch(`${backend}/ask`,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({chat_id, username, character:state.character, problem:state.problem})
      });
      const data=await resp.json();
      document.getElementById('result-box').innerText = data.ok?data.advice||"Пустой ответ":"Ошибка: "+(data.error||JSON.stringify(data));
      show(STEP.RES);
    }catch(err){
      console.error(err);
      document.getElementById('result-box').innerText="Ошибка связи с сервером. Попробуй позже.";
      show(STEP.RES);
    }
  };

  document.getElementById('btn-result-again').onclick = ()=>{
    document.getElementById('input-problem').value='';
    show(STEP.PROB);
  };
  document.getElementById('btn-result-close').onclick = ()=>tg.close();

  show(STEP.NAME);

  try{
    const init=tg.initDataUnsafe||{};
    if(init.user && init.user.first_name){
      document.getElementById('input-name').value=init.user.first_name;
    }
  }catch(e){/* ignore */}
});
