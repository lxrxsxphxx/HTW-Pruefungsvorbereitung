<template>
  <div class="lernset-card">
    <span class="text">{{ title }}</span>
     <!-- {{ title }}   -->
  </div>
</template>

<script>
export default {
  name: "LernsetCard",
  props: {
    title: {
      type: String,
      required: true
    }
  }
};
</script>

<style scoped>
.lernset-card {
  margin: 0.5em 0.2rem ;
  border: 0.2rem solid #797171;
  border-radius: 0.5rem;
  padding: 0.2rem;
  width: 6rem;
  height: 6rem;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  background-color: white;
  cursor: pointer;
  box-sizing: border-box;     /* WICHTIG */
  transition: transform 0.15s ease, box-shadow 0.15s ease;

  word-wrap: break-word;
  text-align: center;
}

.lernset-card:hover {
  transform: scale(1.015);
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

.text {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
  line-clamp: 4;  /* ??? */ 
  overflow: hidden;
  width: 100%;
}

</style>
