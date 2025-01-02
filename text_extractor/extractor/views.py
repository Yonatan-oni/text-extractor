from django.shortcuts import redirect, render
from google.cloud import vision
from django.conf import settings
from django.shortcuts import render
from .models import UploadedImage  
import os
from django.http import HttpResponse


def download_file(request, file_name):
    file_path = os.path.join("media/output/", file_name)
    if not os.path.exists(file_path):
        return redirect('upload_image')


    # Open the file and return it with the appropriate content headers
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response


def save_text_to_file(text, base_path, file_format="txt"):
    if file_format == "txt":
        file_path = f"{base_path}.txt"
        with open(os.path.join(settings.MEDIA_ROOT, file_path), "w", encoding="utf-8") as file:
            file.write(text)
        return file_path

def extract_text_from_images(request):
    if request.method == 'POST':
        if 'images' not in request.FILES:
            context = {
            "btn": "Go back",
            "message": "No image files provided." ,
            "url" : "upload_image"
            }
            return render(request, 'response.html', context=context)

        uploaded_images = request.FILES.getlist('images')
        extracted_text = ""

        try:
            client = vision.ImageAnnotatorClient()

            for uploaded_image in uploaded_images:
                image_instance = UploadedImage.objects.create(image=uploaded_image)
                image_path = image_instance.image.path

                with open(image_path, 'rb') as image_file:
                    image_content = image_file.read()

                image = vision.Image(content=image_content)

                response = client.text_detection(image=image)
                texts = response.text_annotations

                if texts:
                    extracted_text += texts[0].description + "\n\n"
    
                os.remove(image_path)

            if not extracted_text:
                extracted_text += " " + "\n\n"
                
            txt_path = save_text_to_file(extracted_text, "output/output")
            download_url = f"/media/{txt_path}"

            context = {
            "btn": "Download",
            "message": "Text extracted successfully.",
            "url" : "output.txt"
            }
            return render(request, 'response.html', context=context)

        except Exception as e:
            context = {
            "btn": "Go back",
            "message": f"An error occurred: {str(e)}" ,
            "url" : "upload_image"
            }
            return render(request, 'response.html', context=context)
          
    
    return render(request, "response.html", context)
    

def upload_image(request):
    if request.method == "POST":
        uploaded_images = request.FILES.getlist("images")
        if not uploaded_images:
              context = {
                "btn": "Go back",
                "message": "",
                "url" : "upload_image"
                }
              return render(request, 'response.html', context=context)
        
        try:
            client = vision.ImageAnnotatorClient()
            extracted_text = ""
            for image_file in uploaded_images:
                image_instance = UploadedImage.objects.create(image=image_file)
                image_path = image_instance.image.path

                with open(image_path, 'rb') as image_file:
                    image_content = image_file.read()

                image = vision.Image(content=image_content)
                response = client.text_detection(image=image)
                texts = response.text_annotations

                os.remove(image_path)

                if not texts:
                    extracted_text += " " + "\n\n"

                if texts:
                    extracted_text += texts[0].description + "\n\n"

            txt_path = save_text_to_file(extracted_text, "output/output")
            download_url = f"/media/{txt_path}"

        except Exception as e:
            error = "Error: ", str(status=500)
            context = {
                "btn": "Go back",
                "message": error,
                "url" : "upload_image"
            }
            return render(request, 'response.html', context=context)

        context = {
            "btn": "Download",
            "message": "Text extracted successfully.",
            "url" : "output.txt"
        }
        return render(request, 'response.html', context=context)

    return render(request, 'upload.html')
