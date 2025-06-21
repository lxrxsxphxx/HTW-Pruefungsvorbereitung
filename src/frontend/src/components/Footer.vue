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
  background-color: #f99b20;
  text-align: center;
  padding: 10px 0;
}

.footer a {
  color: white;
  font-size: 20px;
  font-family: 'Poppins', sans-serif;
}
</style>