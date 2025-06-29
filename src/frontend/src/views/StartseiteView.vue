<template>
  <div class="container">
    <section class="intro">
      <h1>HTW-Prüfungsvorbereiter</h1>
      <p>Bereit für die Prüfung – mit deiner HTW-Lernplattform.</p>
    </section>

    <section class="features">
      <div class="btn-links">
        <button>
          <img src="@/assets/img/Kurse.png" alt="Kursbutton" class="kurs-button" />
        </button>
      </div>
      <div class="btn-mitte">
        <RouterLink to="/lernen">
          <button>
            <img src="@/assets/img/jetztLernen.png" alt="LernenButton" class="lernen-button" />
          </button>
        </RouterLink>
      </div>
      <div class="btn-rechts">
        <button>
          <img src="@/assets/img/Statistiken.png" alt="StatistikenButton" class="statistiken-button" />
        </button>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "Startseite"
};
</script>



<style scoped>
/* Basiseinstellungen */
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 1rem;
}

.intro {
  background-color: rgba(249, 155, 32, 0.308);
  border-radius: 10px;
  padding: 2rem;
  text-align: center;
  margin-bottom: 2rem;
}

.intro h1 {
  font-size: 2.5rem;
  color: #ec852c;
  font-weight: bold;
  margin-bottom: 1rem;
}

.intro p {
  font-size: 1.25rem;
  margin: 0;
}

.features {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.features > div {
  text-align: center;
}

.features button {
  background: transparent;
  border: none;
  cursor: pointer;
  width: 100%;
}

.features img {
  width: 100%;
  height: auto;
  border-radius: 10px;
  background: white;
  object-fit: contain;
}

.features img {
  width: 100%;
  height: auto;
  max-width: 100%;
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
  
  .features > div {
    width: 30%;
  }
}

/* Extra Large: Große Monitore */
@media screen and (min-width: 1480px) {


  
  .intro {
    margin-top: 90px;
  }
  .container {
  
  max-width: 2000px;
  margin: 0 auto;
  padding: 1rem;
  
}
  .features > div {
    margin-top: 100px;
    width: 25%;
    
  }

  .features{
    gap: 5rem;
  }

  .intro{
    width: 90%;
    margin-left: 5%;
  }
  .intro h1{
    font-size: 80px;
  }

  .intro p{
    font-size:2.0rem ;
  }

  .features img{
    width: 90%;
    height: 90%;
  }
}
</style>








