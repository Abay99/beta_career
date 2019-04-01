# import the User object
from django.contrib.auth.models import User


class SDUPortalAuthenticationBackend:

    def authenticate(self, username=None, password=None):
        """
        Try to find user in SDU portal database and if that user exists, then to create in SBC database
        :param username: Username or maybe email of user
        :type username: str

        :param password: password of user
        :type password: str or maybe encrypted str

        :return: user from SDU portal database
        :rtype: instance of a class
        """
        try:
            if username == username and password == password:
                user = User.objects.create_user(username=username, password=password)
                user.first_name = 'TestFirstName'
                user.last_name = 'TestLastName'
                user.save()
                return user
        except User.DoesNotExists:
            # No user was found, return None - triggers default login failed
            return None
