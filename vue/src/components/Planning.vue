<template>
  <div>
    <div id="set_points_number">
      <p>
        <label for="number_of_points">Сколько точек должно быть в спектре плана?</label>
        <input id="number_of_points" type="number" v-model.number="number_of_points" />
      </p>
      <button @click="send_number_of_points">Проверить</button>
      {{ answer }}
    </div>
    <div id="set_points" style="display: none">
      <table class="table table-borderless table-responsive">
        <thead>
          <tr>
            <th scope="col"></th>
            <th scope="col">Значения Х1</th>
            <th scope="col">Значения Х2</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(n, index) in number_of_points" :key="index">
            <th scope="row">Точка {{ index + 1 }}</th>
            <td><input type="number" step="0.01" v-model.number="points[index][0]" /></td>
            <td><input type="number" step="0.01" v-model.number="points[index][1]" /></td>
          </tr>
        </tbody>
      </table>
      <p>
        <label>Количество параллельных экспериментов (не более 5)</label>
        <input type="number" v-model.number="experiments_number" />
      </p>
      <button @click="send_plan_points">Сохранить</button> {{ answer2 }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  created() {},
  data() {
    return {
      endpoints: ["http://127.0.0.1:5000/api/check/plan_points_number", "http://127.0.0.1:5000/api/check/plan_points_and_number_experiment"],
      answer: "",
      answer2: "",
      number_of_points: 4,
      points: [
        [1, 1],
        [-1, 1],
        [1, -1],
        [-1, -1],
      ],
      experiments_number: 5,
    };
  },
  props: {},
  methods: {
    send_number_of_points: function (e) {
      axios
        .post(this.endpoints[0], {
          data: {
            plan_points_number: this.number_of_points,
          },
        })
        .then((response) => {
          if (response.data.message === "") {
            this.answer = "Правильно!";
            setTimeout(function (e) {
              document.getElementById("set_points_number").style.display = "none";
              document.getElementById("set_points").style.display = "block";
            }, 2000);
          } else this.answer = response.data.message;
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_plan_points: function (e) {
      axios
        .post(this.endpoints[1], {
          data: {
            number_of_experiments: this.experiments_number,
            plan_points: this.points,
          },
        })
        .then((response) => {
          if (response.data.message === "") {
            this.answer2 = "Сохранено!";
          } else this.answer2 = response.data.message;
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
