console.log('Hello Quiz');



const url = window.location.href

const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const ResultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')

const ActivateTimer = (time) => {
    console.log(time)

    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`

    }
    else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(() => {
        seconds--
        if (seconds < 0) {
            seconds = 59
            minutes--
        }

        if (minutes.toString().length < 2) {
            displayMinutes = '0' + minutes
        } else {
            displayMinutes = minutes
        }
        if (seconds.toString().length < 2) {
            displaySeonds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes == 0 && seconds == 0) {
            clearInterval(timer)
            alert('Time is over')
            sendData()
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`



    }, 1000)

    console.log(minutes)
}
console.log(url)

$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: function (response) {
        console.log(response)
        const data = response.data
        let content = ''

        data.forEach(element => {
            for (const [question, answers] of Object.entries(element)) {
                content += `
                    <hr>
                    <div class="card">
                    <div class="card-header">
                        <h><b>${question}</b></h>
                        </div>
                    <div class="card-body">
                `

                answers.forEach(answer => {
                    content += `
                    <div>
                        <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                        <label for="${question}">${answer}</label>
                    </div>
                    `
                })
            }
            content += `
                </div>
                </div>
            `

        });

        content += `<button type="submit" class="btn btn-primary mt-3">Save</button>`
        ActivateTimer(response.time)
        quizForm.innerHTML += content
    },
    error: function (error) {
        console.log(error)
    },

})

const quizForm = document.getElementById("quiz-form")
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const quizHeader = document.getElementById("quiz-header")

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
            quizHeader.classList.add('not-visible')

            scoreBox.innerHTML = `<br>
            <div class="card">
            <div class="card-body align-items-center d-flex justify-content-center"> 
                ${response.passed ? '<b>Passed :)</b>' : '<b>Failed :(</b>'} <br> Your result is ${response.score.toFixed(2)} %
            </div> 
            </div>
            </br>
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

                    if (resp['answered'] == 'null') {
                        resDiv.innerHTML += '<br>| not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correctAnswer = resp['correct_answer']
                        if (answer == correctAnswer) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += `<br>
                            | answered: ${answer}
                            `
                        }
                        else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += `<br>
                            | correct answer: ${correctAnswer}
                            `
                            resDiv.innerHTML += `<br>
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