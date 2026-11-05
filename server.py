import asyncio
import websockets
import google.generativeai as genai
from gtts import gTTS
import os

# আপনার Google AI Studio থেকে নেওয়া Gemini API Key এখানে বসান
genai.configure(api_key="AQ.Ab8RN6Lu-_57uOsUMs1BFKbG7YZ3yX9MqESqy162EC0TnE_rjA")
model = genai.GenerativeModel('gemini-1.5-flash')

async def jarvis_ai_handler(websocket):
    print("Jarvis connected to Gemini Backend!")
    try:
        async for message in websocket:
            if isinstance(message, bytes):
                print(f"Received audio chunk from Jarvis: {len(message)} bytes")
                
                # জেমিনির জন্য প্রম্পট বা কমান্ড
                prompt = "Hello Jarvis, I am ready."
                
                # Gemini API থেকে রেসপন্স নেওয়া
                response = model.generate_content(prompt)
                ai_reply = response.text
                print(f"Gemini Reply: {ai_reply}")

                # জেমিনির উত্তরকে অডিওতে রূপান্তর (TTS)
                tts = gTTS(text=ai_reply, lang='en', slow=False)
                audio_path = "response.mp3"
                tts.save(audio_path)

                # অডিও ফাইলটি বাইনারি আকারে Jarvis-এর কাছে পাঠানো
                with open(audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    await websocket.send(audio_bytes)
                    print("Audio response sent back to Jarvis!")

        except websockets.exceptions.ConnectionClosed:
            print("Jarvis disconnected!")

async def main():
    # Render-এর ডাইনামিক পোর্ট সেটআপ
    port = int(os.environ.get("PORT", 8080))
    async with websockets.serve(jarvis_ai_handler, "0.0.0.0", port):
        print(f"WebSocket Server started on port {port}...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
