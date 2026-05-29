import string

def password(password):
    errors = []
    if not (8 <= len(password) <= 16):
        errors.append("Length of the password should be greater than 8 and less than 16.")
    if not any(char.isdigit() for  char in password):
        errors.append("Password should have at least one digit.")
    if not any(char.isupper() for char in password):
        errors.append("Password should have at least one uppercase letter.")
    if not any(char.islower() for char in password):
        errors.append("Password should have at least one lowercase letter.")
    if not any(char in string.punctuation for char in password):
        errors.append("Password should have at least one special character.")
    
    return len(errors) == 0, errors