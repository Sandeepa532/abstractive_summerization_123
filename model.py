# model.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from keybert import KeyBERT
import torch
import nltk
nltk.download('punkt')
from typing import List, Dict

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def load_summarization_model(model_name="facebook/bart-large-cnn"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model


def generate_summary(text: str, tokenizer, model) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=400,          # for BART
        min_length=120,
        length_penalty=1.0,
        num_beams=6,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    decoded = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Post-processing
    cleaned_summary = decoded.replace('<n>', ' ').replace('\n', ' ').strip()
    cleaned_summary = cleaned_summary[0].upper() + cleaned_summary[1:]

    return cleaned_summary


def get_important_sentences(text: str, summary: str, top_n: int = 5) -> List[str]:
    sentences = sent_tokenize(text)
    important_sentences = sorted(sentences, key=lambda x: len(x), reverse=True)[:top_n]
    return important_sentences

# model.py

def get_excluded_facts(text: str, summary: str, kpm_model=None) -> Dict[str, List[str]]:
    if kpm_model is None:
        kpm_model = KeyBERT()

    sentences = sent_tokenize(text)
    summary_sentences = sent_tokenize(summary)
    excluded = [s for s in sentences if s.strip() not in summary_sentences]
    key_phrases = [phrase for phrase, _ in kpm_model.extract_keywords(text, top_n=10)]

    explanations = {}
    for fact in excluded:
        reasons = []

        fact_lower = fact.lower()
        has_keyphrase = any(kp.lower() in fact_lower for kp in key_phrases)

        if has_keyphrase:
            if len(fact.split()) < 10:
                reasons.append("Omitted because it was a minor fact despite containing a key topic.")
            else:
                reasons.append("Omitted because it was redundant with main summary themes.")
        else:
            reasons.append("Omitted because it did not contain key concepts central to the document.")

        explanations[fact] = reasons

    return explanations
