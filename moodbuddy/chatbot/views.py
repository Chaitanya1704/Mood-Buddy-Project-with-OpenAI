# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatEntry
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
client = OpenAI(api_key="*****") 

def build_prompt(user_input, persona_type):
    personas = {
        "Gentle Friend": "You are MoodBuddy, a warm, caring friend who listens deeply, never judges, and always encourages gently.",
        "Calm Therapist": "You are MoodBuddy, a calm, grounded therapist who helps people reflect with compassion and self-kindness.",
        "Uplifting Coach": "You are MoodBuddy, an optimistic, positive coach who helps people find strength and resilience."
    }
    system_prompt = personas.get(persona_type, personas["Gentle Friend"])
    user_prompt = f"""
    User Message: "{user_input}"
    Your job:
    1. Identify the emotional tone of the message
    2. Acknowledge the feeling with empathy
    3. Offer gentle encouragement
    4. End with a soft question or positive thought
    """
    return {"system": system_prompt, "user": user_prompt}

def index(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
def chat(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        persona = request.POST.get("persona")
        prompt = build_prompt(user_message, persona)
        try:
            # Send to OpenAI's chat API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"reply": "Sorry, something went wrong processing your message."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)