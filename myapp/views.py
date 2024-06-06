from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chat_view(request):
    # Your logic for handling chat interactions
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            # Process the message (e.g., pass it to your LLM chatbot)
            response = {'message': message}
            return JsonResponse(response)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        # If it's not a POST request, return some initial data (if needed)
        return render(request, 'index.html')

