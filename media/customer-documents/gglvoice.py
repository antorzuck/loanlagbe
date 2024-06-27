import pyttsx3

engine = pyttsx3.init()

# List available voices
voices = engine.getProperty('voices')
for voice in voices:
    print(f"ID: {voice.id}\nName: {voice.name}\nGender: {voice.gender}\nAge: {voice.age}")

# Set a specific voice by ID (choose one from the list)
engine.setProperty('voice', voices[2].id)  # Replace 0 with the index of the desired voice

# Set properties like rate and volume
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)   # Volume (0.0 to 1.0)

# Test the voice
engine.say("Hello, how are you today, how can i help you")
engine.runAndWait()

