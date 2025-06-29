<template>
  <div class="container">
    <section class="intro">
      <h1>Lernmodus auswählen</h1>
    </section>

    <section class="features">
      <div>
        <RouterLink to="/karteikarten">
          <button>
            <img src="@/assets/img/Karteikarten.png" alt="Karteikartenbutton" class="karteikarten-button" />
          </button>
        </RouterLink>
      </div>
      <div>
        <RouterLink to="/multiplechoice">
          <button>
            <img src="@/assets/img/MultipleChoice.png" alt="MultipleChoiceButton" class="multipleChoice-button" />
          </button>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "Jetztlernen"
};

</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.intro {
  background-color: rgba(249, 155, 32, 0.308);
  border-radius: 10px;
  padding: 30px 20px;
  text-align: center;
  margin-bottom: 20px;
}

.intro h1 {
  margin-top: -5px;
  color: orange;
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 30px;
  text-align: center;
}

.features {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
  background: transparent;
}

.features > div {
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

.features button {
  background: transparent;
  border: none;
  padding: 0;
  margin: 0;
  cursor: pointer;
}

.karteikarten-button,
.multipleChoice-button {
  width: 100%;
  height: auto;
  max-width: 250px;
  margin-bottom: 10px;
  background: white;
  border-radius: 10px;
}
.features img {
  width: 100%;
  height: auto;
  max-width: 250px;
  aspect-ratio: 1 / 1;
  background: white;
  border-radius: 10px;
  object-fit: contain;
  transition: transform 0.2s ease;
}

.features img:hover {
  transform: scale(1.20);
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


.container{
  height: 2000px;
  width: 2000px;
}

.intro{
  margin-top: 100px;
  height: auto;
  width: 150%;
  margin-left: -25%;
}

.intro h1{
  font-size: 80px;
}

.features > div {
    margin-top: 100px;
    width: 100%;    
  }

.features{
    gap: 5rem;
  }

.features img{
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