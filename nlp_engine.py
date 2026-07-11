import os
import json
import nltk
import numpy as np

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download stopwords if not available
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


class NLPEngine:
    def __init__(self, faq_file):
        self.faq_file = faq_file
        self.stop_words = stopwords.words("english")
        self.vectorizer = TfidfVectorizer(stop_words=self.stop_words)

        self.faqs = []
        self.questions = []
        self.answers = []
        self.tfidf_matrix = None

        self.load_faqs()

    def load_faqs(self):
        """Load FAQs from JSON file"""

        if not os.path.exists(self.faq_file):
            self.faqs = []
            self.questions = []
            self.answers = []
            return

        with open(self.faq_file, "r", encoding="utf-8") as file:
            self.faqs = json.load(file)

        self.questions = [faq["question"] for faq in self.faqs]
        self.answers = [faq["answer"] for faq in self.faqs]

        if len(self.questions) > 0:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def retrain(self):
        """Rebuild TF-IDF model"""

        self.questions = [faq["question"] for faq in self.faqs]
        self.answers = [faq["answer"] for faq in self.faqs]

        if len(self.questions) > 0:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def match_question(self, user_question, threshold=0.30):

        if self.tfidf_matrix is None:
            return (
                "Sorry! FAQ database is empty.",
                0.0,
                []
            )

        user_vector = self.vectorizer.transform([user_question])

        similarity = cosine_similarity(
            user_vector,
            self.tfidf_matrix
        )

        best_index = np.argmax(similarity)

        confidence = float(similarity[0][best_index])

        if confidence >= threshold:

            return (
                self.answers[best_index],
                confidence,
                []
            )

        suggestions = []

        sorted_indexes = similarity.argsort()[0][-3:][::-1]

        for i in sorted_indexes:
            suggestions.append(self.questions[i])

        return (
            "Sorry, I couldn't find an exact answer.",
            confidence,
            suggestions
        )

    def get_all_faqs(self):
        return self.faqs

    def add_faq(self, question, answer):

        new_id = 1

        if len(self.faqs) > 0:
            new_id = max(faq["id"] for faq in self.faqs) + 1

        self.faqs.append({
            "id": new_id,
            "question": question,
            "answer": answer
        })

        self.save_faqs()

    def delete_faq(self, faq_id):

        self.faqs = [
            faq for faq in self.faqs
            if faq["id"] != faq_id
        ]

        self.save_faqs()

    def save_faqs(self):

        with open(self.faq_file, "w", encoding="utf-8") as file:
            json.dump(
                self.faqs,
                file,
                indent=4,
                ensure_ascii=False
            )

        self.retrain()