// gpio radio button event listeners
const gpio02 = document.getElementsByName('GPIO2')
const api_root = 'set_pin/'

gpio02.forEach(elem =>
  elem.addEventListener('change', (evt) => {
    console.log(evt)
    console.log(evt.target.value)
    const res = fetch(api_root + '2', {
      method: 'POST',
      body: {
        value: evt.target.value
      }
    })
  })
)
