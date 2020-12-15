<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
            <div id="set_points_number">
              <label for="number_of_points"
                >Сколько точек должно быть в спектре плана?</label
              >
              <b-form-input
                id="number_of_points"
                type="number"
                v-model.number="number_of_points"
              />
              <b-button class="mt-2" @click="send_number_of_points" variant="primary"
                >Проверить</b-button
              >
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
                    <td>
                      <b-form-input
                        type="number"
                        step="0.01"
                        v-model.number="points[index][0]"
                      />
                    </td>
                    <td>
                      <b-form-input
                        type="number"
                        step="0.01"
                        v-model.number="points[index][1]"
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
              <p>
                <label>Количество параллельных экспериментов (не более 5)</label>
                <b-form-input type="number" v-model.number="experiments_number" />
              </p>
              <b-button @click="send_plan_points" variant="primary">Сохранить</b-button>
            </div>
          </b-card>
          <b-alert class="mt-2" variant="success" :show="answer ? true : false">{{
            answer
          }}</b-alert>
          <b-alert class="mt-2" variant="danger" :show="error ? true : false">{{
            error
          }}</b-alert>
          <b-alert class="mt-2" variant="success" :show="answer2 ? true : false">{{
            answer2
          }}</b-alert>
          <b-alert class="mt-2" variant="danger" :show="error2 ? true : false">{{
            error2
          }}</b-alert>
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
        <p>
          План эксперимента - совокупность данных, определяющих число, условия и порядок
          реализации опытов в ходе эксперимента - совокупность всех точек плана.
        </p>
        <p>
          Результатом планирования эксперимента является построение спектра плана
          эксперимента выбранного типа, определение количества опытов в каждой точке плана
          и задание порядка проведения опытов.
        </p>
        <p>
          Вектор, компонентами которого являются упорядоченные численные значения основных
          уровней факторов, задает точку, являющуюся центром области планирования, в
          окрестности которой и располагаются все точки плана.
        </p>
        <p>
          Спектр плана - совокупность несовпадающих точек плана. Обычно записывается в
          стандартной форме - в виде матрицы спектра плана, представляющей собой таблицу,
          строки которой отвечают точкам факторного пространства, включенным в план, а
          столбцы факторам объекта. Т.е. любой элемент матрицы спектра плана - это
          численное значение фактора с номером, соответствующим номеру текущего столбца, в
          точке плана с номером текущей строки.
        </p>
        <p>
          Число точек спектра плана обозначается N. Как правило, матрица спектра плана
          записывается для нормализованных факторов.
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
      endpoints: [
        "http://127.0.0.1:5000/api/check/plan_points_number",
        "http://127.0.0.1:5000/api/check/plan_points_and_number_experiment",
      ],
      answer: "",
      error: "",
      answer2: "",
      error2: "",
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
            this.answer = "Количество точек в спектре плана указано верно.";
            setTimeout(function (e) {
              document.getElementById("set_points_number").style.display = "none";
              document.getElementById("set_points").style.display = "block";
            }, 2000);
          } else this.error = response.data.message;
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
          } else this.error2 = response.data.message;
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
