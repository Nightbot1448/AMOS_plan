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
            <div id="param_1" style="display: none">
              <label for="param_1">Наблюдаемое значение критерия Стьюдента для {{ params[0] }}:</label>
              <b-form-input v-model.number="param_1" type="number" />
              <b-button @click="display_param_2" variant="primary" class="mt-4" id="param_1_btn">Проверить</b-button>
            </div>
            <div id="param_2" style="display: none">
              <label for="param_2">Наблюдаемое значение критерия Стьюдента для {{ params[1] }}:</label>
              <b-form-input v-model.number="param_2" type="number" />
              <b-button @click="send_params" variant="primary" class="mt-4" id="param_2_btn">Проверить</b-button>
            </div>
            <div id="crit_values" style="display: none">
              <b-row>
                <b-col cols="6">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Число степеней свободы</th>
                    <th>Критическое значение</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(n, i) in vals.length" v-if="i<13" :key="i">
                    <td>{{ df[i] }}</td>
                    <td>{{ vals[i] }}</td>
                  </tr>
                </tbody>
              </table>
              </b-col>
              <b-col cols="6">
                <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Число степеней свободы</th>
                    <th>Критическое значение</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(n, j) in vals.length" v-if="j>=13" :key="j">
                    <td>{{ df[j] }}</td>
                    <td>{{ vals[j] }}</td>
                  </tr>
                </tbody>
              </table>
              </b-col>
              </b-row>
              <label for="param_1">Введите число степеней свободы критерия Стьюдента:</label>
              <b-form-input v-model.number="check_df" type="number" />
              <b-button @click="send_check_df" variant="primary" class="mt-4" id="check_df_btn">Проверить</b-button>
            </div>
            <div id="sign_1" style="display: none">
              <p>Наблюдаемое значение критерия: {{ prac_values[params_index[0]] ? Number(prac_values[params_index[0]].toFixed(2)): prac_values[params_index[0]] }}</p>
              <p>Критическое значение критерия: {{ crit_value }}</p>
              <p>Оценка параметра {{ params[0] }} значима?</p>
              <b-button @click="is_sign(true, params_index[0])" variant="primary">Да</b-button>
              <b-button @click="is_sign(false, params_index[0])" variant="primary">Нет</b-button>
            </div>
            <div id="sign_2" style="display: none">
              <p>Наблюдаемое значение критерия: {{ prac_values[params_index[1]] ? Number(prac_values[params_index[1]].toFixed(2)): prac_values[params_index[1]] }}</p>
              <p>Критическое значение критерия: {{ crit_value }}</p>
              <p>Оценка параметра {{ params[1] }} значима?</p>
              <b-button @click="is_sign(true, params_index[1])" variant="primary">Да</b-button>
              <b-button @click="is_sign(false, params_index[1])" variant="primary">Нет</b-button>
            </div>
            <div id="sign_table" style="display: none">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Обозначение</th>
                    <th>Оценка</th>
                    <th>Критерий</th>
                    <th>Значим?</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(n, i) in params_list.length" :key="i">
                    <td>{{ params_list[i] }}</td>
                    <td>{{ param_values[i] ? Number(param_values[i].toFixed(2)): param_values[i] }}</td>
                    <td>{{ prac_values[i] ? Number(prac_values[i].toFixed(2)) : prac_values[i] }}</td>
                    <td>{{ sign_values[i] }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </b-card>
          <b-alert class="mt-2" variant="danger" :show="significance_answer ? true : false">
            {{ significance_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="param_answer ? true : false">
            {{ param_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="df_answer ? true : false">
            {{ df_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="info" :show="sign_answer ? true : false">
            {{ sign_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="sign_wrong ? true : false">
            {{ sign_wrong }}</b-alert
          >
          <div class="mb-5 mt-5">
            <b-button variant="secondary" to="/adequacy">Далее</b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
        <p>
          Наблюдаемое значение критерия Стьюдента - статистика, вычисленная для указанного
          параметра как отношение модуля оценки к ее среднеквадратическому отклонению,
          вычисленному по дисперсии параметра модели.
        </p>
        <p>Например, если получена дисперсия оценок параметров модели:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Обозначение</th>
                  <th>Оценка</th>
                  <th>Дисперсия</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>B0</td>
                  <td>-0.891</td>
                  <td>0.032</td>
                </tr>
                <tr>
                  <td>B1</td>
                  <td>-6.647</td>
                  <td>0.032</td>
                </tr>
                <tr>
                  <td>B2</td>
                  <td>70.393</td>
                  <td>0.032</td>
                </tr>
                <tr>
                  <td>B12</td>
                  <td>224.764</td>
                  <td>0.032</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>то для параметра В1	наблюдаемое значение критерия Стьюдента:</p>
        <p>Набл_Ст = 6.647 / 0.18 = 37.16</p>
        <p>Для остальных параметров:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Обозначение</th>
                  <th>Набл_Ст</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>B0</td>
                  <td>4.97</td>
                </tr>
                <tr>
                  <td>B1</td>
                  <td>37.16</td>
                </tr>
                <tr>
                  <td>B2</td>
                  <td>393.51</td>
                </tr>
                <tr>
                  <td>B12</td>
                  <td>1256.47</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Число степеней свободы критерия Стьюдента - число степеней свободы дисперсии воспроизводимости, т.е. следующая величина: </p>
        <p>(m-1) * N.</p>
        <p>В результате проверки значимости устанавливается статистическая значимость или незначимость отличия от нуля оценок параметров полученной модели, т.е. выясняется, обусловлено ли отличие коэффициента от нуля чисто случайными обстоятельствами, влиянием помехи или же это отличие не случайно и вызвано тем, что в теоретической регрессионной модели присутствует соответствующий не равный нулю коэффициент регрессии.</p>
        <p>Проверка значимости оценок коэффициентов производится раздельно для оценки каждого коэффициента. При этом проверка значимости сводится к последовательной проверке гипотез вида:
          <ol start="0">
            <li>“Рассматриваемый коэффициент незначимо отличается от нуля”,</li>
            <li>“Рассматриваемый коэффициент нулю не равен”.</li>
          </ol>
        </p>
        <p>Для проверки этих гипотез используется критерий Стьюдента:<br>
если наблюдаемое значение критерия Стьюдента больше критического значения критерия Стьюдента на выбранном уровне значимости, то нулевая гипотеза должна быть отвергнута; следовательно, отличие рассматриваемой оценки от нуля не случайно, этот коэффициент статистически значим и должен быть сохранен в уравнении регрессии. 
</p>
        <p>В противном случае нулевая гипотеза принимается.</p>
        <p>Например, если наблюдаемое значение критерия Стьюдента для параметров:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Обозначение</th>
                  <th>Набл_Ст</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>B0</td>
                  <td>4.97</td>
                </tr>
                <tr>
                  <td>B1</td>
                  <td>37.16</td>
                </tr>
                <tr>
                  <td>B2</td>
                  <td>393.51</td>
                </tr>
                <tr>
                  <td>B12</td>
                  <td>1256.47</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>а критическое: Крит_Ст(8, 0.05) = 2.306,<br>то гипотезы о незначимости параметров отвергаются на уровне значимости а = 0.05, таким образом, для рассматриваемого примера все параметры значимы.</p>
        <p>С физической точки зрения может существовать несколько причин, по которым коэффициент регрессии при определенной переменной оказывается незначимым:
          <ol>
            <li>переменная действительно не влияет на отклик объекта;</li>
            <li>действие переменной не проявилось на фоне помехи, следовательно имеет смысл изменить интервал варьирования фактора или увеличить число параллельных опытов и попытаться еще раз провести эксперимент.</li>
          </ol>
        </p>
        <p>В случае, если коэффициент регрессии оказался незначимым, и предполагается, что незначимость обусловлена тем, что соответствующая базисная функция не влияет на отклик объекта, его стоит исключить из модели. Но необходимо учитывать, что, если в ортогональных планах оценки параметров некоррелированы, и исключение одного из параметров не требует пересчета всех остальных, то в планах, не обладающих свойством ортогональности, уточнение модели сопряжено с пересчетом всех остающихся параметров, т.к. получаемые оценки взаимозависимы.</p>
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
      significance_answer: "",
      params_index: [],
      params_list: ["B0", "B1", "B2", "B12"],
      params: ["B0", "B1", "B2", "B12"],
      param_1: 0,
      param_2: 0,
      param_answer: "",
      vals: [],
      df: [],
      check_df: 0,
      df_answer: "",
      crit_value: 0,
      prac_values: [],
      param_values: [],
      sign_values: [],
      sign_answer: "",
      sign_wrong: "",
      endpoints: [
        "http://127.0.0.1:5000/api/set/significance_level_student",
        "http://127.0.0.1:5000/api/get/params_for_check", 
        "http://127.0.0.1:5000/api/check/params_for_check", 
        "http://127.0.0.1:5000/api/get/student_table", 
        "http://127.0.0.1:5000/api/check/df_student", 
        "http://127.0.0.1:5000/api/check/sign_param", 
        "http://127.0.0.1:5000/api/get/sign_params"]
    };
  },
  props: {},
  methods: {
    send_significance: function (e) {
      axios
        .post(this.endpoints[0], { data: { significance: this.significance } })
        .then((response) => {
          if (!response.data.error) {
            document.getElementById("send_sign").disabled = true;
            document.getElementById("significance").style.display = "none";
            document.getElementById("param_1").style.display = "block";
            axios
            .get(this.endpoints[1])
            .then((response) => {
              if (!response.data.error) {
                let params = ["B0", "B1", "B2", "B12"];
                this.params = [params[response.data.data.params[0]], params[response.data.data.params[1]]]
                this.params_index = [response.data.data.params[0], response.data.data.params[1]]
              } else {
                this.significance_answer = response.data.message
              }
            })
            .catch((error) => {
              console.log("-----error-------");
              console.log(error);
            });
          } else {
            this.significance_answer = response.data.message
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    display_param_2: function (e) {
            document.getElementById("param_1").style.display = "none";
            document.getElementById("param_2").style.display = "block";
    },
    send_params: function (e) {
      axios
        .post(this.endpoints[2], { data: { 
          first_param: this.param_1, 
          second_param: this.param_2, } })
        .then((response) => {
          if (!response.data.error) {
            document.getElementById("param_1_btn").disabled = true;
            document.getElementById("param_1").style.display = "none";
            document.getElementById("param_2").style.display = "none";
            axios
            .get(this.endpoints[3])
            .then((response) => {
              if (!response.data.error) {
                this.vals = response.data.data.vals;
                this.df = response.data.data.df;
              } else {
                this.param_answer = response.data.message
              }
            })
            .catch((error) => {
              console.log("-----error-------");
              console.log(error);
            });
            document.getElementById("crit_values").style.display = "block";
          } else {
            this.param_answer = response.data.message
            if (response.data.message.indexOf("first_param") != -1){
              document.getElementById("param_1").style.display = "block";
              document.getElementById("param_1_btn").style.display = "none";

            }
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_check_df: function (e) {
      axios
        .post(this.endpoints[4], { data: { 
          df_student: this.check_df,  } })
        .then((response) => {
          if (!response.data.error) {
            this.crit_value = response.data.data.crit_val;
            this.prac_values = response.data.data.prac;
            document.getElementById("crit_values").style.display = "none";
            document.getElementById("sign_1").style.display = "block";
          } else {
            this.df_answer = response.data.message
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    is_sign: function(answer, index) {
      axios
        .get(this.endpoints[6])
        .then((response) => {
          if (!response.data.error) {
            this.param_values = response.data.data.params;
            this.sign_values = response.data.data.is_sign;
            if (answer == this.sign_values[index]){
              this.sign_answer = "Правильно. Оценка параметра значима."
              if (document.getElementById("sign_1").style.display == "block"){
                document.getElementById("sign_1").style.display = "none";
                document.getElementById("sign_2").style.display = "block";
              }
              else if (document.getElementById("sign_2").style.display == "block"){
                document.getElementById("sign_2").style.display = "none";
                document.getElementById("sign_table").style.display = "block";
              }
            }
            else {
              this.sign_answer = "Неправильно."
            }
          } else {
            this.sign_wrong = response.data.message
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
