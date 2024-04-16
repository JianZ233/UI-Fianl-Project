
$(document).ready(function(){
    if (window.location.pathname == "/wine-terms"){
        $("#wine-terms-nav").css("text-decoration", "underline");
    }
})
// Function to show explanations and mark correct and incorrect answers
function showExplanation(selectedButton, correctAnswer) {
    document.querySelectorAll('.option').forEach(option => {
        let explanationElement = document.getElementById('explanation-' + option.innerText.trim());
        if (explanationElement) {
            explanationElement.style.display = 'block'; // Show all explanations
        }
        option.classList.add(option.innerText.trim() === correctAnswer ? 'correct' : 'incorrect'); // Mark the correct and incorrect answers
        option.disabled = true; // Disable all options to prevent changing the answer
    });
}

// Function to submit the selected answer and handle navigation
function submitAnswer(option) {
    const data = { answer: option.innerText.trim() };

    fetch('/check-answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Display explanations for all options
        document.querySelectorAll('.explanation').forEach(explanation => {
            explanation.style.display = 'block';
        });

        // Disable all option buttons to prevent further answers
        document.querySelectorAll('.option').forEach(btn => {
            btn.disabled = true;
            btn.classList.add(btn.innerText.trim() === data.correctAnswer ? 'correct' : 'incorrect');
        });

        // Show next question or results button
        const buttonContainer = document.getElementById('answer-form');
        const actionButton = document.createElement('button');
        actionButton.className = 'navigation-btn';
        if (data.endQuiz) {
            actionButton.innerText = 'Show Results';
            actionButton.onclick = () => window.location.href = "/quiz-results";
        } else {
            actionButton.innerText = 'Next Question';
            actionButton.onclick = () => loadQuestion(data);
        }
        buttonContainer.appendChild(actionButton);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error processing your answer, please try again.');
    });
}

// Function to dynamically load the next question
function loadQuestion(data) {
    const quizContainer = document.querySelector('.quiz-container');
    quizContainer.querySelector('h2').innerText = data.question;
    const image = quizContainer.querySelector('img');
    image.src = '/static/pic/' + data.image;
    image.alt = 'Question Image';

    const buttonContainer = document.getElementById('answer-form');
    buttonContainer.innerHTML = ''; // Clear existing buttons

    data.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'option';
        button.onclick = () => submitAnswer(button);
        button.innerText = option.option;
        buttonContainer.appendChild(button);

        const explanation = document.createElement('div');
        explanation.className = 'explanation';
        explanation.id = 'explanation-' + index;
        explanation.style.display = 'none';
        explanation.innerText = option.explanation;
        buttonContainer.appendChild(explanation);
    });
}