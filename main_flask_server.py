#!/usr/bin/python
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

"""Simple server to demonstrate how to use Twitter API and login"""

__author__ = 'joydeepubuntu@gmail.com (Joydeep Bhattacharjee)'

import json
import random
import string

from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from flask import send_file
from flask import session

APPLICATION_NAME = 'Twitter Python QuickStart'

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for x in xrange(32))

@app.route('/', methods=['GET'])
def index():
  """Initialize a session for the current user, and render index.html."""
  # Create a state token to prevent request forgery.
  # Store it in the session for later validation.
  state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                  for x in xrange(32))
  session['state'] = state
  # Set the Client ID, Token State, and Application Name in the HTML while
  # serving it.
  # response = make_response(
  #     render_template('index.html',
  #                     CLIENT_ID=CLIENT_ID,
  #                     STATE=state,
  #                     APPLICATION_NAME=APPLICATION_NAME))
  response = make_response(
       render_template('index.html',
                       STATE=state,
                       APPLICATION_NAME=APPLICATION_NAME))
  response.headers['Content-Type'] = 'text/html'
  return response

@app.route('/signin_button.png', methods=['GET'])
def signin_button():
  """Returns the button image for sign-in."""
  return send_file("templates/signin_button.png", mimetype='image/gif')

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=4568)