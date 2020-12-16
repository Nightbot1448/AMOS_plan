<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
            <h3>Планирование эксперимента</h3>
    <table class="table table-borderless table-responsive">
      <thead>
        <tr>
          <th scope="col"></th>
          <th scope="col">Координаты центра области</th>
          <th scope="col">Интервалы варьирования</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">Фактор X1</th>
          <td><b-form-input type="number" step="0.01" v-model.number="x1c" /></td>
          <td><b-form-input type="number" step="0.01" v-model.number="x1i" /></td>
        </tr>
        <tr>
          <th scope="row">Фактор X2</th>
          <td><b-form-input type="number" step="0.01" v-model.number="x2c" /></td>
          <td><b-form-input type="number" step="0.01" v-model.number="x2i" /></td>
        </tr>
      </tbody>
    </table>
    <div class="mt-3">
    <b-button id="save_data" @click="send_points" size="lg" variant="primary">Сохранить</b-button></div>
    </b-card>
    <b-alert class="mt-2" variant="success" :show="answer">Область планирования успешно задана.</b-alert>
    <b-alert class="mt-2" variant="danger" :show="error ? true : false">{{ error }}</b-alert>
    <div class="mb-5 mt-5"><b-button variant="secondary" to="/planning">Далее</b-button></div>
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
      <p>
        Область планирования - область значений факторов, в которой находятся точки, отвечающие условиям проведения опытов используемого плана эксперимента. Область планирования составляет часть допустимого диапазона изменения факторов или совпадает с ним.
      </p>
      <p>
        Область планирования задается для каждого фактора:
        <ul>
          <li>основным уровнем фактора</li>
          <li>интервалом варьирования фактора</li>
        </ul>
      </p>
      <p>Вектор, компонентами которого являются упорядоченные численные значения основных уровней факторов, задает точку, являющуюся центром области планирования, в окрестности которой и располагаются все точки плана.</p>
      </b-card>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";

export default {
  created() {},
  data() {
    return {
      x1c: -10,
      x1i: 20,
      x2c: 0,
      x2i: 10,
      answer: false,
      error: "",
      endpoint: "http://127.0.0.1:5000/api/check/planning_area",
    };
  },
  props: {},
  methods: {
    save_points: function (e) {
      this.$store.dispatch("changePAPoints", [
        [this.x1c, this.x1i],
        [this.x2c, this.x2i],
      ]);
    },
    send_points: function (e) {
      axios
        .post(this.endpoint, {
          data: {
            pa_points: [
              [this.x1c, this.x1i],
              [this.x2c, this.x2i],
            ],
          },
        })
        .then((response) => {
          if (response.data.message === "") {
            this.answer = true;
            document.getElementById("save_data").disabled = true;
          }
          else {
            this.error = response.data.message
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
