from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import *
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import authentication,permissions
from work.models import *
from api.permissions import OwnerOnly


class Userregister(APIView):

    def post(self,request,*args,**kwargs):

        serializer = Registration(data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    
    
class TodoViewset(ViewSet):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [OwnerOnly]

    def list(self,request,*args,**kwargs):

        qs = taskmodel.objects.all()
        serializer = TodoSerializer(qs,many=True)

        return Response(serializer.data)
    

    def create(self,request,*args,**kwargs):

        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

        return Response(serializer.data)
    

    def destroy(self,request,*args,**kwargs):

        id = kwargs.get('pk')
        qs = taskmodel.objects.get(id=id)

        if qs.user == request.user:
            qs.delete()
            return Response({'message':'task deleted'})
        
        else:
            raise serializers.ValidationError("not allowed")
        

    def update(self,request,*args,**kwargs):

        id = kwargs.get('pk')
        qs = taskmodel.objects.get(id=id)
        serializer = TodoSerializer(data=request.data,instance=qs)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    

    def retrieve(self,request,*args,**kwargs):

        id = kwargs.get('pk')
        qs = taskmodel.objects.get(id=id)
        serializer = TodoSerializer(qs)
        
        if qs.user == request.user:
            return Response(serializer.data)
        
        else:
            raise serializers.ValidationError('not allowed')
        

class TodoModelviewset(ModelViewSet):

    queryset = taskmodel.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [OwnerOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    
    # def perform_destroy(self, instance):
    #     instance = taskmodel.objects.get(id=id)
    #     if instance.user == self.request.user:
    #         return instance.delete()
        
    #     else:
    #         print("not allowed")