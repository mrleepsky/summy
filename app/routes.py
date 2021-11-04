from urllib.parse import unquote_plus

import spacy
from flask import abort, jsonify, request
from sklearn.feature_extraction.text import CountVectorizer
from spacy.lang.en.stop_words import STOP_WORDS

from app import app, db
from app.models import Document

NLP = spacy.load("en_core_web_sm")
TEXT_KEY = "text"


def verify_request():
    """Verify if request content type is correct and necessary keys are included."""
    x_www_form_urlencoded_type = "application/x-www-form-urlencoded"

    if request.content_type != x_www_form_urlencoded_type:
        abort(415, description=f"Supported media type: {x_www_form_urlencoded_type}")

    if TEXT_KEY not in request.form:
        abort(400, description=f"Missing `{TEXT_KEY}` key")


def get_word_frequency(text):
    """Return dictionary with words as keys and frequencies as values."""
    sentences = [sentence.text.lower() for sentence in text.sents]

    cv = CountVectorizer(stop_words=list(STOP_WORDS))
    cv_transformation = cv.fit_transform(sentences)

    words = cv.get_feature_names()
    frequencies = cv_transformation.toarray().sum(axis=0)

    return dict(zip(words, frequencies))


def get_relative_word_frequency(word_frequency):
    """Return dictionary with words as keys and relative frequencies as values."""
    max_frequency = max(word_frequency.values())

    relative_word_frequency = {}
    for word, frequency in word_frequency.items():
        relative_word_frequency[word] = frequency / max_frequency

    return relative_word_frequency


def get_sentence_ranking(text, relative_word_frequency):
    """Return dictionary with sentences as keys and total value of relative word frequencies present in sentence."""
    sentence_ranking = {}
    for sentence in text.sents:
        for word in sentence:
            lower_word = word.text.lower()
            if lower_word in relative_word_frequency.keys():
                frequency = relative_word_frequency[lower_word]
                if sentence in sentence_ranking.keys():
                    sentence_ranking[sentence] += frequency
                else:
                    sentence_ranking[sentence] = frequency

    return sentence_ranking


def get_summary(sentence_ranking, sentence_number=3):
    """Return summary based on sentence ranking. Summary length can be changed by `sentence_number`."""
    sorted_scores = sorted(sentence_ranking.values(), reverse=True)
    summary_scores = sorted_scores[:sentence_number]

    return " ".join([str(sentence) for sentence, score in sentence_ranking.items() if score in summary_scores])


@app.post("/document")
def post_document():
    """Create new document summary."""
    verify_request()

    text = NLP(unquote_plus(request.form[TEXT_KEY]))
    word_frequency = get_word_frequency(text)
    relative_word_frequency = get_relative_word_frequency(word_frequency)
    sentence_ranking = get_sentence_ranking(text, relative_word_frequency)
    summary = get_summary(sentence_ranking)

    document = Document(body=str(text), summary=summary)
    db.session.add(document)
    db.session.commit()

    return jsonify({"document_id": document.id})


@app.route("/document/<document_id>")
def get_document(document_id):
    """Get document summary for provided document ID."""
    document = Document.query.filter_by(id=document_id).first()

    return (
        jsonify({"document_id": document.id, "summary": document.summary})
        if document is not None
        else abort(404, description="Document not found")
    )
