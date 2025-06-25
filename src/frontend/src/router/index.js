import { createRouter, createWebHistory } from 'vue-router'

import StartseiteView from '@/views/StartseiteView.vue'
import JetztlernenView from '@/views/JetztlernenView.vue'
import QuizEingabe from '@/views/quiz-eingabe.vue'
import QuizLoesen from '@/views/quiz-loesen.vue'

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
      path: '/multiplechoice',
      name: 'Multiplechoice',
      component: QuizLoesen
    },
    {
      path: '/multiplechoice/erstellen',
      name: 'Quizerstellen',
      component: QuizEingabe
    }
  ],
})

export default router
