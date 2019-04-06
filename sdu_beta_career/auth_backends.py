# import the User object
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class SDUPortalAuthenticationBackend:

    def authenticate(self, username: str=None, password: str=None) -> 'Optional[User]':
        """
        Try to find and authenticate user in SBC database, and if that user doesn't exist, then
        try to find user in SDU portal database and if that user exists, then to create in SBC database
        :param username: Username or maybe email of user
        :param password: password of user
        :return: user from SBC db or SDU portal db
        """
        try:
            #At first try to find user in SBC database
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExists:
            #Try to find user in SDU portal database
            if username == username and password == password:
                user = User.objects.create_user(username=username,
                                                password=password,
                                                first_name='TestFirstName',
                                                last_name='TestLastName')
                user.save()
                return user
            else:
                return None
