



import datetime

import jwt
from users.models import User
from rest_framework.exceptions import AuthenticationFailed




def generate_payload(request):
    username = request.data['username']
    password = request.data['password']
    
    user = User.objects.filter(username=username).first()
    print(user)
    if user is None:
        raise AuthenticationFailed('User not found')
    
    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect Password')
    
    payload = {
        'id':user.id,
        'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat':datetime.datetime.utcnow()
    }
    return payload
    


def get_token(request):
    token = request.COOKIES.get('access_token')
        
    if not token:
        raise AuthenticationFailed('Unauthenticated')

    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    
    return payload