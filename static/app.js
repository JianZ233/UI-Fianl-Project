
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
function submitAnswer() {
    const selectedOption = document.querySelector('.option.clicked');
    if (selectedOption) {
        const data = { answer: selectedOption.innerText.trim() };

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

            // Disable all option buttons to prevent further answers and color them
            document.querySelectorAll('.option').forEach(btn => {
                if (btn.innerText.trim() === data.correctAnswer) {
                    btn.classList.add('correct');
                } else if (btn.classList.contains('clicked')) {
                    btn.classList.add('incorrect');
                }
                btn.disabled = true;
            });

            // Hide the submit button
            document.getElementById("submit-btn").style.display = 'none';

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
        
        // Remove 'clicked' class and onclick attribute from all options
        document.querySelectorAll('.option').forEach(btn => {
            btn.classList.remove('clicked');
            btn.removeAttribute('onclick');
        });
    } else {
        alert("Please select an option before submitting."); // Alert if no option is selected
    }
}

function markClicked(option) {
    // Remove 'clicked' class from previously clicked options
    document.querySelectorAll('.option').forEach(btn => {
        btn.classList.remove('clicked');
    });

    // Add 'clicked' class to the current clicked option
    option.classList.add('clicked');

    // Enable the submit button
    document.getElementById("submit-btn").disabled = false;
}


// Function to dynamically load the next question
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
        button.onclick = () => markClicked(button);
        button.innerText = option.option;
        buttonContainer.appendChild(button);

        const explanation = document.createElement('div');
        explanation.className = 'explanation';
        explanation.id = 'explanation-' + index;
        explanation.style.display = 'none';
        explanation.innerText = option.explanation;
        buttonContainer.appendChild(explanation);
    });

    // Clear clicked option
    document.querySelectorAll('.option').forEach(btn => {
        btn.classList.remove('clicked');
    });

    // Enable the submit button
    document.getElementById("submit-btn").style.display = 'block'; // Add this line
    document.getElementById("submit-btn").disabled = true; // Add this line
}

