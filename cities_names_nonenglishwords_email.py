import spacy
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect, DetectorFactory

# Ensure reproducibility in langdetect
DetectorFactory.seed = 0

# Load spaCy's English NER model
nlp = spacy.load("en_core_web_sm")

# Initialize the set of English stopwords
nltk.download('stopwords', quiet=True)
english_stopwords = set(stopwords.words('english'))

# Caesar Cipher functions for encryption and decryption
def caesar_cipher(text, shift=3):
    return "".join(chr((ord(char) + shift - 65) % 26 + 65) if char.isupper() else chr((ord(char) + shift - 97) % 26 + 97) if char.islower() else char for char in text)

def caesar_cipher_decrypt(text, shift=3):
    return "".join(chr((ord(char) - shift - 65) % 26 + 65) if char.isupper() else chr((ord(char) - shift - 97) % 26 + 97) if char.islower() else char for char in text)

def encrypt_data(text):
    # Process the text with spaCy for NER
    doc = nlp(text)
    encrypted_text = text

    # Regex for email detection
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.finditer(email_regex, text)

    # Lists for identified entities and encrypted mappings
    encryption_map = []

    # Encrypt entities identified by spaCy NER
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "GPE"]:
            encrypted_entity = caesar_cipher(ent.text)
            encryption_map.append((ent.text, encrypted_entity))
            encrypted_text = encrypted_text.replace(ent.text, encrypted_entity)

    # Encrypt email addresses
    for match in email_matches:
        email = match.group()
        encrypted_email = caesar_cipher(email)
        encryption_map.append((email, encrypted_email))
        encrypted_text = re.sub(re.escape(email), encrypted_email, encrypted_text)

    # Encrypt non-English and non-stop words
    words = set(word_tokenize(encrypted_text))  # Tokenize the already partially encrypted text
    for word in words:
        if word.isalpha() and word.lower() not in english_stopwords:
            try:
                if detect(word) != 'en':
                    encrypted_word = caesar_cipher(word)
                    if word not in dict(encryption_map):  # Check if not already encrypted
                        encryption_map.append((word, encrypted_word))
                        encrypted_text = re.sub(r'\b' + re.escape(word) + r'\b', encrypted_word, encrypted_text)
            except:
                pass

    return encrypted_text, encryption_map

def decrypt_data(text, encryption_map):
    decrypted_text = text
    # Reverse the map for decryption to ensure correct order
    for original, encrypted in reversed(encryption_map):
        decrypted_text = decrypted_text.replace(encrypted, original)
    return decrypted_text

# Example usage
original_text = "John Doe, a Developer from New York, can be reached at john.doe@example.com.John Doe, a Developer from New York, can be reached at john.doe@example.com.John Doe, a Developer from New York, can be reached at john.doe@example.com."

print("Original Text:", original_text)
encrypted_text, encryption_map = encrypt_data(original_text)
print("\nEncrypted Text:", encrypted_text)

decrypted_text = decrypt_data(encrypted_text, encryption_map)
print("\nDecrypted Text:", decrypted_text)
