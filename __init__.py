from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clé privée
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Expiration du jeton après 1 heure
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return render_template('accueil.html')

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    # Vérification des identifiants
    if username == "admin" and password == "admin":
        role = "admin"
    elif username == "test" and password == "test":
        role = "user"
    else:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    # Création du jeton JWT avec l'identité de l'utilisateur et son rôle
    access_token = create_access_token(identity=username, additional_claims={"role": role})
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    # Récupérer les données du JWT
    claims = get_jwt_identity()
    role = claims.get("role")
    
    # Vérifier si l'utilisateur a le rôle "admin"
    if role != "admin":
        return jsonify({"msg": "Accès refusé, vous n'êtes pas un administrateur"}), 403

    return jsonify({"msg": "Bienvenue sur la page admin"}), 200

if __name__ == "__main__":
    app.run(debug=True)
