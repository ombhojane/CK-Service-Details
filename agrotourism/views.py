from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

# Configure your API key here
API_KEY = "AIzaSyBfX_I3gMUg-B78RlHRWfPWL8DgFEpUJ3o"

def generate_content_with_genai(service_name):
    # Configure the Generative AI API
    genai.configure(api_key=API_KEY)
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    prompt_template = f"Please provide the following key details to overview the {service_name} agrotourism service:\n"\
                      "Official Name:\n"\
                      "One Line Description:\n"\
                      "Target Audience:\n"\
                      "Who is the target audience?\n"\
                      "What needs or problems do they have that the service addresses?\n"\
                      "Primary Goal:\n"\
                      "What is the primary goal or purpose of the {service_name} agrotourism service?\n"\
                      "Objectives:\n"\
                      "What are the key objectives or intended outcomes of providing the {service_name} agrotourism service? Please list 2-3 top objectives.\n"

    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    response = model.generate_content([prompt_template])
    return response.text

from django.http import JsonResponse

@csrf_exempt
def generate_agrotourism_content(request):
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        generated_text = generate_content_with_genai(service_name)
        # Return a JsonResponse instead of HttpResponse
        return JsonResponse({'text': generated_text})
    else:
        return render(request, "agrotourism/agrotourism_form.html")

