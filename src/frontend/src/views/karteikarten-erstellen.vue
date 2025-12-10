<template>
    <div id="index-cards-entry-body">
        <div id="index-cards-entry-header">
            <!--h1>gib eine Karteikarte ein</h1-->
            <hr>
        </div>

        <div id="index-cards-entry-main">
            <div id="input">
                <div id="input-container">
                    <div id="error-message"></div>
                    <div id="front-container">
                        <!--label for="front">Vorderseite:</label-->
                        <textarea type="text" id="front" name="front" class="input-field" ref="front_input" v-model="front" placeholder="Vorderseite"></textarea><br>
                    </div>
                    

                    <div id="back-container" class="answer-container">
                        <!--label for="back">Rückseite:</label-->
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

//"use strict";


const emit = defineEmits(['addQuestion', 'editQuestion']);
/*const edit_question = inject('question_to_edit');
const edit_index = inject('index_of_question_to_edit');*/

defineExpose({editQuestion, clearQuestion});


let front = ref('');
let back = ref('');

const ADD_QUESTION_TEXT = 'Frage hinzufügen';
const EDIT_QUESTION_TEXT = 'Übernehmen';
let add_text = ref(ADD_QUESTION_TEXT);

let front_input = ref(null);


const url = "http://localhost:8000/api/cards/";


const ADD_QUESTION = 0;
const EDIT_QUESTION = 1;
let action = ADD_QUESTION;

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


function addQuestion(){
    if(front.value === "" || back.value === ""){
        console.warn("no question was entered");
        return;
    }
    if(action === ADD_QUESTION){       // hinzufügen
        console.log("question: " + front.value);
        transferCard(front.value, back.value);

        clearCardInputs();

        front_input.value.focus();
    }
    else if(action === EDIT_QUESTION){ // Änderung übernehmen
        console.log("question: " + front.value);
        transferCard(front.value, back.value);

        clearCardInputs();
        setAction(ADD_QUESTION);

        front_input.value.focus();
    }
}

function editQuestion(json){
    let card = json.question[0];

    setAction(EDIT_QUESTION);
    front.value = card.front;
    back.value = card.back;
    console.log(card.front);
}


function transferCard(front_text, back_text){
    let json = makeJson(front_text, back_text);

    if(action === ADD_QUESTION) emit('addQuestion', json);
    else if(action === EDIT_QUESTION) emit('editQuestion', json);
}
function makeJson(front_text, back_text){
    let json_str = '{"question_text": "' + front_text + '", ';
    json_str += '"url": "' + url + '", ';
    json_str += '"question_type": "index_card", ';

    json_str += '"question": [{"front": "' + front_text + '", "back": "' + back_text + '"}]}';

    let json = JSON.parse(json_str);

    return json;
}


function clearQuestion(){
    clearCardInputs();
    setAction(ADD_QUESTION);
}
function clearCardInputs(){
    front.value = "";
    back.value = "";
}

</script>