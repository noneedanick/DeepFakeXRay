// static/js/scripts.js
let currentQuestionIndex = 0;
let correctAnswers = 0;
let questions = [];

// load & parse CSV
fetch(window.CSV_URL)
  .then(r => r.text())
  .then(csv => {
    const parsed = Papa.parse(csv, { header: true, skipEmptyLines: true });
    questions = parsed.data.sort(() => 0.5 - Math.random());
    loadQuestion();
  });

  function loadQuestion() {
    if (currentQuestionIndex >= questions.length) {
      window.location.href = 'final.html';
      return;
    }
    const q = questions[currentQuestionIndex];
    document.getElementById('image').src = `images/${q.Image_Name}`;
    document.getElementById('question').innerText = 'Is this radiograph AI‑generated or authentic (real)?';
    document.getElementById('ai-button').onclick   = () => checkAnswer('AI');
    document.getElementById('real-button').onclick = () => checkAnswer('Real');
  
    // SHOW quiz, HIDE result
    document.getElementById('quiz-page').style.display   = 'block';
    document.getElementById('result-page').style.display = 'none';
  
    updateStats();
  }

let answeredCount = 0;

function checkAnswer(userAnswer) {
  const correctAnswer = questions[currentQuestionIndex].Real_or_AI;
  if (userAnswer === correctAnswer) {
    correctAnswers++;
  }
  answeredCount++;
  showResult(userAnswer);
  currentQuestionIndex++;
}

function showResult(userAnswer) {
    const q = questions[currentQuestionIndex];
    const el = document.getElementById('result-page');
    document.getElementById('quiz-page').style.display = 'none';
  
    const userClass    = userAnswer === 'Real' ? 'answer-real' : 'answer-ai';
    const correctClass = q.Real_or_AI  === 'Real' ? 'answer-real' : 'answer-ai';
  
    el.innerHTML = `
      <img src="images/${q.Image_Name}" class="xray-image">
      <p><b>Your answer:</b>
        <span class="answer-btn ${userClass}">${userAnswer}</span>
      </p>
      <p><b>Correct answer:</b>
        <span class="answer-btn ${correctClass}">${q.Real_or_AI}</span>
      </p>
      <p><b>Explanation:</b> ${q.Reasoning}</p>
      <button class="btn" onclick="loadQuestion()">Next Image</button>
    `;
    el.style.display = 'block';
    updateStats();
  }

function updateStats() {
  const asked = answeredCount;
  const wrong = asked - correctAnswers;
  const accuracy = asked > 0
    ? ((correctAnswers / asked) * 100).toFixed(1)
    : '0.0';
  document.getElementById('correct').innerText  = correctAnswers;
  document.getElementById('wrong').innerText    = wrong;
  document.getElementById('accuracy').innerText = accuracy;
  document.getElementById('remaining').innerText = questions.length - asked;
}