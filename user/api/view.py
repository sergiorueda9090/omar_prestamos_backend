from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from user.models import User
from .serializers import UserRegisterSerializer
from django.db.models import Q
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    if request.method == "POST":
        print(request.data)
        if not request.data:
            return Response({'status':'Error faltan los campos username y password'}, status=status.HTTP_200_OK)
    
        fields = ['username', 'password']

        for field in fields:
            if not request.data.get(field):
                return Response({'status':'falta el campo {}'.format(field)})

        # Convertir '1' / '0' a booleano para is_superuser
        data = request.data.copy()
        is_super = data.get('is_superuser')

        # 🔍 asegúrate que sea string antes de comparar
        print("Valor recibido is_superuser:", is_super)

        data['is_superuser'] = str(is_super) == '1'
        
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'status': 'Error: User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegisterSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'User updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status': 'Error: Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id = None):
    if request.method == 'GET':
        try:
            user       = User.objects.get(pk=user_id)  # Retrieve user by ID
            serializer = UserRegisterSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status': 'Error: User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status': 'Error: Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    if request.method == 'GET':
        try:
            users = User.objects.all().order_by('id')  # Puedes ordenar si quieres

            # Paginador
            paginator = PageNumberPagination()
            paginator.page_size = 20  # Cambia este valor si quieres más o menos usuarios por página

            result_page = paginator.paginate_queryset(users, request)
            serializer  = UserRegisterSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({'status': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'Error: Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_filter(request):
    """
    Lista paginada de usuarios, con filtros por búsqueda y fechas.
    """
    search      = request.GET.get('search', '')
    start_date  = request.GET.get('startDate')
    end_date    = request.GET.get('endDate')

    users = User.objects.all().order_by('id')

    # Filtro de búsqueda
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    # Filtro por fecha de creación
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            users = users.filter(created_at__date__gte=start)
        except ValueError:
            return Response({'error': 'Fecha inválida en startDate. Usa formato YYYY-MM-DD.'}, status=400)

    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            users = users.filter(created_at__date__lte=end)
        except ValueError:
            return Response({'error': 'Fecha inválida en endDate. Usa formato YYYY-MM-DD.'}, status=400)

    # Paginación
    paginator = PageNumberPagination()
    paginator.page_size = 20  # puedes hacerlo dinámico con request.GET.get('page_size')
    result_page = paginator.paginate_queryset(users, request)

    serializer = UserRegisterSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id = None):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return Response({'status': 'User delete successfull'},status=status.HTTP_204_NO_CONTENT)  # 204 No Content for successful deletion
        except User.DoesNotExist:
            return Response({'status': 'Error: User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status': 'Error: Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_user_info(request):
    user        = request.user
    serializer  = UserRegisterSerializer(user)
    return Response(serializer.data)