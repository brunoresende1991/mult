# -*- coding: utf-8 -*-
from flask import current_app
from flask_login import UserMixin as LoginUserMixin


class UserMixin(LoginUserMixin):
    """ This class adds methods to the User model class required by Flask-Login and Flask-User."""

    def is_active(self):
        if hasattr(self, 'active'):
            return self.active
        else:
            return self.is_enabled

    def set_active(self, active):
        if hasattr(self, 'active'):
            self.active = active
        else:
            self.is_enabled = active

    def has_role(self, *specified_role_names):
        """ Return True if the user has one of the specified roles. Return False otherwise.

            has_roles() accepts a 1 or more role name parameters
                has_role(role_name1, role_name2, role_name3).

            For example:
                has_roles('a', 'b')
            Translates to:
                User has role 'a' OR role 'b'
        """

        # Allow developers to attach the Roles to the User or the UserProfile object
        if hasattr(self, 'roles'):
            roles = self.roles
        else:
            if hasattr(self, 'user_profile') and hasattr(self.user_profile, 'roles'):
                roles = self.user_profile.roles
            else:
                roles = None
        if not roles:
            return False

        # Translates a list of role objects to a list of role_names
        user_role_names = [role.name for role in roles]

        # Return True if one of the role_names matches
        for role_name in specified_role_names:
            if role_name in user_role_names:
                return True

        # Return False if none of the role_names matches
        return False

    def has_roles(self, *requirements):
        """ Return True if the user has all of the specified roles. Return False otherwise.

            has_roles() accepts a list of requirements:
                has_role(requirement1, requirement2, requirement3).

            Each requirement is either a role_name, or a tuple_of_role_names.
                role_name example:   'manager'
                tuple_of_role_names: ('funny', 'witty', 'hilarious')
            A role_name-requirement is accepted when the user has this role.
            A tuple_of_role_names-requirement is accepted when the user has ONE of these roles.
            has_roles() returns true if ALL of the requirements have been accepted.

            For example:
                has_roles('a', ('b', 'c'), d)
            Translates to:
                User has role 'a' AND (role 'b' OR role 'c') AND role 'd'"""

        # Allow developers to attach the Roles to the User or the UserProfile object
        if hasattr(self, 'roles'):
            roles = self.roles
        else:
            if hasattr(self, 'user_profile') and hasattr(self.user_profile, 'roles'):
                roles = self.user_profile.roles
            else:
                roles = None
        if not roles:
            return False

        # Translates a list of role objects to a list of role_names
        user_role_names = [role.name for role in roles]

        # has_role() accepts a list of requirements
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in user_role_names:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False                    # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if role_name not in user_role_names:
                    return False                    # role_name requirement failed: return False

        # All requirements have been met: return True
        return True

    # Flask-Login is capable of remembering the current user ID in the browser's session.
    # This function enables the user ID to be encrypted as a token.
    # See https://flask-login.readthedocs.org/en/latest/#remember-me
    def get_auth_token(self):
        token_manager = current_app.user_manager.token_manager
        user_id = int(self.get_id())
        token = token_manager.encrypt_id(user_id)
        # print('get_auth_token: user_id=', user_id, 'token=', token)
        return token

    def has_confirmed_email(self):
        db_adapter = current_app.user_manager.db_adapter

        # Handle multiple emails per user: Find at least one confirmed email
        if db_adapter.UserEmailClass:
            has_confirmed_email = False
            user_emails = db_adapter.find_all_objects(db_adapter.UserEmailClass, user_id=self.id)
            for user_email in user_emails:
                if user_email.confirmed_at:
                    has_confirmed_email = True
                    break

        # Handle single email per user
        else:
            has_confirmed_email = True if self.confirmed_at else False

        return has_confirmed_email
