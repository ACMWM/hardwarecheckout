from flask import session, abort
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint, google
import requests

bp = make_google_blueprint(
    client_id="foo",
    client_secret="bar",
    scope=["profile", "email"],
    hosted_domain="acmhw.tookmund.com"
)

@oauth_authorized.connect_via(bp)
def logged_in(blueprint, token):
    resp_json = google.get("/oauth2/v2/userinfo").json()
    if resp_json["hd"] != blueprint.authorization_url_params["hd"]:
        requests.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token["access_token"]}
        )
        session.clear()
        abort(403)
