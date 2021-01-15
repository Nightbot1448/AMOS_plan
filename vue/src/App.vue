<template>
  <div id="app">
    <header></header>
    <main>
      <div>
        <b-nav tabs fill>
          <b-nav-item to="/preparation" exact-active-class>Подготовка</b-nav-item>
          <b-nav-item to="/experiment_menu" exact-active-class>Проведение</b-nav-item>
          <b-nav-item to="/processing" exact-active-class>Обработка</b-nav-item>
        </b-nav>
      </div>
      <div class="content">
        <div>
          <router-view />
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      data: null, // обработанные данные эксперимента
      help: null, // справка
      endpoint: "localhost:5000/generate", //в /generate нужно контролировать выдачу данных в зависимости от состояния выполнения лабы
    };
  },
  created() {
    //this.getAllPosts();
  },

  methods: {
    getDataFromExperiments() {
      axios
        .get(this.endpoint)
        .then((response) => {
          this.posts = response.data;
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    getHelpInfo() {
      axios
        .get(this.endpoint)
        .then((response) => {
          this.posts = response.data;
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
  },
};
</script>
