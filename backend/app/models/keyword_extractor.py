from rake_nltk import Rake
import nltk

nltk.download('stopwords')


class KeywordExtractor:
    def __init__(self):
        self.rake = Rake(language='turkish')

    def extract(self, text, num_keywords=5):
        self.rake.extract_keywords_from_text(text)
        return self.rake.get_ranked_phrases()[:num_keywords]
