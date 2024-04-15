const handleSubmitForm = async (e) => {
  e.preventDefault();
  const body = new FormData(form);
  body.append("insertAt", new Date().getTime());
  //   시간을 스크립트에서 생성해 post보낼 form데이터를
  console.log(body);
  try {
    const res = await fetch("/items", {
      method: "POST",
      body: body,
    });

    const json_res = res.json();
    if (json_res === "200") {
      window.location.pathname = "/";
    }
  } catch {
    console.error(e);
  }
};

const form = document.getElementById("write-form");
form.addEventListener("submit", handleSubmitForm);
