<template>
  <div class="app-container">
    <nav>
      <RouterLink v-slot="{ navigate, isActive }" to="/lernen" custom>
        <button class="control-button" id="change-learning-mode-button" @click="navigate"
          :class="{ active: isActive }">Lernmodus wechseln</button>
      </RouterLink>
    </nav>

    <section id="quizSection">
      <h2>Abfrage</h2>
      <label for="quizSubjectSelect">Fach / Modul wählen:</label>
      <select id="quizSubjectSelect" v-model="quizSubject">
        <option value="">-- Bitte wählen --</option>
        <option v-for="subject in subjects" :key="subject" :value="subject">
          {{ subject }}
        </option>
      </select>

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
import { ref, computed, watch, onMounted } from "vue";
import FlashCard from "@/components/FlashCard.vue";

// API Base URL
const API_BASE = "http://localhost:8000/api/cards";

// Karten aus der API laden
const cards = ref([]);
const loading = ref(false);


// API Funktionen
async function loadCards() {
  loading.value = true;
  try {
    const response = await fetch(API_BASE);
    if (!response.ok) throw new Error('Failed to load cards');
    const apiCards = await response.json();

    // Backend-Format zu Frontend-Format konvertieren
    cards.value = apiCards.map(card => ({
      id: card.id,
      subject: card.modul,
      question: card.front,
      answer: card.back
    }));
  } catch (error) {
    console.error('Error loading cards:', error);
    alert('Fehler beim Laden der Karten!');
  }
  loading.value = false;
}


// Beim Start Karten laden
onMounted(() => {
  loadCards();
});

// Liste aller eindeutigen Fächer
const subjects = computed(() => {
  return [...new Set(cards.value.map((c) => c.subject))].sort();
});


// Quiz-bezogene Daten
const quizSubject = ref("");
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

// Sichtbarkeiten Quiz UI
const quizCardVisible = ref(false);
const answerInputVisible = ref(false);
const progressVisible = ref(false);

// Fortschritt in Prozent
const progressPercent = computed(() => {
  if (quizCards.value.length === 0) return 0;
  return ((currentIndex.value) / quizCards.value.length) * 100;
});

// Aktuelle Karte im Quiz
const currentQuizCard = computed(() => {
  return quizCards.value[currentIndex.value] || null;
});

const statsText = computed(() => {
  let base = `Richtig: ${correctCount.value} | Falsch: ${incorrectCount.value}`;
  if (!quizCardVisible.value && quizCards.value.length > 0) {
    base += " | Quiz beendet!";
  }
  return base;
});


// --- Quiz-Funktionen ---

// Quiz vorbereiten, wenn Fach gewählt wurde
watch(quizSubject, (newSubject) => {
  if (!newSubject) {
    quizCards.value = [];
    quizCardVisible.value = false;
    answerInputVisible.value = false;
    progressVisible.value = false;
    resetQuiz();
    return;
  }
  // Alle Karten mit diesem Fach filtern
  quizCards.value = cards.value.filter((c) => c.subject === newSubject);
  if (quizCards.value.length === 0) {
    alert("Keine Karteikarten für dieses Fach vorhanden.");
    quizCardVisible.value = false;
    answerInputVisible.value = false;
    progressVisible.value = false;
    resetQuiz();
    return;
  }
  shuffleArray(quizCards.value);
  currentIndex.value = 0;
  correctCount.value = 0;
  incorrectCount.value = 0;
  quizCardVisible.value = true;
  answerInputVisible.value = true;
  progressVisible.value = true;
  userAnswer.value = "";
  isFlipped.value = false;
  waitingForFlipBack.value = false;
});

function nextQuestion(click) {
  if (currentIndex.value + 1 >= notes.value.length) {
    flippedOnce.value = false;
    answered.value = false;
    if (currentIndex.value >= notes.value.length) {
      notes.value.push(userAnswer.value);
      if (click == "good") {
        goodCards.value++;
      } else if (click = "okay") {
        okayCards.value++;
      } else if (click = "bad") {
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

// Quiz komplett zurücksetzen
function resetQuiz() {
  quizCards.value = [];
  currentIndex.value = 0;
  correctCount.value = 0;
  incorrectCount.value = 0;
  userAnswer.value = "";
  waitingForFlipBack.value = false;
  isFlipped.value = false;
  quizCardVisible.value = false;
  answerInputVisible.value = false;
  progressVisible.value = false;
  quizSubject.value = "";
}

// Hilfsfunktion: Array mischen (Fisher-Yates)
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

section {
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 6px;
  background: #ffefc4;
}

/* Quiz */
#answerInputArea {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 15px;
}

#answerInputArea textarea {
  height: 8rem;
  padding: 8px;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #aaa;
  resize: none;
}

#answerInputArea button {
  padding: 8px 16px;
  font-size: 1rem;
  background-color: #cc7a00;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

#answerInputArea button:disabled {
  background-color: #9c5c08;
  cursor: default;
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
  background-color: #cc7a00;
  ;
  width: 0%;
  transition: width 0.3s ease;
}

/* Statistik */
#stats {
  text-align: center;
  font-weight: bold;
  margin-top: 5px;
}

/* Loading */
.loading {
  text-align: center;
  padding: 20px;
  font-style: italic;
  color: #666;
}
</style>
