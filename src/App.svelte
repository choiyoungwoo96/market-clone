<!-- svelte는 크게 3덩어리로 구분한다.
1. script
2. thml
3. css
-->

<script>
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router";
  import "./css/style.css";

  // router의 관리 # router로 되어있음
  const routes = {
    "/": Main,
    "/login": Login,
    "/signup": Signup,
    "/write": Write,
    // "*": NotFound 위에 패스외에 다른 패스에 들어갈경우에 뜨는 페이지 설정
    "*": NotFound,
  };
</script>

<Router {routes}></Router>

<main></main>

<style>
  div {
    color: red;
  }
</style>
