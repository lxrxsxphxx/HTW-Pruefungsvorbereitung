<template>
    <div id="mc-quiz-entry-body">
        <div id="mc-quiz-entry-header">
            <hr>
        </div>
        <div id="mc-quiz-entry-main">
            <div id="input">
                <div id="input-container">
                    <div>
                        <label for="question">Frage:</label>
                        <input type="text" id="question" name="question" class="input-field" ref="question_input" v-model="question_entry"><br>
                    </div>
                    <br>

                    <div id="answer_1-container" class="answer-container">
                        <label for="answer_1" class="txt_answer">Antwort 1:</label>
                        <input type="text" id="answer_1" name="answer_1" class="input-field" ref="answer_1_input" v-model="answer_1_entry"><br>
                        <label class="switch">
                            <input type="checkbox" id="answer_1_correct" @click="toggleAnswerCorrectness(0)" v-bind:checked="answers_correct[0]">
                            <span class="slider round"><span class="tooltip" v-text="answers_correct_text[0]"></span></span>
                        </label>
                    </div>
                    <div id="answer_2-container" class="answer-container">
                        <label for="answer_2" class="txt_answer">Antwort 2:</label>
                        <input type="text" id="answer_2" name="answer_2" class="input-field" ref="answer_2_input" v-model="answer_2_entry"><br>
                        <label class="switch">
                            <input type="checkbox" id="answer_2_correct" @click="toggleAnswerCorrectness(1)" v-bind:checked="answers_correct[1]">
                            <span class="slider round"><span class="tooltip" v-text="answers_correct_text[1]"></span></span>
                        </label>
                    </div>
                    <div id="answer_3-container" class="answer-container">
                        <label for="answer_3" class="txt_answer">Antwort 3:</label>
                        <input type="text" id="answer_3" name="answer_3" class="input-field" ref="answer_3_input" v-model="answer_3_entry"><br>
                        <label class="switch">
                            <input type="checkbox" id="answer_3_correct" @click="toggleAnswerCorrectness(2)" v-bind:checked="answers_correct[2]">
                            <span class="slider round"><span class="tooltip" v-text="answers_correct_text[2]"></span></span>
                        </label>
                    </div>
                    <div id="answer_4-container" class="answer-container">
                        <label for="answer_4" class="txt_answer">Antwort 4:</label>
                        <input type="text" id="answer_4" name="answer_4" class="input-field" ref="answer_4_input" v-model="answer_4_entry"><br>
                        <label class="switch">
                            <input type="checkbox" id="answer_4_correct" @click="toggleAnswerCorrectness(3)" v-bind:checked="answers_correct[3]">
                            <span class="slider round"><span class="tooltip" v-text="answers_correct_text[3]"></span></span>
                        </label>
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


const emit = defineEmits(['addQuestion', 'editQuestion', 'error']);

defineExpose({editQuestion, clearQuestion});

const MAX_ANSWERS = 4;


let question_entry = ref('');

let answer_1_entry = ref('');
let answer_2_entry = ref('');
let answer_3_entry = ref('');
let answer_4_entry = ref('');


let answers_correct = ref([false, false, false, false]);

const FALSE_TEXT = 'Falsch';
const RIGHT_TEXT = 'Richtig';
let answers_correct_text = ref([FALSE_TEXT, FALSE_TEXT, FALSE_TEXT, FALSE_TEXT]);


const ADD_QUESTION_TEXT = 'Frage hinzufügen';
const EDIT_QUESTION_TEXT = 'Übernehmen';
let add_text = ref(ADD_QUESTION_TEXT);



let question_input = ref(null);


const ADD_QUESTION = 0;
const EDIT_QUESTION = 1;
let action = ADD_QUESTION;


const url = "http://localhost:8000/api/questions/";


/**
 * @description Construct a JSON Object which contains all the important information of the entered question.
 * This information includes the question with all the question-parameters, the URL the question will be sent to and the type of question (multiple_choice).
 * @param {String} question_text the actual question
 * @param {list[String]} entered_answers the list of entered answers
 * @param {list[Number]} correct_answers a list that contains the numbers of all correct answers
 * @returns {JSON} the json Object
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
 * @description Transfer a question to the parent-view in the JSON-format via an emitted event.
 * @param {String} question_text the actual question
 * @param {list[String]} entered_answers the list of entered answers
 * @param {list[Number]} correct_answers a list that contains the numbers of all correct answers
 * @returns {null}
 */
function transferQuestion(question_text, entered_answers, correct_answers){
    let json = makeJson(question_text, entered_answers, correct_answers);

    if(action === ADD_QUESTION) emit('addQuestion', json);
    else if(action === EDIT_QUESTION) emit('editQuestion', json);

    return;
}



/**
 * @description Change the Action performed by the *add_question* button as well as its text.
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
 * @description Read the inputted values of the question-parameters and transfer the question to the parent-view.
 * @returns {null}
 */
function addQuestion(){
    // construct the list of correct answers and the list of inputted questions
    let correct_answers_arr = [];

    let entered_answers = [];
    if(answer_1_entry.value !== ""){
        entered_answers.push(answer_1_entry.value);
        if(answers_correct.value[0]) correct_answers_arr.push(entered_answers.length);
    }
    if(answer_2_entry.value !== ""){
        entered_answers.push(answer_2_entry.value);
        if(answers_correct.value[1]) correct_answers_arr.push(entered_answers.length);
    }
    if(answer_3_entry.value !== ""){
        entered_answers.push(answer_3_entry.value);
        if(answers_correct.value[2]) correct_answers_arr.push(entered_answers.length);
    }
    if(answer_4_entry.value !== ""){
        entered_answers.push(answer_4_entry.value);
        if(answers_correct.value[3]) correct_answers_arr.push(entered_answers.length);
    }

    if(correct_answers_arr.length === 0) correct_answers_arr.push(1);
    console.log(correct_answers_arr);



    // the question and at least two answers mut be inputted
    if(question_entry.value === "" || entered_answers.length < 2){
        emit('error', 'Die Frage und mind. zwei Antworten müssen eingegeben werden!');
        return;
    }


    // transfer the question to the parent view and clean up
    console.log("question: " + question_entry.value);
    transferQuestion(question_entry.value, entered_answers, correct_answers_arr);

    clearQuestion();
    if(action === EDIT_QUESTION) setAction(ADD_QUESTION); // change to the standard action

    question_input.value.focus();

    return;
}


/**
 * @description This function takes an existing question and sets it up to be edited.
 * It writes the question-parameters into the corresponding input-fields and sets the the action to be *EDIT_QUESTION*.
 * @param {JSON} json A JSON Object which contains all the important information of the question. This information includes the question with all the question-parameters, the URL the question will be sent to and the type of question (multiple_choice).
 * @returns {null}
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

    for(let i = 0; i < num_answers; i++) {
        if(question.answers[i].correct) setAnswerCorrectness(i, true);
        else setAnswerCorrectness(i, false);
    }

    return;
}


/**
 * @description Set an answers correctness by setting its state and description.
 * @param {Number} answer the index of the nswer
 * @param {Boolean} correct the state to set the answer to (true: correct, false: incorrect)
 * @returns {null}
 */
function setAnswerCorrectness(answer, correct){
    if(answer < 0 || answer >= MAX_ANSWERS) return;
    
    answers_correct.value[answer] = correct;

    if(correct) answers_correct_text.value[answer] = RIGHT_TEXT;
    else answers_correct_text.value[answer] = FALSE_TEXT;

    return;
}

/**
 * @description Toggle an answers correctness by setting its state and description
 * @param {Number} answer the index of the nswer
 * @returns {null}
 */
function toggleAnswerCorrectness(answer){
    if(answers_correct.value[answer] === false) setAnswerCorrectness(answer, true);
    else setAnswerCorrectness(answer, false);

    return;
}



/**
 * @description Clear all inputs and reset the action to the standard action (add question).
 * @returns {null}
 */
function clearQuestion(){
    question_entry.value = "";
    answer_1_entry.value = "";
    answer_2_entry.value = "";
    answer_3_entry.value = "";
    answer_4_entry.value = "";

    for(let i = 0; i < MAX_ANSWERS; i++) setAnswerCorrectness(i, false);

    setAction(ADD_QUESTION);
    return;
}

</script>


<style scoped>
@import '@/assets/quiz-eingabe.css';
</style>