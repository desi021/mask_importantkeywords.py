from langdetect import detect, DetectorFactory
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords

# Ensure reproducibility
DetectorFactory.seed = 0

# Initialize the set of English stopwords
nltk.download('stopwords')
english_stopwords = set(stopwords.words('english'))

# Caesar Cipher functions for encryption and decryption
def caesar_cipher(text, shift=3):
    return "".join(chr((ord(char) + shift - 65) % 26 + 65) if char.isupper() else chr((ord(char) + shift - 97) % 26 + 97) if char.islower() else char for char in text)

def caesar_cipher_decrypt(text, shift=3):
    return "".join(chr((ord(char) - shift - 65) % 26 + 65) if char.isupper() else chr((ord(char) - shift - 97) % 26 + 97) if char.islower() else char for char in text)

# Encrypt non-English words and personal information
def encrypt_data(text, name, city, email, designation):
    words = word_tokenize(text)
    encryption_map = []

    # Encrypt non-English words
    for word in words:
        if word.isalpha() and word.lower() not in english_stopwords:
            try:
                if detect(word) != 'en':
                    encrypted_word = caesar_cipher(word)
                    encryption_map.append((word, encrypted_word))
                    text = text.replace(word, encrypted_word)
            except:
                pass

    # Encrypt personal information
    encrypted_name = caesar_cipher(name)
    encrypted_city = caesar_cipher(city)
    encrypted_email = caesar_cipher(email)
    encrypted_designation = caesar_cipher(designation)

    return text, encrypted_name, encrypted_city, encrypted_email, encrypted_designation, encryption_map

# Decrypt encrypted words and personal information
def decrypt_data(text, encrypted_name, encrypted_city, encrypted_email, encrypted_designation, encryption_map):
    # Decrypt words in the text
    for original, encrypted in encryption_map:
        text = text.replace(encrypted, original)

    # Decrypt personal information
    decrypted_name = caesar_cipher_decrypt(encrypted_name)
    decrypted_city = caesar_cipher_decrypt(encrypted_city)
    decrypted_email = caesar_cipher_decrypt(encrypted_email)
    decrypted_designation = caesar_cipher_decrypt(encrypted_designation)

    return text, decrypted_name, decrypted_city, decrypted_email, decrypted_designation

# Example usage
original_text = "John Doe is a Developer from New York. His email is john.doe@example.com."
name = "John Doe"
city = "New York"
email = "john.doe@example.com"
designation = "Developer"

print("Original Text:", original_text)
encrypted_text, encrypted_name, encrypted_city, encrypted_email, encrypted_designation, encryption_map = encrypt_data(original_text, name, city, email, designation)
print("\nEncrypted Text:", encrypted_text)
print("Encrypted Name:", encrypted_name)
print("Encrypted City:", encrypted_city)
print("Encrypted Email:", encrypted_email)
print("Encrypted Designation:", encrypted_designation)

decrypted_text, decrypted_name, decrypted_city, decrypted_email, decrypted_designation = decrypt_data(encrypted_text, encrypted_name, encrypted_city, encrypted_email, encrypted_designation, encryption_map)
print("\nDecrypted Text:", decrypted_text)
print("Decrypted Name:", decrypted_name)
print("Decrypted City:", decrypted_city)
print("Decrypted Email:", decrypted_email)
print("Decrypted Designation:", decrypted_designation)
