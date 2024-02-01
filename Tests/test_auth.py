import asyncio
import json
import unittest
from unittest.mock import patch
from Handlers.authHandlers import loginAccountHandler
import asyncio


class TestLoginAccountHandler(unittest.IsolatedAsyncioTestCase):

    @patch('Services.authServices.hashString')
    @patch('Core.Shared.DatabaseOperations.Database.getAccountsWithFilter')
    @patch('Services.authServices.createJwtToken')
    async def test_successful_login(self, mock_createJwtToken, mock_getAccountsWithFilter, mock_hashString):
        # Arrange
        test_email = "test@example.com"
        test_password = "securepassword"
        hashed_password = "hashedsecurepassword"
        mock_hashString.return_value = hashed_password
        mock_getAccountsWithFilter.return_value = {
            "message": "Accounts retrieved successfully",
            "accounts": [{"email": test_email.lower(), "password": hashed_password, "status": "active"}]
        }
        mock_createJwtToken.return_value = "test_token"

        # Act
        response = await loginAccountHandler(test_email, test_password)

        # Assert
        response_content = json.loads(response.body.decode())
        self.assertTrue(response_content['success'], msg=f"Expected success to be True but got {response_content['success']}")
        self.assertIn('Bearer test_token', response.headers['Authorization'])

if __name__ == '__main__':
    unittest.main()