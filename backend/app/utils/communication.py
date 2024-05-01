from app.models import User

def get_user_phone_number(user_id):
    user = User.query.get(user_id)
    if user:
        return user.phone
    return None