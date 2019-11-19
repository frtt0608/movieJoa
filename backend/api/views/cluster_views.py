from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Cluster
from rest_framework.response import Response

# 영화 수정 movie_udpate
@api_view(['GET', 'POST', 'PUT'])
def cluster(request):
    if request.method == 'GET':
        cluster = Cluster.objects.get(pk=1)
        data = {'n_component' : cluster.n_component, 'way':cluster.way}
        return Response(data=data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        n_component = request.data.get('n_component', None)
        way = request.data.get('way', None)
        cluster = Cluster.objects.get(pk=1)
        cluster.n_component = n_component
        cluster.way = way
        cluster.save()
        return Response(status=status.HTTP_200_OK)