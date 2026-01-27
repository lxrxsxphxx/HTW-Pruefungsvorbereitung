<template>
  <div class="container">
    <section class="intro">
      <h1>HTW-Prüfungsvorbereiter</h1>
      <p>Bereit für die Prüfung – mit deiner HTW-Lernplattform.</p>
    </section>

    <section class="features">
      <div class="btn-links">
        <RouterLink to="/modulwahl">
          <button>
            <img src="@/assets/img/book.png" alt="Kursbutton" class="kurs-button" />
            <p>Module</p>
          </button>
        </RouterLink>
      </div>
      <div class="btn-mitte">
        <RouterLink to="/modul-waehlen">
          <button>
            <img src="@/assets/img/checkmark.png" alt="LernenButton" class="lernen-button" />
            <p>Jetzt Lernen</p>
          </button>
        </RouterLink>
      </div>
      <div class="btn-rechts">
        <button>
          <img src="@/assets/img/bars.png" alt="StatistikenButton" class="statistiken-button" />
          <p>Statistiken</p>
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
  border-radius: 10px;
  padding: 2rem;
  text-align: center;
  margin-bottom: 2rem;
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
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.features>div {
  text-align: center;
}

.features button {
  border: none;
  cursor: pointer;
  width: 100%;
  border-radius: 10px;
}

.features img {
  width: 50%;
  height: auto;
  max-width: 100%;
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

.features button {
  aspect-ratio: 1 / 1;
}



/* Large: Desktop */
@media screen and (min-width: 1080px)
/*and (max-width: 1479px) */
  {
  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 1rem;
  }

  .features>div {
    width: 30%;
  }
}

/* Extra Large: Große Monitore 
@media screen and (min-width: 1480px) {


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

  .intro h1{
    font-size: 80px;
  }

  .intro p{
    font-size:2.0rem ;
  }
}*/
</style>
