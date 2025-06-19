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