const calcTime = (timestamp) => {
  // 한국시간 기준으로 계산하게 됨
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
  const time = new Date(curTime - timestamp);
  const hour = time.getHours();
  const minute = time.getMinutes();
  const second = time.getSeconds();

  if (hour > 0) return `${hour}시간 전`;
  else if (minute > 0) return `${minute}분 전`;
  else if (second >= 0) return `${second}초 전`;
  else return "방금 전";
};

const rederDate = (data) => {
  const main = document.querySelector("main");
  data.reverse().forEach(async (obj) => {
    const div = document.createElement("div");
    div.className = "item-list";

    const InfoDiv = document.createElement("div");
    InfoDiv.className = "item-list__info";

    const InfoTtile = document.createElement("div");
    InfoTtile.className = "item-list__info-title";
    InfoTtile.innerText = obj.title;

    const InfoMeta = document.createElement("div");
    InfoMeta.className = "item-list__info-meta";
    InfoMeta.innerText = obj.place + " " + calcTime(obj.insertAt);

    const Infoprice = document.createElement("div");
    Infoprice.className = "item-list__info-price";
    Infoprice.innerText = obj.price;

    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    img.src = url;

    const imgDiv = document.createElement("div");
    imgDiv.className = "item-list__img";

    imgDiv.appendChild(img);
    InfoDiv.appendChild(InfoTtile);
    InfoDiv.appendChild(InfoMeta);
    InfoDiv.appendChild(Infoprice);
    div.appendChild(imgDiv);
    div.appendChild(InfoDiv);
    main.appendChild(div);
  });
};

const fetchList = async () => {
  const res = await fetch("/items");
  const data = await res.json();
  rederDate(data);
};
fetchList();
