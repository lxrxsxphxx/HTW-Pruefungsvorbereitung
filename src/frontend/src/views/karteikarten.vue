<template>
  <div class="app-container">
    <nav>
      <button @click="showSection('create')">Neue Karteikarte erstellen</button>
      <button @click="showSection('cards')">Erstellte Karteikarten</button>
      <button @click="showSection('quiz')">Abfrage starten</button>
    </nav>

    <section v-show="currentSection === 'create'" id="createSection">
      <h2>Neue Karteikarte erstellen</h2>
      <form @submit.prevent="onSubmit">
        <label for="subjectInput">Fach / Modul:</label>
        <input
          id="subjectInput"
          v-model="form.subject"
          required
          placeholder="z.B. Mathe"
          type="text"
        />

        <label for="topicInput">Lerngebiet:</label>
        <input
          id="topicInput"
          v-model="form.topic"
          required
          placeholder="z.B. Algebra"
          type="text"
        />

        <label for="questionInput">Frage:</label>
        <textarea
          id="questionInput"
          v-model="form.question"
          required
        ></textarea>

        <label for="answerInput">Antwort:</label>
        <textarea
          id="answerInput"
          v-model="form.answer"
          required
        ></textarea>

        <button type="submit">Karte speichern</button>
      </form>
    </section>

    <section v-show="currentSection === 'cards'" id="cardsSection">
      <h2>Erstellte Karteikarten</h2>

      <div id="filterSection">
        <label for="filterSubject">Fach filtern:</label>
        <select id="filterSubject" v-model="filter.subject">
          <option value="">-- Alle Fächer --</option>
          <option v-for="subject in subjects" :key="subject" :value="subject">
            {{ subject }}
          </option>
        </select>

        <label for="filterTopic">Lerngebiet filtern:</label>
        <select id="filterTopic" v-model="filter.topic">
          <option value="">-- Alle Lerngebiete --</option>
          <option v-for="topic in filteredTopics" :key="topic" :value="topic">
            {{ topic }}
          </option>
        </select>
      </div>

      <div id="cardsList">
        <div
          v-for="(card, index) in filteredCards"
          :key="index"
          class="card-item"
        >
          <strong>Fach:</strong> {{ card.subject }} <br />
          <strong>Lerngebiet:</strong> {{ card.topic }} <br />
          <strong>Frage:</strong> {{ card.question }} <br />
          <strong>Antwort:</strong> {{ card.answer }}
          <div class="card-actions">
            <button @click="editCard(index)">Bearbeiten</button>
            <button @click="deleteCard(index)">Löschen</button>
          </div>
        </div>
        <p v-if="filteredCards.length === 0" id="noCardsMsg">
          Keine Karteikarten vorhanden.
        </p>
      </div>
    </section>

    <section v-show="currentSection === 'quiz'" id="quizSection">
      <h2>Abfrage</h2>
      <label for="quizSubjectSelect">Fach / Modul wählen:</label>
      <select id="quizSubjectSelect" v-model="quizSubject">
        <option value="">-- Bitte wählen --</option>
        <option v-for="subject in subjects" :key="subject" :value="subject">
          {{ subject }}
        </option>
      </select>

      <div
        id="quizCard"
        v-show="quizCards.length > 0 && quizCardVisible"
        :class="{ flipped: isFlipped }"
      >
        <div id="cardInner">
          <div class="card-front" id="quizQuestion">
            {{ currentQuizCard?.question }}
          </div>
          <div class="card-back" id="correctAnswer">
            {{ currentQuizCard?.answer }}
          </div>
        </div>
      </div>

      <div id="answerInputArea" v-show="quizCards.length > 0 && answerInputVisible">
        <input
          type="text"
          id="userAnswer"
          v-model="userAnswer"
          placeholder="Deine Antwort hier eingeben"
          autocomplete="off"
          :disabled="waitingForFlipBack"
          @keyup.enter="checkAnswer"
        />
        <button
          id="checkAnswerBtn"
          @click="checkAnswer"
          :disabled="waitingForFlipBack || !userAnswer.trim()"
        >
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

<script>
import { ref, reactive, computed, watch } from "vue";

export default {
  name: "KarteikartenApp",
  setup() {
    // Karten laden oder leeres Array
    const storedCards = localStorage.getItem("flashcards");
    const cards = ref(storedCards ? JSON.parse(storedCards) : []);

    // Aktuelle Sektion: 'create', 'cards', 'quiz'
    const currentSection = ref("create");

    // Formular-Daten (create/edit)
    const form = reactive({
      subject: "",
      topic: "",
      question: "",
      answer: "",
    });

    let editIndex = ref(null);

    // Filter für Karten-Liste
    const filter = reactive({
      subject: "",
      topic: "",
    });

    // Liste aller eindeutigen Fächer
    const subjects = computed(() => {
      return [...new Set(cards.value.map((c) => c.subject))].sort();
    });

    // Liste der Lerngebiete gefiltert nach Fach
    const filteredTopics = computed(() => {
      if (!filter.subject) return [];
      return [
        ...new Set(
          cards.value.filter((c) => c.subject === filter.subject).map((c) => c.topic)
        ),
      ].sort();
    });

    // Karten gefiltert nach Fach und Lerngebiet
    const filteredCards = computed(() => {
      return cards.value.filter((c) => {
        return (
          (!filter.subject || c.subject === filter.subject) &&
          (!filter.topic || c.topic === filter.topic)
        );
      });
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
      if (currentSection.value === "quiz" && !quizCardVisible.value && quizCards.value.length > 0) {
        base += " | Quiz beendet!";
      }
      return base;
    });

    // Karte speichern (neu oder editieren)
    function onSubmit() {
      if (
        !form.subject.trim() ||
        !form.topic.trim() ||
        !form.question.trim() ||
        !form.answer.trim()
      ) {
        alert("Bitte alle Felder ausfüllen!");
        return;
      }

      const newCard = {
        subject: form.subject.trim(),
        topic: form.topic.trim(),
        question: form.question.trim(),
        answer: form.answer.trim(),
      };

      if (editIndex.value !== null) {
        cards.value.splice(editIndex.value, 1, newCard);
        editIndex.value = null;
      } else {
        cards.value.push(newCard);
      }
      saveCards();
      resetForm();
      showSection("cards");
    }

    function resetForm() {
      form.subject = "";
      form.topic = "";
      form.question = "";
      form.answer = "";
    }

    function saveCards() {
      localStorage.setItem("flashcards", JSON.stringify(cards.value));
    }

    function showSection(section) {
      currentSection.value = section;

      if (section === "cards") {
        // Filter zurücksetzen (optional)
        // filter.subject = "";
        // filter.topic = "";
      }
      if (section === "quiz") {
        prepareQuizSubjects();
        resetQuiz();
      }
    }

    // Karte bearbeiten: Formular füllen und auf create wechseln
    function editCard(index) {
      const c = filteredCards.value[index];
      // find original index in cards.value (because filteredCards is filtered)
      const originalIndex = cards.value.findIndex(
        (card) =>
          card.subject === c.subject &&
          card.topic === c.topic &&
          card.question === c.question &&
          card.answer === c.answer
      );
      if (originalIndex !== -1) {
        editIndex.value = originalIndex;
        form.subject = c.subject;
        form.topic = c.topic;
        form.question = c.question;
        form.answer = c.answer;
        showSection("create");
      }
    }

    // Karte löschen
    function deleteCard(index) {
      const c = filteredCards.value[index];
      if (
        confirm(
          `Karteikarte zu Fach "${c.subject}", Lerngebiet "${c.topic}" wirklich löschen?`
        )
      ) {
        // Karte im Original-Array finden und löschen
        const originalIndex = cards.value.findIndex(
          (card) =>
            card.subject === c.subject &&
            card.topic === c.topic &&
            card.question === c.question &&
            card.answer === c.answer
        );
        if (originalIndex !== -1) {
          cards.value.splice(originalIndex, 1);
          saveCards();
        }
      }
    }

    // --- Quiz-Funktionen ---

    function prepareQuizSubjects() {
      // Diese Funktion kann erweitert werden, falls nötig
      // aktuell werden subjects automatisch aus cards.value ermittelt
    }

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

      // Vergleich Antwort - einfache Groß-/Kleinschreibung ignorieren
      const correct = currentQuizCard.value.answer
        .trim()
        .toLowerCase()
        .includes(userAnswer.value.trim().toLowerCase());

      if (correct) {
        correctCount.value++;
      } else {
        incorrectCount.value++;
      }

      // 1,5 Sekunden warten, Karte zurückdrehen, nächste Karte laden
      setTimeout(() => {
        isFlipped.value = false;
        waitingForFlipBack.value = false;
        userAnswer.value = "";
        currentIndex.value++;
        if (currentIndex.value >= quizCards.value.length) {
          // Quiz Ende
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

    return {
      currentSection,
      showSection,
      form,
      onSubmit,
      cards,
      filter,
      filteredCards,
      subjects,
      filteredTopics,
      editCard,
      deleteCard,
      // Quiz
      quizSubject,
      quizCards,
      currentQuizCard,
      userAnswer,
      checkAnswer,
      isFlipped,
      waitingForFlipBack,
      quizCardVisible,
      answerInputVisible,
      progressVisible,
      progressPercent,
      statsText,
      resetQuiz,
    };
  },
};
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
  background: #f9f9f9;
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
  background-color: #0077cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

form button:hover {
  background-color: #005fa3;
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
  background-color: #e0f7e0;
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
  background-color: #0077cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

#answerInputArea button:disabled {
  background-color: #9fc0e6;
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
  background-color: #0077cc;
  width: 0%;
  transition: width 0.3s ease;
}

/* Statistik */
#stats {
  text-align: center;
  font-weight: bold;
  margin-top: 5px;
}
</style>
