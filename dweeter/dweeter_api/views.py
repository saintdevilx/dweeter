from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import JsonResponse
from .serializers import *
from django.db.models import Q
def home(request):
    return render(request,'home.html')


@api_view(["GET","POST"])
def login(request):    
    if request.method=='POST':
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        auth_login(request,user)
        if not user:
            return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    else:
        return redirect('/',request)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def dweet_list(request, dweet_id=None):
    from managers import TimelineManager
    manager = TimelineManager()
    # Dweet and reply dweet 
    dweets = manager.get_timeline_dweet(request.user, dweet_id=dweet_id)
    serializer = TimelineDweetSerializer(dweets, many=True)
    return JsonResponse(serializer.data, safe=False)



def logout(request):    
    if request.user.id:
        #request.user.auth_token.delete()
        auth_logout(request)
    if request.is_ajax():
        return Response(status=status.HTTP_200_OK)
    else:
        return redirect('/')

@api_view(['GET',"POST"])
def register(request):
    if request.method=="POST":
        data_serializer= UserSerializer(data=request.data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response({'success':True,'message':'Registered successfully !'}, status=status.HTTP_200_OK)
        else:
            return Response(data_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    else:    
        return render( request, 'register.html')    



def home(request):
    return render(request,'home.html')


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def add_new_dweet(request):
    data_serializer = DweetSerializer(data=request.data)  
    if data_serializer.is_valid():
        data_serializer.save(user=request.user)
        return Response({"dweet_text":request.data.get('dweet_text')}, status = status.HTTP_200_OK)
    else:        
        return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def people_list(request):
    users_list = User.objects.all()
    data_serializer = UserSerializer(users_list,many=True, fields=['id','first_name','last_name','username'])
    return JsonResponse(data_serializer.data, safe=False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request):
    data_serializer = FollowerSerializer(data=request.data)
    
    if data_serializer.is_valid():
        data_serializer.save(follower = request.user )
        return Response({'success':True}, status=status.HTTP_200_OK)
    else:
        return Response(data_serializer.errors , status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_like(request):
    data_serializer = LikeSerializer(data=request.data)
    if data_serializer.is_valid():
        data_serializer.save(user= request.user)
        return Response(data_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response( data_serializer.errors, status = status.HTTP_400_BAD_REQUEST )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_reply(request):
    data_serializer  =  DweetSerializer(data=request.data)
    if data_serializer.is_valid():
        data_serializer.save(user= request.user)
        return Response( data_serializer.data, status=status.HTTP_200_OK )
    else:
        return Response(  data_serializer.errors , status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])        
@permission_classes([IsAuthenticated])
def search(request,category='user'):
    q = request.GET.get('q','').lower()
    if category == 'people':
        result_list= User.objects.filter( Q(username=q) | Q(first_name__istartswith=q ) | Q(email=q)  )[:10]
        results = UserSerializer( result_list ,many=True, fields=['first_name','last_name','username'])
    elif category == 'dweet':
        result_list = Dweet.objects.filter( dweet_text__icontains = q ) 
        results = DweetSerializer( result_list ,many=True)    
    return Response( results.data , status = status.HTTP_200_OK )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile(request,username):
    profile = UserProfile.objects.prefetch_related('user').get( user__username = username )
    if request.is_ajax():
        response = UserProfileSerializer(profile)
        return Response(response.data, status = status.HTTP_200_OK)
    else:
        return render(request, 'view_profile.html', locals())


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dweet(request,username):
    dweet_list = Dweet.objects.filter( user__username = username )
    data_serializer = DweetSerializer( dweet_list , many=True)
    return Response( data_serializer.data )
