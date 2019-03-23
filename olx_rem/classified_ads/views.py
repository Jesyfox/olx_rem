from django.conf import settings
from django.contrib.auth import authenticate
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Category, Item
from .serializers import LoginSerializer


def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)

    try:
        instance = Category.objects.get(parent=parent, slug=category_slug[-1])
    except Exception as e:
        print('Exception!: ', e)
        instance = get_object_or_404(Item, slug=category_slug[-1])
        return render(request, "index.html", {'instance': instance})
    else:
        return render(request, 'categories.html', {'instance': instance})

@csrf_exempt
@api_view(["GET"])
def index(request):
    context = {}
    instance = Category.objects.all()
    items = Item.objects.all()
    serializer = LoginSerializer

    context.update(instance=instance, items=items, serializer=serializer)
    return render(request, 'index.html', context=context, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
