<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
            <div id="is_experiment_needed">
              <h2>Дополнительный эксперимент</h2>
              <p>Нужно ли провести дополнительный эксперимент?</p>
              <b-button
                id="user_answer_true"
                variant="primary"
                @click="check_add_exp_needed(true)"
                >Да</b-button
              >
              <b-button
                id="user_answer_false"
                variant="primary"
                @click="check_add_exp_needed(false)"
                >Нет</b-button
              >
              <div id="correct" style="display: none"><p>Верно!</p></div>
              <div id="incorrect" style="display: none"><p>Неправильно!</p></div>
            </div>
            <div id="add_experiment" style="display: none">
              <p>Введите значение факторов Х1 и Х2:</p>
              <b-row class="ml-5">
                    <b-col cols="4">
                        <b-form-input type="number" v-model.number="factor_1" />
                    </b-col>
                    <b-col cols="4">
                        <b-form-input type="number" v-model.number="factor_2" />
                    </b-col>
                    <b-col cols="4">
                        <b-button id="send_point" variant="primary" @click="check_add_exp_point()"
                >Отправить</b-button
              >
                    </b-col>
                </b-row>
              <p id="y_value" style="display: none">Результат: {{ y[-1] }} </p>
            </div>
          </b-card>
          <b-alert class="mt-2" variant="danger" :show="needed_answer ? true : false">
            {{ needed_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="point_answer ? true : false">
            {{ point_answer }}</b-alert
          >
          <div class="mb-5 mt-5">
            <b-button variant="secondary" to="/adequacy">Далее</b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  created() {},
  data() {
    return {
      is_exp_needed: false,
      needed_answer: "",
      factor_1: 0,
      factor_2: 0,
      y: 0,
      y_vals: 0,
      point_answer: "",
      endpoints: [
        "http://127.0.0.1:5000/api/check/need_additional_experiment",
        "http://127.0.0.1:5000/api/check/additional_experiment_point",
      ],
    };
  },
  props: {},
  methods: {
    check_add_exp_needed: function (user_answer) {
      document.getElementById("correct").style.display = "none";
      document.getElementById("incorrect").style.display = "none";
      axios
        .post(this.endpoints[0])
        .then((response) => {
          if (!response.data.error) {
            this.is_exp_needed = response.data.data.is_additional_experiment_needed;
            if (user_answer == this.is_exp_needed) {
              document.getElementById("correct").style.display = "block";
                  document.getElementById("user_answer_true").disabled = true;
                  document.getElementById("user_answer_false").disabled = true;
                  this.needed_answer = response.data.message;
              if (user_answer == true){
                  document.getElementById("add_experiment").style.display = "block";
              }
            } else {
              document.getElementById("incorrect").style.display = "block";
            }
          } else {
            this.needed_answer = response.data.message;
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    check_add_exp_point: function (e) {
      axios
        .post(this.endpoints[1], {
          data: { additional_experiment_point: [this.factor_1, this.factor_2] },
        })
        .then((response) => {
          if (!response.data.error) {
            this.y = response.data.data.y;
            this.y_vals = response.data.data.y_vals;
            document.getElementById("y_value").style.display = 'block';
            document.getElementById("send_point").disabled = true;
          } else {
            this.point_answer = response.data.message;
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
