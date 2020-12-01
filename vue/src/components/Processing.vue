<template>
  <div>
    <p>
      <label for="variant">Номер варианта задания</label>
      <input id="variant" v-model="variant" type="number" name="variant" />
      <button @click="save_variant">Сохранить</button>
    </p>
    <router-link class="nav-link" to="/planning_area">Далее</router-link>
  </div>
</template>

<script>
export default {
  created() {},
  data() {
    return {
      variant: 2,
      help: null,
    };
  },
  props: {},
  methods: {
    save_variant: function (e) {
      this.$store.dispatch("changeVariant", this.variant);
    },
  },
};
</script>

<style scoped></style>
