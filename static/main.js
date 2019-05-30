// gpio radio button event listeners
const pins = document.getElementsByName('pins')
const csrftoken = Cookies.get('csrftoken')
const headers = new Headers({
"X-CSRFToken": csrftoken
});

//from html these call things in views.py via pi_urls.py:

let app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data: {
    pins: null,
    timer: null,
  },
  mounted: function() {
    this.timer = setInterval(this.getAllPins, 500)
    this.getAllPins()
  },
  beforeDestroy: function() {
    clearInterval(this.timer)
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
    setPin: function(pin, func) {
        if (func == 1) {
          api_root = 'gpin/'
        } else {
          api_root = 'gpout/'
        }

        // const api_root = (pin == 1 ? 'gpin/' : 'gpout/')

        const request = fetch(api_root + pin, {
          method: 'POST',
          credentials: 'same-origin',
          headers: headers
        }).then(in_lvl => {
           this.getAllPins()
        }).catch(err => console.log(err))
    },
	 readPin: function(pin, in_lvl) {
        const request = fetch('gpread/' + pin)
        	.then(response => {
          return response.json()
       }).then(in_lvl => {
          this.getAllPins()
       }).catch(err => console.log(err))
   },
   gphigh: function(pin, high) {
        const request = fetch('gphigh/' + pin)
        	.then(response => {
          return response.json()
       }).then(high => {
         this.getAllPins()
       }).catch(err => console.log(err))
   },
   gplow: function(pin, low) {
        const request = fetch('gplow/' + pin)
        	.then(response => {
          return response.json()
       }).then(low => {
          this.getAllPins()
       }).catch(err => console.log(err))
   },
   gpup: function(pin, high) {
        const request = fetch('gpup/' + pin)
          .then(response => {
          return response.json()
       }).then(high => {
         this.getAllPins()
       }).catch(err => console.log(err))
   },
   gpdn: function(pin, low) {
        const request = fetch('gpdn/' + pin)
          .then(response => {
          return response.json()
       }).then(low => {
          this.getAllPins()
       }).catch(err => console.log(err))
   },




   gptest: function(pin) {
        const request = fetch('gptest/' + pin)
        	.then(response => {
          return response.json()
        })
   }
  }
})
