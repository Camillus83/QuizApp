console.log('Hello Quiz');



const url = window.location.href

const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const ResultBox = document.getElementById('result-box')
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
        success: function (response) {
            const results = response.attempt_details
            console.log(results)
            console.log(response)
            quizForm.classList.add('not-visible')

            scoreBox.innerHTML = `
                ${response.passed ? 'Passed' : 'Failed'} Your result is ${response.score} %

            `

            results.forEach(result => {
                const resDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(result)) {
                    console.log(question)
                    console.log(resp)
                    console.log('*********')

                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'text-light', 'h3']
                    resDiv.classList.add(...cls)

                    if (resp == 'not answered') {
                        resDiv.innerHTML += '- not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correctAnswer = resp['correct_answer']
                        if (answer == correctAnswer) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += `
                            answered: ${answer}
                            `
                        }
                        else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += `
                            | correct answer: ${correctAnswer}
                            `
                            resDiv.innerHTML += `
                            | answered: ${answer}
                            `
                        }
                    }
                }
                //const body = document.getElementsByTagName('BODY')[0]
                ResultBox.append(resDiv)
            })

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