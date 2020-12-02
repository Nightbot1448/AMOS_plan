<template>
  <div>
    <p>
      <label for="variant">Номер варианта задания</label>
      <input id="variant" v-model="variant" type="number" name="variant" />
      <button @click="send_variant">Сохранить</button>
    </p>
    <router-link class="nav-link" to="/planning_area">Далее</router-link>
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
      endpoint: "localhost:5000/check/task",
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
        .then((response) => {
          console.log(response.message);
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
