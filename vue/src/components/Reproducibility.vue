<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
            <div id="significance">
              <label for="significance">Уровень значимости</label>
              <b-form-select id="significance" v-model.number="significance" type="number">
                <option>0.01</option>
                <option>0.05</option>
              </b-form-select>
              <b-button @click="send_significance" variant="primary" class="mt-4" id="send_sign">Сохранить</b-button>
            </div>
            <div id="sum_var" style="display: none">
              <label for="sum_var">Сумма дисперсий отклика по всем точкам:</label>
              <p>{{ sum_var }}</p>
            </div>
            <div id="cochrain" style="display: none">
              <label for="cochrain">Наблюдаемое значение критерия Кохрена:</label>
              <b-form-input v-model.number="cochrain" type="number" />
              <b-button id="send_coch" @click="send_cochrain()" class="mt-4" variant="primary">Сохранить</b-button>
            </div>
            <div id="table_cochrain" style="display: none">ТАБЛИЦА</div>
            <div id="cochrain_freedom_degree" style="display: none">
              <div>
                <label for="df_numerator"
                  >Введите число степеней свободы <b>числителя</b> критерия Кохрена:</label
                ><br />
                <b-form-input v-model.number="df_numerator" type="number" />
              </div>
              <div>
                <label for="df_denominator"
                  >Введите число степеней свободы <b>знаменателя</b> критерия Кохрена:</label
                ><br />
                <b-form-input v-model.number="df_denominator" type="number" />
              </div>
              <div>
                <b-button class="mt-4" id="send_coch_free" @click="send_cochrain_freedom_degree()" variant="primary">Сохранить</b-button>
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
                <b-button @click="is_reproducible(true)" variant="primary">Да</b-button>
                <b-button @click="is_reproducible(false)" variant="primary">Нет</b-button>
              </div>
              <p id="reproducible_answer"></p>
            </div>
            <div id="reproducible_var" style="display: none">
              <label for="reproducible_var"
                >Введите значение дисперсии ошибки эксперимента:</label
              >
              <b-form-input v-model.number="reproducible_var" type="number" />
              <b-button class="mt-4" id="rep_var" @click="send_reproducible_var" variant="primary">Сохранить</b-button>
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
          </b-card>
          <b-alert class="mt-2" variant="danger" :show="cochrain_answer ? true : false">
            {{ cochrain_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="cochrain_answer ? true : false">
            {{ freedom_answer }}</b-alert
          >
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
        <p>Уровень значимости - вероятность отвержения правильной гипотезы</p>
        <p>
          Наблюдаемое значение критерия Кохрена - статистика, вычисляемая как отношение
          максимальной дисперсии отклика к сумме дисперсий отклика по всем точкам спектра
          плана.<br />Например, пусть получены следующие оценки дисперсии отклика:
        </p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка ФП</th>
                  <th>Оценка дисперсии</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>0.20</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>0.65</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>0.12</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>0.56</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>
          Тогда расчет наблюдаемого значения критерия Кохрена проводится так:<br />
          Набл_Кох = 0.65 / ( 0.20 + 0.65 + 0.12 + 0.56 ) = 0.423
        </p>
        <p>
          Число степеней свободы числителя критерия Кохрена - число степеней свободы
          дисперсии отклика, т.е. число параллельных опытов минус единица:
          <p class="ml-4">m-1,</p>т.к. одна степень свободы “израсходована” для вычисления средних
          значений отклика.<br />
          Число степеней свободы знаменателя критерия Кохрена - число степеней свободы
          суммы дисперсий по всех точкам спектра плана, т.е. - общее число точек спектра
          плана.
        </p>
        <p>
          Если воспроизводимость эксперимента подтвердилась, то значит каждая из построчных дисперсий оценивает одну и ту же величину - дисперсии воспроизводимости ( дисперсии ошибки эксперимента ), которую можно оценить более точно путем усреднения построчных дисперсий. <br>Например, пусть получены следующие оценки дисперсии отклика:
        </p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка ФП</th>
                  <th>Оценка дисперсии</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>0.20</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>0.65</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>0.12</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>0.56</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>
          Тогда дисперсия воспроизводимости рассчитывается так:<br>
          Диспр_воспр = ( 0.20 + 0.65 + 0.12 + 0.56) /4 = 0.39
        </p>
        <p>Проверка воспроизводимости - проверка постоянства дисперсии шума. Считается, что условие постоянства дисперсии шума выполнено, если справедлива гипотеза:</p>
        <p>"дисперсии в каждой точке факторного пространства оценивают одну и ту не величину”</p>
        <p>Проверка этой гипотезы при альтернативной:</p>
        <p>
          “хотя бы одна из построчных дисперсий не равна остальным"
        </p>
        <p>производится с помощью критерия Кохрена:</p>
        <p>если наблюдаемое значение критерия Кохрена меньше критического значения на выбранном уровне значимости, то считается, что экспериментальные данные не опровергают гипотезу об однородности ряда дисперсий, тогда можно вычислить оценку дисперсии шума - дисперсии воспроизводимости, и продолжать обработку результатов эксперимента, который в данном случае является воспроизводимым.</p>
        <p>
          В противном случае дисперсию шума нельзя считать постоянной, и эксперимент
          считается невоспроизводимым.
        </p>
        <p>
          Например, если наблюдаемое значение критерия Кохрена:<br />
          Набл_Кох = 0.423,<br />
          а критическое:<br />
          Крит_Cox(2, 4, 0. 05) = 0.768,<br />
          то гипотеза о воспроизводимости эксперимента принимается на уровне значимости а
          = 0. 05.
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
      significance: 0.01,
      sum_var: 0,
      cochrain: 0,
      df_numerator: 0,
      df_denominator: 0,
      crit_cochrain: 0,
      reproducibility: 0,
      reproducible_var: 0,
      cochrain_answer: "",
      freedom_answer: "",
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
            document.getElementById("send_sign").disabled = true;
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
            document.getElementById("send_coch").disabled = true;
            //do smth with cochrain table
            alert("Допустим, отрисовалась таблица Кохрена");
            document.getElementById("table_cochrain").style.display = "block";
            document.getElementById("cochrain_freedom_degree").style.display = "block";
          } else {
            this.cochrain_answer = response.data.message;
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
            document.getElementById("send_coch_free").disabled = true;
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
            this.freedom_answer = response.data.message
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
            document.getElementById("rep_var").disabled = true;
            document.getElementById("cochrain_compare").style.display = "none";
            document.getElementById("reproducible_var").style.display = "none";
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
