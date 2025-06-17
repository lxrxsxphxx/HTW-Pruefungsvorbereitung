<template>
    <header>
        <h1>Quiz lösen</h1>
        <hr>
    </header>

    <main>
        <div id="menu">
            <div id="quiz-choice-container">
                <p>Wähle ein Quiz aus:</p>
                <div id="quiz-choice">
                    <button v-for="(key,index) in keys" :key="index" @click="v.quizChoice" v-bind:id="key">{{ key }}</button>
                </div>
            </div>
            <button class="control-button" id="change-learning-mode-button">Lernmodus wechseln</button>
        </div>

        <div id="middle">
            <button class="control-button" id="cancel-quiz-button" @click="v.cancelQuiz">{{ cancel_quiz }}</button>
            <div id="progress-bar-container">
                <p id="progress-text">{{ progress_percent }}</p>
                <div id="progress-bar">
                    <div id="progress" :style="{ width: progress_percent }"></div>
                </div>
            </div>
            <div id="question-container">
                <p id="task">{{ task }}</p>
                <p>Frage:</p>
                <p id="question">{{ question }}</p> <br/><br/>

                <div class="answer-container" id="answer-buttons">
                    <button class="answer-button" id="answer-button_0" v-bind:number="button_1_number" @click="v.evaluate">{{ button_1 }}</button>
                    <button class="answer-button" id="answer-button_1" v-bind:number="button_2_number" @click="v.evaluate">{{ button_2 }}</button>
                    <button class="answer-button" id="answer-button_2" v-bind:number="button_3_number" @click="v.evaluate">{{ button_3 }}</button>
                    <button class="answer-button" id="answer-button_3" v-bind:number="button_4_number" @click="v.evaluate">{{ button_4 }}</button>
                </div>
            </div>
            <div id="statistic">
                <div v-for="(text, index) in statistic" :key="index" v-text="text"></div>
                <br/>
                <div>Richtig beantwortet: ✅<br/></div>
                <div>Falsch beantwortet: ❌<br/></div>
                <div>Nicht beantwortet: 🚫<br/></div>
            </div>

            <button id="new-task-button" @click="v.newTask">{{ new_task }}</button>
        </div>
    </main>
</template>





<script setup>
import { ref } from "vue";

let m;
let p;
let v;


let keys = ref([]);


let progress_percent = ref("0%");

let task = ref("...");
let question = ref("Wird geladen.");

let button_1 = ref("...");
let button_2 = ref("...");
let button_3 = ref("...");
let button_4 = ref("...");

let new_task = ref("Neue Frage");
let cancel_quiz = ref("Quiz abbrechen");

let statistic = ref([]);


let button_1_number = ref(1);
let button_2_number = ref(2);
let button_3_number = ref(3);
let button_4_number = ref(4);




document.addEventListener("DOMContentLoaded", function(){
    m = new Model();
    p = new Presenter();
    v = new View(p);

    p.setModelAndView(m, v);
    p.start();
});



// ======================================= Model =======================================
class Model{
    constructor(){
        this.file_path = "./quiz.json"
    }

    getJson(){
        let response = '{"lustiges quiz 123":[{"txt":"klicke die 1 an", "answers":["1","2","3","4"],"correct":["0"]},{"txt":"Welcher ist der am Weitesten von der Sonne entfernte Planet im Sonnensystem?", "answers":["Ankara","Banane","Rucola","Schachbrettmuster"],"correct":["0","2"]}],"quiz 2":[{"txt":"hallo", "answers":["1","2","3","4"],"correct":["0"]},{"txt":"eine andere Frage als im lustigen Quiz", "answers":["Ankara","Banane","Rucola","Schachbrettmuster"],"correct":["0","2"]}]}'
        const data = JSON.parse(response);

        console.log(data);
        return data;
    }
}


// ======================================= Presenter =======================================
class Presenter{
    setModelAndView(m, v){
        this.model = m;
        this.view = v;
    }

    start(){
        this.data = this.model.getJson();

        keys.value = Object.keys(this.data);
        console.log("Keys: " + keys.value);

        this.view.showQuizChoice();
    }

    getTaskSet(){
        this.view.showLoading();

        this.view.block_new_task = true;

        let task_set = this.data[this.quiz];
        console.log(task_set);

        this.view.block_new_task = false;


        const shuffled_task_set = task_set.sort((a, b) => 0.5 - Math.random());

        console.log(shuffled_task_set);

        this.task_set = shuffled_task_set;
        this.current_task_nr = 0;

        this.statistic = [];
        for(let i = 0; i < this.task_set.length; i++){
            this.statistic.push("🚫");
        }

        this.view.showTask(this.task_set[this.current_task_nr], this.current_task_nr + 1);
        this.view.setProgress(0);
    }



    getNewTask(){
        if(this.task_set){
            this.current_task_nr++;
            if(this.task_set[this.current_task_nr]){
                this.view.showTask(this.task_set[this.current_task_nr], this.current_task_nr + 1);

                if(!this.task_set[this.current_task_nr + 1]){ // Aktuelle Task ist letzte Task im Set
                    this.view.setAction(1);
                }
            }
            else this.current_task_nr--;
        }
    }

    evaluate(answer){
        console.log("Presenter -> Antwort: " + answer);

        this.view.block_new_task = true;

        console.log("correct answers: " + this.task_set[this.current_task_nr].correct);
        let success = this.task_set[this.current_task_nr].correct.includes(answer.toString());
        if(success) this.updateProgress(1);
        else this.updateProgress(0);

        this.view.block_new_task = false;

        return success;
    }

    updateProgress(success){
        if(success == 1){
            this.statistic[this.current_task_nr] = "✅";
        } else if(success == 0){
            this.statistic[this.current_task_nr] = "❌";
        }
        //this.view.liveStatistic(this.statistic, this.current_task_nr);

        let width = (this.current_task_nr+1) / this.task_set.length * 100;
        this.view.setProgress(width);
    }

    showStatistic(){
        this.view.showStatistic(this.statistic, this.task_set);
    }

    setTask(quiz){
        console.log("Presenter -> Aufgabenwahl: " + quiz);
        this.quiz = quiz;
    }
}


// ======================================= View =======================================
class View{
    constructor(p) {
        this.presenter = p;  // Presenter
        this.setAction(0);
        this.pressed = false;
        this.statistic = false;
        this.block_task_choice = false;
        this.block_new_task = false;
    }


    setAction(action){
        if(action === 0){
            this.action = 0;
            new_task.value    = "Neue Frage";
            cancel_quiz.value = "Quiz abbrechen";
        }
        if(action === 1){
            this.action = 1;
            new_task.value    = "Übersicht";
            cancel_quiz.value = "Quiz abbrechen";
        }
        if(action === 2){
            this.action = 2;
            new_task.value    = "Neue Runde";
            cancel_quiz.value = "Anderes Quiz lösen";
        }
    }




    showQuizChoice(){
        document.getElementById("menu").style.display = "flex";
        document.getElementById("middle").style.display = "none";
    }

    quizChoice(event){
        let key = event.target.id;
        console.log(key);

        this.presenter.setTask(key);

        document.getElementById("menu").style.display = "none";
        document.getElementById("middle").style.display = "flex";

        this.presenter.getTaskSet();
        this.setAction(0);
    }


    showTask(data, nr){
        console.log("show Task: " + data + " | " + nr);
        
        task.value = "Aufgabe " + nr;

        let text = data.txt;
        console.log("Task: " + text);

        let answers = data.answers;
        console.log(answers);

        let answer_order = [0, 1, 2, 3];
        answer_order = answer_order.sort((a, b) => 0.5 - Math.random());


        button_1.value = answers[answer_order[0]];
        button_2.value = answers[answer_order[1]];
        button_3.value = answers[answer_order[2]];
        button_4.value = answers[answer_order[3]];


        question.value = text;


        button_1_number.value = answer_order[0];
        button_2_number.value = answer_order[1];
        button_3_number.value = answer_order[2];
        button_4_number.value = answer_order[3];

        this.loading = false;
        this.pressed = false;
    }

    showLoading(){
        this.loading = true;
        task.value = "...";

        question.value = "Wird geladen.<br/><br/>"

        button_1.value = "...";
        button_2.value = "...";
        button_3.value = "...";
        button_4.value = "...";
    }



    setProgress(width){
        progress_percent.value = width + "%";
    }

    evaluate(event){
        console.log("View -> Evaluate: " + event.type + " " + event.target.nodeName);

        if(!this.pressed && !this.loading && !this.statistic){
            let success = this.presenter.evaluate(Number(event.target.attributes.getNamedItem("number").value));
            //-----------------------------------------------------------------------------------------
            this.color = event.target.style.backgroundColor;
            this.pressed_button = event.target.id;
            this.pressed = true;

            if(success){
                event.target.style.backgroundColor = "#269200";
                task.value = "Richtig!";
            }
            else {
                event.target.style.backgroundColor = "#ad0a0a";
                task.value = "Falsch!";
            }
        }
    }



    newTask(event){
        document.getElementById("answer-button_0").style.backgroundColor = this.color;
        document.getElementById("answer-button_1").style.backgroundColor = this.color;
        document.getElementById("answer-button_2").style.backgroundColor = this.color;
        document.getElementById("answer-button_3").style.backgroundColor = this.color;

        if(this.block_new_task) return;
        if(this.action === 0){
            this.statistic = false;
            if(this.pressed && !this.loading){
                console.log("new-task: " + event.type + " Color: " + this.color);
                // mit getElementById alle buttons zurücksetzen
                console.log("ID: " + this.pressed_button);
                document.getElementById(this.pressed_button).style.backgroundColor = this.color;
                this.pressed = false;
            }
            if(!this.loading) this.presenter.updateProgress(-1);

            this.presenter.getNewTask();
        }
        else if(this.action === 1){
            this.setAction(2);

            this.presenter.updateProgress(-1);
            this.presenter.showStatistic();
        }
        else if(this.action === 2){
            this.setAction(0);

            this.statistic = false;

            document.getElementById("question-container").style.display = "block";
            document.getElementById("statistic").style.display = "none";

            this.setProgress(0);

            //document.getElementById("live-statistic").innerHTML = "";

            this.presenter.getTaskSet();
        }
    }

    cancelQuiz(){
        this.setAction(2);
        this.newTask();
        this.presenter.start();
    }



    showStatistic(statistic_data, task_set){

        this.statistic = true;

        statistic.value = [];

        document.getElementById("question-container").style.display = "none";
        document.getElementById("statistic").style.display = "block";

        for(let i = 0; i < task_set.length; i++){
            let text = String(task_set[i].txt);
            text = text.replaceAll("<br/>", ", ");

            statistic.value.push((i + 1) + ": " + statistic_data[i] + " " + text);
        }

        return;
    }
}
</script>