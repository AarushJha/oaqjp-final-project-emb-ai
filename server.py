"""
This module initiates a Flask web application server layer interface.
It handles user requests and routes them to the EmotionDetection backend engine.
"""
from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector")
def emotion_detector_function():
    """
    Web route interface wrapper function. Evaluates text inputs from query strings
    and returns custom formatted response strings or explicit error fallbacks.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)
    
    # Intercept when dominant_emotion evaluates to None
    if response.get('dominant_emotion') is None:
        return "Invalid text! Please try again!"
        
    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

@app.route("/")
def render_index_page():
    """
    Serves the default index interface view layout page upon arrival.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
