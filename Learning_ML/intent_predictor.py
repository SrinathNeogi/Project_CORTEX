# Learning_ML/intent_predictor.py

import pickle
import re
import warnings
warnings.filterwarnings("ignore")

class IntentPredictor:
    def __init__(self):
        with open("Models/intent_model3.pkl", "rb") as f:
            self.model = pickle.load(f)

        with open("Models/vectorizer3.pkl", "rb") as f:
            self.vectorizer = pickle.load(f)

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return text

    def predict_intent(self, text):
        cleaned_text = self.clean_text(text)

        text_vec = self.vectorizer.transform([cleaned_text])

        prediction = self.model.predict(text_vec)[0]

        # confidence using decision function
        confidence_scores = self.model.decision_function(text_vec)
        confidence = max(confidence_scores[0])

        print(f"[DEBUG] Cleaned: {cleaned_text}")
        print(f"[DEBUG] Prediction: {prediction}")

        return prediction, confidence