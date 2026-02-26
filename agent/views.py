# import json
# import uuid
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils import timezone
# from .models import Conversation, Message
# from .nlp_utils import get_answer, detect_language

# def chat_page(request):
#     """Render the chat interface."""
#     # Generate a session ID if not present
#     if 'session_id' not in request.session:
#         request.session['session_id'] = str(uuid.uuid4())
#     return render(request, 'agent/chat.html')

# @csrf_exempt  # for simplicity; use proper CSRF in production
# def chat_api(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_message = data.get('message', '')
#         session_id = request.session.get('session_id', str(uuid.uuid4()))
#         request.session['session_id'] = session_id

#         # Detect language
#         lang = detect_language(user_message)

#         # Get or create conversation
#         conversation, created = Conversation.objects.get_or_create(
#             session_id=session_id,
#             defaults={'started_at': timezone.now()}
#         )

#         # Save user message
#         user_msg = Message.objects.create(
#             conversation=conversation,
#             is_user=True,
#             text=user_message,
#             language_detected=lang
#         )

#         # Get bot answer
#         answer, confidence = get_answer(user_message)

#         # Save bot message
#         bot_msg = Message.objects.create(
#             conversation=conversation,
#             is_user=False,
#             text=answer,
#             confidence=confidence
#         )

#         return JsonResponse({
#             'response': answer,
#             'confidence': confidence,
#             'language': lang,
#         })
#     return JsonResponse({'error': 'Invalid request'}, status=400)


# agent/views.py
import json
import traceback
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .rag_engine import get_rag_engine

def chat_page(request):
    return render(request, 'agent/chat.html')

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            print(f"📝 User asked: {user_message}")  # ডিবাগ লাইন
            
            rag = get_rag_engine()
            result = rag.query(user_message)
            print(f"✅ Response: {result['answer'][:100]}...")  # ডিবাগ লাইন
            
            return JsonResponse({'response': result['answer']})
            
        except json.JSONDecodeError:
            print("❌ JSON decode error")
            return JsonResponse({'response': 'Invalid request format'}, status=400)
            
        except Exception as e:
            # পুরো error traceback প্রিন্ট করুন
            print("❌ Error details:")
            traceback.print_exc()
            return JsonResponse({'response': f"Error: {str(e)}"})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)