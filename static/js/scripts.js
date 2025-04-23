// This file contains the JavaScript code for the web application, handling user interactions, managing the flow between pages, and processing user input.

let currentQuestionIndex = 0;
let correctAnswers = 0;
let totalQuestions = 0;
let questions = [];

// Fetch questions from the CSV file
fetch('/q_and_answer.csv')
    .then(response => response.text())
    .then(data => {
        const rows = data.split('\n').slice(1);
        totalQuestions = rows.length;
        questions = rows.map(row => {
            const [imageName, realOrAI, reasoning] = row.split(',');
            return { imageName, realOrAI, reasoning };
        });
        shuffleQuestions();
        loadQuestion();
    });

// Shuffle questions for random order
function shuffleQuestions() {
    for (let i = questions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [questions[i], questions[j]] = [questions[j], questions[i]];
    }
}

// Load the current question
function loadQuestion() {
    if (currentQuestionIndex < totalQuestions) {
        const question = questions[currentQuestionIndex];
        document.getElementById('image').src = `/static/images/${question.imageName}`;
        document.getElementById('question').innerText = "Is this radiograph AI‑generated or authentic (real)?";
        document.getElementById('ai-button').onclick = () => checkAnswer('AI');
        document.getElementById('real-button').onclick = () => checkAnswer('Real');
    } else {
        window.location.href = '/final';
    }
}

// Check the user's answer
function checkAnswer(userAnswer) {
    const correctAnswer = questions[currentQuestionIndex].realOrAI;
    if (userAnswer === correctAnswer) {
        correctAnswers++;
    }
    currentQuestionIndex++;
    showResult();
}

// Show the result of the current answer
function showResult() {
    const resultPage = document.getElementById('result-page');
    resultPage.style.display = 'block';
    resultPage.innerHTML = `
        <img src="/static/images/${questions[currentQuestionIndex - 1].imageName}" alt="X-Ray Image">
        <p>Your answer: ${questions[currentQuestionIndex - 1].realOrAI}</p>
        <p>Total correct answers: ${correctAnswers}</p>
        <p>Questions left: ${totalQuestions - currentQuestionIndex}</p>
        <button onclick="loadQuestion()">Next Question</button>
    `;
}