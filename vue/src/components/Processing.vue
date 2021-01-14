<template>
  <div>
    <div>
      <b-list-group>
        <b-list-group-item><b>Воспроизводимость:</b></b-list-group-item>
        <b-list-group-item to="/mean_var">Средние и дисперсии </b-list-group-item>
        <b-list-group-item to="/reproducibility"
          >Проверка воспроизводимости (Критерий Кохрена)
        </b-list-group-item>
        <b-list-group-item><b>Модель объекта:</b></b-list-group-item>
        <b-list-group-item to="/parameter_estimation"
          >Оценка параметров</b-list-group-item
        >
        <b-list-group-item to="/significance"
          >Значимость оценок (Критерий Стьюдента)</b-list-group-item
        >
        <b-list-group-item to="/addexp"
          >Дополнительный эксперимент</b-list-group-item
        >
        <b-list-group-item><b>Адекватность:</b></b-list-group-item>
        <b-list-group-item to="/adequacy"
          >Адекватность модели (Критерий Фишера)</b-list-group-item
        >
      </b-list-group>
    </div>
    <div class="documentation">
      <b-card bg-variant="info"> </b-card>
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
