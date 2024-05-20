# %% Import Libraries ---------------------------------------------------------
import re
import requests
import base64


# %% Function Definitions -----------------------------------------------------
# Remove and Add Whitespace Characters
def add_remove_characters(text):
    """
    1. Removing leading and trailing whitespace characters.
    2. Replacing consecutive whitespace characters with a single space.
    3. Adding a space before each opening parenthesis and
        removing any space after it.
    4. Removing any space before a closing parenthesis.
    5. Adding a space after each closing parenthesis,
        except for those at the end of the text.
    6. Removing any space before and after the hyphen character.
    7. Removing special character.

    Args:
        text (str): The input text to be cleaned

    Returns:
        str: The cleaned text
    """
    # Remove leading and trailing whitespace characters
    text = text.strip()

    # Replace consecutive whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text)

    # Add a space before each opening parenthesis
    # and remove any space after it
    text = re.sub(r'(?<!\s)\(', ' (', text)
    text = re.sub(r'\(\s', '(', text)

    # Remove any space before a closing parenthesis
    text = re.sub(r'\s+\)', ')', text)

    # Add a space after each closing parenthesis,
    # except for those at the end of the text
    text = re.sub(r'\)(?=\S)', ') ', text)

    # Remove any space before and after the hyphen character
    text = re.sub(r'\s*-\s*', '-', text)

    # Remove the underscore character
    text = text.replace('_', '')
    text = text.replace('*', '')

    return text


# Get Elevation
def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        elevation_data = response.json()
        elevation = elevation_data['results'][0]['elevation']
        return elevation
    else:
        return None


# Generate Base64 ID
def generate_base64_id(text):
    btext = text.encode('utf-8')
    btext64 = base64.b64encode(btext)
    return base64.b64encode(btext64).decode("ascii")

# %%
