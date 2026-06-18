import json
import requests
from sseclient import SSEClient


def listen_to_job(job_id : str):
    """
    Listen to FastAPI SSE endpoint and yield events.
    """

    url = f"http://localhost:8000/api/jobs/{job_id}/stream"

    response = requests.get(
        url,
        stream = True,
        headers = {
            "Accept" : "text/event-stream"
        }
    )

    response.raise_for_status()

    client = SSEClient(response)

    for event in client.events():

        try:
            data = json.loads(event.data)
        
        except Exception:
            data = {}
        
        yield {
            "event" : event.event,
            "data" : data
        }