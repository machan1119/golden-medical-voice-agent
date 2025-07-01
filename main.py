import uuid
import asyncio
import requests
import multiprocessing
from typing import cast, Annotated, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from prompt import SYSTEM_PROMPT
from livekit import rtc, agents
from livekit.agents import (
    Agent, AgentSession, AutoSubscribe, JobContext,
    WorkerOptions, ChatContext
)
from livekit.agents.llm import function_tool
from livekit.plugins import deepgram, silero, aws, openai
from openai.types.beta.realtime.session import TurnDetection

from config import settings
from helpers import data_parse_from_chat


class PrivatePayInput(BaseModel):
    patient_name: str
    weight: str
    pickup_address: str
    dropoff_address: str
    appointment_date: str
    one_way_or_round_trip: str
    equipment_needed: str
    any_stairs_and_accompanying_passengers: str
    user_name: str
    phone_number: str
    email: str


class InsuranceCaseManagerInput(BaseModel):
    patient_name: str
    pickup_address: str
    dropoff_address: str
    authorization_number: str
    appointment_date: str


class DischargeInput(BaseModel):
    patient_name: str
    pickup_facility_name: str
    pickup_facility_address: str
    pickup_facility_room_number: str
    dropoff_facility_name: str
    dropoff_facility_address: str
    dropoff_facility_room_number: str
    appointment_date: str
    is_oxygen_needed: str
    oxygen_amount: str
    is_infectious_disease: str
    weight: str


class VoiceAIAgent:
    def __init__(self):
        self.user_phone = None

    def _generate_chat_id(self) -> str:
        return uuid.uuid4().hex

    def get_participant_details(self, participant: rtc.RemoteParticipant) -> dict:
        if participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP:
            return {
                "user_phone_number": participant.attributes.get("sip.phoneNumber", "unknown"),
                "twilio_phone_number": participant.attributes.get("sip.trunkPhoneNumber", "unknown"),
                "chat_id": self._generate_chat_id(),
            }
        return {
            "user_phone_number": participant.identity,
            "twilio_phone_number": "unknown",
            "chat_id": self._generate_chat_id(),
        }

    async def post_payload(self, intent: str, data: dict):
        print("payload", data)
        payload = {
            "intent": intent,
            "data": data_parse_from_chat(data, intent, "voice_call", self.user_phone),
        }
        try:
            requests.post(
                f"{settings.BACKEND_URL}/store/",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
        except Exception as e:
            print("Error posting to backend:", e)

    @function_tool()
    async def handle_private_pay(self, payload: Annotated[PrivatePayInput, Field()]):
        await self.post_payload("PRIVATE_PAY", payload.model_dump())
        return "Thanks for calling! Please reply with the trip details listed above so we can prepare your quote and confirm availability."

    @function_tool()
    async def handle_insurance(self, payload: Annotated[InsuranceCaseManagerInput, Field()]):
        await self.post_payload("INSURANCE_CASE_MANAGERS", payload.model_dump())
        return "Thank you — we’ve received the transport request for you. We’ll forward this to dispatch for review and follow up shortly."

    @function_tool()
    async def handle_discharge(self, payload: Annotated[DischargeInput, Field()]):
        await self.post_payload("DISCHARGE", payload.model_dump())
        return "Got it! Our dispatch team will review this now and follow up shortly."

    async def entrypoint(self, ctx: JobContext):
        self.vad = silero.VAD.load(
            min_speech_duration=0.05,
            min_silence_duration=0.5,
            prefix_padding_duration=0.3,
            max_buffered_speech=30.0,
            activation_threshold=0.5,
            sample_rate=16000,
            force_cpu=True,
        )
        self.stt = deepgram.STT(model="nova-3", language="en-US")
        self.llm = openai.LLM(
            model="gpt-3.5-turbo",  # or "gpt-4-turbo", "gpt-3.5-turbo"
            tool_choice="auto",  # Disable auto-tool calls for faster interaction
            parallel_tool_calls=True,  # Use parallel tools for faster processing
            temperature=0.2, 
        )
        self.tts = aws.TTS(voice="Ruth", speech_engine="neural", language="en-US", region="us-east-1")

        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        participant = await ctx.wait_for_participant()
        details = self.get_participant_details(participant)
        self.user_phone = details["user_phone_number"]

        chat_ctx = ChatContext()
        chat_ctx.add_message(
            role="system",
            content=[SYSTEM_PROMPT],
            id=details["chat_id"]
        )

        agent = Agent(
            instructions="Assist with non-emergency medical transport. Collect and confirm structured data and use tools to submit.",
            chat_ctx=chat_ctx,
            tools=[self.handle_private_pay, self.handle_insurance, self.handle_discharge],
            llm=self.llm,
            stt=self.stt,
            tts=self.tts,
            vad=self.vad,
        )

        session = AgentSession()
        await session.start(agent=agent, room=ctx.room)
        await session.say("Hi! This is Golden State Medical Transport. How can I assist you today?")

        try:
            while session._activity:
                await asyncio.sleep(0.5)  # Reduced polling delay to 0.5s for faster responsiveness
        except Exception as e:
            print("Session error:", e)
        finally:
            await session.aclose()

    def run(self):
        agents.cli.run_app(WorkerOptions(entrypoint_fnc=self.entrypoint, load_threshold=1))


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    VoiceAIAgent().run()
