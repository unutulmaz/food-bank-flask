from flask import redirect, request, url_for, session
from app import app

import os
import tempfile
import simplejson as json

import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery

# CLIENT_SECRET_FILE = json.loads(os.environ['CLIENT_SECRETS_FILE'])
# CLIENT_SECRET_FILE = os.environ['CLIENT_SECRETS_FILE']

SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/calendar']
APPLICATION_NAME='Bethany Food Bank'
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']

def client_secrets():
    # secret =  {
    #     "web": {
    #         "client_id": os.environ['CLIENT_ID'],
    #         "client_secret": os.environ['CLIENT_SECRET'],
    #         "redirect_uris": ['https://bethany-food-bank.herokuapp.com/oauth2callback', 'http://localhost:5000/oauth2callback'],
    #         "auth_uri": 'https://accounts.google.com/o/oauth2/auth'
    #         "token_uri": 'https://accounts.google.com/o/oauth2/token'
    #     }
    # }

    secret =  {
        'web': {
            'client_id': os.environ['CLIENT_ID'],
            'project_id': 'bethany-food-bank',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://accounts.google.com/o/oauth2/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_secret': os.environ['CLIENT_SECRET'],
            'redirect_uris': ['https://bethany-food-bank.herokuapp.com/oauth2callback', 'http://localhost:5000/oauth2callback'],
            'javascript_origins': ['https://bethany-food-bank-heroku.herokuapp.com', 'http://localhost:5000']
        }
    }

    return secret




def credentials_to_dict(credentials):
    return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

@app.route('/authorize')
def authorize():
    CLIENT_SECRET_FILE = client_secrets()
    flow=google_auth_oauthlib.flow.Flow.from_client_config(client_config=CLIENT_SECRET_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    CLIENT_SECRET_FILE = client_secrets()
    state = session['state']

    flow=google_auth_oauthlib.flow.Flow.from_client_config(client_config=CLIENT_SECRET_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('admin_login'))
