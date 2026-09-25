"""A deliberately tiny custom-trained model: useful for UI work, not deployment accuracy."""
from functools import lru_cache
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

@lru_cache(maxsize=1)
def load_model():
    examples = [
        ("excellent clear lesson", 1), ("helpful teacher and useful exercises", 1),
        ("great course I enjoyed it", 1), ("good practical examples", 1),
        ("I love the clear explanations", 1), ("wonderful helpful workshop", 1),
        ("terrible confusing lesson", 0), ("unhelpful teacher and boring exercises", 0),
        ("bad course I disliked it", 0), ("poor unclear examples", 0),
        ("I hate the confusing explanations", 0), ("awful unhelpful workshop", 0),
    ]
    model = make_pipeline(TfidfVectorizer(), LogisticRegression(random_state=42))
    model.fit([x for x, _ in examples], [y for _, y in examples])
    return model

def predict(text, threshold=0.6, display="Detailed"):
    if not text or not text.strip():
        return "Please enter a review."
    if len(text) > 2000:
        return "Please use 2,000 characters or fewer."
    probabilities = load_model().predict_proba([text])[0]
    confidence = float(max(probabilities))
    label = "Positive" if probabilities[1] >= probabilities[0] else "Negative"
    if confidence < threshold:
        label = "Needs human review"
    if display == "Label only":
        return label
    return f"{label} | model score: {confidence:.2f} (uncalibrated; not a guarantee)"
