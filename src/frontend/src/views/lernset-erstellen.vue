<template>
  <div id="learning-set-choice-body">
    <div id="learning-set-choice-header">
      <h1>Lernset erstellen</h1>
    </div>

    <div id="learning-set-entry-main">
      <div id="question-type-container" ref="question_type_container">
        <div>
          <label for="quiz_name">Name des Lernsets:</label>
          <input type="text" id="quiz_name" name="quiz_name" class="input-field" ref="quiz_name_input" v-model="learning_set_name"><br>
          
          <div id="module-choice-container">
            <label for="module">Modul: </label>
            <select name="module_choice" id="module-choice" ref="module_choice" @change="moduleChoice">
              <option class="module" v-for="module in modules" :value="module.id">{{ module.name }}</option>
            </select>
          </div>
        </div>
        <br>
        <div id="error-message" ref="error_message_container" v-text="error_message"></div>

        <div id="index-cards-container" class="entry-container" ref="index_cards_entry">
          <KarteikartenErstellen class="entry-view" ref="card_entry_view" @addQuestion="addQuestion" @editQuestion="editQuestion" @error="showErrorMessage"/>
        </div>
        <div id="multiple-choice-container" class="entry-container" ref="multiple_choice_entry">
          <QuizEingabe class="entry-view" ref="quiz_entry_view" @addQuestion="addQuestion" @editQuestion="editQuestion" @error="showErrorMessage"/>
        </div>

        <div id="control-button-container">
          <div><button class="control-button" id="save_card_set" @click="saveLearningSet">Lernset speichern</button></div>
          <div><button class="control-button" id="cancel" @click="showCancelPopup">Abbrechen</button></div>
        </div>
      </div>


      <aside id="aside" ref="aside">
        <div id="choice-container">
          <select name="question_type" id="question_type" ref="question_type" @change="questionTypeChoice">
            <option class="question_type_option" value="index_card">Karteikarte</option>
            <option class="question_type_option" value="multiple_choice">Multiple-choice Frage</option>
          </select>
        </div>
        <br>
        <div id="entered_questions">
          <h3>Eingegebene Fragen:<br></h3>
          <div class="entered_question" v-for="(card, index) in entered_questions" :key="index">
            <div class="question_text" v-text="(index+1) + ': ' + card" @click="provideQuestion(index)"></div>
            <button class="delete_question" @click="deleteQuestion(index)">löschen</button>
          </div>
        </div>
      </aside>

      

      <div id="done-container" ref="done_container">
        <h2>Lernset wurde erfolgreich erstellt</h2>
        <br>
        <RouterLink v-slot="{navigate, isActive}" to="/lernset-waehlen" custom>
          <button class="control-button" @click="navigate" :class="{active: isActive}">Zurück zur Lernset-Übersicht</button>
        </RouterLink>
      </div>
    </div>
    <Popup ref="cancel_popup" @buttonClicked="popupReaction"/>
  </div>
</template>

<style scoped>
@import '@/assets/lernset-erstellen.css';
</style>



<script setup>
import { provide, ref, onMounted } from 'vue';
import KarteikartenErstellen from './karteikarten-erstellen.vue';
import QuizEingabe from './quiz-eingabe.vue';
import Popup from "./popup.vue";


"use strict";



const question_type = ref(null);
const index_cards_entry = ref(null);
const multiple_choice_entry = ref(null);
const card_entry_view = ref(null);
const quiz_entry_view = ref(null);
const question_type_container = ref(null);
const aside = ref(null);
const cancel_popup = ref(null);
const done_container = ref(null);

const module_choice = ref(null);
const modules = ref([])
const learning_set_name = ref('');
const error_message = ref('');

const entered_questions = ref([]);
let question_set = [];


const TYPE_INDEX_CARD = 'index_card';
const TYPE_MULTIPLE_CHOICE = 'multiple_choice';


let edit_index = -1;
let module_id = -1;

const API_LEARNING_SETS = 'http://localhost:8000/api/learning_set/';
const API_MODULES = "http://localhost:8000/api/users/modules/";



onMounted(() => {loadUserModules();});


/**
 * @description Get the user-specific modules and write them into the list of modules.
 * @returns {null}
 */
async function loadUserModules(){
  try {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), 5000);

  const response = await fetch(API_MODULES, {method: "GET", credentials: "include", signal: controller.signal});
  if (!response.ok) {throw new Error(`Response status: ${response.status}`);}

  modules.value = await response.json();
  module_id = modules.value[0].id;
  return null;
  }
  catch (error) {
  console.error(error.message);
  return null;
  }
}



/**
 * @description Set the module_id to the id of the chosen module.
 * @returns {null}
 */
function moduleChoice(){
  module_id = module_choice.value.options[module_choice.value.selectedIndex].value;

  return;
}


/**
 * @description Construct a JSON Object of a learning set.
 * @param {String} name the name of the learning set
 * @returns {JSON} the json Object describing the learning set
 */
function makeLearningSetJson(name){
  let json_str = '{"name": "' + name + '"}'

  let json = JSON.parse(json_str);
  return json;
}


/**
 * @description Post the learning set and all its questions to the backend.
 * @returns {null}
 */
async function saveLearningSet(){
  if(learning_set_name.value === ''){
    showErrorMessage('Name und Modul des Lernsets müssen eingegeben werden!');
    return;
  }
  if(question_set.length === 0){
    showErrorMessage('Es muss midestens eine Frage eingegeben werden!');
    return;
  }
  if(edit_index >= 0){
    showErrorMessage('Eine Frage befindet sich noch in bearbeitung!');
    return;
  }


  let learning_set_json = makeLearningSetJson(learning_set_name.value);

  let data = await postJsonToURL(learning_set_json, API_LEARNING_SETS + '?modul_id=' + module_id);
  let learning_set_id;
  if(data === null){
    console.error('Post learning set failed');
    return;
  }
  else{
    learning_set_id = data.id;
  }

  for(let i = 0; i < question_set.length; i++){
    let json = question_set[i].question;
    let url = question_set[i].url;
    url += '?learning_set_id=' + learning_set_id;

    data = await postJsonToURL(json, url);
    if(data === null){
      console.error('Post question failed');
      return;
    }
  }

  learningSetDone();

  return;
}


/**
 * @description Post a JSON Object to the given url.
 * @param {JSON} json the JSON Object to be posted
 * @param {String} url the URL to post the JSON to
 * @returns {null|JSON} the data from the POST-response
 */
async function postJsonToURL(json, url){
  const json_str = JSON.stringify(json);

  const postHeader = new Headers();
  postHeader.set("accept", "application/json");
  postHeader.set("Content-Type", "application/json");

  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), 5000);

  try {
    const response = await fetch(url, {method: "POST",
                      headers: postHeader,
                      body: json_str,
                      signal: controller.signal,
                      credentials: 'include'});
    if (!response.ok) {throw new Error(`Response status: ${response.status}`);}

    clearTimeout(id);

    const data = await response.json();
    return data;
  }
  catch (error) {
    console.error(error.message);
    return null;
  }
}


/**
 * @description Delete all the questions and the other entries of the learning set.
 * @returns {null}
 */
function deleteLearningSet(){
  hideEntryViews(TYPE_INDEX_CARD);
  editQuestion(question_set[edit_index]);

  for(let i = question_set.length-1; i >= 0; i--){
    deleteQuestion(i);
  }

  learning_set_name.value = "";

  return;
}

/**
 * @description Show a Popup asking weather the learning-set shall be deleted.
 * @returns {null}
 */
function showCancelPopup(){
  let text = 'Achtung, alle Fragen werden gelöscht. Wirklich Abbrechen?';
  let buttons = ['Ja', 'Nein'];
  cancel_popup.value.setTextAndButtons(text, buttons);
  cancel_popup.value.setVisibility(true);
  return;
}
/**
 * @description React to the user input about deleteing the learning-set.
 * @param {Number} button index of the button that was pressed
 * @returns {null}
 */
function popupReaction(button){
  cancel_popup.value.setVisibility(false);

  if(button === 0) deleteLearningSet();
  return;
}


/**
 * @description Indicate that the learning set is created and let the user go to the learning set viewer.
 * @returns {null}
 */
function learningSetDone(){
  question_type_container.value.style.display = 'none';
  aside.value.style.display = 'none';

  done_container.value.style.display = 'inline';
  return;
}



/**
 * @description Hide the entry-views and clear their inputted values.
 * Set one of the Views visible again.
 * @param {String|null} choice if not null determines the view that will be set visible again
 * @returns {null}
 */
function hideEntryViews(view){
  if(!view){
    if(index_cards_entry.value.style.display !== "none") view = TYPE_INDEX_CARD;
    if(multiple_choice_entry.value.style.display !== "none") view = TYPE_MULTIPLE_CHOICE;
  }
  

  index_cards_entry.value.style.display = "none";
  multiple_choice_entry.value.style.display = "none";

  card_entry_view.value.clearQuestion();
  quiz_entry_view.value.clearQuestion();

  if(view === TYPE_INDEX_CARD){
    index_cards_entry.value.style.display = "inline";
    question_type.value.value = TYPE_INDEX_CARD;
  }
  if(view === TYPE_MULTIPLE_CHOICE){
    multiple_choice_entry.value.style.display = "inline";
    question_type.value.value = TYPE_MULTIPLE_CHOICE;
  }

  return;
}


/**
 * @description Set only the chosen entry-view visible.
 * @returns {null}
 */
function questionTypeChoice(){
  let choice = question_type.value.options[question_type.value.selectedIndex].value;

  hideEntryViews(choice);

  return;
}


/**
 * @description Save all the important information about a question into the list of entered questions.
 * @param {JSON} json Object, which contains the Question, the question-type, the JSON to be sent to the Backend and the URL it will be sent to
 * @returns {null}
 */
function addQuestion(json){

  entered_questions.value.push(json.question_text);
  question_set.push(json);

  return;
}
/**
 * @description Change an existing question to the provided JSON.
 * @param {JSON} json Object, which contains the Question, the question-type, the JSON to be sent to the Backend and the URL it will be sent to
 * @returns {null}
 */
function editQuestion(json){
  let index = edit_index;
  if(index >= 0 && index < question_set.length){

    entered_questions.value[index] = json.question_text;
    question_set[index] = json;
  }
  edit_index = -1;

  return;
}


/**
 * @description Provide an entry-view with the question to be edited.
 * @param {Number} index the index of the question to be edited
 * @returns {null}
 */
function provideQuestion(index){

  let edit_question = question_set[index];
  edit_index = index;

  hideEntryViews(edit_question.question_type);

  if(edit_question.question_type === TYPE_INDEX_CARD){
    card_entry_view.value.editQuestion(edit_question);
  }
  if(edit_question.question_type === TYPE_MULTIPLE_CHOICE){
    quiz_entry_view.value.editQuestion(edit_question);
  }
  return;
}


function showErrorMessage(message){
  error_message.value = message;
  setTimeout(() => hideErrorMessage(), 5000);
  return;
}
function hideErrorMessage(){
  error_message.value = '';
  return;
}


/**
 * @description Delete a question from the entered questions.
 * @param {Number} index the index of the question to be deleted
 * @returns {null}
 */
function deleteQuestion(index){
  
  if(edit_index === index) hideEntryViews(question_set[index].question_type);
  spliceQuestionFromArrays(index);
  if(edit_index > index) edit_index--;

  return;
}

/**
 * @description Delete a question from the lists it appears in.
 * @param {Number} index the index of the question to be deleted
 * @returns {null}
 */
function spliceQuestionFromArrays(index){
  question_set.splice(index, 1);
  entered_questions.value.splice(index, 1);
  return;
}

</script>