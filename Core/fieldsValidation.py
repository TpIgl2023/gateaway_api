import re
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

class errorsTypes:
    emailInvalid = "Invalid email"
    mobileInvalid = "Invalid mobile"
    nameInvalid = "Invalid name"

class validations:
    
    def validate_email_syntax(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None
    
    
    def validate_password(passwd):
        SpecialSym =['$', '@', '#', '%']
        val = True
        missings = []
        if len(passwd) < 6:
            missings.append('length should be at least 6')
            val = False
        if not any(char.isdigit() for char in passwd):
            missings.append('Password should have at least one numeral')
            val = False
        if not any(char.isupper() for char in passwd):
            missings.append('Password should have at least one uppercase letter')
            val = False
        if not any(char.islower() for char in passwd):
            missings.append('Password should have at least one lowercase letter')
            val = False
        if not any(char in SpecialSym for char in passwd):
            missings.append('Password should have at least one of the symbols $@#%')
            val = False
        return val,missings 
    
    
    def validate_mobile(mobile):
        return carrier._is_mobile(number_type(phonenumbers.parse(mobile)))
        #return True
        
    def validate_name(name):
        if (name.replace(" ", "").isalpha()):
            return True
        else:
            return False
