from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime

class UserRegisterView(APIView):
  def post(self, req):
    serializer = UserSerializer(data=req.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  
class UserLoginView(APIView):
  def post(self,req):
    id = req.data['id']
    password = req.data['password']

    user = User.objects.filter(id=id).first()
    serialize_user = UserSerializer(user)
    json_user = JSONRenderer().render(serialize_user.data)

    if user is None :
      raise AuthenticationFailed('User does not found!')
    
    if not user.check_password(password) :
      raise AuthenticationFailed("Incorrect password!")

    payload = {
      'id' : user.id,
      'exp' : datetime.datetime.now() + datetime.timedelta(minutes=60),
      'iat' : datetime.datetime.now()
      }

    token = jwt.encode(payload,"secretJWTkey",algorithm="HS256")

    res = Response()
    res.set_cookie(key='jwt', value=token, httponly=True)
    res.data = {
        'jwt' : token
      }


    return res
  
class UserView(APIView) :
  def get(self,req):
    token = req.COOKIES.get('jwt')

    if not token :
      raise AuthenticationFailed('UnAuthenticated!')

    try :
      payload = jwt.decode(token,'secretJWTkey',algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('UnAuthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)

    return Response(serializer.data)
  
class LogoutView(APIView) :
  def post(self,req):
    res = Response()
    res.delete_cookie('jwt')
    res.data = {
        "message" : 'success'
      }

    return res