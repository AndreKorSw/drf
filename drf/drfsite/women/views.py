import json

from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .models import *
from rest_framework import generics, viewsets
from . serializers import *
from rest_framework.renderers import TemplateHTMLRenderer
# Create your views here.

class WomenAPIView(APIView):
    # generics.ListAPIView
    # queryset = Women.objects.all()
    # serializer_class = WomenSerializer
    def get(self, request):
        w = Women.objects.all()
        return Response({'posts': WomenSerializer(w, many=True).data})

    def post(self, request):
        serializer=WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        post_data={'post': serializer.data}
        print(post_data['post'])
        with open("company_data.txt", "a", encoding="utf-8") as file:
            file.write(post_data['post'])
        return Response({'post': serializer.data})






    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error":"No such object"})
        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "No such object"})

        serializer= WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post":serializer.data})



    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if not pk:
            return Response({"error": "No such object"})
        try:
            instance = Women.objects.get(pk=pk).delete()
        except:
            return Response({"error": "No such object"})

        return Response({"post":"delete post" + str(pk)})

# class WomenAPIUpdate(UpdateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
# class WomenAPIList(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#
#
# class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

# class WomenViewSet(viewsets.ModelViewSet):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         if not pk:
#             return Women.objects.all()[:3]
#         return Women.objects.filter(pk=pk)
#
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=None):
#         cats=Category.objects.get(pk=pk)
#         return Response({'cats':cats.name})
class WomenAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5
class WomenAPIList(generics.ListCreateAPIView):
    serializer_class = WomenSerializer
    queryset = Women.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = [TemplateHTMLRenderer,]
    template_name="women/index.html"
    def get(self, request):
        queryset = Women.objects.all()
        return Response({'posts':queryset})




class WomenAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WomenSerializer
    queryset = Women.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    #authentication_classes = (TokenAuthentication,) аутентификация только по токенам



class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = WomenSerializer
    queryset = Women.objects.all()
    permission_classes = (IsAdminOrReadOnly,)




