<template>
    <footer class="footer">
        <a>Über uns</a>
    </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 5%;
  background-color: var(--htw-orange);
  text-align: center;
  padding: 3px 0;
  
}

.footer a {
  color: white;
  font-size: 20px;
  font-family: 'Poppins', sans-serif;
}
</style>