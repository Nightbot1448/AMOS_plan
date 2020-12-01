<template>
  <div>
    <table class="table table-borderless table-responsive">
      <thead>
        <tr>
          <th scope="col"></th>
          <th scope="col">Координаты центра области</th>
          <th scope="col">Интервалы варьирования</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">Фактор X1</th>
          <td><input type="number" step="0.01" v-model="x1c" id="x1c" /></td>
          <td><input type="number" step="0.01" v-model="x1i" id="x1i" /></td>
        </tr>
        <tr>
          <th scope="row">Фактор X2</th>
          <td><input type="number" step="0.01" v-model="x2c" id="x2c" /></td>
          <td><input type="number" step="0.01" v-model="x2i" id="x2i" /></td>
        </tr>
      </tbody>
    </table>
    <button @click="save_points">Сохранить</button>
    <router-link class="nav-link" to="/planning">Далее</router-link>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  created() {},
  data() {
    return {
      x1c: -10,
      x1i: 20,
      x2c: 0,
      x2i: 10,
    };
  },
  props: {},
  methods: {
    save_points: function (e) {
      this.$store.dispatch("changePAPoints", [
        [x1c.value, x1i.value],
        [x2c.value, x2i.value],
      ]);
    },
  },
};
</script>

<style scoped></style>
