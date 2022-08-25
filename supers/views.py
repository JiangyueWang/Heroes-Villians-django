from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from supers.models import Super
from supers.serializer import SuperSerializer
# Create your views here.


@api_view(['POST'])
def supers_list(request):
    if request.method == 'POST':
        serializer_super = SuperSerializer(data=request.data)
        serializer_super.is_valid(raise_exception=True)
        serializer_super.save()

    return Response(serializer_super.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def super_details(requst, pk):
    requested_super = Super.objects.get(pk=pk)
    if requst.method == 'GET':
        serializer_super = SuperSerializer(requested_super)
        return Response(serializer_super.data, status=status.HTTP_200_OK)
