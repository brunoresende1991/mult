""" This file creates event notification signals for Flask-User.
    Signals are based on Flask.signals which are based on the blinker signals.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from flask.signals import Namespace

_signals = Namespace()        # Place Flask-User signals in our own namespace

""" *******************
** Flask Signals **
*******************
Flask signals are based on blinker.
Neither Flask nor Flask-User installs blinker
If you plan to use signals, please install blinker with 'pip install blinker'
See http://flask.pocoo.org/docs/signals/"""

# Sent when a user changed their password
user_changed_password = _signals.signal('user.user_changed_password')

# Sent when a user changed their username
user_changed_username = _signals.signal('user.user_changed_username')

# Sent when a user changed their theme
user_changed_theme = _signals.signal('user.user_changed_theme')

# Sent when a user adds a tenant
user_added_tenant = _signals.signal('user.user_added_tenant')

# Sent when a user edits a tenant
user_edited_tenant = _signals.signal('user.user_edited_tenant')

# Sent when a user adds a tenant user
user_added_tenant_user = _signals.signal('user.user_added_tenant_user')

# Sent when a user removes a tenant user
user_removed_tenant_user = _signals.signal('user.user_removed_tenant_user')

# Sent when a user deletes a tenant
user_deleted_tenant = _signals.signal('user.user_deleted_tenant')

# Sent when a user confirmed their email
user_confirmed_email = _signals.signal('user.user_confirmed_email')

# Sent when a user submitted a password reset request
user_forgot_password = _signals.signal('user.forgot_password')

# Sent when a user logged in
user_logged_in = _signals.signal('user.user_logged_in')

# Sent when a user logged out
user_logged_out = _signals.signal('user.user_logged_out')

# Sent when a user registered a new account
user_registered = _signals.signal('user.user_registered')

# Signal sent just after a password was reset
user_reset_password = _signals.signal('user.user_reset_password')

# Signal sent just after a user sent an invitation  # TODO: Not yet implemented
user_sent_invitation = _signals.signal('user.user_sent_invitation')
