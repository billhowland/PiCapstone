// gpio radio button event listeners
const pins = document.getElementsByName('pins')
const scripts = document.getElementsByName('scripts')
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
    scripts: null,
  },
  mounted: function() {
    this.timer = setInterval(this.getAllPins, 250) //call getAllPins 4 times/sec
    this.timer = setInterval(this.getScripts, 250)
    this.getAllPins()
    this.getScripts()
  },
  beforeDestroy: function() {
    clearInterval(this.timer)
  },
  methods: {
    getScripts: function() {
      const request = fetch('get_scripts')
        .then(response => {
          return response.json()
        }).then(scriptData => {
          this.scripts = scriptData
        }).catch(err => console.log(err)) // unexpected character in JSON
    },
    runscript: function(num) { // was (url)
         const request = fetch('run_script/' + num) // was (url)
           .then(response => {
           return response.json()
         })
    },
    scrrunning: function(script) {
         return scriptData(scrrunning==True)
    },
  // leftcol pin-related methods:
    getAllPins: function() {
      const request = fetch('get_all_pins') // Calls get_all_pins in views.py
        .then(response => {
          return response.json()
        }).then(pinData => {
          this.pins = pinData.filter(pin => pin.used)
        }).catch(err => console.log(err))
    },
    setPin: function(pin, func) {
        if (func == 0) {
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
   gpoff: function(pin, off) {
        const request = fetch('gpoff/' + pin)
          .then(response => {
          return response.json()
       }).then(off => {
          this.getAllPins()
       }).catch(err => console.log(err))
   },
   pinused: function(pin) {
        return pinData(pinused==True)
   },
   gptest: function(pin) {
        const request = fetch('gptest/' + pin)
        	.then(response => {
          return response.json()
        }).then(test => {
           this.getAllPins()
        }).catch(err => console.log(err))
   }
  }
})
