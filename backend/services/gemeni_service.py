import base64
import httpx

from google import genai
from google.genai import types

from config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def generate_thumbnail(
    prompt: str,
    style_prompt: str,
    headshot_url: str,
) -> bytes:
    """
    Generate thumbnail using Gemini image generation model.
    Uses the user's headshot as a reference image.
    Returns raw PNG bytes.
    """

    full_prompt = (
        f"{style_prompt}\n\n"
        f"User request: {prompt}\n\n"
        "IMPORTANT: The generated thumbnail MUST prominently feature "
        "the person shown in the provided reference headshot photo. "
        "Keep their likeness accurate."
    )

    # Download reference image
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(headshot_url)
        response.raise_for_status()
        image_bytes = response.content

    # Generate image
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="png",  
            ),
            full_prompt,
        ],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    # Extract generated image
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            return part.inline_data.data

    raise RuntimeError("No image generation result found")