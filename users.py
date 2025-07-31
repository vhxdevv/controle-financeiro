from models import User

def verificador_user(email):
    usuario = User.query.filter_by(email=email).first()
    return usuario is not None