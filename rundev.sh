export DEBUG=True
export OAUTHLIB_INSECURE_TRANSPORT=1
export SECRET_KEY='clavesecreto'
# export CLIENT_SECRET_FILE='client_secret.json'
export CLIENT_SECRET_FILE='client_secret.json'
export CLIENT_ID='673297702802-meoqb93la7chfs2frqpbqrdqa0c0ts0k.apps.googleusercontent.com'
export ADMIN_EMAIL='xana.wines.ada@gmail.com'
export DATABASE_URL="sqlite:///$(pwd)/app.db"
export CLIENT_SECRET='_kEtgRvZDc5oIqujt_Qle9FL'
echo $DATABASE_URL

python flask-app.py
