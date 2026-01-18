<template>
  <header>
    <img v-if="dark_mode" src="@/assets/img/HtwLogo_white.png" alt="HtwLogo" />
    <img v-else  src="@/assets/img/HtwLogo.png" alt="HtwLogo" />
    <div class="login-wrapper">
      <template v-if="!isLoggedIn">
        <button @click="showLogin = !showLogin">Login</button>
        <div v-if="showLogin" class="login-form">
          <input v-model="email" placeholder="HTW-Mail" />
          <input v-model="password" type="password" placeholder="Passwort" />
          <button @click="login">Anmelden</button>
        </div>
      </template>
      <template v-else>
        👤 {{ username }}
      </template>
    </div>
  </header>
</template>

<script>
import { ref } from 'vue';

  
  
export default {
  /**
   * - email: Benutzer-E-Mail für Login
   * - password: Passwort für Login
   * - showLogin: Steuert, ob das Login-Formular angezeigt wird
   * - isLoggedIn: Gibt an, ob der Benutzer eingeloggt ist
   * - username: Wird gesetzt wenn der Login erfolgreich war
   */
  name: 'Header',
  data() {
    return {
      email: '',
      password: '',
      showLogin: false,
      isLoggedIn: false,
      username: ''
    };
  },
  methods: {
    /**
     * Führt einen einfachen Login durch.
     * Prüft, ob E-Mail und Passwort korrekt sind.
     * Setzt Zustände (isLoggedIn, username, showLogin).
     * Zeigt eine Fehlermeldung, bei falschen Zugangsdaten.
     */
    login() {
      if (this.email === 'test@htw.de' && this.password === '1234') {
        this.isLoggedIn = true;
        this.username = 'Tobi';
        this.showLogin = false;
      } else {
        alert('Falsche Zugangsdaten');
      }
    }
  },
  setup () {
    const dark_mode = ref(true);
    dark_mode.value = window.matchMedia('(prefers-color-scheme: dark)').matches;

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
      dark_mode.value = event.matches;
    })
  
  return {dark_mode}
  }
};
</script>

<style scoped>
/* Basis-Layout */
header {
  margin-top: 2px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 50px;
}

.login-wrapper button {
  border-radius: 8px;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
}

.login-form input {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}



/* Mittlere Bildschirme (Tablet) */
@media screen and (min-width: 769px) and (max-width: 1079px) {
  header {
    padding: 25px 30px;
  }

  header img {
    width: 220px;
  }

  .login-wrapper button {
    padding: 9px 18px;
    font-size: 1rem;
  }
}

/* Große Bildschirme (Desktop & größer) */
@media screen and (min-width: 1080px) {
  header {
    padding: 30px 50px;
  }

  header img {
    width: 250px;
  }

  .login-wrapper button {
    padding: 10px 20px;
    font-size: 1.05rem;
  }
}
</style>
