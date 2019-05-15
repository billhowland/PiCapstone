// gpio radio button event listeners
const gpio02 = document.getElementsByName('GPIO17')
const api_root = 'set_pin/'
const csrftoken = Cookies.get('csrftoken')
const headers = new Headers({
"X-CSRFToken": csrftoken
});

gpio02.forEach(elem =>
  elem.addEventListener('change', (evt) => {
    console.log(evt)
    console.log(evt.target.value)
    const res = fetch(api_root + '17', {
      method: 'POST',
      credentials: 'same-origin',
      headers: headers,
      body: {
        value: evt.target.value
      }
    })
  })
)
