from google.cloud import language
from google.cloud.language import Document


def get_sentiment_score(text):
    client = language.LanguageServiceClient()
    document = Document(content=text, type=Document.Type.PLAIN_TEXT)
    
    return client.analyze_sentiment(document=document).document_sentiment.score
