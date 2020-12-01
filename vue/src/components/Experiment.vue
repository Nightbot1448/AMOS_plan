<template>
  <div>
    <div v-for="(experiment, index) in experiments_data" :key="index">
      <h3>Опыт {{ index + 1 }}</h3>
      <p>
        <input type="number" v-model="experiments_data[index][0]" />
        <input type="number" v-model="experiments_data[index][1]" />
        <input type="number" v-model="experiments_data[index][1]" />
      </p>
    </div>
    <button @click="save_points">Сохранить</button>
    <router-link class="nav-link" to="/planning">Далее</router-link>
  </div>
</template>

<script>
/* нужно переделать с учетом того, что опыты нужно производить по одному */
export default {
  created() {},
  data() {
    return {
      experiments_data: [
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      result_data: [],
    };
  },
  props: {},
  methods: {
    save_points: function (e) {
      this.$store.dispatch("changeExpData", this.experiments_data);
    },
  },
};
</script>

<style scoped></style>
