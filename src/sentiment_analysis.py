from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze(text_obj: dict) -> dict:
    scores = []
    for text in text_obj.values():
        if isinstance(text, str):
            vs = analyzer.polarity_scores(text)
            scores.append(vs["compound"])

        if not scores:
            return {"compound": None, "divergence": None}

        if len(scores) == 1:
            return {"compound": scores[0], "divergence": None}

        return {
            "compound": sum(scores) / len(scores),
            "divergence": max(scores) - min(scores)
        }
