<template>
  <div>
    <div>
      <ul>
        <li>
          <router-link class="nav-link" to="/task">Задание (выбор варианта)</router-link>
        </li>
        <li>
          <router-link class="nav-link" to="/planning_area"
            >Область планирования</router-link
          >
        </li>
        <li><router-link class="nav-link" to="/planning">Планирование</router-link></li>
      </ul>
    </div>
    <div class="documentation">
      <p>Этап подготовки эксперимента предусматривает определение режима проведения работы, задание исходных данных, необходимых для построения плана и проведения эксперимента, а также построение плана эксперимента.</p>
      <p>
        Задание исходных данных включают в себя:
        <ul>
          <li>задание объекта исследования</li>
          <li>задание области планирования</li>
          <li>выбор типа плана эксперимента</li>
        </ul>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {},
};
</script>

<style scoped></style>
