import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary data (only required the first time)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

def remove_stopwords(input_text):
    """
    Removes stop words from the given text using NLTK.

    Args:
        input_text (str): The text to process.

    Returns:
        str: Text without stop words.
    """
    # Get the list of English stop words
    stop_words = set(stopwords.words('english'))

    # Tokenize the input text
    words = word_tokenize(input_text)

    # Remove stop words
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Join the words back into a single string
    return ' '.join(filtered_words)


# Example usage
example_text = "This is an example sentence demonstrating how to remove stop words using NLTK."
cleaned_text = remove_stopwords(example_text)
print(cleaned_text)
