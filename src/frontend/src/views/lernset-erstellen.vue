<template>
    <div id="learning-set-choice-body">
        <div id="learning-set-choice-header">
            <h1>Lernset erstellen</h1>
        </div>

        <div id="learning-set-entry-main">
            <div id="question-type-container">
                <div>
                    <label for="quiz_name">Quizname:</label>
                    <input type="text" id="quiz_name" name="quiz_name" class="input-field" ref="quiz_name_input" v-model="quiz_name"><br>
                </div>
                <br>

                <div id="index-cards-container" class="entry-container" ref="index_cards_entry">
                    <KarteikartenErstellen class="entry-view" ref="card_entry_view" @addQuestion="addQuestion" @editQuestion="editQuestion"/>
                </div>
                <div id="multiple-choice-container" class="entry-container" ref="multiple_choice_entry">
                    <QuizEingabe class="entry-view" ref="quiz_entry_view" @addQuestion="addQuestion" @editQuestion="editQuestion"/>
                </div>

                <div id="control-button-container">
                    <button class="control-button" id="save_card_set">Lernset speichern</button>
                    <button class="control-button" id="cancel">Abbrechen</button>
                </div>
            </div>


            <aside id="aside">
                <div id="choice-container">
                    <!--label for="question_type"></label-->
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
        </div>
    </div>
</template>

<style scoped>
@import '@/assets/lernset-erstellen.css';
</style>



<script setup>
import { provide, ref } from 'vue';
import KarteikartenErstellen from './karteikarten-erstellen.vue';
import QuizEingabe from './quiz-eingabe.vue';


"use strict";



let question_type = ref(null);

let index_cards_entry = ref(null);
let multiple_choice_entry = ref(null);

let card_entry_view = ref(null);
let quiz_entry_view = ref(null);


let entered_questions = ref([]);
let question_set = [];

/*let edit_question = ref(undefined);
let edit_index = ref(-1);

provide('question_to_edit', edit_question);
provide('index_of_question_to_edit', edit_index);*/
let edit_index = -1;


function hideEntryViews(){
    index_cards_entry.value.style.display = "none";
    multiple_choice_entry.value.style.display = "none";

    card_entry_view.value.clearQuestion();
    quiz_entry_view.value.clearQuestion();
}


function questionTypeChoice(){
    hideEntryViews();
    let choice = question_type.value.options[question_type.value.selectedIndex].value;
    console.log(choice);
    
    if(choice === 'index_card') index_cards_entry.value.style.display = "inline";
    if(choice === 'multiple_choice') multiple_choice_entry.value.style.display = "inline";
}


/**
 * Saves all the important information about a question into the list of entered questions
 * @param json Object, which contains the Question, the question-type, the JSON to be sent to the Backend and the URL it will be sent to
 */
function addQuestion(json){
    console.log(json);

    entered_questions.value.push(json.question_text);
    question_set.push(json);
}
function editQuestion(json){
    let index = edit_index;
    if(index >= 0 && index < question_set.length){
        console.log(json);

        entered_questions.value[index] = json.question_text;
        question_set[index] = json;
    }
    edit_index = -1;
}

function provideQuestion(index){
    console.log('edit: ' + index);

    let edit_question = question_set[index];
    edit_index = index;
    console.log(edit_question);

    hideEntryViews();

    if(edit_question.question_type === 'index_card'){
        index_cards_entry.value.style.display = "inline";
        question_type.value.value = 'index_card';

        card_entry_view.value.editQuestion(edit_question);
    }
    if(edit_question.question_type === 'multiple_choice'){
        multiple_choice_entry.value.style.display = "inline";
        question_type.value.value = 'multiple_choice';

        quiz_entry_view.value.editQuestion(edit_question);
    }
}
function deleteQuestion(index){
    console.log('delete: ' + index);
    

    if(edit_index === index) console.warn('Frage ist in Bearbeitung. Kann nicht gelöscht werden.');
    else{
        spliceQuestionFromArrays(index);
        if(edit_index > index) edit_index--;
    }
}
function spliceQuestionFromArrays(index){
    question_set.splice(index, 1);
    entered_questions.value.splice(index, 1);
}

</script>