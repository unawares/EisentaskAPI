Vue.use(Vuetify)

var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    ready: false,
    passwordVisibility: false,
    login: '',
    username: '',
    password: '',
    password1: '',
    password2: '',
    email: '',
    loginErrorMessages: [],
    passwordErrorMessages: [],
    usernameErrorMessages: [],
    emailErrorMessages: [],
    passwordFirstErrorMessages: [],
    passwordSecondErrorMessages: [],
  },
  mounted () {
    setTimeout(() => {
      this.ready = true
    }, 30)
  },
  watch: {
    login () {
      if (this.ready) {
          this.loginErrorMessages = []
      }
    },

    username () {
      if (this.ready) {
          this.usernameErrorMessages = []
      }
    },

    password () {
      if (this.ready) {
          this.passwordErrorMessages = []
      }
    },

    email () {
      if (this.ready) {
          this.emailErrorMessages = []
      }
    },

    password1 () {
      if (this.ready) {
          this.passwordFirstErrorMessages = []
      }
    },

    password2 () {
      if (this.ready) {
          this.passwordSecondErrorMessages = []
      }
    },
  }
})
