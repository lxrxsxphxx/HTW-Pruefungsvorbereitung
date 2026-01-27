<template>
    <h1>Lernmodus für Modul</h1> 
    <div class="Container">
        <div class="Body-Container">
            <RouterLink to="/lernset-erstellen" class="lernset-link">
                <img src="@/assets/img/Lernseterstellen.png" alt="Lernseterstellen" class="lernseterstellenbild"></img>
                <span class="link-text">Lernset erstellen</span>
            </RouterLink>
        </div>
        <!--Ende: Body-Container-->

        <!--Start: Content-Container-->
        <div class="Content-Container">
            <div class="module-container" v-for="module in modules" :key="module.id">
                <h2>{{ module.module_name }}</h2>
                <div class="scroll-row">
                    <LernsetCard
                    v-for="set in module.learning_sets"
                    :key="set.id"
                    :title="set.name"
                    />
                </div>
            </div> <!--scroll section ende-->
        </div>
        <!--Ende: Content:Container-->
    </div>
    <!--Ende: Container-->

</template>

<script setup>

import { ref, onMounted } from 'vue';
import LernsetCard from "@/components/LernsetCard.vue";


const modules = ref(null);


const API_LEARNING_SETS = "http://localhost:8000/api/learning_set/";
const API_MODULES = "http://localhost:8000/api/modules/";
const LOGIN_URL = "http://localhost:8000/api/users/login";

onMounted(() => {loadContent();});

/**
 * @description Login with the dummy credentials to test Getting the user-specific modules. (temporary)
 * @returns {JSON, Null} the response from the server as a JSON Object
 */
async function login(){
    try{
        const postHeader = new Headers();
        postHeader.set("accept", "application/json");
        postHeader.set("Content-Type", "application/json");

        const response = await fetch(LOGIN_URL, {method: "POST", credentials: "include", headers: postHeader, body: JSON.stringify({username: "test@htw.de", passwd: "1234"})});
        console.log(response);
        if (!response.ok) throw new Error(`Response status: ${response.status}`);
        return response;
    }
    catch(error){
        console.error(error.message);
        return null;
    }
}


async function loadContent(){
    await login();

    const user_modules = await loadUserModules();
    if(!user_modules) return;

    let json_str = '[{';

    for(let i = 0; i < user_modules.length; i++){
        const module_name = user_modules[i].name;
        const module_id = user_modules[i].id;
        const learning_sets = await loadLearningSets(module_id);
        if(!learning_sets) return;

        json_str += '"module_name": "' + module_name + '", "module_id": "' + module_id + '", "learning_sets": ' + JSON.stringify(learning_sets) + '}';
        if(i !== user_modules.length - 1) json_str += ',';
    }
    json_str += ']';

    modules.value = await JSON.parse(json_str);
    console.log(modules.value);

    return;
}


async function loadUserModules(){
    try{
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), 5000);

        const response = await fetch(API_MODULES, {method: "GET", credentials: "include", signal: controller.signal});
        if (!response.ok) {throw new Error(`Response status: ${response.status}`);}

        const modules = await response.json();
        return modules;
    }
    catch (error){
        console.error(error.message);
        alert("Die nutzerspezifischen Module konnten nicht geladen werden.");
        return null;
    }
}

async function loadLearningSets(modul_id) {
    try {
        let url = API_LEARNING_SETS + '?modul=' + modul_id;

        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), 5000);

        const response = await fetch(url, {method: "GET", credentials: "include", signal: controller.signal});
        if (!response.ok) {throw new Error(`Response status: ${response.status}`);}

        const learning_sets = await response.json();
        return learning_sets;
    }
    catch (error) {
        console.error(error.message);
        return null;
    }
}
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

.module-container{
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
    margin-bottom: 4rem;
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
