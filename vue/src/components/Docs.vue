<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
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
                <b-list-group-item><b>Адекватность:</b></b-list-group-item>
                <b-list-group-item to="/adequacy"
                >Адекватность модели (Критерий Фишера)</b-list-group-item
                >
            </b-list-group>
            </div>
            </b-card>
        </b-col>
      </b-row>
    </b-container>
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
