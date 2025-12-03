<template>
    <h1>Lernmodus für Modul</h1> 
    <div class="Container">                     
        <div class="Body-Container">
            <RouterLink to="/lernset-erstellen" class="lernset-link">
                <img src="@/assets/img/lernseterstellen.png" alt="Lernseterstellen" class="lernseterstellenbild"></img>
                <span class="link-text">Lernset erstellen</span>
            </RouterLink>

        <div class="dropdown">
            <button class="dropbtn" @click="toggleSortieren">
            <img src="@/assets/icons/sortieren.svg" alt="Sortieren" class="sortier-icon" />
                Sortieren
            </button>

            <div v-if="istSortierSichtbar" class="dropdown-content">
                <a href="#" @click.prevent="sortierOption = 'alphabetisch'">Alphabetisch</a>
                <a href="#" @click.prevent="sortierOption = 'zuletzt'">Zuletzt verwendet</a>
            </div>
        </div>   
    </div>
    <!--Ende: Body-Container-->

    <!--Start: Content-Container-->
    <div class="Content-Container">
        <div class="scroll-section">
            <h2>Meine Lernsets</h2>
                <div class="scroll-row">
                     
                        <LernsetCard 
                         v-for="set in lernsets"
                         :key="set.setId"
                         :title="set.name"
                        />

                    </div>
            
            <h2>Beliebt</h2>
                <div class="scroll-row">
                   <LernsetCard></LernsetCard>
                </div>
            <h2>Community-Lernsets</h2>
                <div class="scroll-row">
                    <LernsetCard></LernsetCard> 
                </div>    

        </div> <!--scroll section ende-->
    </div>
    <!--Ende: Content:Container-->
    </div>
    <!--Ende: Container-->

</template>

<script>
import LernsetCard from "@/components/LernsetCard.vue";

export default {
  name: "LernsetWaehlen",

  components:{
    LernsetCard
  },

  data() {
    return {
      istSortierSichtbar: false,
      sortierOption: '',
      lernsets: []
    };
  },

  mounted(){
    this.loadLernset();
  },

  methods: {
    toggleSortieren() {
      this.istSortierSichtbar = !this.istSortierSichtbar;
    },

    async loadLernset() {
        try {
            const res = await fetch("noch hinzufügen");
            const data = await res.json();
            this.lernsets = data;
        } catch (err) {
            console.error("Fehler beim Laden", err);
        }
    }
  }
};
</script>


<style scoped>

.LernsetBsp:hover {
  transform: scale(1.05);
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  cursor: pointer;
}

.scroll-row::-webkit-scrollbar {
  height: 0; /* Chrome/Safari – initial unsichtbar */
}

.scroll-row:hover::-webkit-scrollbar {
  height: 8px; /* Sichtbar beim Hover */
}
.scroll-row:hover::-webkit-scrollbar-thumb {
  background-color: #aaa; /* Farbe des Balkens */
  border-radius: 10px;
}

.scroll-section{
    display: flex;
    flex-direction: column;
    max-width: 100%;
    margin-top: 2rem;
}

.scroll-row {
  display: flex;
  flex-direction: row;
  overflow-x: auto;         /* Aktiviert horizontales Scrollen */
  gap: 2rem;                /* Abstand zwischen den Items */
  padding-bottom: 1rem;     /* Platz für Scrollbar */
  max-width: 100%;          /* Begrenzung auf Container-Breite */
  margin: 0rem 3rem 1rem 3rem;
  padding-bottom: 1rem;
  border-bottom: 0.2rem solid rgb(104, 102, 102);
}

.Content-Container {
  display: flex;
  flex-direction: column;
  padding: 1rem 2rem;
  gap: 2rem;
  max-width: 100%;
  overflow: hidden;
  box-sizing: border-box;
}

.Container {
  display: flex;  
  flex-direction: row;
  width: 95%;
  height: 75%;
  background-color: white;
  margin: 0% 2.5% 1% 2.5%;
  border: 0.1rem solid #797171;
  border-radius: 0.75rem;
}


h1 {
  text-align: center;
  margin-top: -2rem;
  margin-left: 3rem;
  font-size: 3rem;
}

.Body-Container {
  height: 100%;
  display: flex;
  gap: 2rem;
  flex-direction: column;
  align-items: flex-start;      /* vertikal: unten */
  justify-content: flex-start; /* horizontal: links */
  padding: 1rem;
}


.lernset-link{
    margin-top: 3rem;
    display: flex;
    background-color: transparent;
    flex-direction: column;
    font-weight: bold;
    font-size: 1rem;  
}

.lernseterstellenbild{
    margin-left: 0.5rem;
    width: 7rem;
    height: 7rem;
}

.link-text{
    margin-top: -1rem;
    color: black;
    font-size: 1.2rem;

}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropbtn {
    margin-left: 0.5rem;
  background-color: #ffffff;
  color: black;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dropdown-content {
  position: absolute;
  background-color: white;
  min-width: 160px;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
  padding: 0.5rem 0;
  margin-top: 0.3rem;
}

.dropdown-content a {
  color: black;
  padding: 0.5rem 1rem;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #f0f0f0;
}



</style>
