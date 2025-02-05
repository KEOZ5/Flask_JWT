from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Configuration de JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # C'est une clé secrète pour signer les JWT
jwt = JWTManager(app)

# Route publique d'accueil
@app.route('/')
def hello_world():
    return jsonify(message="Bienvenue sur l'API JWT!")

# Route de login pour obtenir un jeton JWT
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # Exemple de vérification des utilisateurs et rôles
    if username == "admin" and password == "admin":
        role = "admin"
    elif username == "test" and password == "test":
        role = "user"
    else:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    # Génération du jeton avec un champ 'roles'
    access_token = create_access_token(identity=username, additional_claims={"roles": role})
    return jsonify(access_token=access_token)

# Route protégée (requiert un jeton valide)
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Récupère l'identité de l'utilisateur à partir du jeton
    return jsonify(logged_in_as=current_user), 200

# Route admin protégée (accessible uniquement si le rôle est 'admin')
@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    claims = get_jwt()  # Récupère toutes les informations du jeton JWT
    role = claims.get("roles")  # Récupère le rôle du jeton

    if role != "admin":
        return jsonify({"msg": "Accès refusé, vous n'êtes pas un administrateur"}), 403

    return jsonify({"msg": "Bienvenue sur la page admin"}), 200

if __name__ == "__main__":
    app.run(debug=True)
