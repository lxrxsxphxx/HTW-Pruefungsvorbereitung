import { createRouter, createWebHistory } from 'vue-router'

import StartseiteView from '@/views/StartseiteView.vue'
import JetztlernenView from '@/views/JetztlernenView.vue'
import QuizEingabe from '@/views/quiz-eingabe.vue'
import QuizLoesen from '@/views/quiz-loesen.vue'
import Karteikarten from '@/views/karteikarten.vue'
import ModulWaehlen from '@/views/modul-waehlen.vue'
import LernsetWaehlen from '@/views/lernset-waehlen.vue'
import ModulWaehlenView from '@/views/ModulWaehlenView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Startseite',
      component: StartseiteView,
    },
    {
      path: '/lernen',
      name: 'Jetztlernen',
      component: JetztlernenView,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      
    },
    {
      path: '/lernset-waehlen',
      name: 'Lernset-waehlen',
      component: LernsetWaehlen
    },
    {
      path: '/multiplechoice',
      name: 'Multiplechoice',
      component: QuizLoesen
    },
    {
      path: '/multiplechoice/erstellen',
      name: 'Quizerstellen',
      component: QuizEingabe
    },
   {
      path: '/karteikarten/:learningSetId',
      name: 'Karteikarten',
      component: Karteikarten
    },
    {
      path: '/modul-waehlen',
      name: 'Modul-waehlen',
      component: ModulWaehlen
    },
        {
      path: '/modulwahl',
      name: 'Modulwahl',
      component: ModulWaehlenView
    }
  ],
})

export default router
