from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, db  # "your_models_file" yerine models.py dosyanızın adını kullanın
from app.forms import RegistrationForm, LoginForm, ProfileForm  # Form dosyalarınızı içe aktarın
from sqlalchemy import text
import json  # JSON modülünü içe aktarma

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    form = RegistrationForm(data=data)
    if form.validate():
        new_user = User(email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered"}), 201
    return jsonify({"errors": form.errors}), 400

@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        # Profil sayfasına yönlendirme bilgisi içeren yanıt
        return jsonify({"message": "User logged in", "redirect": "/profile"}), 200

    return jsonify({"message": "Invalid credentials"}), 401

@api_blueprint.route('/profile', methods=['POST'])
def update_profile():
    if not current_user.is_authenticated:
        return jsonify({"message": "Unauthorized"}), 401
    data = request.get_json()
    form = ProfileForm(data=data, obj=current_user)
    if form.validate():
        form.populate_obj(current_user)
        db.session.commit()
        return jsonify({"message": "Profile updated"}), 200
    return jsonify({"errors": form.errors}), 400

@api_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "User logged out"}), 200


@api_blueprint.route('/mapdata', methods=['GET'])
def map_data():
    sql = text("""
    SELECT id AS feature_id, ST_AsGeoJSON(geom)::jsonb As geometry, oda_id, geom_type, 
           line_thickness, line_type, color_code, thickness, factor, 
           text_data, object_properties, point_height, length
    FROM harita
    """)

    results = db.session.execute(sql).fetchall()


    features = []
    for row in results:
        feature = {
            "type": "Feature",
            "properties": {
                "id": row['feature_id'],
                "oda_id": row['oda_id'],
                "geom_type": row['geom_type'],
                "line_thickness": row['line_thickness'],
                "line_type": row['line_type'],
                "color_code": row['color_code'],
                "thickness": row['thickness'],
                "factor": row['factor'],
                "text_data": row['text_data'],
                "object_properties": row['object_properties'],
                "point_height": row['point_height'],
                "length": row['length']
                # Diğer sütunlar burada eklenebilir
            },
            "geometry": row['geometry']
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return jsonify(geojson)
