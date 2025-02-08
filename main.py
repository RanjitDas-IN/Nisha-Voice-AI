import requests
from requests import Response
import json
import os
import time
import asyncio
from config import settings

url = "https://typecast.ai/api/speak"

inputText = input("Enter a text to regerate AI Voice: ")
generated_speech_name = "ai-voice.mp3"

payload = json.dumps({
  "actor_id": "627ae5cd14dc32608fdaffa8",
  "text": inputText,
  "lang": "auto",
  "tempo": 1,
  "volume": 100,
  "pitch": 0,
  "xapi_hd": True,
  "max_seconds": 60,
  "model_version": "latest",
  "xapi_audio_format": "mp3"
})

headers = {
  'Authorization': 'Bearer ' + settings.TYPECAST_API_KEY,
  'Content-Type': 'application/json'
}

async def send_text() -> Response:
    print("Sending Audio to cloud.....")
    return requests.request("POST", url, headers=headers, data=payload)

async def get_status(speak_url: str) -> Response:
    return requests.request("GET", speak_url, headers=headers)

async def check_status(url: str) -> Response:
    print("Process text to speech....")
    while True:
        statusResponse = await get_status(url)

        statusResponseJson = statusResponse.json()
        if statusResponseJson["result"]["status"] == "done":
            return statusResponse
        time.sleep(2)

async def get_audio(audio_url: str) -> Response:
    return requests.request("GET", audio_url, headers=headers)

async def save_audio(audio_url: str):
    res =  await get_audio(audio_url)
    open(generated_speech_name, 'wb').write(res.content)

async def main():
    r1 = await send_text()
    r1 = r1.json()

    r2 = await check_status(r1["result"]["speak_url"])
    r2 = r2.json()

    await save_audio(r2["result"]["audio"]["url"])

    os.system("mpg123 " + generated_speech_name)

asyncio.run(main())

