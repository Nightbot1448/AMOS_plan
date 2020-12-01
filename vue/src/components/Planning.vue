<template>
  <div>
    <p>
      <label for="number_of_points">Количество точек в спектре плана</label>
      <input id="number_of_points" type="number" v-model="number_of_points" />
    </p>
    <table class="table table-borderless table-responsive">
      <thead>
        <tr>
          <th scope="col"></th>
          <th scope="col">Значения Х1</th>
          <th scope="col">Значения Х2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">Точка 1</th>
          <td><input type="number" step="0.01" id="x1" v-model="points[0][0]" /></td>
          <td><input type="number" step="0.01" id="y1" v-model="points[0][1]" /></td>
        </tr>
        <tr>
          <th scope="row">Точка 2</th>
          <td><input type="number" step="0.01" id="x2" v-model="points[1][0]" /></td>
          <td><input type="number" step="0.01" id="y2" v-model="points[1][1]" /></td>
        </tr>
        <tr>
          <th scope="row">Точка 3</th>
          <td><input type="number" step="0.01" id="x3" v-model="points[2][0]" /></td>
          <td><input type="number" step="0.01" id="y3" v-model="points[2][1]" /></td>
        </tr>
        <tr>
          <th scope="row">Точка 4</th>
          <td><input type="number" step="0.01" id="x4" v-model="points[3][0]" /></td>
          <td><input type="number" step="0.01" id="y4" v-model="points[3][1]" /></td>
        </tr>
      </tbody>
    </table>
    <p>
      <label for="number_of_experiments">Количество параллельных опытов (не более 5)</label>
      <input id="number_of_experiments" type="number" name="number_of_experiments" v-model="number_of_experiments" />
    </p>
    <p>
      <button @click="save_points">Сохранить</button>
    </p>
  </div>
</template>

<script>
export default {
  created() {},
  data() {
    return {
      number_of_points: 4,
      points: [
        [1, 1],
        [-1, 1],
        [1, -1],
        [-1, -1],
      ],
      number_of_experiments: 5,
      randomization: false,
    };
  },
  props: {},
  methods: {
    save_points: function (e) {
      this.$store.dispatch("changePPoints", [
        [this.points[0][0], this.points[0][1]],
        [this.points[1][0], this.points[1][1]],
        [this.points[2][0], this.points[2][1]],
        [this.points[3][0], this.points[3][1]],
      ]);
      this.$store.dispatch("changePPointsLen", this.number_of_points);
      this.$store.dispatch("changeNExperiments", this.number_of_experiments);
    },
  },
};
</script>

<style scoped></style>
