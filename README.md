# QuizApp
Online Quiz application based on Django, for Frontend I've used Bootstrap 4.

## Current Features
### Site Access
<ul>
<li> Creating user accounts/login with GitHub. For simplify the authentication is not implented, user can create an account on fake email.
<li> Every quiz can be accessed only if the user is logged in.
</ul>
### Quiz 
<ul>
<li> Every logged in user can create his own quiz or take an existing quiz. 
<li> Quiz creating/edit section is based in My Quizes section. Quiz attempting/preview is based in All Quizes section.
<li> While creating new quiz user can set title, short description, percentage required to pass and max time to resolve.
<li> User can add questions and answers in my Quizes section. Question can have multiple correct answers.
<li> Every quiz attempt has an timer, while timer stops answers will be automatically saved.
<li> After completing quiz, app will shown informations about passing and every question with answer.
<li> User can check his Quiz Attempts in My Attempts section.
</ul>

## Future Features
<ul>
<li> Uploading questions and answers via csv file -- in progress.
<li> Creating a pdf file with quiz form
<li> New frontend design
</ul>


## Project Snapshots
![image](https://user-images.githubusercontent.com/87909623/190331891-7f333da9-c0ca-49e4-996c-5b65fe384909.png)
![image](https://user-images.githubusercontent.com/87909623/190331988-4f187fdb-fc61-449a-943e-5480c134dfa6.png)
![image](https://user-images.githubusercontent.com/87909623/190332175-7b6f85b0-a539-4ed8-85e2-f6b8d3ccc51d.png)
![image](https://user-images.githubusercontent.com/87909623/190332251-8b3cff0e-8a4b-4e51-bdce-76d0f400cea3.png)
![image](https://user-images.githubusercontent.com/87909623/190332289-70f24aa3-925c-42dc-b9e6-ebc88cc34b92.png)
![image](https://user-images.githubusercontent.com/87909623/190332326-adcad225-d1ad-4d31-8352-1bad98977169.png)

## Reference
During the development of the application, I relied on the knowledge contained in <br>
[Django for Begginers - William S. Vincent](https://djangoforbeginners.com/)<br>
[Django for Proffesionals - William S. Vincent](https://djangoforprofessionals.com/)<br>
[Materials provided by PyPlane](https://www.pyplane.com/)<br>

## Instructions
### Heroku
Visit ```https://vast-savannah-19196.herokuapp.com/```
### Docker
# Clone repo <br>
``` git clone https://github.com/Camillus83/QuizApp ``` <br>
``` cd quiz ``` <br>
# Build <br>
``` docker compose up --build ``` <br>
# Checkout in browser <br>
Visit http://127.0.0.1:8080/ in your browser
