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
              <b-button
                id="check_num_points"
                class="mt-2"
                @click="send_number_of_points"
                variant="primary"
              >
                <div class="d-flex justify-content-center">
                  <b-spinner small id="spinner_check" style="display: none"></b-spinner>
                </div>
                Проверить</b-button
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
              <b-button id="set_data" @click="send_plan_points" variant="primary"
                >Сохранить</b-button
              >
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
          <div class="mb-5 mt-5">
            <b-button variant="secondary" to="/experiment">Далее</b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
        <p>
          Количество точек спектра плана ПФЭ - количество различных точек плана, число
          которых для ПФЭ определяется числом возможных комбинаций факторов, каждый из
          которых варьируется на двух уровнях<br />
          См. пример построения спектра плана ПФ3.
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
        <p>Пример записи матрицы спектра плана:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка плана</th>
                  <th>Х1</th>
                  <th>Х2</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>-1</td>
                  <td>-1</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>+1</td>
                  <td>-1</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>-1</td>
                  <td>+1</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>+1</td>
                  <td>+1</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
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
            document.getElementById("check_num_points").disabled = true;
            document.getElementById("spinner_check").style.display = "block";
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
            document.getElementById("set_data").disabled = true;
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
