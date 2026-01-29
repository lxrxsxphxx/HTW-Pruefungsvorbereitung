<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal">
      <h3>Login</h3>
      <input v-model="email" placeholder="Email" type="email" />
      <input v-model="password" placeholder="Passwort" type="password" />
      <p v-if="error" class="error">{{ error }}</p>
      <div class="buttons">
        <button class="btn secondary" @click="close">Abbrechen</button>
        <button class="btn primary" @click="submit">Einloggen</button>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * @component LoginDialog
 * @description Modal dialog component for user authentication
 * Provides email/password input fields with validation and emits login events
 */
export default {
  name: 'LoginDialog',
  
  /**
   * Component data properties
   * @returns {Object} Reactive data properties
   * @property {string} email - User email input value
   * @property {string} password - User password input value
   * @property {string} error - Error message to display (empty when no error)
   */
  data() {
    return {
      email: '',
      password: '',
      error: ''
    };
  },
  
  /**
   * Component methods
   */
  methods: {
    /**
     * Closes the login dialog
     * Clears any error messages and emits close event to parent
     * @emits close - Emitted when dialog should be closed
     */
    close() {
      this.error = '';
      this.$emit('close');
    },
    
    /**
     * Handles login form submission
     * Validates email and password fields before emitting login event
     * Trims whitespace from email input
     * @emits login - Emitted with {email, password} object when validation passes
     * @property {Object} loginData - Login credentials object
     * @property {string} loginData.email - Trimmed email address
     * @property {string} loginData.password - User password
     */
    submit() {
      this.error = '';
      if (!this.email) {
        this.error = 'Bitte E‑Mail eingeben';
        return;
      }
      if (!this.password) {
        this.error = 'Bitte Passwort eingeben';
        return;
      }
      this.$emit('login', { email: this.email.trim(), password: this.password });
    }
  }
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.35);
  z-index: 9999;
  -webkit-backdrop-filter: blur(6px);
  backdrop-filter: blur(6px);
}
.modal {
  width: 320px;
  max-width: calc(100% - 40px);
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  text-align: center;
  z-index: 10000;
}
.modal h3 {
    margin: 0 0 20px;
  font-size: 1.5rem;
  font-weight: 800;
  color: #333;
}
.modal input {
  width: 100%;
  padding: 8px;
  margin: 6px 0;
  border-radius: 6px;
  border: 1px solid #ddd;
  box-sizing: border-box;
}
.buttons {
  display: flex;
  gap: 8px;
  justify-content: space-between;
  margin-top: 12px;
}
.btn {
  flex: 1;
  padding: 10px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}
.btn.primary {
  font-weight: bold;
}
.btn.secondary {
  background: #f0f0f0;
  color: black;
}
.error {
  color: #c0392b;
  margin-top: 6px;
}
</style>