from pickle import TRUE
import re
from django.http import JsonResponse, HttpResponse, Http404

# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, parsers, status, pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import HospitalSerializer
from .models import Hospital


@api_view(["GET", "POST"])
def hospital_list(request, format=None):
    if request.method == "GET":
        paginator = pagination.PageNumberPagination()
        paginator.page_size = 3
        paginator.page_query_param = "page"
        qry_set = Hospital.objects.filter(is_deleted=False)
        order = request.query_params.get("order")
        if order is not None:
            qry_set = Hospital.objects.filter(is_deleted=False).order_by(order)
        hospitals = paginator.paginate_queryset(queryset=qry_set, request=request)
        serializer = HospitalSerializer(hospitals, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
def hospital_details(request, id, format=None):
    try:
        hospital = Hospital.objects.get(id=id)
    except Hospital.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        # return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = HospitalSerializer(hospital)
        # return JsonResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = parsers.JSONParser().parse(request)
        serializer = HospitalSerializer(hospital, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
            # return Response(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def hospital_remove(request, id, format=None):
    try:
        hospital = Hospital.objects.get(id=id)
    except Hospital.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = parsers.JSONParser().parse(request)
        data["is_deleted"] = 1
        serializer = HospitalSerializer(hospital, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class HospitalViewSet(viewsets.ModelViewSet):
#     queryset = Hospital.objects.all()
#     serializer_class = HospitalSerializer


# class HospitalList(APIView):
#     def get(self, request, format=None):
#         hospitals = Hospital.objects.all()
#         serializer = HospitalSerializer(hospitals, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = HospitalSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class HospitalDetail(APIView):
#     def get_object(self, id):
#         try:
#             return Hospital.objects.get(id=id)
#         except Hospital.DoesNotExist:
#             raise Http404

#     def get(self, request, id, format=None):
#         hospitals = self.get_object(id)
#         serializer = HospitalSerializer(hospitals)
#         return Response(serializer.data)

#     def put(self, request, id, format=None):
#         hospitals = self.get_object(id)
#         serializer = HospitalSerializer(hospitals, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id, format=None):
#         hospital = self.get_object(id)
#         hospital.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
