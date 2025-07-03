# Voice AI Agent

**An end-to-end voice AI agent built with LiveKit, Twilio, Deepgram, OpenAI, and AWS Polly.**  
This agent receives voice calls, understands user goals, gathers required information, and stores results in Google Sheets.

---

## Features

- **Voice Call Integration:** Users call the agent via Twilio.
- **Real-Time Speech Recognition:** Deepgram API transcribes user speech to text.
- **Conversational Intelligence:** OpenAI LLM interprets user intent and manages dialog flow.
- **Dynamic Data Collection:** Gathers required fields based on user goals (e.g., private pay, insurance case manager, discharge).
- **Natural Voice Responses:** AWS Polly generates lifelike speech for agent replies.
- **Data Storage:** Captured information is stored in Google Sheets via backend API.

---

## Workflow

1. **User places a voice call**  
   The user calls a Twilio number connected to the agent.

2. **Audio streaming & transcription**  
   LiveKit manages real-time audio. Deepgram transcribes incoming speech to text[3][4][5].

3. **Intent & data extraction**  
   The transcribed text is processed by an OpenAI LLM, which:
   - Identifies the user's goal (e.g., private pay, insurance case manager, discharge)
   - Determines which fields are required based on the goal
   - Extracts relevant data from the conversation

4. **Conversational response**  
   The agent replies using AWS Polly to synthesize natural speech.

5. **Data storage**  
   Collected data is sent to a backend service, which saves it to a Google Sheet.

---

## Tech Stack

| Component          | Technology      | Purpose                                              |
|--------------------|----------------|------------------------------------------------------|
| Telephony          | Twilio         | Receives and manages voice calls                     |
| Real-time Audio    | LiveKit        | Handles audio streaming and low-latency connections  |
| Speech-to-Text     | Deepgram API   | Transcribes user speech to text                      |
| Language Model     | OpenAI GPT     | Interprets intent, manages dialog, extracts fields   |
| Text-to-Speech     | AWS Polly      | Converts agent's text responses to speech            |
| Data Storage       | Google Sheets  | Stores collected user data via backend API           |

---

## Quick Start

### Prerequisites

- Twilio account and phone number
- LiveKit project and credentials
- Deepgram API key
- OpenAI API key
- AWS credentials for Polly
- Google Sheets API credentials

### Setup

1. **Clone the repository**
   
    ```git clone https://github.com/machan1119/golden-medical-voice-agent.git```
    
    ```cd golden-medical-voice-agent```
  
3. **Install dependencies**
     
     ```pip install -r requirements.txt```
   
4. **Configure environment variables**
     
    Create a `.env` file with your API keys and credentials:
      
      ```
      AWS_ACCESS_KEY_ID=
      AWS_SECRET_ACCESS_KEY=
      AWS_REGION=
      LIVEKIT_API_KEY=
      LIVEKIT_API_SECRET=
      LIVEKIT_URL=
      OPENAI_API_KEY=
      DEEPGRAM_API_KEY=
      BACKEND_URL=
      ```
    
5. **Run the agent**
   
   ```python main.py```



---

## Example Use Case

> **User:** "Hi, I need to talk to the insurance case manager about my discharge."
>
> **Agent:** "Sure, I can help with that. May I have your policy number and discharge date?"

The agent identifies the user's goal, asks for required fields, and stores the information in Google Sheets.

---

## Customization

- **Add new user goals:** Update the LLM prompt and backend logic to handle more scenarios.
- **Change storage backend:** Replace Google Sheets integration with your preferred database.
- **Voice customization:** Adjust AWS Polly settings for different voices or languages.

---

## Contributing

Pull requests and feature suggestions are welcome!

---

