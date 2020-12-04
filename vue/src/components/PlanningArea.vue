<template>
  <div>
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
          <td><input type="number" step="0.01" v-model.number="x1c" /></td>
          <td><input type="number" step="0.01" v-model.number="x1i" /></td>
        </tr>
        <tr>
          <th scope="row">Фактор X2</th>
          <td><input type="number" step="0.01" v-model.number="x2c" /></td>
          <td><input type="number" step="0.01" v-model.number="x2i" /></td>
        </tr>
      </tbody>
    </table>
    <button @click="send_points">Сохранить</button>
    <router-link class="nav-link" to="/planning">Далее</router-link>
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
