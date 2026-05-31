from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# The actual function lives right here in the same file!
def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyze } }
    
    response = requests.post(url, json=myobj, headers=headers)
    if response.status_code == 400:
        return {
            'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }
        
    formatted_response = json.loads(response.text)
    emotion_predictions = formatted_response['emotionPredictions'][0]['emotion']
    
    emotions = {
        'anger': emotion_predictions.get('anger', 0),
        'disgust': emotion_predictions.get('disgust', 0),
        'fear': emotion_predictions.get('fear', 0),
        'joy': emotion_predictions.get('joy', 0),
        'sadness': emotion_predictions.get('sadness', 0)
    }
    emotions['dominant_emotion'] = max(emotions, key=emotions.get)
    return emotions

@app.route("/emotionDetector")
def emotion_detector_function():
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)
    
    if not response or response.get('dominant_emotion') is None:
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
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)