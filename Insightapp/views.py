from django.shortcuts import render
from .forms import Searchform
from .models import SearchHistory
from django.views import View

import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64
import os
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.environ.get('API_KEY'))
class SearchView(View):
    def get(self,request,*args,**kwargs):
        form = Searchform()
        context = {
            'searchform':form
        }
        return render(request,'Search.html',context)
    def post(self, request, *args, **kwargs):
        form = Searchform(request.POST)
        context = {}
        if form.is_valid():
            searched = form.cleaned_data['search_text']
            form.save()
            # Use the Gemini model
            model = genai.GenerativeModel(model_name="gemini-2.0-flash-preview-image-generation")

            try:
                response = model.generate_content(
                    contents=[searched],
                    generation_config={
                        "response_mime_type": "text/plain",
                        "response_modalities": ["TEXT", "IMAGE"]
                        })

                text_result = ""
                image_base64 = None

                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'text') and part.text:
                        text_result += part.text
                    elif hasattr(part, 'inline_data') and part.inline_data:
                        image_data = part.inline_data.data
                        image = Image.open(BytesIO(image_data))

                        # Convert to base64
                        buffered = BytesIO()
                        image.save(buffered, format="PNG")
                        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

                # Add results to context
                context['text'] = searched
                context['result_text'] = text_result
                context['image_base64'] = image_base64

            except Exception as e:
                context['error'] = f"Error: {str(e)}"

        return render(request, 'result.html', context)

class HistoryView(View):
    def get(self,request,*args,**kwargs):
        history = SearchHistory.objects.all()
        context = {
            'history':history
        }
        return render(request,'history.html',context)
