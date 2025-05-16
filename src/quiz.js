"use strict";

let model, presenter, view;

document.addEventListener('DOMContentLoaded', function(){
    model = new Model();
    presenter = new Presenter();
    view = new View(presenter);

    presenter.setModelAndView(model, view);
    presenter.start();
});


/* ---------------------------- Model ---------------------------- */
class Model{
    getQuestionSet(id){
        let json_quiz_set = fetch("quiz.json");

        let question_set = json_quiz_set.sets[id];
        return question_set;
    }
}



/* ---------------------------- Presenter ---------------------------- */
class Presenter{

    setModelAndView(m, v){
        this.model = m;
        this.view = v;
    }

    start(){
        console.log("started");
    }

    getQuiz(id){
        const question_set = this.model.getQuestionSet(id);

        const shuffled_question_set = question_set.sort((a, b) => 0.5 - Math.random());
        return shuffled_question_set;
    }
}



/* ---------------------------- View ---------------------------- */
class View{
    constructor(p){
        this.presenter = p;
    }

    playQuiz(id){
        const quiz = this.presenter.getQuiz(id);

        let question_num;
        for(question_num = 0; question_num < quiz.length; question_num++){

            // TODO: überlegen, ob Schlwife sinnvoll
            console.log(quiz[question_num].a);
        }
    }
}