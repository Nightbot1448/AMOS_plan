<template>
  <div>
    <div>
      <b-list-group>
        <b-list-group-item to="/task">Задание (выбор варианта)
        </b-list-group-item>
        <b-list-group-item to="/planning_area"> Область планирования
          
        </b-list-group-item>
        <b-list-group-item to="/planning">Планирование</b-list-group-item>
      </b-list-group>
    </div>
    <div class="documentation">
      <b-card bg-variant="info">
      <p>Этап подготовки эксперимента предусматривает определение режима проведения работы, задание исходных данных, необходимых для построения плана и проведения эксперимента, а также построение плана эксперимента.</p>
      <p>
        Задание исходных данных включают в себя:
        <ul>
          <li>задание объекта исследования</li>
          <li>задание области планирования</li>
          <li>выбор типа плана эксперимента</li>
        </ul>
      </p>
      </b-card>
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
