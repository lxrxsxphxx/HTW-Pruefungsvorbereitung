<script setup>
import { computed } from "vue";
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
const {question, answer, isFlipped} = defineProps(['question', 'answer', 'isFlipped']);

    const answertext = computed(() => {
      if (answer)
        return marked.parse(answer)
      else return "test"})
</script>

<template>
    <div class="quizCard" 
        :class="[{ flipped: isFlipped }]">
        <div class="cardInner">
          <div class="card-front">
            <p>{{ question }}</p>
            <div class="htw-stripe"><img src="@/assets/img/HtwLogo_black.png"></img></div>
          </div>
          <div class="card-back">
            <p v-html="answertext"></p>
            <div class="htw-stripe"><img src="@/assets/img/HtwLogo_black.png"></img></div>
          </div>
        </div>
      </div>
</template>

<style scoped>

.quizCard {
  width: 100%;
  height: 11rem;
  perspective: 1000px;
  margin: 20px 0;
}

.cardInner {
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

.quizCard.flipped .cardInner {
  transform: rotateY(180deg);
}

.card-front,
.card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-top: auto;
  box-sizing: border-box;
}

.card-front p,
.card-back p {
  margin-top: auto;
  color: black;
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

.card-back {
  transform: rotateY(180deg);
  font-weight: bold;
}

</style>