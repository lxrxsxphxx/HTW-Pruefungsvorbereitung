<template>
    <header>
        <h1>gib eine Quizfrage und die Lösungen ein</h1>
        <hr>
    </header>
    <main>
        <div id="input">
            <div id="input-container">
                <div>
                    <label for="quiz_name">Quizname:</label>
                    <input type="text" id="quiz_name" name="quiz_name" class="input-field" ref="quiz_name_input" v-model="quiz_name"><br>
                </div>
                <hr style="border: 0;">
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
                <button class="control-button" id="add_question" v-text="add_text" @click="v.addQuestion"></button>
                <button class="control-button" id="save_quiz" v-text="save_text" @click="v.saveQuiz"></button>
                <button class="control-button" id="cancel" v-text="cancel_text" @click="v.showCancelPopup"></button>
            </div>

            <div id="cancel-popup" ref="cancel_popup">
                <div id="cancel-popup-text">
                    <div style="margin-bottom: 1em;">Achtung, alle Fragen werden gelöscht.</div><div>Wirklich Abbrechen?</div>
                </div>
                <div id="cancel_button_container">
                    <button id="commit_cancel" class="cancel_option" ref="commit_cancel" @click="v.commitCancel">Ja</button>
                    <button id="cancel_cancel" class="cancel_option" ref="cancel_cancel" @click="v.cancelCancel">Nein</button>
                </div>
            </div>
        </div>

        <aside id="aside">
            <!--Hier werden die eingegebenen Fragen stehen-->
            <h3>Eingegebene Fragen:<br/></h3>
            <div class="entered_question" v-for="(question, index) in entered_questions" :key="index">
                <div class="question_text" v-text="(index+1) + ': ' + question"></div>
                <button class="delete_question" @click="v.deleteQuestion(index)">löschen</button>
                <button class="edit_question" @click="v.editQuestion(index)">bearbeiten</button>
            </div>
        </aside>
    </main>
</template>


<script setup>

import { ref } from 'vue';

</script>

<script>
"use strict";

let m;
let p;
let v;

let quiz_name = ref('');
let question = ref('');

let answer_1 = ref('');
let answer_2 = ref('');
let answer_3 = ref('');
let answer_4 = ref('');

let correct_answers = ref('');

let entered_questions = ref([]);


let add_text = ref('Frage Hinzufügen');
let save_text = ref('Quiz Speichern');
let cancel_text = ref('Abbrechen');



let quiz_name_input = ref(null);
let question_input = ref(null);

let answer_1_input = ref(null);
let answer_2_input = ref(null);
let answer_3_input = ref(null);
let answer_4_input = ref(null);

let correct_answers_input = ref(null);


let cancel_popup = ref(null);

let commit_cancel = ref(null);
let cancel_cancel = ref(null);




document.addEventListener('DOMContentLoaded', async function(){
    m = new Model();
    p = new Presenter();
    v = new View(p);

    p.setModelAndView(m, v);
});


// ======================================= Model =======================================
/**
 * schreibt das eingegeben Quiz in die json-Datei
 */
class Model{
    constructor(){
        this.file_path = "./quiz.json"
    }

    async writeSetToFile(str){
        try{
            const fileHandle = await window.showSaveFilePicker();

            const file_stream = await fileHandle.createWritable();
            await file_stream.write(str);

            await file_stream.close();
        }
        catch (err) {
            console.error(err.name, err.message);
            return -1;
        }
    }
}



// ======================================= Presenter =======================================
/**
 * erstellt ein Quiz aus den einzelnen Fragen
 */
class Presenter{
    constructor(){
        this.question_set = [];
    }
    setModelAndView(m, v){
        this.model = m;
        this.view = v;
    }

    makeJsonString(question_text, answer_1, answer_2, answer_3, answer_4, correct_answers){
        console.log(correct_answers);
        let correct_answers_str = correct_answers.toString();
        correct_answers_str.replaceAll(" ","");

        let correct_answers_arr = correct_answers_str.split(",");

        let json_str = '{"txt":"' + question_text + '", "answers":["' + answer_1 + '","' + answer_2 + '","' + answer_3 + '","' + answer_4 + '"],"correct":[';

        let correct_str = '';
        for(let i = 0; i < correct_answers_arr.length-1; i++){
            if(correct_answers_arr[i] >= 1 && correct_answers_arr[i] <= 4) correct_str += '"' + parseInt(correct_answers_arr[i]-1) + '",';
        }
        if(correct_answers_arr[correct_answers_arr.length-1] >= 1 && correct_answers_arr[correct_answers_arr.length-1] <= 4) correct_str += '"' + parseInt(correct_answers_arr[correct_answers_arr.length-1]-1) + '"';
        if(correct_str === '') correct_str = '"0"';

        json_str += correct_str + ']}';

        return json_str;
    }
    addQuestionToSet(question_text, answer_1, answer_2, answer_3, answer_4, correct_answers){
        let json_str = this.makeJsonString(question_text, answer_1, answer_2, answer_3, answer_4, correct_answers);

        console.log(json_str);
        this.question_set.push(json_str);

        this.view.addEnteredQuestion(question_text);
    }
    changeQuestionAtIndex(index, question_text, answer_1, answer_2, answer_3, answer_4, correct_answers){
        let json_str = this.makeJsonString(question_text, answer_1, answer_2, answer_3, answer_4, correct_answers);

        console.log(json_str);
        this.question_set[index] = json_str;
    }

    async saveQuiz(quiz_name){
        if(this.question_set.length > 0){
            let json_str = '{\n\t"quiz_name": "' + quiz_name +  '",\n\t"questions": [\n';

            let max_index = this.question_set.length - 1;
            for(let i = 0; i < max_index; i++){
                json_str += '\t\t' + this.question_set[i] + ',\n';
            }
            json_str += '\t\t' + this.question_set[max_index] + '\n\t]\n}';
            console.log(json_str);

            let ret_val = await this.model.writeSetToFile(json_str);
            if(ret_val == -1){
                return false;
            }
            else{
                this.deleteQuestionSet();
                return true;
            }
        }
    }
    deleteQuestion(index){
        this.question_set.splice(index, 1);
    }
    deleteQuestionSet(){
        const len = this.question_set.length
        for(let i = 0; i < len; i++){
            this.question_set.pop();
        }
    }

    getQuestion(index){
        return this.question_set[index];
    }
}



// ======================================= View =======================================
/**
 * liest Eingaben aus der Website und gibt diese an den Presenter
 */
class View{
    constructor(p){
        this.presenter = p;
        this.setAction(0);
        quiz_name_input.value.focus();
    }


    /**
     * 
     * @param val 0: neue Frage hinzufügen
     * @param val 1: Änderung übernehmen
     */
    setAction(val){
        if(val === 0){
            this.action = 0;
            add_text.value = 'Frage Hinzufügen';
        }
        else if(val === 1){
            this.action = 1;
            add_text.value = 'Übernehmen';
        }
    }
    addQuestion(){
        if(question.value === "" || answer_1.value === "" || answer_2.value === "" || answer_3.value === "" || answer_4.value === ""){
            console.warn("no question was entered");
            //document.getElementById("error-message").innerHTML = "Bitte die Frage mit allen Antwortmöglichkeiten eingeben.";
            return;
        }
        if(this.action === 0){       // hinzufügen
            //document.getElementById("error-message").innerHTML = "";
            console.log("question: " + question.value);
            this.presenter.addQuestionToSet(question.value, answer_1.value, answer_2.value, answer_3.value, answer_4.value, correct_answers.value);

            this.clearQuestionInputs();

            question_input.value.focus();
        }
        else if(this.action === 1){ // Änderung übernehmen
            console.log("question: " + question.value);
            this.presenter.changeQuestionAtIndex(this.edit_index, question.value, answer_1.value, answer_2.value, answer_3.value, answer_4.value, correct_answers.value);

            entered_questions.value[this.edit_index] = question.value;

            this.clearQuestionInputs();

            this.setAction(0);
        }
    }
    addEnteredQuestion(question_text){
        entered_questions.value.push(question_text);
    }


    async saveQuiz(){
        if(quiz_name.value !== ""){
            let ret = await this.presenter.saveQuiz(quiz_name.value);
            if(ret)this.clearEnteredQuestions();
        }
        quiz_name_input.value.focus();
    }


    showCancelPopup(){
        cancel_popup.value.style.display = "inline";
    }
    commitCancel(){
        this.presenter.deleteQuestionSet();
        this.clearEnteredQuestions();

        quiz_name_input.value.focus();
        cancel_popup.value.style.display = "none";
    }
    cancelCancel(){
        cancel_popup.value.style.display = "none";
    }


    clearQuestionInputs(){
        question.value = "";
        answer_1.value = "";
        answer_2.value = "";
        answer_3.value = "";
        answer_4.value = "";
        correct_answers.value = "";
    }
    clearEnteredQuestions(){
        quiz_name.value = "";

        this.clearQuestionInputs();

        entered_questions.value = [];
    }

    deleteQuestion(index){
        console.log("delete: " + index);

        this.presenter.deleteQuestion(index);
        entered_questions.value.splice(index, 1);
    }
    editQuestion(index){
        this.edit_index = index;
        console.log("edit: " + index);
        let question_json = this.presenter.getQuestion(index);

        let question_obj = JSON.parse(question_json);

        question.value = question_obj.txt;

        answer_1.value = question_obj.answers[0];
        answer_2.value = question_obj.answers[1];
        answer_3.value = question_obj.answers[2];
        answer_4.value = question_obj.answers[3];

        correct_answers.value = (parseInt(question_obj.correct[0]) + 1);
        for(let i = 1; i < question_obj.correct.length; i++) correct_answers.value += ', ' + (parseInt(question_obj.correct[i]) + 1);

        this.setAction(1);
    }
}


</script>


<style scoped>
@import '@/assets/quiz-eingabe.css';
</style>