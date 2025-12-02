<template>
    <div id="mc-quiz-entry-body">
        <div id="mc-quiz-entry-header">
            <!--h1>gib eine Quizfrage und die Lösungen ein</h1-->
            <hr>
        </div>
        <div id="mc-quiz-entry-main">
            <div id="input">
                <div id="input-container">
                    <div id="error-message"></div>
                    <div>
                        <label for="question">Frage:</label>
                        <input type="text" id="question" name="question" class="input-field" ref="question_input" v-model="question"><br>
                    </div>
                    <br>

                    <div id="answer_1-container" class="answer-container">
                        <label for="answer_1" class="txt_answer">Antwort 1:</label>
                        <input type="text" id="answer_1" name="answer_1" class="input-field" ref="answer_1_input" v-model="answer_1"><br>
                    </div>
                    <div id="answer_2-container" class="answer-container">
                        <label for="answer_2" class="txt_answer">Antwort 2:</label>
                        <input type="text" id="answer_2" name="answer_2" class="input-field" ref="answer_2_input" v-model="answer_2"><br>
                    </div>
                    <div id="answer_3-container" class="answer-container">
                        <label for="answer_3" class="txt_answer">Antwort 3:</label>
                        <input type="text" id="answer_3" name="answer_3" class="input-field" ref="answer_3_input" v-model="answer_3"><br>
                    </div>
                    <div id="answer_4-container" class="answer-container">
                        <label for="answer_4" class="txt_answer">Antwort 4:</label>
                        <input type="text" id="answer_4" name="answer_4" class="input-field" ref="answer_4_input" v-model="answer_4"><br>
                    </div>
                    <br>
                    <div id="correct_answers-container">
                        <label for="correct_answers">richtige Antworten: </label>
                        <input type="text" id="correct_answers" name="correct_answers" class="input-field" ref="correct_answers_input" v-model="correct_answers">
                        <div id="example">z.B.: 1, 4</div>
                    </div>
                    <br>
                </div>

                <div id="control-button-container">
                    <button class="control-button" id="add_question" v-text="add_text" @click="addQuestion"></button>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>

import { defineProps, ref } from 'vue';

"use strict";

const emit = defineEmits(['addQuestion']);


let question = ref('');

let answer_1 = ref('');
let answer_2 = ref('');
let answer_3 = ref('');
let answer_4 = ref('');

let correct_answers = ref('');


let add_text = ref('Frage hinzufügen');



let question_input = ref(null);

let answer_1_input = ref(null);
let answer_2_input = ref(null);
let answer_3_input = ref(null);
let answer_4_input = ref(null);

let correct_answers_input = ref(null);


let cancel_popup = ref(null);




let url = "http://localhost:8000/api/questions/";



function makeJson(question_text, answer_1, answer_2, answer_3, answer_4, correct_answers) {
    let correct_answers_str = correct_answers.toString();
    correct_answers_str.replaceAll(" ","");

    let arr = correct_answers_str.split(",");
    let correct_answers_arr = [];
    let i;
    for(i = 0; i < arr.length; i++){
        console.log(arr[i]);
        if(parseInt(arr[i]) >= 1 && parseInt(arr[i]) <= 4) correct_answers_arr.push(parseInt(arr[i]));
    }
    if(correct_answers_arr.length === 0) correct_answers_arr.push(1);

    console.log(correct_answers_arr);


    let answers = [answer_1, answer_2, answer_3, answer_4];


    let json_str = '{"question_text": "' + question_text + '", ';
    json_str += '"url": "' + url + '", ';
    json_str += '"question_type": "multiple_choice", ';

    json_str += '"question": {"question": {"question":"' + question_text + '"}, "answers":[';

    for(i = 0; i < 4; i++){
        json_str += '{"answer":"' + answers[i] + '","correct":';
        if(correct_answers_arr.includes((i+1))) json_str += 'true}';
        else json_str += 'false}';
        if(i !== 3) json_str += ',';
    }

    json_str += ']}}';

    let json = JSON.parse(json_str);

    return json;
}
function addQuestionToSet(question_text, answer_1, answer_2, answer_3, answer_4, correct_answers){
    let json = makeJson(question_text, answer_1, answer_2, answer_3, answer_4, correct_answers);

    emit('addQuestion', json);
}


let action = 0;


/**
 * 
 * @param val 0: neue Frage hinzufügen
 * @param val 1: Änderung übernehmen
 */
function setAction(val){
    if(val === 0){
        action = 0;
        add_text.value = 'Frage Hinzufügen';
    }
    else if(val === 1){
        action = 1;
        add_text.value = 'Übernehmen';
    }
}
function addQuestion(){
    if(question.value === "" || answer_1.value === "" || answer_2.value === "" || answer_3.value === "" || answer_4.value === ""){
        console.warn("no question was entered");
        return;
    }
    if(action === 0){       // hinzufügen
        console.log("question: " + question.value);
        addQuestionToSet(question.value, answer_1.value, answer_2.value, answer_3.value, answer_4.value, correct_answers.value);

        clearQuestionInputs();

        question_input.value.focus();
    }
    else if(action === 1){ // Änderung übernehmen
        console.log("question: " + question.value);
        changeQuestionAtIndex(edit_index, question.value, answer_1.value, answer_2.value, answer_3.value, answer_4.value, correct_answers.value);

        //entered_questions.value[edit_index] = question.value;

        clearQuestionInputs();

        setAction(0);
    }
}


function clearQuestionInputs(){
    question.value = "";
    answer_1.value = "";
    answer_2.value = "";
    answer_3.value = "";
    answer_4.value = "";
    correct_answers.value = "";
}

/*function editQuestion(index){
    edit_index = index;
    console.log("edit: " + index);
    let question_json = getQuestion(index);

    let question_obj = JSON.parse(question_json);

    question.value = question_obj.question.question;

    answer_1.value = question_obj.answers[0].answer;
    answer_2.value = question_obj.answers[1].answer;
    answer_3.value = question_obj.answers[2].answer;
    answer_4.value = question_obj.answers[3].answer;


    let correct = [];
    for(let i = 0; i < 4; i++) if(question_obj.answers[i].correct) correct.push(i);

    correct_answers.value = (correct[0] + 1);
    for(let i = 1; i < correct.length; i++) correct_answers.value += ', ' + (correct[i] + 1);

    setAction(1);
}*/


</script>


<style scoped>
@import '@/assets/quiz-eingabe.css';
</style>