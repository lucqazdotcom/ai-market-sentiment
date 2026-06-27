from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
def analyze(something: str):
    vs = analyzer.polarity_scores(something)
    if vs.get("compound") >= 0.05:
        print("positive")
    if vs.get("compound") > -0.05 and vs.get("compound") < 0.05:
        print("neutral")
    if vs.get("compound") <= -0.05:
        print("negative")
