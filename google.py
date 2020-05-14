from flask import flash, abort, session
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint, google
import requests
import os

import auth


def loggedin():
    return google.authorized

def userinfo():
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return resp.json()

class Blueprint:
    def __init__(self, sql):
        self.sql = sql
        self.bp = make_google_blueprint(
            client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
            client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
            scope=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
            hosted_domain=auth.domain
        )

    def setstorage(self, s):
        self.bp.storage = s

def setupoauth(bpobj):
    @oauth_authorized.connect_via(bpobj.bp)
    def check_hosted_domain_and_email(blueprint, token):
        user = userinfo()
        lguser = bpobj.sql.getuser(user['email'])
        if lguser is None:
            flash("Unauthorized user "+user['email'])
            if user["hd"] != blueprint.authorization_url_params["hd"]:
                print("HOSTED DOMAIN ERROR: "+user["hd"])
            requests.post(
                "https://accounts.google.com/o/oauth2/revoke",
                params={"token": token["access_token"]}
            )
            session.clear()
            abort(403)
        else:
            flash("Logged in "+user['email'])
            if lguser.name is None:
                bpobj.sql.setname(lguser, user['name'])
            auth.login_user(lguser)
