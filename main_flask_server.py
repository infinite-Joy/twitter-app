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
from threading import Timer

from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from flask import send_file
from flask import session

import twitter
from twitter.oauth_dance import parse_oauth_tokens
from twitter.oauth import read_token_file, write_token_file

import webbrowser

OAUTH_FILE = "/tmp/twitter_oauth"

CONSUMER_KEY='eRns5llTwtaKEtRIuUitLza16'
CONSUMER_SECRET='82GLcF9igdVH09o3Ti8GsBtTqqxtPalxBiZvM3XQRIRKpxuClM'
oauth_callback = 'http://127.0.0.1:5000/oauth_helper'

APPLICATION_NAME = 'Twitter Python QuickStart'

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))


#@webserver.route("/oauth_helper")
@app.route("/oauth_helper")
def oauth_helper():
    
    oauth_verifier = request.args.get('oauth_verifier')

      # Pick back up credentials from ipynb_oauth_dance
    oauth_token, oauth_token_secret = read_token_file(OAUTH_FILE)
    
    _twitter = twitter.Twitter(
        auth=twitter.OAuth(
            oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
        format='', api_version=None)

    oauth_token, oauth_token_secret = parse_oauth_tokens(
        _twitter.oauth.access_token(oauth_verifier=oauth_verifier))

    # This web server only needs to service one request, so shut it down
    # shutdown_after_request = request.environ.get('werkzeug.server.shutdown')
    # shutdown_after_request()

    # Write out the final credentials that can be picked up after the blocking
    # call to webserver.run() below.
    write_token_file(OAUTH_FILE, oauth_token, oauth_token_secret)
    return "%s %s written to %s" % (oauth_token, oauth_token_secret, OAUTH_FILE)


def ipynb_oauth_dance():
    
    _twitter = twitter.Twitter(
        auth=twitter.OAuth('', '', CONSUMER_KEY, CONSUMER_SECRET),
        format='', api_version=None)

    oauth_token, oauth_token_secret = parse_oauth_tokens(
            _twitter.oauth.request_token(oauth_callback=oauth_callback))

    # Need to write these interim values out to a file to pick up on the callback from Twitter
    # that is handled by the web server in /oauth_helper
    write_token_file(OAUTH_FILE, oauth_token, oauth_token_secret)
    
    oauth_url = ('http://api.twitter.com/oauth/authorize?oauth_token=' + oauth_token)
    oauth_url = oauth_url.replace("http", "https")
    print oauth_url
    
    # Tap the browser's native capabilities to access the web server through a new window to get
    # user authorization
    webbrowser.open_new(oauth_url)
    #display(JS("window.open('%s')" % oauth_url))


def oauth_login():
    # After the webserver.run() blocking call, start the oauth dance that will ultimately
    # cause Twitter to redirect a request back to it. Once that request is serviced, the web
    # server will shutdown, and program flow will resume with the OAUTH_FILE containing the
    # necessary credentials
    Timer(1, lambda: ipynb_oauth_dance()).start()

    #webserver.run(host='0.0.0.0')
    print "2"

    # The values that are read from this file are written out at
    # the end of /oauth_helper
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_token_file(OAUTH_FILE)
    # XXX: Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://dev.twitter.com/docs/auth/oauth for more information
    # on Twitter's OAuth implementation.
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


@app.route('/', methods=['POST', 'GET'])
def index():
    """Initialize a session for the current user, and render index.html."""
    # Create a state token to prevent request forgery.
    # Store it in the session for later validation.
    if request.method == 'POST':
      oauth_login()
        #return redirect(oauth_login())
        return response

    elif request.method == 'GET':


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
    app.run(host='0.0.0.0', port=5000)