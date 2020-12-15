<template>
  <div>
    <p>
      <label for="variant">Номер варианта задания</label>
      <select id="variant" v-model.number="variant" type="number">
        <option v-for="(n, index) in 6" :key="index">{{ index + 1 }}</option>
      </select>
      <button @click="send_variant">Сохранить</button>
    </p>
    <router-link class="nav-link" to="/planning_area">Далее</router-link>
    <div class="documentation">
      <b-card bg-variant="info">
      <p>
        Уточните по списку существующих переменных, сколько параметром должно присутствовать в модели объекта.
      </p>
      <p>
        Для вычисления оценок параметров модели используется метод наименьших квадратов (МНК)
Исходными данными для вычисления являются:
<ol>
<li>матрица спектра плана</li>
<li>средние значения отклика в эксперименте, записанные в виде вектора, номера строк которого соответствуют номерам точек плана</li>
<li>матрица численных значений базисных функций</li>
</ol>
      </p>
      <p>
        Оценивается вектор параметров модели, номера строк этого вектора - порядковые номера базисных функций ( имеется в виду тот порядок, в котором базисные функции воли в матрицу численных значений базисных функций
      </p>
      <p>
        Поскольку результаты измерения отклика сопровождается случайными ошибками, оценки параметров модели будут случайными величинами.
      </p>
      <p>
        При использовании МНК неизвестный вектор коэффициентов находится из условия минимизации суммы квадратов отклонений измеренных значений отклика от от получаемых по модели.
      </p>
      <p>
        Например, пусть требуется оценить параметры модели для объекта со следующим списком существенных переменных:<br> 1, X1, X2, X1*X2<br>
      </p>
      <p>
        Дана матрица спектра плана: ПФЭ, n=2, m=4. 
      </p>
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
                  <td>+1</td>
                  <td>+1</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-1</td>
                  <td>+1</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>+1</td>
                  <td>-1</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>-1</td>
                  <td>-1</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
      <p>
        Известно, что в результате проведения эксперимента получены средние значения отклика:
      </p>
      <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка ФП</th>
                  <th>Среднее значение</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>287.62</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-148.62</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>-302.70</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>160.13</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
      <p>
        Построим матрицу численных значений базисных функций:
      </p>
      <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <td rowspan="2">Точка плана</td>
                  <td colspan="3">Сущ. переменные</td>
                </tr>
                <tr>
                  <td>X1</td>
                  <td>X2</td>
                  <td>X1*X2</td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>+1</td>
                  <td>+1</td>
                  <td>+1</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-1</td>
                  <td>+1</td>
                  <td>-1</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>+1</td>
                  <td>-1</td>
                  <td>-1</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>-1</td>
                  <td>-1</td>
                  <td>+1</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
      <p>
        Тогда расчет параметров модели будет проводиться так:<br>
В0 = (287.62 + (-148.62) + (-302.70) + 160. 13) / 4 = -0.891<br>
B1 = (1×287.62 + (-1)*(-148.62) + 1*(-302.70) + (-1)*160.13) / 4 = -6.647<br>
B2 = (1*287.62 + 1×(-148.62) + (-1)*(-302.70) + (-1)*160.13) / 4 = 70.393<br>
B12 = (1*287.62 + (-1)*(-148.62) + (-1)*(-302.70) + 1*160.13) / 4 = 224. 764<br>
      </p>
      <p>Это получены параметры для нормированной модели:<br>
у = -0.891 -6.647 * ((X1 - 1)/ 9) + 70.393*((X2 - 0)/ 20.0) + 225. 764 ( ((X1 - 1)/9)*((X2 - 0)/ 20.0),
</p>
<p>где область планирования определена следующим образом.</p>
<b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <td>Факторы</td>
                  <td>X1</td>
                  <td>X2</td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Основной уровень</td>
                  <td>1</td>
                  <td>0</td>
                </tr>
                <tr>
                  <td>Интервал варьирования</td>
                  <td>9</td>
                  <td>20</td>
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
      variant: 2,
      help: null,
      endpoint: "http://127.0.0.1:5000/api/check/task",
    };
  },
  props: {},
  methods: {
    save_variant: function (e) {
      this.$store.dispatch("changeVariant", this.variant);
    },
    send_variant: function (e) {
      axios
        .get(this.endpoint, { params: { task_id: this.variant } })
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
