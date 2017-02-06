#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EM_RE =re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EM_RE.match(email)

def html_escape(s):
    return cgi.escape(s, quote=True)

#HTML header
form = """
<!DOCTYPE html>
<htmL>
    <head>
        <title>User Signup</title>
        <style type="text/css">
            .error {
                color:red;
            }
        </style>
    </head>
    <body>
        <h1>Signup</h1>
<form method="post">
    <table>
        <tbody>
            <tr>
                <td><label for="username">Username</label>
                 <td>
                        <input type=text name="username" value="%(username)s" value required>
                        <span class="error">%(username_error)s</span>
                    </td>
                <tr>
                    <td>
                        <label for="password">Password</label>
                    </td>
                    <td>
                        <input type=password name="password" value="%(password)s" required>
                        <span class="error">%(password_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="verify_password">Verify password</label>
                    </td>
                    <td>
                        <input type=password name="verify_password" value="%(verify_password)s" required>
                        <span class="error">%(verify_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="email">Email (optional)</label>
                    </td>
                    <td>
                        <input type=email name="email" value="%(email)s" value>
                        <span class="error">%(email_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                    <input type=submit name="submit">
                    </td>
                </tr>
                </tbody>
            </table>
        </form>
    </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username = "", password = "", verify_password = "", email = "", username_error = "", password_error = "", verify_error = "", email_error = ""):
        self.response.out.write(form % {"username": html_escape(username),
        "password": html_escape(password),
        "verify_password": html_escape(verify_password),
        "email": html_escape(email),
        "username_error": username_error,
        "password_error": password_error,
        "verify_error": verify_error,
        "email_error": email_error})

    def get(self):
        self.write_form()

    def post(self):
            have_error = False
            username = self.request.get("username")
            password = self.request.get("password")
            verify_password = self.request.get("verify_password")
            email = self.request.get("email")
            username_error = ""
            password_error = ""
            verify_error = ""
            email_error = ""

            if (not valid_username) or (not username) or (username.strip() =="") or (" " in username):
                username_error = "That's not a valid username"
                have_error = True

            if (not valid_password) or (not password) or (password.strip()=="") or (" " in password):
                password_error = "That's not a valid password"
                have_error = True

            if password != verify_password:
                verify_error = "Your passwords don't match"
                have_error = True

            if not valid_email(email):
                email_error= "That's not a valid email"
                have_error = True

            if have_error == True:
                self.write_form(username,password,verify_password,email,username_error,password_error,verify_error,email_error)
            else:
                self.redirect("/welcome?username=" + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("<h1>Welcome, " + username + "!</h1>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
