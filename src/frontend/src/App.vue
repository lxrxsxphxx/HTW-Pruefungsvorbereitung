<script setup>
import Footer from './components/Footer.vue'
import Header from './components/Header.vue'


import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <Header/>    
    <RouterView />
    <Footer />
  </div>
</template>

<style>

.app-container {
  height: 100vh;   
  width: 100vw;      
  margin: 0;
  background-color: #fcecd8;
  display: flex;
  flex-direction: column;
}




</style>