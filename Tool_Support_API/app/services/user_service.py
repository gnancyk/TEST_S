from ..models import db, User

def get_all_users():
    users = User.query.all()
    return [user.to_dict() for user in users]

def create_user(data):
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict()
