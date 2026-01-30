import { createRouter, createWebHistory } from 'vue-router'

import StartseiteView from '@/views/StartseiteView.vue'
import JetztlernenView from '@/views/JetztlernenView.vue'
import LernsetErstellen from '@/views/lernset-erstellen.vue'
import QuizLoesen from '@/views/quiz-loesen.vue'
import Karteikarten from '@/views/karteikarten.vue'
import LernsetWaehlen from '@/views/lernset-waehlen.vue'
import ModulWaehlenView from '@/views/ModulWaehlenView.vue'
import PersoenlicherBereich from '@/views/persoenlicher-bereich.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Startseite',
      component: StartseiteView,
    },
    {
      path: '/lernen/:learningSetId',
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
      path: '/lernset-erstellen',
      name: 'Lernset-erstellen',
      component: LernsetErstellen
    },
   {
      path: '/karteikarten/:learningSetId',
      name: 'Karteikarten',
      component: Karteikarten
    },
    {
      path: '/modulwahl',
      name: 'Modulwahl',
      component: ModulWaehlenView
    },
    {
      path: '/user',
      name: 'Nutzer',
      component: PersoenlicherBereich
    }
  ],
})

export default router
