from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
import io
from rest_framework.parsers import JSONParser
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def list(request):
    if request.method =="GET":
        user = Student.objects.all()
        serializer_data = StudentSerializer(user,many=True)
        # print(serializer_data.data)
        json_data = JSONRenderer().render(serializer_data.data)
        return HttpResponse(json_data,content_type = 'application/json')
    
    elif request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data) 
        python_data = JSONParser().parse(stream)
        serializer = StudentSerializer(data = python_data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    elif request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        stu = Student.objects.get(id=id)
        serializer = StudentSerializer(stu, data=python_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Data Updated !!'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json') 
    
    elif request.method == 'PATCH':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        stu = Student.objects.get(id=id)
        serializer = StudentSerializer(stu, data=python_data, partial = True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Data partially Updated !!'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json') 

    elif request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        if id:
            stu = Student.objects.get(id=id)
            stu.delete()
            res = {'msg': 'Data Deleted!!'}
            return JsonResponse(res, safe=False)
        else:
            res = {'msg': 'id not present in Database'}
            return JsonResponse(res)
    