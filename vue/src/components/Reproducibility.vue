<template>
  <div>
    <div id="significance">
      <label for="significance">Уровень значимости</label>
      <select id="significance" v-model.number="significance" type="number">
        <option>0.01</option>
        <option>0.05</option>
      </select>
      <button @click="send_significance">Сохранить</button>
    </div>
    <div id="sum_var" style="display: none">
      <label for="sum_var">Сумма дисперсий отклика по всем точкам:</label>
      <p>{{ sum_var }}</p>
    </div>
    <div id="cochrain" style="display: none">
      <label for="cochrain">Наблюдаемое значение критерия Кохрена:</label>
      <input v-model.number="cochrain" type="number" />
      <button @click="send_cochrain()">Сохранить</button>
      <p id="cochrain_answer"></p>
    </div>
    <div id="table_cochrain" style="display: none">ТАБЛИЦА</div>
    <div id="cochrain_freedom_degree" style="display: none">
      <div>
        <label for="df_numerator"
          >Введите число степеней свободы <b>числителя</b> критерия Кохрена:</label
        ><br />
        <input v-model.number="df_numerator" type="number" />
      </div>
      <div>
        <label for="df_denominator"
          >Введите число степеней свободы <b>знаменателя</b> критерия Кохрена:</label
        ><br />
        <input v-model.number="df_denominator" type="number" />
      </div>
      <div>
        <button @click="send_cochrain_freedom_degree()">Сохранить</button>
        <p id="freedom_answer"></p>
      </div>
    </div>
    <div id="cochrain_compare" style="display: none">
      <label for="cochrain">Наблюдаемое значение критерия Кохрена: {{ cochrain }}</label
      ><br />
      <label for="crit_cochrain"
        >Критическое значение критерия Кохрена: {{ crit_cochrain }}</label
      >
      <div>
        <label>Гипотеза о воспроизводимости эксперимента подтверждается?</label>
        <button @click="is_reproducible(true)">Да</button>
        <button @click="is_reproducible(false)">Нет</button>
      </div>
      <p id="reproducible_answer"></p>
    </div>
    <div id="reproducible_var" style="display: none">
      <label for="reproducible_var"
        >Введите значение дисперсии ошибки эксперимента:</label
      >
      <input v-model.number="reproducible_var" type="number" />
      <button @click="send_reproducible_var">Сохранить</button>
      <p id="reproducible_var_answer"></p>
    </div>
    <div id="results" style="display: none">
      <p>
        Проверка проводилась по критерию Кохрена на уровне значимости {{ significance }}
      </p>
      <p>Наблюдаемое значение критерия Кохрена: {{ cochrain }}</p>
      <p>Критическое значение критерия Кохрена: {{ crit_cochrain }}</p>
      <p>Вывод: эксперимент <span v-if="!reproducibility">не</span> воспроизводим</p>
      <p>Дисперсия ошибки (воспроизводимости) эксперимента: {{ reproducible_var }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  created() {},
  data() {
    return {
      significance: 0.01,
      sum_var: 0,
      cochrain: 0,
      df_numerator: 0,
      df_denominator: 0,
      crit_cochrain: 0,
      reproducibility: 0,
      reproducible_var: 0,
      endpoints: [
        "http://127.0.0.1:5000/api/set/significance_level",
        "http://127.0.0.1:5000/api/check/cochrain",
        "http://127.0.0.1:5000/api/check/cochrain_freedom_degree",
        "http://127.0.0.1:5000/api/get/cochrain",
        "http://127.0.0.1:5000/api/check/is_reproducible",
        "http://127.0.0.1:5000/api/check/reproducible_var",
      ],
    };
  },
  props: {},
  methods: {
    send_significance: function (e) {
      axios
        .post(this.endpoints[0], { data: { significance: this.significance } })
        .then((response) => {
          if (response.data.message === "") {
            document.getElementById("significance").style.display = "none";
            document.getElementById("sum_var").style.display = "block";
            document.getElementById("cochrain").style.display = "block";
            this.sum_var = Number(response.data.data.sum_var.toFixed(2));
          } else {
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_cochrain: function (e) {
      axios
        .post(this.endpoints[1], {
          data: { cochrain: this.cochrain },
        })
        .then((response) => {
          if (
            response.data.message ===
            "Тут могла быть таблица для Кохрана, но её не завезли"
          ) {
            document.getElementById("sum_var").style.display = "none";
            document.getElementById("cochrain").style.display = "none";
            //do smth with cochrain table
            alert("Допустим, отрисовалась таблица Кохрена");
            document.getElementById("table_cochrain").style.display = "block";
            document.getElementById("cochrain_freedom_degree").style.display = "block";
          } else {
            document.getElementById("cochrain_answer").innerText = "Неправильно.";
            this.$forceUpdate();
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_cochrain_freedom_degree: function (e) {
      axios
        .post(this.endpoints[2], {
          data: {
            df_numerator: this.df_numerator,
            df_denominator: this.df_denominator,
          },
        })
        .then((response) => {
          if (response.data.message == "") {
            document.getElementById("freedom_answer").innerText = "Правильно.";
            setTimeout(function (e) {
              document.getElementById("table_cochrain").style.display = "none";
              document.getElementById("cochrain_freedom_degree").style.display = "none";
            }, 1500);
            document.getElementById("cochrain_compare").style.display = "block";
            this.$forceUpdate();
            axios
              .get(this.endpoints[3])
              .then((response) => {
                if (response.data.message == "") {
                  this.crit_cochrain = Number(
                    response.data.data.crit_cochrain.toFixed(2)
                  );
                  this.cochrain = Number(response.data.data.prac_cochrain.toFixed(2));
                } else {
                }
              })
              .catch((error) => {
                console.log("-----error-------");
                console.log(error);
              });
          } else {
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    is_reproducible: function (user_answer) {
      axios
        .post(this.endpoints[4], { data: { is_reproducible: user_answer } })
        .then((response) => {
          if (response.data.message == "") {
            document.getElementById("reproducible_answer").innerText = "Правильно.";
            document.getElementById("reproducible_var").style.display = "block";
            this.reproducibility = true;
          } else {
            document.getElementById("reproducible_answer").innerText = "Неправильно.";
            document.getElementById("reproducible_var").style.display = "none";
            this.reproducibility = false;
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_reproducible_var: function (e) {
      axios
        .post(this.endpoints[5], { data: { reproducible_var: this.reproducible_var } })
        .then((response) => {
          if (response.data.message == "") {
            document.getElementById("results").style.display = "block";
            document.getElementById("reproducible_var_answer").innerText = "Правильно.";
          } else {
            document.getElementById("reproducible_var_answer").innerText = "Неправильно.";
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
