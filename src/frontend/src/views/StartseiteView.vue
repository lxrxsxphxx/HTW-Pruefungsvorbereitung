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
        <button>
          <img src="@/assets/img/jetztLernen.png" alt="LernenButton" class="lernen-button" />
        </button>
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
/* Deine Styles wie oben eingefügt */
</style>

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

.intro p {
  font-size: 20px;
  margin: 0px;
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

.lernen-button,
.kurs-button,
.statistiken-button {
  width: 100%;
  height: auto;
  margin-bottom: 10px;
  background: white;
  border-radius: 10px;
}
</style>
