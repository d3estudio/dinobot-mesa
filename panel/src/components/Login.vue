<template>
  <div class="uk-flex uk-flex-center uk-flex-middle uk-padding">
    <form class="uk-card uk-card-default uk-card-body uk-form-stacked uk-width-large"
          :class="classes" @submit.prevent="submit">
      <fieldset class="uk-fieldset" :disabled="submitting">
        <!-- TODO: Remove this div for Xandão's version -->
        <div class="uk-form-controls uk-margin">
          <label class="uk-form-label">Conta</label>
          <input class="uk-input" v-model="domain" placeholder="temperodafamilia">
        </div>
        <div class="uk-form-controls uk-margin">
          <label class="uk-form-label">Email</label>
          <input class="uk-input" v-model="email" placeholder="Digite seu email">
        </div>
        <div class="uk-form-controls uk-margin">
          <label class="uk-form-label">Senha</label>
          <input type="password" class="uk-input" v-model="password" placeholder="Digite sua senha">
        </div>
        <div class="uk-form-controls uk-margin">
          <button class="uk-button uk-button-primary">Entrar</button>
        </div>
      </fieldset>
    </form>
  </div>
</template>

<script>
import Submittable from '../mixins/Submittable';

export default {
  mixins: [
    Submittable,
  ],
  data() {
    return {
      domain: 'temperodafamilia',
      email: null,
      password: null,
    };
  },
  computed: {
    classes() {
      return {
        'uk-animation-shake': this.failed,
      };
    },
  },
  watch: {
    email() {
      this.$delete(this.errors, 'email');
    },
    password() {
      this.$delete(this.errors, 'password');
    },
  },
  methods: {
    submitHandler() {
      return this.$store.dispatch('login', {
        domain: this.domain,
        email: this.email,
        password: this.password,
      });
    },
    submitSuccess() {
      this.$router.push(this.$route.query.redirect || '/');
    },
  },
};
</script>
