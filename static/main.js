// gpio radio button event listeners
const pins = document.getElementsByName('pins')
const csrftoken = Cookies.get('csrftoken')
const headers = new Headers({
"X-CSRFToken": csrftoken
});

//these call things in views.py via pi_urls.py:

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
        })
    },
	 readPin: function(pin, in_lvl) {
        const request = fetch('gpread/' + pin)
        	.then(response => {
          return response.json()
       }).then(in_lvl => {
          this.pins = in_lvl
       }).catch(err => console.log(err))
   },
   gphigh: function(pin, high) {
        const request = fetch('gphigh/' + pin)
        	.then(response => {
          return response.json()
       }).then(high => {
          this.pins = high
       }).catch(err => console.log(err))
   },
   gplow: function(pin, low) {
        const request = fetch('gplow/' + pin)
        	.then(response => {
          return response.json()
       }).then(low => {
          this.pins = low
       }).catch(err => console.log(err))
   },
   gptest: function(pin, test) {
        const request = fetch('gptest/' + pin)
        	.then(response => {
          return response.json()
       }).then(test => {
          this.pins = test
       }).catch(err => console.log(err))
   }
  }
})
