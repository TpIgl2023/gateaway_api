import re
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

def validate_email_syntax(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_password(password):  
    if len(password) < 8:  
        return False  
    if not re.search("[a-z]", password):  
        return False  
    if not re.search("[A-Z]", password):  
        return False  
    if not re.search("[0-9]", password):  
        return False  
    return True 


"""
def validate_mobile(value):
    Raise a ValidationError if the value looks like a mobile telephone number.
    rule = re.compile(r'/^[0-9]{10,14}$/')

    if not rule.search(value):
        msg = u"Invalid mobile number."
        raise ValidationError(msg)

"""

def validate_mobile(mobile):
    return carrier._is_mobile(number_type(phonenumbers.parse(mobile)))

def validate_name(name):
    if (name.replace(" ", "").isalpha() & len(name) < 20):
        return True
    else:
        return False