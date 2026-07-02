"""
TEDxVibe MCP Server
Il talk giusto per ogni emozione — unibg_tedx_2026
"""

from mcp.server.fastmcp import FastMCP
from motor.motor_asyncio import AsyncIOMotorClient
from mcp.server.transport_security import TransportSecuritySettings
import uvicorn

MONGO_URI = (
    "mongodb+srv://giorgiounibg2026:giorgiounibg2026"
    "@clustertcm.g9si2se.mongodb.net/?appName=Cluster0"
)

client = AsyncIOMotorClient(MONGO_URI)
db = client["unibg_tedx_2026"]
watch_next_collection = db["tedx_watch_next"]

mcp = FastMCP(
    "TEDxVibe MCP Server — Il talk giusto per ogni emozione",
    transport_security=TransportSecuritySettings(
        allowed_hosts=["*", "54.88.185.153", "54.88.185.153:8443"]
    )
)


@mcp.tool()
async def get_talks_by_emotion(emotion: str, limit: int = 10) -> dict:
    """
    TEDxVibe core feature: given a user emotional state, return the most
    relevant TEDx talks to watch right now.
    Available emotions: stress, tristezza, paura, depressione, rabbia,
    stanchezza, motivazione, felicita, curiosita, crescita.
    Talks are pre-computed by the TEDxVibe ETL pipeline on AWS Glue
    using a hybrid model: emotion + tag similarity + popularity.
    """
    cursor = watch_next_collection.find({"emotion": emotion}).limit(limit)
    talks = []
    async for doc in cursor:
        talks.append({
            "id": str(doc.get("_id")),
            "emotion": doc.get("emotion"),
            "duration": doc.get("duration"),
            "tags": doc.get("tags"),
            "description": (doc.get("description") or "")[:200] + "..."
        })

    if not talks:
        return {
            "error": f"No talks found for emotion '{emotion}'.",
            "hint": "Try: stress, motivazione, felicita, curiosita, crescita"
        }

    return {
        "emotion": emotion,
        "count": len(talks),
        "talks": talks,
        "powered_by": "TEDxVibe — il talk giusto per ogni emozione"
    }


@mcp.tool()
async def list_emotions() -> dict:
    """
    List all available emotions in the TEDxVibe system.
    Use this to discover which emotions are supported before
    calling get_talks_by_emotion.
    """
    emotions = [
        {"emotion": "stress", "description": "Talk per gestire lo stress e trovare calma"},
        {"emotion": "tristezza", "description": "Talk per ritrovare felicita e connessione"},
        {"emotion": "paura", "description": "Talk per affrontare le paure e crescere"},
        {"emotion": "depressione", "description": "Talk per la salute mentale e il benessere"},
        {"emotion": "rabbia", "description": "Talk su attivismo, giustizia e cambiamento"},
        {"emotion": "stanchezza", "description": "Talk su riposo, equilibrio e recupero"},
        {"emotion": "motivazione", "description": "Talk per ispirarsi e raggiungere obiettivi"},
        {"emotion": "felicita", "description": "Talk su gioia, creativita e community"},
        {"emotion": "curiosita", "description": "Talk su scienza, scoperta e innovazione"},
        {"emotion": "crescita", "description": "Talk su sviluppo personale e leadership"}
    ]
    return {
        "available_emotions": emotions,
        "total": len(emotions),
        "powered_by": "TEDxVibe — il talk giusto per ogni emozione"
    }


if __name__ == "__main__":
    uvicorn.run(
        mcp.streamable_http_app(),
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem"
    )
