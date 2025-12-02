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

import { inject, ref } from 'vue';

"use strict";


const emit = defineEmits(['addQuestion']);
const edit_question = inject('question_to_edit');
const edit_index = inject('index_of_question_to_edit');


let front = ref('');
let back = ref('');

let add_text = ref('Frage hinzufügen');

let front_input = ref(null);


const url = "http://localhost:8000/api/cards/";



let action = 0;



function addQuestion(){
    if(front.value === "" || back.value === ""){
        console.warn("no question was entered");
        return;
    }
    if(action === 0){       // hinzufügen
        console.log("question: " + front.value);
        addCardToSet(front.value, back.value);

        clearCardInputs();

        front_input.value.focus();
    }
    else if(action === 1){ // Änderung übernehmen
        console.log("question: " + front.value);

        clearCardInputs();

        //setAction(0);
    }
}


function addCardToSet(front_text, back_text, modul){
    let json = makeJson(front_text, back_text, modul);

    emit('addQuestion', json);
}
function makeJson(front_text, back_text, modul){
    let json_str = '{"question_text": "' + front_text + '", ';
    json_str += '"url": "' + url + '", ';
    json_str += '"question_type": "index_card", ';

    json_str += '"question": [{"front": "' + front_text + '", "back": "' + back_text + '", "modul": "' + modul + '"}]}';

    let json = JSON.parse(json_str);

    return json;
}


function clearCardInputs(){
    front.value = "";
    back.value = "";
}

</script>