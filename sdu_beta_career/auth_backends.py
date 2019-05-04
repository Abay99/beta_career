from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


UserModel = get_user_model()


class SBCAuthenticationBackend(ModelBackend):

    def authenticate(self, username: Optional[str]=None, password: Optional[str]=None, **kwargs) -> Optional[User]:
        """
        At first try to find and authenticate user in SBC database, and if that user doesn't exist, then
        try to find user in SDU portal database and if that user exists, then to create in SBC database
        :param username: Username or maybe email of user
        :param password: password of user
        :return: user from SBC db or SDU portal db
        """
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if not(user.check_password(password) and self.user_can_authenticate(user)):
                # Try to find user in SDU portal database
                user = self.get_portal_user(username, password)
            return user

    @staticmethod
    def get_portal_user(username: Optional[str]=None, password: Optional[str]=None) -> Optional[User]:
        if username == username and password == password:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name='TestFirstName',
                                            last_name='TestLastName')
            return user
