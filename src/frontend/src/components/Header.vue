<template>
  <header>
    <img src="@/assets/img/HtwLogo.png" alt="HtwLogo" />
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
export default {
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
    login() {
      if (this.email === 'test@htw.de' && this.password === '1234') {
        this.isLoggedIn = true;
        this.username = 'Tobi';
        this.showLogin = false;
      } else {
        alert('Falsche Zugangsdaten');
      }
    }
  }
};
</script>

<style scoped>
  header {
  margin-top: 2px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 50px;
}

header img {
  width: 250px;
  height: auto;
}

.login-wrapper button {
  background-color: orange;
  border-radius: 8px;
  padding: 10px 20px;
  color: white;
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

</style>