from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView

from mainapp.models import Client, CSVFile
from mainapp.serializers import ClientSerializer, CSVSerializer, ClientCSVDataSerializer
from rest_framework import parsers, renderers


class CSVUploadView(CreateAPIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    queryset = CSVFile.objects.all()
    serializer_class = CSVSerializer


class ClientCreateView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientCSVDataView(APIView):
    serializer_class = ClientCSVDataSerializer
    
    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        top_customers_data = serializer.get_top_customers(request.data)
        return Response(top_customers_data)
