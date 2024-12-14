import os
import subprocess

from django.http import JsonResponse
from django.shortcuts import render
from WebApplication.models import Data

# Create your views here.


# Calling the Web Application
def home(request):
    return render(request, "index.html")


def dataset(request):
    data = list(Data.objects.values())
    return JsonResponse(data, safe=False)


# Calling the Machine Learning Script
def runMLScript(request):
    script_path = os.path.join('WebApplication', 'Text_Preprocessing', 'import_csv.py')

    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        output = result.stdout
        error = result.stderr
    except Exception as e:
        output = f"Error occurred: {str(e)}"
        error = None

    context = {
        'output': output,
        'error': error
    }
    return render(request, "index.html", context)


def regex(request):
    script_path = os.path.join('Backend_ML', 'Text_Preprocessing', 'filter_regex.py')

    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        output = result.stdout
        error = result.stderr
    except Exception as e:
        output = f"Error occurred: {str(e)}"
        error = None

    context = {
        'output': output,
        'error': error
    }
    return render(request, "index.html", context)
