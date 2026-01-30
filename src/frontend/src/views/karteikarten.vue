<template>
  <div class="app-container">
    <nav>
      <RouterLink v-slot="{ navigate, isActive }" :to="'/lernen/'+learningSetId" custom>
        <button class="control-button" id="change-learning-mode-button" @click="navigate"
          :class="{ active: isActive }">Zurück zum Lernset</button>
      </RouterLink>
    </nav>

    <section id="quizSection">
      <h2>Abfrage</h2>

      <FlashCard :question="currentQuizCard?.question" :answer="currentQuizCard?.answer" :is-flipped="isFlipped"
        v-show="quizCards?.length > 0 && quizCardVisible"></FlashCard>

      <div id="answerInputArea" v-show="quizCards?.length > 0 && answerInputVisible">
        <textarea id="userAnswer" v-model="userAnswer" placeholder="Notizen" autocomplete="off"
          :disabled="flippedOnce" />
        <button id="seeAnswerBtn" @click="seeAnswer" v-show="!isFlipped">
          Antwort anzeigen
        </button>
        <button id="skipQuestionBtn" @click="skipQuestion" v-show="!flippedOnce">
          Frage überspringen
        </button>
        <button id="seeQuestionBtn" @click="seeQuestion" v-show="isFlipped">
          Zurück zur Frage
        </button>
        <div class="rating" v-show="flippedOnce">
          <button id="badBtn" @click="nextQuestion('bad')" v-show="flippedOnce && !answered">
            Nicht gewusst
          </button>
          <button id="okayBtn" @click="nextQuestion('okay')" v-show="flippedOnce && !answered">
            Teilweise gewusst
          </button>
          <button id="goodBtn" @click="nextQuestion('good')" v-show="flippedOnce && !answered">
            Vollständig gewusst
          </button>
        </div>
        <button id="nextBtn" @click="nextQuestion('next')" v-show="flippedOnce && answered">
          Nächste Frage
        </button>
        <button id="prevQuestionBtn" @click="prevQuestion" v-show="!firstQuestion">
          Zurück zur vorherigen Frage
        </button>
      </div>

      <div id="progressContainer" v-show="quizCards.length > 0 && progressVisible">
        <div id="progressBar" :style="{ width: progressPercent + '%' }"></div>
      </div>

      <div id="stats">{{ statsText }}</div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import FlashCard from "@/components/FlashCard.vue";
import { useRoute } from "vue-router";


// API Base URL
const API_BASE = `${import.meta.env.VITE_API_URL}/cards`;

// API data
const cards = ref([]);
const loading = ref(false);
const route = useRoute();
const learningSetId = ref(0);

/**
 * function to load data from api
 */
async function loadCards() {
  loading.value = true;
  try {
    learningSetId.value = route.params.learningSetId;
    const response = await fetch(API_BASE + `?learning_set_id=${learningSetId.value}`, {credentials: "include"});
    if (!response.ok) throw new Error('Failed to load cards');
    const apiCards = await response.json();

    cards.value = apiCards.map(card => ({
      id: card.id,
      question: card.front,
      answer: card.back
    }));
  } catch (error) {
    console.error('Error loading cards:', error);
    alert('Fehler beim Laden der Karten!');
  }
  loading.value = false;
  quizCards.value = cards.value;
  shuffleArray(quizCards.value);

  quizCardVisible.value = true;
  answerInputVisible.value = true;
  progressVisible.value = true;
}


/**
 * load cards from api when view is mounted
 */
onMounted(() => {
  loadCards();
});


// variables for flash card learning
const quizCards = ref([]);
const currentIndex = ref(0);
const goodCards = ref(0);
const okayCards = ref(0);
const badCards = ref(0);
const userAnswer = ref("");
const flippedOnce = ref(false);
const answered = ref(false);
const isFlipped = ref(false);
const firstQuestion = ref(true);
const notes = ref([]);

// ui visibility variables
const quizCardVisible = ref(false);
const answerInputVisible = ref(false);
const progressVisible = ref(false);

/**
 * computed value for percent of progress
 */
const progressPercent = computed(() => {
  if (quizCards.value.length === 0) return 0;
  return ((currentIndex.value) / quizCards.value.length) * 100;
});

/**
 * computed for the current flash card
 */
const currentQuizCard = computed(() => {
  return quizCards.value[currentIndex.value] || null;
});

/**
 * computed text for stats at the end of learning
 */
const statsText = computed(() => {
  let base = `${currentIndex.value}/${quizCards.value.length}`;
  if (!quizCardVisible.value && quizCards.value.length > 0) {
    base = "Quiz beendet!\n";
    base += `Nicht gewusst: ${badCards.value}\n`;
    base += `Teilweise gewusst gewusst: ${okayCards.value}\n`;
    base += `Vollständig gewusst: ${goodCards.value}\n`;
    base += `Gewusste Karten: ${Math.round(goodCards.value / quizCards.value.length * 100)} %`
  }
  return base;
});


/**
 * function to flip the flash card to back side
 */
function seeAnswer() {
  isFlipped.value = true;
  flippedOnce.value = true;
}

/**
 * function to flip the flash card to front side
 */
function seeQuestion() {
  isFlipped.value = false;
}


/**
 * function to set the self rating for a flash card or next for already rated card
 * saves notes to the card for later reuse
 * @param rating rating given by the student : 'good', 'ok', 'bad', 'next'
 */
function nextQuestion(rating) {
  if (currentIndex.value + 1 >= notes.value.length) {
    flippedOnce.value = false;
    answered.value = false;
    if (currentIndex.value >= notes.value.length) {
      notes.value.push(userAnswer.value);
      if (rating == "good") {
        goodCards.value++;
      } else if (rating = "okay") {
        okayCards.value++;
      } else if (rating = "bad") {
        badCards.value++;
      }
    }
    userAnswer.value = "";

  } else {
    userAnswer.value = notes.value[currentIndex.value + 1];
  }

  if (isFlipped.value) {
    setTimeout(() => {
      currentIndex.value++;
    }, 600);
  } else {
    currentIndex.value++;
  }
  isFlipped.value = false;
  firstQuestion.value = false;


  if (currentIndex.value + 1 >= quizCards.value.length) {
    quizCardVisible.value = false;
    answerInputVisible.value = false;
    progressVisible.value = false;
  }
}

/**
 * function to go back to the last flash card
 * also sets notes of the corresponding card back into the notes field
 */
function prevQuestion() {
  if (isFlipped.value) {
    isFlipped.value = false;
    setTimeout(() => {
      currentIndex.value--;
      if (currentIndex.value === 0) {
        firstQuestion.value = true;
      }
      userAnswer.value = notes.value[currentIndex.value];
    }, 600);
  }
  else {
    currentIndex.value--;
    if (currentIndex.value === 0) {
      firstQuestion.value = true;
    }
    userAnswer.value = notes.value[currentIndex.value];
  }
  flippedOnce.value = true;
  answered.value = true;
}

/**
 * function to skip the current flash card and append it at the end
 */
function skipQuestion() {
  isFlipped.value = false;
  flippedOnce.value = false;

  const skipped = quizCards.value.splice(currentIndex.value, 1);
  quizCards.value.push(skipped[0]);


  userAnswer.value = "";
  if (currentIndex.value >= quizCards.value.length) {
    quizCardVisible.value = false;
    answerInputVisible.value = false;
    progressVisible.value = false;
  }
}

/**
 * function to shuffle an array, acts of the array itself
 * @param array the array to be shuffled
 */
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}
</script>

<style scoped>
.app-container {
  max-width: 600px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}

nav {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
}

nav button {
  padding: 8px 12px;
  font-size: 1rem;
  cursor: pointer;
}

/* Quiz */
#answerInputArea {
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
  margin-bottom: 15px;
}

.rating {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  justify-content: center;
}

#answerInputArea textarea {
  height: 8rem;
  padding: 8px;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #aaa;
  resize: none;
}

#answerInputArea textarea:disabled {
  background-color: #ebebeb;
}


#answerInputArea button {
  padding: 8px 16px;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* Fortschrittsbalken */
#progressContainer {
  width: 100%;
  height: 20px;
  background-color: #ddd;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
}

#progressBar {
  height: 100%;
  background-color: var(--htw-orange);
  width: 0%;
  transition: width 0.3s ease;
}

/* Statistik */
#stats {
  text-align: center;
  font-weight: bold;
  margin-top: 5px;
  white-space: pre;
}

/* Loading */
.loading {
  text-align: center;
  padding: 20px;
  font-style: italic;
  color: #666;
}
</style>
