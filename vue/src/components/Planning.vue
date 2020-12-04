<template>
  <div>
    <p>
      <label for="number_of_points">Сколько точек должно быть в спектре плана?</label>
      <input id="number_of_points" type="number" v-model="number_of_points" />
    </p>
    <button @click="send_number_of_points">Проверить</button>
    {{ answer }}
  </div>
</template>

<script>
import axios from "axios";
export default {
  created() {},
  data() {
    return {
      endpoint: "http://127.0.0.1:5000/api/check/plan_points_number",
      answer: "",
      number_of_points: 4,
    };
  },
  props: {},
  methods: {
    send_number_of_points: function (e) {
      axios
        .post(this.endpoint, {
          data: {
            plan_points_number: this.number_of_points,
          },
        })
        .then((response) => {
          if (response.data.message === "") this.answer = "Правильно!";
          else this.answer = response.data.message;
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
