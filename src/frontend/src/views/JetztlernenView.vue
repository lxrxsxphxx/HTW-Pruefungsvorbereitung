<template>
  <div class="container">
    <section class="intro">
      <h1>"{{ learningSet.name }}" ausgewählt</h1>
      <p>Für dein ausgewähltes Lernset wurden {{ learningSet.cards.length }} Karteikarten und {{
        learningSet.questions.length }} Multiple Choice Fragen hinterlegt.</p>
        <p>Bitte wähle einen Lernmodus</p>
    </section>

    <section class="features">
      <div>
        <RouterLink :to="'/karteikarten/' + learningSetId">
          <button :disabled="learningSet.cards.length == 0">
            <img src="@/assets/img/Karteikarten.png" alt="Karteikartenbutton" class="karteikarten-button" />
            <p>Karteikarten</p>
          </button>
        </RouterLink>
      </div>
      <div>
        <RouterLink :to="'/multiplechoice/' + learningSetId">
          <button :disabled="learningSet.questions.length == 0">
            <img src="@/assets/img/MultipleChoice.png" alt="MultipleChoiceButton" class="multipleChoice-button" />
            <p>Multiple Choice</p>
          </button>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';


const learningSet = ref({
  questions: [],
  cards: []
});
const route = useRoute();
const learningSetId = route.params.learningSetId;

const API_BASE = "http://localhost:8000/api/learning_set/";

onMounted(async () => {
  try {
    const response = await fetch(API_BASE + learningSetId, { credentials: "include" });
    if (!response.ok) throw new Error('Failed to load cards');
    learningSet.value = await response.json();
    console.log(learningSet)
  } catch (error) {
    console.error('Error loading learn set:', error);
  }
}
)

</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.intro {
  border-radius: 10px;
  padding: 30px 20px;
  text-align: center;
  margin-bottom: 20px;
}

.intro h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.intro p {
  font-size: 1.25rem;
  font-weight: bold;
  margin: 0;
}

.features {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
  background: transparent;
}

.features>div {
  flex: 1;
  background: transparent;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  min-height: 280px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.karteikarten-button,
.multipleChoice-button {
  width: 100%;
  height: auto;
  max-width: 250px;
  margin-bottom: 10px;
}

button {
  border-radius: 10px;
  aspect-ratio: 1/1;
  width: 17rem;
}

.features img {
  width: 10rem;
  height: auto;
  max-width: 250px;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  object-fit: contain;
  transition: transform 0.2s ease;
}

.features p {
  font-size: 2rem;
  font-weight: bold;
  margin-top: 1rem;
}

/* Large: Desktop */
@media screen and (min-width: 1080px) and (max-width: 1479px) {
  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 1rem;
  }
}

/* Extra Large: Große Monitore */
@media screen and (min-width: 1480px) {


  .container {
    height: 2000px;
    width: 2000px;
  }

  .intro {
    margin-top: 100px;
    height: auto;
    width: 150%;
    margin-left: -25%;
  }

  .intro h1 {
    font-size: 80px;
  }

  .features>div {
    margin-top: 100px;
    width: 100%;
  }

  .features {
    gap: 5rem;
  }

  .features img {
    width: 90%;
    height: 90%;
    max-width: none;
  }

  .karteikarten-button,
  .multipleChoice-button {
    width: 100%;
    max-width: none;

  }

}
</style>