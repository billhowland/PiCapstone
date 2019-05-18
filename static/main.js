// gpio radio button event listeners
const pins = document.getElementsByName('pins')
const csrftoken = Cookies.get('csrftoken')
const headers = new Headers({
"X-CSRFToken": csrftoken
});

let app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data: {
    pins: null,
  },
  mounted: function() {
    this.getAllPins()
  },
  methods: {
    getAllPins: function() {
      const request = fetch('get_all_pins')
        .then(response => {
          return response.json()
        }).then(pinData => {
          this.pins = pinData
        }).catch(err => console.log(err))
    },
    setPin: function(pin, state) {
        if (state == 1) {
          api_root = 'gpin/'
        } else {
          api_root = 'gpout/'
        }

        // const api_root = (pin == 1 ? 'gpin/' : 'gpout/')

        const request = fetch(api_root + pin, {
          method: 'POST',
          credentials: 'same-origin',
          headers: headers
        })
      }

  }
})
