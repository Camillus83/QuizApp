console.log('pierdol sie');



const url = window.location.href

const quizBox = document.getElementById('quiz-box')
console.log(url)

$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: function (response) {
        console.log(response)
        const data = response.data

        data.forEach(element => {
            for (const [question, answers] of Object.entries(element)) {
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `

                answers.forEach(answer => {
                    quizBox.innerHTML += `
                    <div>
                        <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                        <label for="${question}">${answer}</label>
                    </div>
                    `
                })
            }
        });
    },
    error: function (error) {
        console.log(error)
    },

})

const quizForm = document.getElementById("quiz-form")
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(element => {
        if (element.checked) {
            data[element.name] = element.value
        } else {
            if (!data[element.name]) {
                data[element.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        data: data,
        succes: function (response) {
            const results = response.results
            console.log(results)
            console.log(response)
        },
        error: function (error) {
            console.log(error)
        }

    })


}

quizForm.addEventListener('submit', e => {
    e.preventDefault()

    sendData()
})