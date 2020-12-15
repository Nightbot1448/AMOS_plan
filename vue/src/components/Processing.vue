<template>
  <div>
    <ul>
      <label>Воспроизводимость</label>
      <li>
        <router-link to="/mean_var">Средние и дисперсии</router-link>
      </li>
      <li>
        <router-link to="/reproducibility"
          >Проверка воспроизводимости (Критерий Кохрена)</router-link
        >
      </li>
      <label>Модель объекта</label>
      <li>
        <router-link to="/parameter_estimation">Оценка параметров</router-link>
      </li>
      <li>
        <router-link to="/significance"
          >Значимость оценок (Критерий Стьюдента)</router-link
        >
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  created() {},
  data() {
    return {
      variant: 2,
      help: null,
    };
  },
  props: {},
  methods: {
    save_variant: function (e) {
      this.$store.dispatch("changeVariant", this.variant);
    },
  },
};
</script>

<style scoped></style>
