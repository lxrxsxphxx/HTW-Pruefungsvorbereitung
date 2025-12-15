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
                    <label for="module">Modul:</label>
                    <input type="text" id="module" name="module" class="input-field" ref="module_input" v-model="module_name"><br>
                </div>
                <br>

                <div id="index-cards-container" class="entry-container" ref="index_cards_entry">
                    <KarteikartenErstellen class="entry-view" ref="card_entry_view" @addQuestion="addQuestion" @editQuestion="editQuestion"/>
                </div>
                <div id="multiple-choice-container" class="entry-container" ref="multiple_choice_entry">
                    <QuizEingabe class="entry-view" ref="quiz_entry_view" @addQuestion="addQuestion" @editQuestion="editQuestion"/>
                </div>

                <div id="control-button-container">
                    <button class="control-button" id="save_card_set" @click="saveLearningSet">Lernset speichern</button>
                    <button class="control-button" id="cancel" @click="deleteLearningSet">Abbrechen</button>
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

let question_type_container = ref(null);
let aside = ref(null);
let done_container = ref(null);

let learning_set_name = ref('');
let module_name = ref('');

let entered_questions = ref([]);
let question_set = [];


let edit_index = -1;

const learning_set_url = 'http://localhost:8000/api/learning_set/';




/**
 * @description Construct a JSON Object of a learning set.
 * @param {String} name the name of the learning set
 * @param {String} module the module the learning set will belong to
 * @returns {JSON} the json Object describing the learning set
 */
function makeLearningSetJson(name, module){
    let json_str = '{"name": "' + name + '", "module": "' + module + '"}'

    let json = JSON.parse(json_str);
    return json;
}


/**
 * @description Post the learning set and all its questions to the backend.
 * @returns {null}
 */
async function saveLearningSet(){
    if(learning_set_name.value === '' || module_name.value === ''){
        console.warn('The name of the learning set must be entered!');
        return;
    }
    if(question_set.length === 0){
        console.warn('At least one question must be entered!');
        return;
    }
    if(edit_index >= 0){
        console.warn('Finish editing all the questions first!');
        return;
    }


    let learning_set_json = makeLearningSetJson(learning_set_name.value, module_name.value);

    let data = await postJsonToURL(learning_set_json, learning_set_url);
    let learning_set_id;
    if(data === null){
        console.error('Post learning set failed');
        return;
    }
    else{
        learning_set_id = data.id;
        console.log(learning_set_id);
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
 * @returns {null/JSON} the data from the POST-response
 */
async function postJsonToURL(json, url){
    const json_str = JSON.stringify(json);
    console.log(json_str);
    console.log(url);

    const postHeader = new Headers();
    postHeader.set("accept", "application/json");
    postHeader.set("Content-Type", "application/json");

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 5000);

    try {
        const response = await fetch(url, {method: "POST",
                                            headers: postHeader,
                                            body: json_str,
                                            signal: controller.signal});
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
 * @description Delete the entire learning set.
 * @returns {null}
 */
function deleteLearningSet(){
    hideEntryViews();
    index_cards_entry.value.style.display = "inline";
    editQuestion(question_set[edit_index]);

    for(let i = question_set.length-1; i >= 0; i--){
        deleteQuestion(i);
    }
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
 * @returns {null}
 */
function hideEntryViews(){
    index_cards_entry.value.style.display = "none";
    multiple_choice_entry.value.style.display = "none";

    card_entry_view.value.clearQuestion();
    quiz_entry_view.value.clearQuestion();

    return;
}


/**
 * @description Set only the chosen entry-view visible.
 * @returns {null}
 */
function questionTypeChoice(){
    hideEntryViews();
    let choice = question_type.value.options[question_type.value.selectedIndex].value;
    console.log(choice);
    
    if(choice === 'index_card') index_cards_entry.value.style.display = "inline";
    if(choice === 'multiple_choice') multiple_choice_entry.value.style.display = "inline";

    return;
}


/**
 * @description Save all the important information about a question into the list of entered questions.
 * @param {JSON} json Object, which contains the Question, the question-type, the JSON to be sent to the Backend and the URL it will be sent to
 * @returns {null}
 */
function addQuestion(json){
    console.log(json);

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
        console.log(json);

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
    return;
}


/**
 * @description Delete a question from the entered questions.
 * @param {Number} index the index of the question to be deleted
 * @returns {null}
 */
function deleteQuestion(index){
    console.log('delete: ' + index);
    

    if(edit_index === index) console.warn('Frage ist in Bearbeitung. Kann nicht gelöscht werden.');
    else{
        spliceQuestionFromArrays(index);
        if(edit_index > index) edit_index--;
    }
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