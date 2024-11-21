import re
from Backend.models import Data

all_records = Data.objects.all()

for record in all_records:
    print(record)


def clean_text(input_text):
    """
    Removes special characters, emojis, and any non-alphanumeric text, leaving pure text.

    Args:
        input_text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    # Remove emojis and non-printable characters
    text = re.sub(r'[^\x00-\x7F]+', '', input_text)
    # Remove special characters, keeping only letters and numbers
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Example usage
example_text = "Hello! 😊 How are you doing today? Let's clean this text! 🚀✨"
cleaned_text = clean_text(example_text)
print(cleaned_text)  # Output: Hello How are you doing today Lets clean this text

