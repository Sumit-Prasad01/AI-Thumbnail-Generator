import requests

API_BASE = "http://localhost:8000/api"


def upload_headshot(file):
    files = {
        "file" : {
            file.name,
            file.getvalue(),
            file.type
        }
    }

    res = requests.post(
        f"{API_BASE}/upload-headshot",
        files = files
    )

    res.raise_for_status()

    return res.json()



def create_job(
    prompt,
    num_thumbnails,
    headshot_url    
):
    
    payload = {
        "prompt" : prompt,
        "num_thumbnails" : num_thumbnails,
        "headshot_url" : headshot_url
    }

    res = requests.post(
        f"{API_BASE}/jobs",
        json = payload
    )

    res.raise_for_status()

    return res.json()



def get_job(job_id):

    res = requests.get(
        f"{API_BASE}/jobs/{job_id}"
    )

    res.raise_for_status()

    return res.json()