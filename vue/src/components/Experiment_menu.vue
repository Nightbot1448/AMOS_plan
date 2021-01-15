<template>
  <div>
    <div>
      <b-list-group>
        <b-list-group-item to="/experiment">Основной эксперимент</b-list-group-item>
        <b-list-group-item to="/addexp"
          >Дополнительный эксперимент
        </b-list-group-item>
      </b-list-group>
    </div>
    <div class="documentation">
      <b-card bg-variant="info"> </b-card>
    </div>
  </div>
</template>

<script>
export default {
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {},
};
</script>

<style scoped></style>
