from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import ProjectSerializer
from projects.models import project


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET','/api/projects'},
        {'GET','/api/projects/id'},
        {'POST','/api/projects/id/vote'},

        {'POST','/api/users/token'},
        {'POST','/api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
def getprojects(request):
    projects = project.objects.all()
    serializer = ProjectSerializer(projects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getprojec(request,pk):
    projec = project.objects.get(Id=pk)
    serializer = ProjectSerializer(projec,many=False)
    return Response(serializer.data)
