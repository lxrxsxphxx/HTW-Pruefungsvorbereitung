<template>
  <div v-show="visible">
    <div id="main">
      <p v-text="text"></p>
      <div id="button-container">
        <button class="button" ref="displayed_buttons" v-for="(desc, index) in buttons" :key="index" @click="buttonClicked(index)" v-text="desc"></button>
      </div>
    </div>
  </div>
</template>


<script setup>

import {defineExpose, ref } from 'vue';

const emit = defineEmits(['buttonClicked']);
defineExpose({setTextAndButtons, setVisibility});


let visible = ref(false);

let text = ref('');
let buttons = ref([]);

/**
 * @description Set the text and Buttons to the provided values.
 * @param {String} new_text The text to be shown at the top of the popup.
 * @param {Array[String]} new_buttons The Strings to be shown in the buttons.
 * @returns {null}
 */
function setTextAndButtons(new_text, new_buttons){
  text = new_text;
  buttons = new_buttons;
  return;
}
function setVisibility(visibility){
  visible.value = visibility;
  return;
}

function buttonClicked(index){
  emit('buttonClicked', index);
  return;
}

</script>

<style scoped>

#main {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--color-background-soft);
  border: 2px solid var(--color-border-hover);
  text-align: center;
  padding: 0.5em;
  border-radius: 0.5em;
}
p {
  margin: 1em;
  max-width: 16em;
}
#button-container {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.button{
  flex: 1 1 0;
  width: 100%;
  font-size: 1em;
  border: none;
  border-radius: 0.25em;
  white-space: nowrap;
  margin-top: 1em;
  cursor: pointer;
}


</style>