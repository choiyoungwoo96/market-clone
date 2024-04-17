const form = document.querySelector("#login-form");

const hadleSubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  const div = document.querySelector("#info");

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });
  const data = await res.json();
  accessToken = data.acces_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인되었습니다.");
  window.location.pathname = "/";
  //   window.sessionStorage.setItem("token", accessToken);
  //   const infoDiv = document.querySelector("#info");
  //   infoDiv.innerText = "로그인되었습니다";
  //
  //   const btn = document.createElement("button");
  //   btn.innerText = "상품가지고오기";
  //   btn.addEventListener("click", async () => {
  //     const res = await fetch("/items", {
  //       headers: {
  //         Authorization: `Bearer ${accessToken}`,
  //       },
  //     });
  //     const data = await res.json();
  //     console.log(data);
  //   });
  //   infoDiv.appendChild(btn);
  //   status : 서버에서 내려주는 값
  //   if (res.status === 200) {
  //     alert("로그인에 성공했습니다");
  //     window.location.pathname = "/";
  //   } else if (res.status === 401) {
  //     alert("로그인에 실패하였습니다");
  //   }
};

form.addEventListener("submit", hadleSubmit);
