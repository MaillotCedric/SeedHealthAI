from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView

from dotenv import load_dotenv
from project.settings import MEDIA_ROOT
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import os
import ssl
import json
import urllib.request

@login_required(login_url="login")
def home(request):
    return render(request, "home.html", {})

def login_(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect("home")
        else:
            messages.warning(request, "Username and/or password not valid")

            return redirect("login")
    else:
        return render(request, "login.html", {})

def logout_(request):
    logout(request)
    messages.success(request, "Logged out")

    return redirect("login")

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

class PredictAPIView(APIView):
    def post(self, *args, **kwargs):
        allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
        load_dotenv()

        PREDICT_ENDPOINT_URL = str(os.getenv("PREDICT_ENDPOINT_URL"))
        print(PREDICT_ENDPOINT_URL)
        PREDICT_API_KEY = str(os.getenv("PREDICT_API_KEY"))
        print(PREDICT_API_KEY)

        data = self.request.data
        body = str.encode(json.dumps(data))
        url = PREDICT_ENDPOINT_URL
        api_key = PREDICT_API_KEY

        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': ('Bearer ' + api_key)
        }

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read()

            return Response(json.loads(result))
        except urllib.error.HTTPError as error:
            code_error = str(error.code)
            reason_error = error.reason

            return Response(
                "The request failed with status code: " + code_error + " (" + reason_error + ")"
            )

class ClassifyAPIView(APIView):
    def get(self, *args, **kwargs):
        IMAGES_PATH = MEDIA_ROOT / "images"
        nb_images = len(os.listdir(IMAGES_PATH))
        nb_classes = {
            "normal": 0,
            "pyriform": 0,
            "amorphous": 0,
            "tapered": 0
        }
        repartition_classes = {
            "normal": "0%",
            "pyriform": "0%",
            "amorphous": "0%",
            "tapered": "0%"
        }
        predictions = {}

        load_dotenv()

        try:
            # Get Configuration Settings
            CLASSIFY_PREDICTION_KEY = str(os.getenv("CLASSIFY_PREDICTION_KEY"))
            CLASSIFY_PREDICTION_ENDPOINT = str(os.getenv("CLASSIFY_PREDICTION_ENDPOINT"))
            CLASSIFY_PROJECT_ID = str(os.getenv("CLASSIFY_PROJECT_ID"))
            CLASSIFY_MODEL_NAME = str(os.getenv("CLASSIFY_MODEL_NAME"))

            # Authenticate a client for the training API
            credentials = ApiKeyCredentials(in_headers={"Prediction-key": CLASSIFY_PREDICTION_KEY})
            prediction_client = CustomVisionPredictionClient(endpoint=CLASSIFY_PREDICTION_ENDPOINT, credentials=credentials)

            # Classify test images
            for index, image in enumerate(os.listdir(IMAGES_PATH)):
                image_data = open(os.path.join(IMAGES_PATH, image), "rb").read()
                results = prediction_client.classify_image(CLASSIFY_PROJECT_ID, CLASSIFY_MODEL_NAME, image_data)
                predictions[f"prediction {index}"] = {}

                # Loop over each label prediction and print any with probability > 50%
                for prediction in results.predictions:
                    if prediction.probability > 0.5:
                        predictions[f"prediction {index}"]["image"] = image
                        predictions[f"prediction {index}"]["predict label"] = prediction.tag_name
                        predictions[f"prediction {index}"]["probability"] = f"{prediction.probability:.0%}"

                        nb_classes[prediction.tag_name] += 1

            for classe in nb_classes:
                pourcentage = (100 * int(nb_classes[classe])) / nb_images
                repartition_classes[classe] = f"{round(pourcentage)}"

            # return Response(nb_classes)
            return Response(repartition_classes)
            # return Response(predictions)
        except Exception as ex:
            return Response({
                "exeption": str(ex)
            })
