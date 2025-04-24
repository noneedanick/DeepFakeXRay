# AI generated X-Ray Detection Training

This project is an educational web application that allows users to determine whether X-Ray images are AI-generated or authentic. The application is built using HTML, CSS, and Python Flask.

URL: https://deepfakexray.onrender.com/

## Project Structure

```
xray-ai-detector
├── app.py                  # Main application file for the Flask web server
├── requirements.txt        # Lists dependencies required for the project
├── q_and_answer.csv        # Ground truth data for the X-Ray images
├── static
│   ├── css
│   │   └── styles.css      # CSS styles for the web application
│   ├── js
│   │   └── scripts.js      # JavaScript code for handling user interactions
│   └── images              # Directory containing X-Ray images
├── templates
│   ├── index.html          # Main page of the application
│   ├── question.html       # Question page displaying X-Ray images
│   ├── result.html         # Results page after user answers
│   └── final.html          # Final page thanking users for participation
└── README.md               # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd DeepFakeXRay
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.

## Usage Guidelines

- Start on the main page, which explains the exercise and its benefits.
- Click the "Start" button to begin answering questions about X-Ray images.
- After each question, view your results and proceed to the next question until all images have been evaluated.
- At the end of the exercise, you will receive a summary of your performance and contact information for further questions.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
