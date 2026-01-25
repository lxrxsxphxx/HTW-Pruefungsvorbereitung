<template>
    <div id="mc-quiz-body">
        <div id="mc-quiz-header">
            <h1>Quiz lösen</h1>
            <!--hr-->
        </div>

        <div id="mc-quiz-main">
            <div id="middle">
                <button class="control-button" id="cancel-quiz-button" @click="cancelQuiz">{{ cancel_quiz }}</button>
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
        </div>
    </div>
</template>





<script setup>

import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

"use strict";


const URL = "http://localhost:8000/api/questions";
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



async function getQuestions(){
    let url
    if(id) url = URL + `?learning_set_id=${route.params.learningSetId}`;

    // {"question":{"question": "Welcher ist der am weitesten von der Sonne entfernte Planet im Sonnensystem?"}, "answers": [{"answer": "Basketball", "correct": true}, {"answer": "Pluto", "correct": false}]}
    // {"question":{"question": "Was ist 1 + 1?"}, "answers": [{"answer": "11", "correct": true}, {"answer": "2", "correct": false}]}


    try {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), 5000);

        const response = await fetch(url, {method: "GET", signal: controller.signal});
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



async function start(){
    end_of_quiz = false;
    task_info.value = "...";
    setAction(ACTION_NEW_QUESTION);

    let data = await getQuestions();
    // console.log(data);

    if(data !== null){
        keys.value = Object.keys(data);
        // console.log("Keys: " + keys.value);
    }
    
    task_set = data.sort((a, b) => 0.5 - Math.random());
    // console.log(task_set);
    current_task_nr = 0;

    for(let i = 0; i < task_set.length; i++){
        statistic_data.push("🚫");
    }
    
    showTask(task_set[current_task_nr], current_task_nr + 1);

    if(!task_set[current_task_nr + 1]){ // Current task is last task in set
        end_of_quiz = true;
        setAction(ACTION_SHOW_STATISTIC);
    }

    setProgress(0);
}



function getNewTask(){
    if(task_set){
        current_task_nr++;
        if(task_set[current_task_nr]){
            showTask(task_set[current_task_nr], current_task_nr + 1);

            if(!task_set[current_task_nr + 1]){ // Current task is last task in set
                end_of_quiz = true;
                setAction(ACTION_SHOW_STATISTIC);
            }
        }
        else current_task_nr--;
    }
}


function answerChoice(answer, index){
    if(evaluated) return;

    let index_in_arr = chosen_answers.indexOf(answer);

    const button = answer_buttons.value[index];

    if(index_in_arr !== -1){
        chosen_answers.splice(index_in_arr, 1);
        chosen_answers_indices.splice(index_in_arr, 1);
        button.style.border = "2px solid #0000";
    }
    else{
        chosen_answers.push(answer);
        chosen_answers_indices.push(index);
        button.style.border = "2px solid black";
    }

    if(chosen_answers.length > 0){  // One or more answers chosen
        setAction(ACTION_CHECK_ANSWERS);
        
    }
    else{                           // no answers chosen
        if(end_of_quiz) setAction(ACTION_SHOW_STATISTIC);
        else setAction(ACTION_NEW_QUESTION);
    }
}


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
                    button.style.backgroundColor = "var(--light-green)";
                }
                else{
                    success = EVAL_FAIL;
                    button.style.backgroundColor = "var(--light-red)";
                }
            }
            else{
                if(answers.value[answer_nr].correct){
                    success = EVAL_FAIL;
                    button.style.backgroundColor = "var(--light-green)";
                }
            }
        }
    }

    chosen_answers = [];
    chosen_answers_indices = [];

    if(success == EVAL_SUCC) task_info.value = "Richtig!";
    else task_info.value = "Falsch!";
    

    // console.log(success);
    updateProgress(success);

    return success;
}


function setProgress(val){
    progress_percent.value = "0%";
}

function updateProgress(success){
    if(success == EVAL_SUCC){
        statistic_data[current_task_nr] = "✅";
    } else if(success == EVAL_FAIL){
        statistic_data[current_task_nr] = "❌";
    }

    let width = (current_task_nr+1) / task_set.length * 100;
    progress_percent.value = parseFloat(width).toFixed(0)  + "%";
}





let block_task_choice = false;
let block_new_task = false;



function setAction(a){
    if(a === ACTION_NEW_QUESTION){
        action = ACTION_NEW_QUESTION;
        new_task.value    = "Neue Frage";
        cancel_quiz.value = "Quiz abbrechen";
    }
    if(a === ACTION_CHECK_ANSWERS){
        action = ACTION_CHECK_ANSWERS;
        new_task.value    = "Auflösen";
        cancel_quiz.value = "Quiz abbrechen";
    }
    if(a === ACTION_SHOW_STATISTIC){
        action = ACTION_SHOW_STATISTIC;
        new_task.value    = "Übersicht";
        cancel_quiz.value = "Quiz abbrechen";
    }
    if(a === ACTION_QUIZ_DONE){
        action = ACTION_QUIZ_DONE;
        new_task.value    = "Neue Runde";
        cancel_quiz.value = "Anderes Quiz lösen";
    }
}



function showTask(task, nr){
    // console.log("show Task: " + task + " | " + nr);
    
    task_info.value = "Frage " + nr;

    question_text.value = task.question;
    answers.value = task.answers.sort((a, b) => 0.5 - Math.random());

    evaluated = false;
}





function newTask(event){
    if(action === ACTION_CHECK_ANSWERS){
        evaluate();

        if(end_of_quiz) setAction(ACTION_SHOW_STATISTIC);
        else setAction(ACTION_NEW_QUESTION);
    }
    else {
        for(let i = 0; i < answer_buttons.value.length; i++){
            const button = answer_buttons.value[i]
            button.style.backgroundColor = color;
            button.style.border = "2px solid #0000";
        }

        if(block_new_task) return;
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
}

function cancelQuiz(){
    setAction(ACTION_QUIZ_DONE);
    newTask();
}



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