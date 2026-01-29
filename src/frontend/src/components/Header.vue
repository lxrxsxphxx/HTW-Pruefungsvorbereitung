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
        <div class="user-area" @click="logout" title="Abmelden">👤 {{ username }}</div>
      </template>

      <LoginDialog v-if="showLogin" @login="handleLogin" @close="showLogin = false" />
    </div>
  </header>
</template>

<script>
import { ref } from 'vue';
import LoginDialog from './LoginDialog.vue';

/**
 * @component Header
 * @description Application header component with login/logout functionality and adaptive logo
 * Manages user authentication state and displays user information
 */
export default {
  name: 'Header',
  components: { LoginDialog },
  
  /**
   * Component data properties
   * @returns {Object} Reactive data properties
   * @property {boolean} showLogin - Controls visibility of login dialog
   * @property {boolean} isLoggedIn - User authentication status
   * @property {string} username - Currently logged in username
   */
  data() {
    return {
      showLogin: false,
      isLoggedIn: false,
      username: ''
    };
  },
  
  /**
   * Lifecycle hook - checks authentication status on component mount
   * Fetches user data from backend if valid session exists
   */
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
  
  /**
   * Component methods
   */
  methods: {
    /**
     * Opens the login dialog
     * Displays modal overlay and prevents body scrolling
     */
    openLogin() {
      this.showLogin = true;
      document.body.classList.add('modal-open');
    },
    
    /**
     * Handles user login
     * Sends credentials to backend and fetches user data on success
     * @param {Object} credentials - User login credentials
     * @param {string} credentials.email - User email address
     * @param {string} credentials.password - User password
     * @throws {Error} When login fails
     */
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
    
    /**
     * Logs out the current user
     * Clears user session and resets authentication state
     * Note: Currently only clears frontend state, no backend logout call
     */
    logout() {
      this.isLoggedIn = false;
      this.username = '';
      document.body.classList.remove('modal-open');
    }
  },
  
  /**
   * Composition API setup function
   * Handles dark mode detection and automatic theme switching
   * @returns {Object} Reactive properties for template
   * @property {import('vue').Ref<boolean>} dark_mode - Current dark mode state
   */
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
