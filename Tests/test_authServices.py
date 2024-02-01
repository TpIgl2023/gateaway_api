from unittest import TestCase

from Services.authServices import validate_email_syntax, validate_password, validate_mobile, validate_name


class Testvalidations(TestCase):
    def test_validate_email_syntax_valid(self):
        self.assertTrue(validate_email_syntax("test@example.com"))

    def test_validate_email_syntax_invalid(self):
        self.assertFalse(validate_email_syntax("invalid-email"))
        self.assertFalse(validate_email_syntax("test@.com"))
        self.assertFalse(validate_email_syntax("test@com"))
        self.assertFalse(validate_email_syntax("test@."))
        self.assertFalse(validate_email_syntax("test@.example."))
        self.assertFalse(validate_email_syntax("test@.example"))
        self.assertFalse(validate_email_syntax("test@example"))
        self.assertFalse(validate_email_syntax("test@.example."))

    def test_validate_password_valid(self):
        val, missings = validate_password("Pass@123")
        self.assertTrue(val)
        self.assertEqual(missings, [])

    def test_validate_password_invalid_short(self):
        val, missings = validate_password("weak")
        self.assertFalse(val)
        self.assertEqual(missings, ['length should be at least 6', 'Password should have at least one numeral',
                                    'Password should have at least one uppercase letter',
                                    'Password should have at least one of the symbols $@#%'])

    def test_validate_password_invalid_no_numeral(self):
        val, missings = validate_password("Weak@Password")
        self.assertFalse(val)
        self.assertEqual(missings, ['Password should have at least one numeral'])

    def test_validate_password_invalid_no_uppercase(self):
        val, missings = validate_password("weak@password1")
        self.assertFalse(val)
        self.assertEqual(missings, ['Password should have at least one uppercase letter'])

    def test_validate_password_invalid_no_lowercase(self):
        val, missings = validate_password("WEAK@PASSWORD1")
        self.assertFalse(val)
        self.assertEqual(missings, ['Password should have at least one lowercase letter'])

    def test_validate_password_invalid_no_symbol(self):
        val, missings = validate_password("WeakPassword1")
        self.assertFalse(val)
        self.assertEqual(missings, ['Password should have at least one of the symbols $@#%'])

    def test_validate_mobile_valid(self):
        self.assertTrue(validate_mobile("1234567890"))
        self.assertTrue(validate_mobile("11234567890"))

    def test_validate_mobile_invalid(self):
        self.assertFalse(validate_mobile("invalid-number"))
        self.assertFalse(validate_mobile("+12345"))  # Too short
        self.assertFalse(validate_mobile("+12345678901234567890"))  # Too long
        self.assertFalse(validate_mobile("1234567890"))  # Missing '+'
        self.assertFalse(validate_mobile("invalid"))  # No digits
        self.assertFalse(validate_mobile("+1234invalid"))  # Alphanumeric

    def test_validate_name_valid(self):
        self.assertTrue(validate_name("John Doe"))

    def test_validate_name_invalid(self):
        self.assertFalse(validate_name("John123"))