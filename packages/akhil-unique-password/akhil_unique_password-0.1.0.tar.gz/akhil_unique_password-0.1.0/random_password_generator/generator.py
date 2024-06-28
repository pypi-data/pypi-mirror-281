# random_password_generator/generator.py
import random
import string

def generate_password(length=12, include_symbols=True):
    """Generate a random password with the given length.
    
    Args:
        length (int): Length of the password.
        include_symbols (bool): Whether to include symbols in the password.
    
    Returns:
        str: The generated password.
    """
    characters = string.ascii_letters + string.digits
    if include_symbols:
        characters += string.punctuation
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
