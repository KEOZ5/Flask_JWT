from flask import Flask, jsonify, request, make_response, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Configuration de JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # C'est une clé secrète pour signer les JWT
jwt = JWTManager(app)

# Route publique d'accueil (affiche le formulaire HTML)
@app.route('/')
def home():
    return render_template('formulaire.html')

# Route de login pour obtenir un jeton JWT et le stocker dans un cookie
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)

    # Vérification des utilisateurs et de leurs rôles
    if username == "admin" and password == "admin":
        role = "admin"
    elif username == "test" and password == "test":
        role = "user"
    else:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    # Création du jeton JWT avec le rôle
    access_token = create_access_token(identity=username, additional_claims={"roles": role})

    # Création de la réponse et stockage du jeton dans un cookie
    response = make_response(jsonify({"msg": "Login réussi, jeton stocké dans un cookie"}))
    response.set_cookie("access_token", access_token, httponly=True)  # Cookie sécurisé et HTTPOnly
    return response

# Route protégée (requiert un jeton valide dans un cookie)
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
