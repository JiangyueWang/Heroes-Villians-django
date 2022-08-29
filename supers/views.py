from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from supers.models import Super
from super_types.models import SuperType
from supers.serializer import SuperSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def supers_list(request):
    if request.method == 'GET':
        queryset = Super.objects.all()
        super_types = SuperType.objects.all()
        custom_response_dict = {}

        super_type_param = request.query_params.get('type')

        if super_type_param:
            super_type_param = super_type_param.capitalize()
            queryset = queryset.filter(super_type__type=super_type_param)
            serializer_queryset = SuperSerializer(
                queryset, many=True)
            return Response(serializer_queryset.data, status=status.HTTP_200_OK)

        else:
            for super_type in super_types:
                all_supers = Super.objects.filter(super_type=super_type)
                serializer_supers = SuperSerializer(all_supers, many=True)
                custom_response_dict[super_type.type] = serializer_supers.data

            return Response(custom_response_dict, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer_super = SuperSerializer(data=request.data)
        serializer_super.is_valid(raise_exception=True)
        serializer_super.save()
        return Response(serializer_super.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def super_details(request, pk):

    requested_super = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer_super = SuperSerializer(requested_super)
        return Response(serializer_super.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer_super = SuperSerializer(requested_super, data=request.data)
        serializer_super.is_valid(raise_exception=True)
        serializer_super.save()
        return Response(serializer_super.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        requested_super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
