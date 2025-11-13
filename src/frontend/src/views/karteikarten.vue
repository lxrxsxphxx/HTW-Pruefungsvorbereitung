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

      <div id="quizCard" v-show="quizCards.length > 0 && quizCardVisible"
        :class="[cardResultColor, { flipped: isFlipped }]">
        <div id="cardInner">
          <div class="card-front" id="quizQuestion">
            <p>{{ currentQuizCard?.question }}</p>
            <div class="htw-stripe"><img src="@/assets/img/HtwLogo_black.png"></img></div>
          </div>
          <div class="card-back" id="correctAnswer">
            <p>{{ currentQuizCard?.answer }}</p>
            <div class="htw-stripe"><img src="@/assets/img/HtwLogo_black.png"></img></div>
          </div>
        </div>
      </div>

      <div id="answerInputArea" v-show="quizCards.length > 0 && answerInputVisible">
        <input type="text" id="userAnswer" v-model="userAnswer" placeholder="Deine Antwort hier eingeben"
          autocomplete="off" :disabled="waitingForFlipBack" @keyup.enter="checkAnswer" />
        <button id="checkAnswerBtn" @click="checkAnswer" :disabled="waitingForFlipBack || !userAnswer.trim()">
          Antwort prüfen
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

// API Base URL
const API_BASE = "http://localhost:8000/api/cards";

// Karten aus der API laden
const cards = ref([]);
const loading = ref(false);
const cardResultColor = ref(""); // '' | 'correct' | 'incorrect'


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
const correctCount = ref(0);
const incorrectCount = ref(0);
const userAnswer = ref("");
const waitingForFlipBack = ref(false);
const isFlipped = ref(false);

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

// Antwort prüfen
function checkAnswer() {
  if (waitingForFlipBack.value) return;
  if (!userAnswer.value.trim()) return;

  isFlipped.value = true;
  waitingForFlipBack.value = true;

  const correct = currentQuizCard.value.answer
    .trim()
    .toLowerCase()
    .includes(userAnswer.value.trim().toLowerCase());

  if (correct) {
    correctCount.value++;
    cardResultColor.value = "correct";
  } else {
    incorrectCount.value++;
    cardResultColor.value = "incorrect";
  }

  setTimeout(() => {
    isFlipped.value = false;
    waitingForFlipBack.value = false;
    cardResultColor.value = "";
    userAnswer.value = "";
    currentIndex.value++;

    if (currentIndex.value >= quizCards.value.length) {
      quizCardVisible.value = false;
      answerInputVisible.value = false;
      progressVisible.value = false;
    }
  }, 1500);
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

form label {
  display: block;
  margin-top: 10px;
  font-weight: bold;
}

form input[type="text"],
form textarea,
form select {
  width: 100%;
  padding: 6px;
  margin-top: 4px;
  border: 1px solid #aaa;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
  resize: vertical;
}

form textarea {
  height: 80px;
}

form button {
  margin-top: 15px;
  padding: 10px 16px;
  font-size: 1rem;
  background-color: #cc7a00;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

form button:hover {
  background-color: #9e6207;
}

/* Kartenliste */
#cardsList {
  margin-top: 15px;
}

.card-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  background: white;
  border-radius: 4px;
  position: relative;
}

.card-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}

.card-actions button {
  cursor: pointer;
  background-color: #e1e1e1;
  border: none;
  padding: 6px 10px;
  border-radius: 4px;
}

.card-actions button:hover {
  background-color: #c0c0c0;
}

#noCardsMsg {
  font-style: italic;
  color: #555;
}

/* Filter */
#filterSection {
  margin-bottom: 10px;
}

#filterSection label {
  margin-right: 5px;
}

/* Quiz */
#quizCard {
  width: 100%;
  height: 150px;
  perspective: 1000px;
  margin: 20px 0;
}

#quizCard.correct #cardInner {
  background-color: #e0f7e0;
  border: 2px solid #2e7d32;
}

#quizCard.incorrect #cardInner {
  background-color: #fdecea;
  border: 2px solid #c62828;
}

#cardInner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.8s;
  transform-style: preserve-3d;
  border: 1px solid #aaa;
  border-radius: 6px;
  background: white;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  text-align: center;
}

#quizCard.flipped #cardInner {
  transform: rotateY(180deg);
}

.card-front,
.card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  box-sizing: border-box;
}

.card-back {
  transform: rotateY(180deg);
  font-weight: bold;
}

#answerInputArea {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 15px;
}

#answerInputArea input {
  flex-grow: 1;
  padding: 8px;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #aaa;
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

.card-front p,
.card-back p {
  margin-top: auto;
}

.htw-stripe {
  width: 100%;
  height: 2rem;
  background-color: var(--htw-orange);
  margin-top: auto;
  text-align: right;
  justify-self: end;
}

.htw-stripe img {
  width: auto;
  height: 2rem;
}
</style>
