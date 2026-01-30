<template>
  <div id="mc-quiz-body">
    <div id="mc-quiz-header">
    <h1>Quiz lösen</h1>
    </div>

    <div id="mc-quiz-main">
      <div id="middle">
        
        <div id="progress-bar-container">
          <p id="progress-text">{{ progress_percent }}</p>
          <div id="progress-bar">
            <div id="progress" :style="{ width: progress_percent }"></div>
          </div>
        </div>
        <div id="question-container" v-show="!STATISTIC_SHOWN">
          <p id="task_info">{{ task_info }}</p>
          <p>Frage:</p>
          <p id="question">{{ question_text }}</p> <br/><br/>

          <div class="answer-container" id="answer-buttons">
            <button v-for="(answer, index) in answers" :key="index" :ref="el => { if (el) answer_buttons[index] = el }" class="answer-button" @click="answerChoice(answer, index)">{{ answer.answer }}</button>
          </div>
        </div>
        <div id="statistic" v-show="STATISTIC_SHOWN">
          <div v-for="(text, index) in statistic" :key="index" v-text="text"></div>
          <br/>
          <div>Richtig beantwortet: ✅<br/></div>
          <div>Falsch beantwortet: ❌<br/></div>
          <div>Nicht beantwortet: 🚫<br/></div>
        </div>

        <button id="new-task-button" @click="newTask">{{ new_task }}</button>
      </div>
      <RouterLink :to="'/lernen/' + route.params.learningSetId">
        <button class="control-button" id="cancel-quiz-button">{{ cancel_quiz }}</button>
      </RouterLink>
    </div>
  </div>
</template>





<script setup>

import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

"use strict";


const URL = `${import.meta.env.VITE_API_URL}/questions`;
const route = useRoute();


const keys = ref([]);

const progress_percent = ref("0%");
const task_info = ref("...");
const question_text = ref('');
const answers = ref([]);
const new_task = ref("Neue Frage");
const cancel_quiz = ref("Quiz abbrechen");
const statistic = ref([]);

const answer_buttons = ref([]);

let evaluated = false;
let STATISTIC_SHOWN = false;
let BLOCK_NEW_TASK = false;

let task_set;
let current_task_nr = 0;
let statistic_data = [];

let chosen_answers = [];
let chosen_answers_indices = [];

let color;



const ACTION_NEW_QUESTION = 0;
const ACTION_CHECK_ANSWERS = 1;
const ACTION_SHOW_STATISTIC = 2;
const ACTION_QUIZ_DONE = 3;
let action = ACTION_NEW_QUESTION;

let end_of_quiz = false;




const EVAL_SKIP = -1;
const EVAL_SUCC = 1;
const EVAL_FAIL = 0;


onMounted(() => {start();});


/**
 * @description Get the multiple-choice-questions of the learning-set defined by the learning-set-id in the url.
 * @returns {JSON|null} A JSON Object containing all questions and their answers.
 */
async function getQuestions(){
  let url = URL + `?learning_set_id=${route.params.learningSetId}`;

  try {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(url, {method: "GET", credentials: 'include', signal: controller.signal});
    if (!response.ok) {throw new Error(`Response status: ${response.status}`);}

    const questions = await response.json();
    return questions;
  }
  catch (error) {
    console.error(error.message);
    alert("Fehler beim laden der Fragen!");
    return null;
  }
}


/**
 * @description Load the questions for the chosen learning-set and randomize them, initialize the statistic and show the first question.
 * @returns {null}
 */
async function start(){
  end_of_quiz = false;
  task_info.value = "...";
  setAction(ACTION_NEW_QUESTION);

  let data = await getQuestions();

  if(data !== null){
    keys.value = Object.keys(data);
  }
  
  task_set = data.sort((a, b) => 0.5 - Math.random());
  current_task_nr = 0;

  for(let i = 0; i < task_set.length; i++){
    statistic_data.push("🚫");
  }
  
  showTask(task_set[current_task_nr], current_task_nr + 1);

  resetProgress(0);
  return;
}



/**
 * @description Load the next question from the list of questions.
 * @returns {null}
 */
function getNewTask(){
  if(task_set){
    current_task_nr++;
    if(task_set[current_task_nr]){
      showTask(task_set[current_task_nr], current_task_nr + 1);
    }
    else current_task_nr--;
  }
  return;
}



/**
 * @description Select or deselect an answer by adding it to / splicing it from a list of selected answers.
 * @param {JSON} answer the answer as a JSON Object
 * @param {Number} index the index of the answer in the list of answer-buttons
 * @returns {null}
 */
function answerChoice(answer, index){
  if(evaluated) return;

  let index_in_arr = chosen_answers.indexOf(answer);

  const button = answer_buttons.value[index];

  if(index_in_arr !== -1){
    chosen_answers.splice(index_in_arr, 1);
    chosen_answers_indices.splice(index_in_arr, 1);
    button.style.borderColor = "#0000";
  }
  else{
    chosen_answers.push(answer);
    chosen_answers_indices.push(index);
    button.style.borderColor = "var(--htw-orange)";
  }

  if(chosen_answers.length > 0){  // One or more answers chosen
    setAction(ACTION_CHECK_ANSWERS);
  }
  else{                           // no answers chosen
    if(end_of_quiz) setAction(ACTION_SHOW_STATISTIC);
    else setAction(ACTION_NEW_QUESTION);
  }
  return;
}


/**
 * @description Evaluate the list of chosen answers and deternine whether it is correct.
 * 
 * The question was skipped if the list is empty.
 * 
 * The question was answered correctly if all answers in the list are correct and all correct answers are in the list.
 * 
 * Otherwise the questions was not answered correctly.
 * @returns {Number} the correctness of the answer (-1: skip, 0: incorrect, 1: correct)
 */
function evaluate(){
  evaluated = true;

  let success = EVAL_SKIP;

  color = answer_buttons.value[0].style.backgroundColor;

  if(chosen_answers.length > 0){
    success = EVAL_SUCC;

    for(let answer_nr = 0; answer_nr < answers.value.length; answer_nr++){
      const button = answer_buttons.value[answer_nr];

      if(chosen_answers.includes(answers.value[answer_nr])){
        if(answers.value[answer_nr].correct){
          button.style.backgroundColor = "#00c000";
        }
        else{
          success = EVAL_FAIL;
          button.style.backgroundColor = "#e00000";
        }
      }
      else{
        if(answers.value[answer_nr].correct){
          success = EVAL_FAIL;
          button.style.backgroundColor = "#00c000";
        }
      }
    }
  }

  chosen_answers = [];
  chosen_answers_indices = [];

  if(success == EVAL_SUCC) task_info.value = "Richtig!";
  else task_info.value = "Falsch!";
  
  updateProgress(success);

  return success;
}


function resetProgress(){
  progress_percent.value = "0%";
}


/**
 * @description Update the progress and the statistic depending on the correctness of the answered question.
 * @param {Number} success the correctness of the answer (-1: skip, 0: incorrect, 1: correct)
 * @returns {null}
 */
function updateProgress(success){
  if(success == EVAL_SUCC){
    statistic_data[current_task_nr] = "✅";
  } else if(success == EVAL_FAIL){
    statistic_data[current_task_nr] = "❌";
  }

  let width = (current_task_nr+1) / task_set.length * 100;
  progress_percent.value = parseFloat(width).toFixed(0)  + "%";
  return;
}



/**
 * @description Set the action performed by the `new-task-button`
 * @param {Number} a the action to set to
 * @returns {null}
 */
function setAction(a){
  if(a === ACTION_NEW_QUESTION){
    action = ACTION_NEW_QUESTION;
    new_task.value  = "Neue Frage";
    cancel_quiz.value = "Quiz abbrechen";
  }
  if(a === ACTION_CHECK_ANSWERS){
    action = ACTION_CHECK_ANSWERS;
    new_task.value  = "Auflösen";
    cancel_quiz.value = "Quiz abbrechen";
  }
  if(a === ACTION_SHOW_STATISTIC){
    action = ACTION_SHOW_STATISTIC;
    new_task.value  = "Übersicht";
    cancel_quiz.value = "Quiz abbrechen";
  }
  if(a === ACTION_QUIZ_DONE){
    action = ACTION_QUIZ_DONE;
    new_task.value  = "Neue Runde";
    cancel_quiz.value = "Zurück zum Lernset";
  }
  return;
}


/**
 * @description Show a question.
 * @param {JSON} task the question to be shown
 * @param {Number} nr the number of the question
 * @returns {null}
 */
function showTask(task, nr){
  task_info.value = "Frage " + nr;

  question_text.value = task.question;
  answers.value = task.answers.sort((a, b) => 0.5 - Math.random());

  evaluated = false;

  if(!task_set[current_task_nr + 1]){ // Current task is last task in set
    end_of_quiz = true;
    setAction(ACTION_SHOW_STATISTIC);
  }
  return;
}




/**
 * @description Perform the action defined by the value of `action`.
 * 
 * `action = ACTION_CHECK_ANSWERS`: evaluate the list of chosen answers.
 * 
 * `action = ACTION_NEW_QUESTION`: show the next question.
 * 
 * `action = ACTION_SHOW_STATISTIC`: show the statistic at the ent of the quiz.
 * 
 * `action = ACTION_QUIZ_DONE`: start the quiz again.
 * @returns {null}
 */
function newTask(){
  if(action === ACTION_CHECK_ANSWERS){
    evaluate();

    if(end_of_quiz) setAction(ACTION_SHOW_STATISTIC);
    else setAction(ACTION_NEW_QUESTION);
  }
  else {
    for(let i = 0; i < answer_buttons.value.length; i++){
      const button = answer_buttons.value[i]
      button.style.backgroundColor = color;
      button.style.borderColor = "#0000";
    }

    if(BLOCK_NEW_TASK) return;
    if(action === ACTION_NEW_QUESTION){
      STATISTIC_SHOWN = false;
      if(evaluated){
        evaluated = false;
      }
      updateProgress(-1);

      getNewTask();
    }
    else if(action === ACTION_SHOW_STATISTIC){
      setAction(ACTION_QUIZ_DONE);

      updateProgress(-1);
      showStatistic();
    }
    else if(action === ACTION_QUIZ_DONE){
      setAction(ACTION_NEW_QUESTION);

      STATISTIC_SHOWN = false;

      updateProgress(0);

      answers.value = [];
      question_text.value = "...";

      statistic.value = [];
      statistic_data = [];


      start();
    }
  }
  return;
}



/**
 * @description Show the statistic by showing a checkmark for korrect answers, an X for wrong answers and a prohibition sign for skipped answers.
 * @returns {null}
 */
function showStatistic(){

  STATISTIC_SHOWN = true;

  statistic.value = [];

  for(let i = 0; i < task_set.length; i++){
    let text = String(task_set[i].question);
    text = text.replaceAll("<br/>", ", ");

    statistic.value.push((i + 1) + ": " + statistic_data[i] + " " + text);
  }

  return;
}
</script>


<style scoped>
@import '@/assets/quiz-loesen.css';
</style>