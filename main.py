form = """

<!DOCTYPE html>
<html>
<head>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
<body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tbody><tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s">
                        <span class="error">%(usernameError)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password">
                        <span class="error">%(passwordError)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password">
                        <span class="error">%(matchError)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="text" value="%(email)s">
                        <span class="error">%(emailError)s</span>
                    </td>
                </tr>
            </tbody></table>
            <input type="submit">
        </form>

</body>
</html>
"""

import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def validUsername(username):
    return USER_RE.match(username)

def validPassword(password):
    return PASS_RE.match(password)

def validEmail(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", email="", usernameError = "", passwordError ="", matchError = "",emailError=""):
        self.response.out.write(form % {"username": username, "email": email, "usernameError": usernameError, "passwordError":passwordError, "matchError":matchError, "emailError": emailError})

    def get(self):
        self.write_form()

    def post(self):

        usernameInput = self.request.get('username')
        passwordInput = self.request.get('password')
        emailInput = self.request.get('email')
        verifyInput = self.request.get('verify')

        username = usernameInput
        email = emailInput
        password = passwordInput
        verify = verifyInput


        usernameVal = validUsername(usernameInput)
        passwordVal  = validPassword(passwordInput)
        emailVal = validEmail(emailInput)

        matchVal = True
        if passwordInput != verifyInput:
            matchVal = False

        if not usernameVal:
            usernameError = "Please enter a valid username"
        else: usernameError = ""

        if not passwordVal:
            passwordError = "Please enter a valid password"
        else: passwordError = ""

        if not matchVal:
            matchError = "Passwords do not match"
        else: matchError = ""

        if not email:
            emailError = ""
            emailVal = True
        elif not emailVal:
            emailError = "Please enter a valid email address"
        else: emailError = ""

        if not (usernameVal and passwordVal and emailVal and matchVal):
            self.write_form(usernameInput, emailInput, usernameError, passwordError, matchError, emailError)
        else:
            self.redirect('/welcome?username=%s' % username)

class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        print "The string username = ", username
        welcomeMessage = "Welcome, %s!"
        self.response.out.write(welcomeMessage % username)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
