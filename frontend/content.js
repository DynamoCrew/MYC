const attention = {
  animation: [
    { transform: 'rotate(0deg)' },
    { transform: 'rotate(-2deg)' },
    { transform: 'rotate(2deg)' },
    { transform: 'rotate(0deg)' }
  ],
  options: {
    duration: 1000,
    iterations: 1,
    easing: "ease"
  }
}

const grow = {
  animation: [
    { height: '0' },
    { height: '448px' }
  ],
  options: {
    duration: 300,
    iterations: 1,
    fill: 'forwards'
  }
}

const shrink = {
  animation: [
    { height: '448px' },
    { height: '0' }
  ],
  options: {
    duration: 300,
    iterations: 1,
    fill: 'forwards'
  }
}

let buttonToggled = false
let stores = {
  dropdown: undefined,
  video: undefined,
  btn: undefined,
  currentTime: 0,
}
const toggleDropdown = () => {
  if(!buttonToggled) {
    stores.dropdown.animate(grow.animation, grow.options)
    stores.video.pause()
    stores.btn.textContent = "Close Conversation"
    buttonToggled = true
  } else {
    stores.dropdown.animate(shrink.animation, shrink.options)
    stores.video.play()
    stores.btn.textContent = "Talk to Myc"
    buttonToggled = false
  }
}

const mountDropdownToggle = (elem) => {
  const btn = document.createElement("button")
  btn.textContent = "Talk to Myc"
  btn.style.width = "100%"
  btn.style.transition = "box-shadow 200ms ease"
  btn.style.backgroundColor = "var(--yt-spec-text-primary)"
  btn.style.color = "var(--yt-spec-text-primary-inverse)"
  btn.style.padding = "0 var(--ytd-margin-3x)"
  btn.style.fontFamily = '"Roboto", "Arial", sans-serif'
  btn.style.font = "1.4rem"
  btn.style.lineHeight = "2rem"
  btn.style.fontWeight = "500"
  btn.style.border = "none"
  btn.style.borderRadius = "8px"
  btn.style.height = "32px"
  btn.style.cursor = "pointer"
  btn.id = "toggle-interface"
  btn.addEventListener("click", toggleDropdown)

  const firstChild = elem.firstElementChild

  elem.insertBefore(btn, firstChild)
  stores.btn = btn
  console.log("Successfully mounted interface toggle")
}

const mountDropdown = (elem) => {
  const dropdown = document.createElement("section")
  dropdown.style.width = "100%"
  dropdown.style.backgroundColor = "blue"
  dropdown.style.height = "0"
  dropdown.id = "dropdown"

  const firstChild = elem.firstElementChild

  elem.insertBefore(dropdown, firstChild)
  stores.dropdown = dropdown
  console.log("Successfully mounted interface")
}

window.onload = () => {
  let tries = 0;
  console.log("Searching for #secondary-inner")
  let secondaryInner = document.getElementById("secondary-inner")

  const forceSelect = setInterval(() => {
    if (!secondaryInner) {
      secondaryInner = document.getElementById("secondary-inner")
      console.log("#secondary-inner element not detected. Searching again. Current attempt:", tries)
      ++tries
    } else if (tries >= 5) {
      console.log("Maximum number of tries exceeded. Ending search")
      clearInterval(forceSelect)
    } else {
      clearInterval(forceSelect)
      
      mountDropdownToggle(secondaryInner)
      setTimeout(() => {
        mountDropdown(secondaryInner)
      }, 500)

      stores.video = document.querySelector('.video-stream.html5-main-video')
      stores.video.addEventListener("pause", () => {
        if(!buttonToggled) {
          stores.btn.animate(attention.animation, attention.options)
        }
      })
      stores.video.addEventListener("timeupdate", () => {
        stores.currentTime = stores.video.currentTime.toFixed(3)
        console.log(stores.currentTime)
      })

      console.log(stores)
    }
  }, 800)
}