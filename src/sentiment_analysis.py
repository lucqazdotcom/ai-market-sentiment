from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze(text_obj: dict) -> dict:

    score = {"compound": 0, "divergence": 0}
    for text in text_obj.values():
        if text is not None:
            vs = analyzer.polarity_scores(text)
            score["divergence"] = abs(score.get("compound") - vs.get("compound"))
            score["compound"] = score.get("compound") + vs.get("compound")

    return score
