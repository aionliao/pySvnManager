# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 OpenSourceXpress Ltd. (http://www.ossxp.com)
# Author: Jiang Xin
# Contact: http://www.ossxp.com
#          http://www.worldhello.net
#          http://moinmo.in/JiangXin
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import logging

from pysvnmanager.lib.base import *

from crypt import crypt

log = logging.getLogger(__name__)

class SecurityController(BaseController):

    def index(self):
        """
        Show login form. Submits to login/submit
        """
        return render('/login/login.mako')

    def submit(self):
        """
        Verify username and password
        """
        auth_passed = False
        # Both fields filled?
        username = request.params.get('username')
        password = request.params.get('password')

        for auth in cfg.auth:
            if auth(username=username, password=password, config=cfg):
                auth_passed = True
                break
        
        # Mark user as logged in
        if auth_passed:
            session['user'] = username
            log.info(_(u"User %s logged in") % session['user'])
            session.save()

            # Send user back to the page he originally wanted to get to
            if session.get('path_before_login'):
                redirect_to(session['path_before_login'])
            else: # if previous target is unknown just send the user to a welcome page
                redirect_to(h.url_for(controller='check'))
        else:
            session.clear()
            session.save()
            c.login_message = _(u"Login failed for user: %s") % username
            return render('/login/login.mako')

    def logout(self):
        """
        Logout the user and display a confirmation message
        """
        if 'user' in session:
            log.info(_("User %s logged out") % session['user'])
            del session['user']
            session.save()
        redirect_to(h.url_for(controller="security"))

    def failed(self):
        return render('/auth_failed.mako')