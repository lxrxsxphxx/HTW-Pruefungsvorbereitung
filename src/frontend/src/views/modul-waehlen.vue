<template>
  <div class="modulwaehlen-container">

    <div class="header-row">
      <h1>Module an denen ich teilnehme</h1> 

      <!-- SUCHFELD -->
      <div class="suchleiste">
        <img class="search-icon" src="@/assets/icons/suchen.svg" alt="suche" />
        <input
          v-model="search"
          type="text"
          placeholder="Suche nach Lernset"
        />
      </div>
    </div>  
    <div class="module-scroll">
      <RouterLink
        v-for="(modul, index) in moduleListe"
        :key="index"
        to="/lernset-waehlen"
        class="module-link"
        >
      <div class="module-card">
        <span class="module-icon">
          <img src="@/assets/icons/modul-icon.svg" alt="icon" />
        </span>
        <span>{{ modul.name }}</span>
      </div>
      </RouterLink>
    </div>

  </div>
</template>

<script>
export default {
  name: "Modulwaehlen",

  data() {
    return {
      moduleListe: [
        { name: "Programmieren 1" },
        { name: "Mathematik 2" },
        { name: "Theoretische Informatik" },
        { name: "BWL Grundlagen" },
        { name: "Programmieren 1" },
        { name: "Mathematik 2" },
        { name: "Theoretische Informatik" },
        { name: "BWL Grundlagen" }
      ]
    };
  }  

};
</script>

<style scoped>
.modulwaehlen-container {
  width: 60%;                    /* nimmt die rechte Hälfte ein */
  max-width: 2000px;
  height: 100%;
  max-height: 70rem;
  margin: 1rem 80px 60px auto;  /* top right bottom left */
 
  background-color: white;
  
  border: 0.2rem solid #797171;
  border-radius: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);

  padding: 2rem;
  
  display: flex;
  flex-direction: column;
  height: 90vh;
  overflow: hidden;
}

.header-row{
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;          
  flex-wrap: nowrap;    /* verhindert Umbruch */
  margin-bottom: 2rem;
}

.header-row h1{
    margin: 0;
    font-size: 2rem;
   

}

.suchleiste {
  display: flex;
  align-items: center;
  gap: 0.6rem;

  border: 2px solid black;
  border-radius: 0.6rem;
  padding: 0.4rem 0.8rem;
  width: 18rem;
  background: white;
  margin-right: 5.5rem;
}

.search-icon {
  width: 1.2rem;
  height: 1.2rem;
}

.suchleiste input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 1rem;
  
  
}

.module-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  margin: 0px 15px 5px 1px;
  overflow-y: auto;
  overflow-x: hidden;
  
}

.module-link {
  display: block;          /* wichtig: Link wird wie ein div */
  text-decoration: none;   /* keine Unterstreichung */
  color: inherit;          /* kein blau/purple */
  margin: 0;
  padding: 0;
}

.module-card {
    position: relative;
    display: flex;
    align-items: center;
    gap: 3rem;
    margin: 0.3rem 5rem 1rem 2rem;
    padding: 1.5rem 3rem;
    
    border: 0.1rem solid #797171;
    border-radius: 2rem;
    cursor: pointer;

    font-size: 1.5rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.module-card * {
  position: relative;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.module-icon img{
    
    height: 2rem;
    width: 3rem;
    filter: brightness(0) saturate(100%) invert(53%) sepia(94%) saturate(2092%) hue-rotate(5deg) brightness(102%) contrast(101%);
    
}

.module-card:hover {
  transform: translateY(-4px);
  z-index: 10;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.12);
}
</style>
