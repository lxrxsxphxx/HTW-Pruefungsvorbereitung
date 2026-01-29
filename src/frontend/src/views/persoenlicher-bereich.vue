<template>
  <div id="personal-space-main">
    <div id="personal-info-container">
      <img src="../assets/img/dummy-picture.jpg" alt="Profilbild" id="profile-picture" width="256" height="256"><br>
      <div class="user-information" id="username" v-text="USERNAME"></div>
      <div class="user-information" id="faculty" v-text="FACULTY"></div>
      <div class="user-information" id="major" v-text="MAJOR"></div>
      <div class="user-information" id="semester" v-text="SEMESTER"></div>
    </div>
    <div id="modules-container">
      <h2 id="modules-header">Eingetragene Module</h2>
      <hr>

      <div id="user-modules">
        <div class="module" v-for="module in user_modules" :key="module.id"><div class="module-name" v-text="module.name"></div><div class="module-info-wrapper"><div class="module-prof" v-text="module.lecturer"></div><div class="module-semester">{{ module.semester }}. Semester</div></div></div>
      </div>

      <div id="manage-modules-container">
        <RouterLink to="/modulwahl" style="padding: 0px;">
          <button id="manage-modules-button">Module verwalten</button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>



<script setup>

import { ref, onMounted } from 'vue';


const USERNAME = ref('');
const FACULTY = ref('');
const MAJOR = ref('');
const SEMESTER = ref('');

const user_modules = ref({});

const API_MODULES = "http://localhost:8000/api/users/modules/";
const API_USER_DATA = "http://localhost:8000/api/users/data/";
const API_COURSES = "http://localhost:8000/api/courses/";


onMounted(() => {loadContent();});

/**
 * @description Get the Information about the user that is currently logged in and write it to the Template.
 * @returns {null}
 */
async function loadContent(){
  const userData = await getUserData();
  const userMajor = await getCourse(userData.course_id);

  USERNAME.value = userData.name;
  FACULTY.value  = userData.faculty;
  MAJOR.value    = userMajor.name;
  SEMESTER.value = userData.curr_semester + '. Semester';

  user_modules.value = await getUserModules();
  return;
}


/**
 * @description Get the username, faculty, course of study and current semester of the user from the backend.
 * @returns {JSON|null} on success the user information in a JSON object
 */
async function getUserData(){
  try {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(API_USER_DATA, {method: "GET", credentials: "include", signal: controller.signal});
    console.log(response);
    if (!response.ok) {throw new Error(`Response status: ${response.status}`);}

    const data = await response.json();
    return data;
  }
  catch (error) {
    console.error(error.message);
    return null;
  }
}


/**
 * @description Get the user-specific modules.
 * @returns {JSON|null} on success the modules in which the user is enrolled.
 */
async function getUserModules(){
  try {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(API_MODULES, {method: "GET", credentials: "include", signal: controller.signal});
    console.log(response);
    if (!response.ok) {throw new Error(`Response status: ${response.status}`);}

    const modules = await response.json();
    return modules;
  }
  catch (error) {
    console.error(error.message);
    alert("Die nutzerspezifischen Module konnten nicht geladen werden.");
    return null;
  }
}


/**
 * @description Get a course of study from the backend.
 * @param {Number|String} course_id the id of the wanted course of study
 * @returns {JSON|null} on success the wanted course of study
 */
async function getCourse(course_id) {
  try {
    const url = API_COURSES + course_id;

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(url, {method: "GET", credentials: "include", signal: controller.signal});
    console.log(response);
    if (!response.ok) {throw new Error(`Response status: ${response.status}`);}

    const course = await response.json();
    return course;
  }
  catch (error) {
    console.error(error.message);
    alert("Die nutzerspezifischen Module konnten nicht geladen werden.");
    return null;
  }
}

</script>

<style scoped>

#personal-space-main {
  text-align: center;
  display: flex;
  flex-direction: row;
  height: 100%;
  margin-bottom: 4em;
  overflow: hidden;
}

#personal-info-container {
  flex: 1 1 0%;
  padding-left: 2em;
  padding-right: 2em;
}

#modules-container {
  flex: 3 3 0%;
  border: 2px solid var(--color-border);
  border-radius: 16px;
  margin-left: 8em;
  margin-right: 8em;
  display: flex;
  flex-direction: column;
}


/* inside personal-info-container */

#profile-picture {
  object-fit: cover;
  image-rendering: high-quality;
  height: 8em;
  width: 8em;
  border-radius: 50%;
}

.user-information {
  margin-top: 1rem;
  font-size: large;
}


/* inside modules-container */


#modules-header {
  padding: 0.5em;
  background-color: var(--htw-orange);
  border-top-left-radius: 14px;
  border-top-right-radius: 14px;
}
hr {
  background-color: var(--color-border);
  height: 0;
  border: 1px solid var(--color-border);
}


#user-modules {
  flex: 1;
  overflow-y: auto;
}

.module {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
  border-radius: 0.5em;
  background-color: var(--color-background-soft);
  margin-top: 1em;
  margin-bottom: 1em;
  padding-left: 0.5em;
  padding-right: 0.5em;
}

.module-name {
  text-align: left;
  font-weight: bold;
  overflow: hidden;
}

.module-info-wrapper {
  display: flex;
  flex-direction: column;
}
.module-prof {
  color: var(--htw-grey);
  overflow: hidden;
}
.module-semester {
  color: var(--htw-grey);
  overflow: hidden;
}

#manage-modules-container {
  padding: 0px;
  margin-left: auto;
}
#manage-modules-button {
  width: 12em;
  border: none;
  border-radius: 0.5em;
  padding: 0.5em;
  font-size: large;
  cursor: pointer;
}


</style>