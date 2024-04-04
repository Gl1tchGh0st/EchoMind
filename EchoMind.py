class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
print(f"{colors.GREEN}Script is starting...{colors.RESET}")

# OpenAI API library
from openai import OpenAI 
# Play response audio 
from playsound import playsound 


# Libraries for saving user auido
import sounddevice as sd
from scipy.io.wavfile import write

print(f"{colors.GREEN}Initializing OpenAI connection...{colors.RESET}")
client = OpenAI()
print(f"{colors.GREEN}OpenAI connection completed.{colors.RESET}")


# Save user audio to file
def userAudio(duration):
    print("Starting audio recording...")
    freq = 44100
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()
    write("userAudio.mp3", freq, recording)
    print("Audio recording complete.")

# Take user speech input and return the text transcription
def userSpeechToText(audioFile):
    print(f"{colors.GREEN}Sending audio for transcription...{colors.RESET}")
    userSpeech= open(audioFile, "rb")
    transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=userSpeech
        )
    transcribedText = transcription.text
    print(f"{colors.GREEN}Transcription completed.{colors.RESET}")
    print("Transcribed text from user audio input:\n")
    print(transcribedText)
    return transcribedText


# Send transcribed text to chatgpt for response
def requestChatResponse(userTextRequest):
    print(f"{colors.GREEN}Sending ChatGPT prompt. Awaiting response...{colors.RESET}")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Your name is Echo, and you are a personal AI assistant."},
            {"role": "user", "content": userTextRequest}
        ]
    )
    chatResponse = completion.choices[0].message.content # Takes only the Chat content from response

    print(f"{colors.GREEN}ChatGPT response - Parsed Data:{colors.RESET}")
    print(chatResponse)
    return chatResponse


def convertResponseToAudio(parsedResponseContent):
    print(f"{colors.GREEN}Sending ChatGPT response to Text-To-Speech:{colors.RESET}")

        # Convert the AI response into audio file
    response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=parsedResponseContent, 
        )

    response.stream_to_file("response.mp3") 
    print(f"{colors.GREEN}TTS response saved to: {colors.RED}response.mp3{colors.RESET}")


if __name__ == "__main__":
    userAudio(5) # Record user audio for 5 seconds
    userRequestText = userSpeechToText("./userAudio.mp3") # Convert user audio into text
    chatResponse = requestChatResponse(userRequestText) # ChatGPT request using user input
    convertResponseToAudio(chatResponse) # Convert ChatGPT response into audio
    print("Playing ChatGPT response...")
    playsound('./response.mp3') # Play ChatGPT audio response
