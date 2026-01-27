<template>
  <header>
    <RouterLink to="/">
      <img v-if="dark_mode" src="@/assets/img/HtwLogo_white.png" alt="HtwLogo" />
      <img v-else src="@/assets/img/HtwLogo.png" alt="HtwLogo" />
    </RouterLink>
    <div class="login-wrapper">
      <template v-if="!isLoggedIn">
        <button @click="openLogin">Login</button>
      </template>
      <template v-else>
        <RouterLink to="/user" style="padding: 0px;">
          <div class="user-area">👤 {{ username }}</div>
        </RouterLink>
      </template>

      <LoginDialog v-if="showLogin" @login="handleLogin" @close="showLogin = false" />
    </div>
  </header>
</template>

<script>
import { ref } from 'vue';
import LoginDialog from './LoginDialog.vue';

export default {
  name: 'Header',
  components: { LoginDialog },
  data() {
    return {
      showLogin: false,
      isLoggedIn: false,
      username: ''
    };
  },
  mounted() {
    fetch('http://localhost:8000/api/users/data', {
      credentials: "include"
    })
      .then(response => {
        if (response.status == 200) {
          response.json().then(
            data => {
              this.username = data.name;
              this.isLoggedIn = true;
            }
          )
        }
      })
  },
  methods: {
    openLogin() {
      this.showLogin = true;
      document.body.classList.add('modal-open');
    },
    handleLogin({ email, password }) {
      fetch('http://localhost:8000/api/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'accept': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          username: email,
          passwd: password
        })
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Login fehlgeschlagen');
          }
          return response.json();
        })
        .then(data => {
          fetch('http://localhost:8000/api/users/data', {
            credentials: "include"
          })
            .then(response => {
              if (response.status == 200) {
                response.json().then(
                  data => {
                    this.username = data.name;
                    this.isLoggedIn = true;
                  }
                )
              }
            })
          this.showLogin = false;
          document.body.classList.remove('modal-open');
        })
        .catch(error => {
          console.error('Login-Fehler:', error);
          alert('Login fehlgeschlagen. Bitte prüfe deine Zugangsdaten.');
        });
    },
    logout() {
      this.isLoggedIn = false;
      this.username = '';
      document.body.classList.remove('modal-open');
    }
  },
  setup() {
    const dark_mode = ref(true);
    dark_mode.value = window.matchMedia('(prefers-color-scheme: dark)').matches;

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
      dark_mode.value = event.matches;
    })

    return { dark_mode }
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

.user-area {
  color: var(--color-text);
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
