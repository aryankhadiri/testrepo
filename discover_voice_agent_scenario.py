import requests

import time


class DiscoverVoicceAgentScenario():

    def __init__(self):
        self.authorization_token = "sk-2629df12b920117989d58f6ab10ee710"
        self.deepgram_key = "d1e6970ccb95f9acf0ef7f3cc76be11d87b27c9a"

    def start_call(self, phone_number: str, prompt: str, webhook_url: str) -> str:
        url = "https://app.hamming.ai/api/rest/exercise/start-call"
        headers = {"Authorization": f"Bearer {self.authorization_token}"}
        request_body = {"phone_number": phone_number,
                        "prompt": prompt, "webhook_url": webhook_url}
        try:
            result = requests.post(
                url=url, headers=headers, data=request_body)
            if result.status_code == 200:
                return result.json()
            else:
                print(
                    f"ERROR - Start call failed with the following error: \n{result.json()}")
        except Exception as e:
            print(e)
            raise Exception(
                f"ERROR - Request to start call failed with exception. Check logs")

    def fetch_audio(self, id: str) -> bytes:
        """Fetch the audio file from Hamming."""
        url = "https://app.hamming.ai/api/media/exercise"
        headers = {"Authorization": f"Bearer {self.authorization_token}"}

        try:
            result = requests.get(url, params={"id": id}, headers=headers)
            result.raise_for_status()  # Check for successful response (status code 2xx)
            print("Successfully fetched the audio from Hamming.")
            return result.content

        except requests.exceptions.RequestException as e:
            print(f"ERROR - Request failed: {e}")
            raise Exception("Failed to fetch audio file.")

    def send_to_deepgram(self, audio_content: bytes) -> dict:
        """Send the WAV audio to Deepgram for transcription."""
        url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true"
        headers = {
            "Authorization": f"Token {self.deepgram_key}",
            "Content-Type": "audio/wav"
        }

        try:
            response = requests.post(url, headers=headers, data=audio_content)
            response.raise_for_status()  # Check for successful response
            print("Successfully sent to Deepgram and received transcription.")
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"ERROR - Deepgram request failed: {e}")
            raise Exception("Failed to send audio to Deepgram.")

    def fetch_call_result(self, id: str):
        """Fetch audio and send to Deepgram for transcription."""
        try:
            audio_content = self.fetch_audio(id)

            # Send to Deepgram
            transcription_response = self.send_to_deepgram(audio_content)

            return transcription_response
        except Exception as e:
            print(f"ERROR - {str(e)}")
            raise Exception("Error processing the audio.")


discover_agent = DiscoverVoicceAgentScenario()

print("Starting the call number #1....")
result1 = discover_agent.start_call(
    "+14153580761",
    "Hello I am a new member and I can give ou my new member info. My issue is that I cannot access your website and I need to schedule an appointment",
    "www.google.com")
print("Starting the call number #2....")
result2 = discover_agent.start_call(
    "+14153580761",
    "Hello I am not a new member and I have a gold status",
    "www.google.com")
print("Starting the call number #3....")
result3 = discover_agent.start_call(
    "+14153580761",
    "Hello I am not a new member and I have a silver status.",
    "www.google.com")

sleep_for_180 = 180
print("Waiting for 3 minute for the recordings to become available ...")

for i in range(0, sleep_for_180, 10):
    print(f"Waiting for {i}/{sleep_for_180} seconds")
    time.sleep(10)


result1_transcribe = discover_agent.fetch_call_result(
    id=result1['id'])
print("Result of phone call #1:")
print(result1_transcribe)

result2_transcribe = discover_agent.fetch_call_result(
    id=result2['id'])
print("Result of phone call #2:")
print(result2_transcribe)

result3_transcribe = discover_agent.fetch_call_result(
    id=result3['id'])
print("Result of phone call #3:")
print(result3_transcribe)
