<template>
  <div>
    <p>
      <label for="variant">Номер варианта задания</label>
      <select id="variant" v-model.number="variant" type="number">
        <option v-for="(n, index) in 6" :key="index">
          {{ index + 1 }}
        </option>
      </select>
      <button @click="send_variant">Сохранить</button>
    </p>
    <router-link class="nav-link" to="/planning_area">Далее</router-link>
    <div class="documentation">
      <p>
        В лабораторных работах объект, над которым проводится эксперимент, внешне
        представляется как "черный ящик" с определенным числом независимых факторов и
        одним откликом.
      </p>
      <p>
        Конкретное число независимых факторов и функциональная связь между факторами и
        откликом определяется вариантом задания.
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  created() {},
  data() {
    return {
      variant: 2,
      help: null,
      endpoint: "http://127.0.0.1:5000/api/check/task",
    };
  },
  props: {},
  methods: {
    save_variant: function (e) {
      this.$store.dispatch("changeVariant", this.variant);
    },
    send_variant: function (e) {
      axios
        .get(this.endpoint, { params: { task_id: this.variant } })
        .then((response) => {})
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
  },
};
</script>

<style scoped></style>
