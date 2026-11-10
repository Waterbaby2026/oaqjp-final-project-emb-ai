"""Watson NLP emotion detection function for the Skills Network project."""



import requests



URL = (
  
    "https://sn-watson-emotion.labs.skills.network/"
  
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
  
)

HEADERS = {
  
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
  
}

EMOTION_LABELS = ("anger", "disgust", "fear", "joy", "sadness")





def emotion_detector(text_to_analyze):
  
    """Return Watson NLP emotion scores and the dominant emotion for text."""
  
    empty_result = {label: None for label in EMOTION_LABELS}
  
    empty_result["dominant_emotion"] = None
  


    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
      
        return empty_result
      


    payload = {"raw_document": {"text": text_to_analyze.strip()}}
  
    response = requests.post(
      
        URL,
      
        headers=HEADERS,
      
        json=payload,
      
        timeout=30,
      
    )
  
    if response.status_code == 400:
      
        return empty_result
      


    response.raise_for_status()
  
    data = response.json()
  
    predictions = data.get("emotionPredictions", [])
  
    if not predictions or not isinstance(predictions[0], dict):
      
        return empty_result
      


    emotions = predictions[0].get("emotion", {})
  
    scores = {label: emotions.get(label) for label in EMOTION_LABELS}
  
    if any(not isinstance(score, (int, float)) for score in scores.values()):
      
        return empty_result
      


    scores["dominant_emotion"] = max(
      
        EMOTION_LABELS,
      
        key=lambda label: scores[label],
      
    )
  
    return scores
  


































