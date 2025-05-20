import asyncio

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

openai = AsyncOpenAI()

input = """Yeah, yeah, ya got Big Apple Insurance, whaddaya need? Let's make this quick, I got places to be.\n\nIf ya gotta file a claim, press 1—lemme guess, someone cut ya off? Figures.\n\nWanna check the status? Press 2, I know, I know, hurry it up, right?\n\nIf ya just wanna hold, press 3—hey, your call, but don't say I didn't warn ya.\n\nNeed a real person? Press 4, and I'll get ya through—just don't start yellin' at 'em, they're doin' their best.\n\nAlright, let's move it along, time is money, buddy!"""

instructions = """Voice: Gruff, fast-talking, and a little worn-out, like a New York cabbie who's seen it all but still keeps things moving.\n\nTone: Slightly exasperated but still functional, with a mix of sarcasm and no-nonsense efficiency.\n\nDialect: Strong New York accent, with dropped \"r\"s, sharp consonants, and classic phrases like whaddaya and lemme guess.\n\nPronunciation: Quick and clipped, with a rhythm that mimics the natural hustle of a busy city conversation.\n\nFeatures: Uses informal, straight-to-the-point language, throws in some dry humor, and keeps the energy just on the edge of impatience but still helpful."""

async def main() -> None:

    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="echo",
        input=input,
        instructions=instructions,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

if __name__ == "__main__":
    asyncio.run(main())