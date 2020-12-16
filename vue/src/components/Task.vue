<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
            <h3>Номер варианта задания</h3>
            <b-form-select id="variant" v-model.number="variant" type="number">
              <option v-for="(n, index) in 6" :key="index">
                {{ index + 1 }}
              </option>
            </b-form-select>
            <div class="mt-3">
              <b-button id="save_var" @click="send_variant" size="lg" variant="primary"
                >Сохранить</b-button
              >
            </div>
          </b-card>
          <b-alert class="mt-2" variant="success" :show="answer">Вариант выбран.</b-alert>
          <div class="mb-5 mt-5">
            <b-button variant="secondary" to="/planning_area">Далее</b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
        <p>
          В лабораторных работах объект, над которым проводится эксперимент, внешне
          представляется как "черный ящик" с определенным числом независимых факторов и
          одним откликом.
        </p>
        <p>
          Конкретное число независимых факторов и функциональная связь между факторами и
          откликом определяется вариантом задания.
        </p>
      </b-card>
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
      answer: false,
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
        .then((response) => {
          if (response.data.message === "") {
            this.answer = true;
            document.getElementById("save_var").disabled = true;
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
  },
};
</script>

<style scoped></style>
