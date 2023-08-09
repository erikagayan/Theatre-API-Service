from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from theatre.models import Play
from theatre.serializers import PlaySerializer


@api_view(['GET', 'POST'])
def play_list(request):
    if request.method == 'GET':
        plays = Play.objects.all()
        serializer = PlaySerializer(plays, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PlaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def play_detail(request, pk):
    play = get_object_or_404(Play, pk=pk)

    if request.method == 'GET':
        serializer = PlaySerializer(play)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PlaySerializer(play, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        play.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
