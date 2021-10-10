let scraller = document.querySelector('.scraller')
let titles = document.querySelector('.moreReccs')

scraller.addEventListener('click', clickScrallerEvent)

function clickScrallerEvent() {
    scraller.classList.toggle('open')
    titles.classList.toggle('open') 
}
