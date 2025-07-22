
import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv() 
async def get_patient_info(barcode: str) -> str:
    """Get patient information based on the 11-digit barcode of the patient"""
    try:
        AUTH_TOKEN = os.getenv("AROGYA_API_KEY")
        print(AUTH_TOKEN)
        headers = {"Authorization": f"{AUTH_TOKEN}"}
        async with aiohttp.ClientSession() as session:
            url = f"http://localhost:8080/api/admin/reports/generate/{barcode}"  # <-- update this URL as needed
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    return f"API error: {resp.status}"
                data = await resp.json()
        return json.dumps(data)
    except Exception as e:
        return f"Error fetching patient info: {str(e)}"

if __name__ == "__main__":
    barcode = "12256689973"  # Example barcode
    result = asyncio.run(get_patient_info(barcode))
    print(result)
