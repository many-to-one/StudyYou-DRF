import datetime
from rest_framework import generics, status, views
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .serializers import EmailVerificationSerializer, RegisterSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, UserSerializer
from .models import User
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.decorators import api_view



class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        # Send data to our RegisterSerializer
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Here we get a data from RegisterSerializer
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email_verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)        


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if not token:
                return Response({'error': 'No token'}, status=status.HTTP_400_BAD_REQUEST)
            if not settings.SECRET_KEY:
                return Response({'error': 'No settings.SECRET_KEY'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            if not user:
                return Response({'error': 'No user'}, status=status.HTTP_400_BAD_REQUEST)    
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(views.APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        congregation = request.data['congregation']

        user = User.objects.filter(
            email=email,
            # congregation=congregation,
            ).first()
        user.is_active = True
        user.save()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256') 

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'id': payload['id'],
            'jwt': token,
            'email': user.email,
            'username': user.username,
            'congregation': user.congregation,
        }
        return response
       

class UserView(views.APIView):

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        payload = {'id': user.id}
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        response = Response()
        response.data = {
            'message': 'Success',
            'status': status.HTTP_200_OK,
            'data': serializer.data,
            'token': token,
        }
        return response
    
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        payload = {'id': user.id}
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        data = request.data
        for k, v in data.items():
            if k == 'admin':
                user.admin = v
                user.save()
            elif k == 'editor':
                user.editor = v
                user.save()
            elif k == 'helper':
                user.helper = v
                user.save()
            elif k == 'leader':
                user.leader = v
                user.save()
            elif k == 'ministry_event':
                user.ministry_event = v
                user.save()
            elif k == 'service':
                user.service = v
                user.save()
            elif k == 'report':
                user.report = v
                user.save()

        serializer = UserSerializer(user)
        response = Response()
        response.data = {
            'message': 'Success',
            'status': status.HTTP_200_OK,
            'data': serializer.data,
            'token': token,
        }
        return response


class AllUsers(views.APIView):

    def get(self, request, congregation):
        users = User.objects.filter(congregation=congregation)
        serializer = UserSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    

class AllUsersByService(views.APIView):

    def get(self, request, congregation):
        users = User.objects.filter(
            congregation=congregation,
            service=True,
            )
        serializer = UserSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    

class AllUsersByLeader(views.APIView):

    def get(self, request, congregation):
        users = User.objects.filter(
            congregation=congregation,
            leader=True,
            )
        serializer = UserSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
    
# Duties
class AllUsersByHelper(views.APIView):

    def get(self, request, congregation):
        users = User.objects.filter(
            congregation=congregation,
            helper=True,
            )
        serializer = UserSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    

class AllUsersByMinistry(views.APIView):

    def get(self, request, congregation):
        users = User.objects.filter(
            congregation=congregation,
            ministry_event=True,
            )
        serializer = UserSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class AllUsersByGroupe(views.APIView):

    def get(self, request, congregation, groupe):
        users = User.objects.filter(
            congregation=congregation,
            groupe=groupe,
            )
        serializer = UserSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = "http://localhost:3000" # get_current_site(request=request).domain
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                f"http://127.0.0.1:8000/users/mapp/password-reset-complete/{user.id}/" # absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response(
            {   
                'success': 'We have sent you a link to reset your password',
                'token' : token,
                'uidb64': uidb64,
                'reletive_link' : reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token}),
            }, 
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response('The token is not valid, please request a new one')

            return Response(
                {
                    'success': True,
                    'message': 'Credentials valid',
                    'uidb64': uidb64,
                    'token': token,
                },
                status=status.HTTP_200_OK,
            )
        except DjangoUnicodeDecodeError():
            if not PasswordResetTokenGenerator().check_token(user):
                return Response('The user is not valid, please request a new one')   


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer   

    def patch(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
        except Exception:
            raise('data is invalid')
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'success': True,
                'message': 'Password reseted successfully!'
            },
            status=status.HTTP_200_OK,
        )  


# class LogoutView(views.APIView):

#     def post(self, request):
#         token = request.COOKIES.get('jwt')
#         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         user = User.objects.get(id=payload['id'])
#         user.is_active = False
#         user.save()
#         try:
#             refresh_token = RefreshToken(request.data.get('jwt'))
#             refresh_token.blacklist()
#             # token.delete_cookie("JWT", path="/")
#             # return Response({'message': 'Success', 'status': status.HTTP_205_RESET_CONTENT})
#             response = Response()
#             response.delete_cookie('jwt', path='/')
#             response.data = {
#                 'message': 'Success',
#                 'status': status.HTTP_205_RESET_CONTENT
#             }
#             return response

#         except TokenError:
#             raise('Bad token')   


class LogoutView(views.APIView):

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        user.is_active = False
        user.save()
        payload = {'id': user.id}
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        try:
            blst_token = RefreshToken(request.data.get(token))
            blst_token.blacklist()
            response = Response()
            response.delete_cookie('jwt', path='/')
            response.data = {
                'message': 'Success',
                'status': status.HTTP_205_RESET_CONTENT
            }
            return response
        except TokenError:
            raise('Bad token')  
        

class SetGroupeView(views.APIView):

    def post(self, request, pk):
        data = request.data
        user = User.objects.get(id=pk)
        user.groupe = data
        user.save()
        serializer = UserSerializer(
            user, 
            many = False,
        )
        try:
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            raise e


from .forms import SetPasswordForm
from django.contrib import messages
from django.shortcuts import redirect, render

def password_change(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('http://127.0.0.1:8000/users/success/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})


def success(request):
    return render(request, 'success.html')