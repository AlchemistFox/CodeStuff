import streamlit as st
import re

st.set_page_config(page_title="Veyrathi Translator")

# --- Veyrathi Encoding ---
def to_veyrathi(text):
    words = re.findall(r'\b\w+\b[^\s\w]*|\S', text)
    if not words:
        return ""

    stripped_words = []
    last_letters = []

    for word in words:
        match = re.match(r'(\w+)([^\w]*)', word)
        if not match:
            stripped_words.append(word)
            last_letters.append("")
            continue
        core, punct = match.groups()
        if not core:
            stripped_words.append(word)
            last_letters.append("")
            continue
        stripped_words.append(core[:-1] + punct)
        last_letters.append(core[-1])

    shifted_words = []
    carry = last_letters[-1]

    for i, word in enumerate(stripped_words):
        if not word:
            shifted_words.append(carry)
            carry = last_letters[i]
            continue

        shifted_word = carry + word

        if word[0].isalpha() and word[0].isupper():
            shifted_word = shifted_word.lower()
            shifted_word = shifted_word[0].upper() + shifted_word[1:]

        carry = last_letters[i]
        shifted_words.append(shifted_word)

    return " ".join(shifted_words)

# --- Veyrathi Decoding ---
def from_veyrathi(text):
    words = re.findall(r'\b\w+\b[^\s\w]*|\S', text)
    if not words:
        return ""

    reconstructed_words = []
    carry = words[0][0]

    for i, word in enumerate(words):
        if len(word) <= 1:
            reconstructed_words.append(word)
            continue

        match = re.match(r'(\w+)([^\w]*)', word)
        if not match:
            reconstructed_words.append(word)
            continue

        core, punct = match.groups()

        if i < len(words) - 1:
            new_core = core[1:]
            reconstructed_words.append(new_core + punct)
        else:
            new_core = core[1:] + carry
            reconstructed_words.append(new_core + punct)

    return " ".join(reconstructed_words)

# --- UI ---
st.title("🧬 Veyrathi Translator")

tab1, tab2 = st.tabs(["🔁 English → Veyrathi", "🔁 Veyrathi → English"])

with tab1:
    english_input = st.text_area("Enter English text:")
    if st.button("Translate to Veyrathi"):
        result = to_veyrathi(english_input)
        st.text_area("Veyrathi Output", result, height=150, key="out1")

with tab2:
    veyrathi_input = st.text_area("Enter Veyrathi text:")
    if st.button("Translate to English"):
        result = from_veyrathi(veyrathi_input)
        st.text_area("English Output", result, height=150, key="out2")
