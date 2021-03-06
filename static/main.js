// gpio radio button event listeners
const pins = document.getElementsByName('pins')
const pwms = document.getElementsByName('pwms')
const spis = document.getElementsByName('spis')
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
    pwms: null,
    spis: null,
    i2cs: null,
  },
  mounted: function() {
    this.timer = setInterval(this.getAllPins, 250) //call getAllPins 4 times/sec
    this.timer = setInterval(this.getScripts, 250)
    this.getAllPins()
    this.getScripts()
    this.getPwms()
    this.getSpis()
    this.getI2cs()
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
        }).catch(err => console.log(err))
    },
    runscript: function(num) { // was (url)
         const request = fetch('run_script/' + num) // was (url)
         .then(sfrq => {
          this.getPwms()})
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
    getPwms: function() {
      const request = fetch('get_pwms') // Calls get_pwms in views.py
        .then(response => {
          return response.json()
        }).then(pwmData => {
          this.pwms = pwmData
        }).catch(err => console.log(err))
    },
    getSpis: function() {
      const request = fetch('get_spis') // Calls get_spis in views.py
        .then(response => {
          return response.json()
        }).then(spiData => {
          this.spis = spiData
        }).catch(err => console.log(err))
    },
    getI2cs: function() {
      const request = fetch('get_i2cs') // Calls get_i2cs in views.py
        .then(response => {
          return response.json()
        }).then(i2cData => {
          this.i2cs = i2cData
        }).catch(err => console.log(err))
    },
    setPin: function(pin, func) {
        if (func == 0) {
          api_root = 'gpin/'
        } else {
          api_root = 'gpout/'
        }
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
   gpused: function(pin) {
        return pinData(used==True)
   },
   gpuse: function(pin) {
        const request = fetch('gpuse/' + pin)
          .then(response => {
          return response.json()
        }).then(off => {
           this.getAllPins()
        }).catch(err => console.log(err))
   },
   gptest: function(pin) {
        const request = fetch('gptest/' + pin)
        	.then(response => {
          return response.json()
        }).then(test => {
           this.getAllPins()
        }).catch(err => console.log(err))
   },
   // path('gpfrq/<int:pin>', views.gpfrq, name='gpfrq'),
   gpfrq: function(pin) {
        const request = fetch('gpfrq/' + pin)
          .then(response => {
          return response.json()
        }).then(frq => {
           this.getAllPins()
        }).catch(err => console.log(err))
   },
   // path('gpsfrq/<int:pin>', views.gpsfrq, name='gpsfrq'),
   gpsfrq: function(pin, sfrq) {
         const request = fetch('gpsfrq/' + pin  + '/' + sfrq)
           .then(response => {
           return response.json()
         }).then(sfrq => {
            this.getAllPins()
         }).catch(err => console.log(err))
   },

   gpcfrq: function(pin, sfrq) {
         const request = fetch('gpcfrq/' + pin  + '/' + sfrq)
           .then(response => {
           return response.json()
         }).then(sfrq => {
            this.getAllPins()
         }).catch(err => console.log(err))
   },
   // path('gpdc/<int:pin>', views.gpdc, name='gpdc'),
   gpdc: function(pin) {
         const request = fetch('gpdc/' + pin)
           .then(response => {
           return response.json()
         }).then(dc => {
            this.getAllPins()
         }).catch(err => console.log(err))
   },
   // path('gpsdc/<int:pin>', views.gpsdc, name='gpsdc'),
   gpsdc: function(pin, sdc) {
          const request = fetch('gpsdc/' + pin + '/' + sdc)
            .then(response => {
            return response.json()
          }).then(sdc => {
             this.getAllPins()
          }).catch(err => console.log(err))
   },
   gphfrq: function(pin) {
        const request = fetch('gphfrq/' + pin)
          .then(response => {
          return response.json()
        }).then(hfrq => {
           this.getAllPins()
        }).catch(err => console.log(err))
   },
   gpshfrq: function(pin, shfrq) {
         const request = fetch('gpshfrq/' + pin + '/' + shfrq)
           .then(response => {
           return response.json()
         }).then(shfrq => {
            this.getAllPins()
         }).catch(err => console.log(err))
   },
   gphdc: function(pin) {
         const request = fetch('gphdc/' + pin)
           .then(response => {
           return response.json()
         }).then(hdc => {
            this.getAllPins()
         }).catch(err => console.log(err))
   },
   gpshdc: function(pin, shdc) {
          const request = fetch('gpshdc/' + pin + '/' + shdc)
            .then(response => {
            return response.json()
          }).then(shdc => {
             this.getAllPins()
          }).catch(err => console.log(err))
   },
   gpsspibaud: function(spi, baud) {
          const request = fetch('gpsspibaud/' + spi + '/' + baud)
            .then(response => {
            return response.json()
          }).then(baud => {
             this.getSpis()
          }).catch(err => console.log(err))
   },
   gpsi2caddr: function(i2c, address) {
          const request = fetch('gpsi2caddr/' + i2c + '/' + address)
            .then(response => {
            return response.json()
          }).then(address => {
             this.getI2cs()
          }).catch(err => console.log(err))
   },
   gpsspiflags: function(spi, flags) {
          const request = fetch('gpsspiflags/' + spi + '/' + flags)
            .then(response => {
            return response.json()
          }).then(flags => {
             this.getSpis()
          }).catch(err => console.log(err))
   },
   gpspibaud: function(spi) {
          const request = fetch('gpspibaud/' + spi)
            .then(response => {
            return response.json()
          }).then(baud => {
             this.getSpis()
          }).catch(err => console.log(err))
   },
   gpi2caddr: function(i2c) {
          const request = fetch('gpi2caddr/' + i2c)
            .then(response => {
            return response.json()
          }).then(address => {
             this.getI2cs()
          }).catch(err => console.log(err))
   },
   gpspiflags: function(spi) {
          const request = fetch('gpspiflags/' + spi)
            .then(response => {
            return response.json()
          }).then(flags => {
             this.getSpis()
          }).catch(err => console.log(err))
   },
  }
})
