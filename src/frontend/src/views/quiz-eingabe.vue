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
                        <input type="text" id="question" name="question" class="input-field" ref="question_input" v-model="question_entry"><br>
                    </div>
                    <br>

                    <div id="answer_1-container" class="answer-container">
                        <label for="answer_1" class="txt_answer">Antwort 1:</label>
                        <input type="text" id="answer_1" name="answer_1" class="input-field" ref="answer_1_input" v-model="answer_1_entry"><br>
                    </div>
                    <div id="answer_2-container" class="answer-container">
                        <label for="answer_2" class="txt_answer">Antwort 2:</label>
                        <input type="text" id="answer_2" name="answer_2" class="input-field" ref="answer_2_input" v-model="answer_2_entry"><br>
                    </div>
                    <div id="answer_3-container" class="answer-container">
                        <label for="answer_3" class="txt_answer">Antwort 3:</label>
                        <input type="text" id="answer_3" name="answer_3" class="input-field" ref="answer_3_input" v-model="answer_3_entry"><br>
                    </div>
                    <div id="answer_4-container" class="answer-container">
                        <label for="answer_4" class="txt_answer">Antwort 4:</label>
                        <input type="text" id="answer_4" name="answer_4" class="input-field" ref="answer_4_input" v-model="answer_4_entry"><br>
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

import { defineExpose, ref } from 'vue';

//"use strict";

const emit = defineEmits(['addQuestion', 'editQuestion']);
/*const edit_question = inject('question_to_edit');
const edit_index = inject('index_of_question_to_edit');*/

defineExpose({editQuestion, clearQuestion});


let question_entry = ref('');

let answer_1_entry = ref('');
let answer_2_entry = ref('');
let answer_3_entry = ref('');
let answer_4_entry = ref('');

let correct_answers = ref('');


const ADD_QUESTION_TEXT = 'Frage hinzufügen';
const EDIT_QUESTION_TEXT = 'Übernehmen';
let add_text = ref(ADD_QUESTION_TEXT);



let question_input = ref(null);

let answer_1_input = ref(null);
let answer_2_input = ref(null);
let answer_3_input = ref(null);
let answer_4_input = ref(null);

let correct_answers_input = ref(null);


let cancel_popup = ref(null);


const ADD_QUESTION = 0;
const EDIT_QUESTION = 1;
let action = ADD_QUESTION;


const url = "http://localhost:8000/api/questions/";


/**
 * This function constructs a JSON Object which contains all the important information of the entered question.
 * This information includes the question with all the question-parameters, the URL the question will be sent to and the type of question (multiple_choice).
 * @param question_text the actual question
 * @param entered_answers the list of entered answers as strings
 * @param correct_answers a list that contains the numbers of all correct answers
 */
function makeJson(question_text, entered_answers, correct_answers) {
    let json_str = '{"question_text": "' + question_text + '", ';
    json_str += '"url": "' + url + '", ';
    json_str += '"question_type": "multiple_choice", ';

    json_str += '"question": {"question": {"question":"' + question_text + '"}, "answers":[';

    let len = entered_answers.length;
    for(let i = 0; i < len; i++){
        json_str += '{"answer":"' + entered_answers[i] + '","correct":';
        if(correct_answers.includes((i+1))) json_str += 'true}';
        else json_str += 'false}';
        if(i !== len-1) json_str += ',';
    }

    json_str += ']}}';

    let json = JSON.parse(json_str);

    return json;
}


/**
 * Transfers a question to the parent-view in the JSON-format via an emitted event
 * @param question_text the actual question
 * @param entered_answers the list of entered answers as strings
 * @param correct_answers a list that contains the numbers of all correct answers
 */
function transferQuestion(question_text, entered_answers, correct_answers){
    let json = makeJson(question_text, entered_answers, correct_answers);

    if(action === ADD_QUESTION) emit('addQuestion', json);
    else if(action === EDIT_QUESTION) emit('editQuestion', json);
}



/**
 * Changes the Action performed by the add_question button
 * @param val 0: add a new question
 * @param val 1: Save edited question
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
}


/**
 * Reads the inputted values of the question-parameters and transfers the question to the parent-view.
 */
function addQuestion(){
    
    // construct a list with the correct answers (as they are inputted)
    let correct_answers_str = correct_answers.value.toString();
    correct_answers_str.replaceAll(" ","");

    let arr = correct_answers_str.split(",");
    let correct_answers_input_arr = [];

    for(let i = 0; i < arr.length; i++){
        let index = parseInt(arr[i]);
        if(index >= 1 && index <= 4) correct_answers_input_arr.push(index);
    }


    // construct the list of correct answers and the list of inputted questions
    let correct_answers_arr = [];

    let entered_answers = [];
    if(answer_1_entry.value !== ""){
        entered_answers.push(answer_1_entry.value);
        if(correct_answers_input_arr.includes(1)) correct_answers_arr.push(entered_answers.length);
    }
    if(answer_2_entry.value !== ""){
        entered_answers.push(answer_2_entry.value);
        if(correct_answers_input_arr.includes(2)) correct_answers_arr.push(entered_answers.length);
    }
    if(answer_3_entry.value !== ""){
        entered_answers.push(answer_3_entry.value);
        if(correct_answers_input_arr.includes(3)) correct_answers_arr.push(entered_answers.length);
    }
    if(answer_4_entry.value !== ""){
        entered_answers.push(answer_4_entry.value);
        if(correct_answers_input_arr.includes(4)) correct_answers_arr.push(entered_answers.length);
    }

    if(correct_answers_arr.length === 0) correct_answers_arr.push(1);
    console.log(correct_answers_arr);



    // the question and at least two answers mut be inputted
    if(question_entry.value === "" || entered_answers.length < 2){
        console.warn("no question was entered");
        return;
    }


    // transfer the question to the parent view and clean up
    console.log("question: " + question_entry.value);
    transferQuestion(question_entry.value, entered_answers, correct_answers_arr);

    clearQuestionInputs();
    if(action === EDIT_QUESTION) setAction(ADD_QUESTION); // change to the standard action

    question_input.value.focus();
}


/**
 * This function takes an existing question and sets it up to be edited.
 * It writes the question-parameters into the corresponding input-fields and sets the the action to be "edit".
 * @param json A JSON Object which contains all the important information of the question. This information includes the question with all the question-parameters, the URL the question will be sent to and the type of question (multiple_choice).
 */
function editQuestion(json){
    let question = json.question;

    setAction(EDIT_QUESTION);

    let num_answers = question.answers.length

    question_entry.value = question.question.question;
    answer_1_entry.value = question.answers[0].answer;
    answer_2_entry.value = question.answers[1].answer;
    if(num_answers > 2) answer_3_entry.value = question.answers[2].answer;
    if(num_answers > 3) answer_4_entry.value = question.answers[3].answer;

    let correct = [];
    for(let i = 0; i < num_answers; i++) if(question.answers[i].correct) correct.push(i);

    correct_answers.value = (correct[0] + 1);
    for(let i = 1; i < correct.length; i++) correct_answers.value += ', ' + (correct[i] + 1);
}




/**
 * Clears all inputs and resets the action to the standard action (add question).
 */
function clearQuestion(){
    clearQuestionInputs();
    setAction(ADD_QUESTION);
}
/**
 * Clears all input fields.
 */
function clearQuestionInputs(){
    question_entry.value = "";
    answer_1_entry.value = "";
    answer_2_entry.value = "";
    answer_3_entry.value = "";
    answer_4_entry.value = "";
    correct_answers.value = "";
}


</script>


<style scoped>
@import '@/assets/quiz-eingabe.css';
</style>