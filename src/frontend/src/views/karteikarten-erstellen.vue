<template>
  <div id="index-cards-entry-body">
    <div id="index-cards-entry-header">
      <hr>
    </div>

    <div id="index-cards-entry-main">
      <div id="input">
        <div id="input-container">
          <div id="front-container">
            <textarea type="text" id="front" name="front" class="input-field" ref="front_input" v-model="front" placeholder="Vorderseite"></textarea><br>
          </div>
          

          <div id="back-container" class="answer-container">
            <textarea type="text" id="back" name="back" class="input-field" ref="back_input" v-model="back" placeholder="Rückseite"></textarea><br>
          </div>
          <br>
        </div>

        <div id="control-button-container">
          <button class="control-button" id="add_card" v-text="add_text" @click="addQuestion"></button>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
@import '@/assets/karteikarten-erstellen.css';
</style>



<script setup>

import { defineExpose, ref } from 'vue';



const emit = defineEmits(['addQuestion', 'editQuestion', 'error']);

defineExpose({editQuestion, clearQuestion});


let front = ref('');
let back = ref('');

const ADD_QUESTION_TEXT = 'Frage hinzufügen';
const EDIT_QUESTION_TEXT = 'Übernehmen';
let add_text = ref(ADD_QUESTION_TEXT);

let front_input = ref(null);


const url = `${import.meta.env.VITE_API_URL}/cards/`;


const ADD_QUESTION = 0;
const EDIT_QUESTION = 1;
let action = ADD_QUESTION;


/**
 * @description Change the Action performed by the *add_card* button as well as its text.
 * @param {Number} a action to change to (can be *ADD_QUESTION* or *EDIT_QUESTION*)
 * @returns {null}
 */
function setAction(a){
  if(a === ADD_QUESTION){
    action = ADD_QUESTION;
    add_text.value = ADD_QUESTION_TEXT;
  }
  else if(a === EDIT_QUESTION){
    action = EDIT_QUESTION;
    add_text.value = EDIT_QUESTION_TEXT;
  }
  return;
}


/**
 * @description Read the inputted values for the front and back of the card and transfer the card to the parent-view.
 * @returns {null}
 */
function addQuestion(){
  if(front.value === "" || back.value === ""){
    emit('error', 'Vorder- und Rückseite müssen eingegeben werden!');
    return;
  }
  
  // transfer the card to the parent view and clean up
  transferCard(front.value, back.value);

  clearQuestion();
  if(action === EDIT_QUESTION) setAction(ADD_QUESTION);

  front_input.value.focus();

  return;
}


/**
 * @description This fuction takes an existing card and sets it up to be edited.
 * It writes the card-parameters into the corresponding input-fields and sets the the action to be *EDIT_QUESTION*.
 * @param {JSON} json The JSON Object which contains all the important information of the question.
 * This information includes the card with all the card-parameters, the URL the question will be sent to and the type of question (index_card).
 * @returns {null}
 */
function editQuestion(json){
  let card = json.question[0];

  setAction(EDIT_QUESTION);
  front.value = card.front;
  back.value = card.back;

  return;
}


/**
 * @description Transfer a question to the parent-view in the JSON-format via an emitted event.
 * @param {String} front_text the question (front of the card)
 * @param {String} back_text the text on the back of the card
 * @returns {null}
 */
function transferCard(front_text, back_text){
  let json = makeJson(front_text, back_text);

  if(action === ADD_QUESTION) emit('addQuestion', json);
  else if(action === EDIT_QUESTION) emit('editQuestion', json);

  return;
}


/**
 * @description Construct a JSON Object which contains all the important information of the entered card.
 * This information includes the question with all the card-parameters, the URL the card will be sent to and the type of question (index_card).
 * @param {String} front_text the question (front of the card)
 * @param {String} back_text the text on the back of the card
 * @returns {JSON} the json Object
 */
function makeJson(front_text, back_text){
  let json_str = '{"question_text": "' + front_text + '", ';
  json_str += '"url": "' + url + '", ';
  json_str += '"question_type": "index_card", ';

  json_str += '"question": [{"front": "' + front_text + '", "back": "' + back_text + '"}]}';

  let json = JSON.parse(json_str);

  return json;
}


/**
 * @description Clear all inputs and reset the action to the standard action (add question).
 * @returns {null}
 */
function clearQuestion(){
  front.value = "";
  back.value = "";

  setAction(ADD_QUESTION);
  return;
}

</script>