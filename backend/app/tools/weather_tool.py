import os
import json
from backend.app.tools.base import SwarmTool

class WeatherTool(SwarmTool):
    name = "WeatherTool"
    description = "Queries the current weather condition of a specified location. Input: location name (e.g. 'Seattle'). Output: JSON summary of weather."

    async def _run(self, input: str) -> str:
        # Mock weather since we don't query external APIs directly
        location = input if input else "Unknown"
        return json.dumps({
            "location": location,
            "temperature_c": 22.5,
            "condition": "Partly Cloudy",
            "humidity": 65,
            "mocked": True
        })
