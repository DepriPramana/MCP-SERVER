import logging

import httpx
from mcp.server import MCPServer

logging.basicConfig(level=logging.INFO)  # log ke stderr, BUKAN stdout
BMKG = "https://data.bmkg.go.id/DataMKG/TEWS"

mcp = MCPServer("Info Gempa BMKG")


async def ambil(file: str) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BMKG}/{file}")
        r.raise_for_status()
        return r.json()["Infogempa"]["gempa"]


def rapikan(g: dict) -> str:
    return (f"{g['Tanggal']} {g['Jam']} | M{g['Magnitude']} | "
            f"kedalaman {g['Kedalaman']} | {g['Wilayah']}")


@mcp.tool()
async def gempa_terkini() -> str:
    """Gempa terbaru (satu kejadian) di Indonesia, dari data BMKG."""
    g = await ambil("autogempa.json")
    logging.info("gempa_terkini dipanggil")
    return f"{rapikan(g)} | {g['Potensi']}"


@mcp.tool()
async def gempa_dirasakan(min_magnitudo: float = 0.0) -> str:
    """Daftar gempa yang dirasakan warga (maks. 15 terbaru), bisa difilter magnitudo minimum."""
    daftar = await ambil("gempadirasakan.json")
    hasil = [rapikan(g) for g in daftar if float(g["Magnitude"]) >= min_magnitudo]
    return "\n".join(hasil) or "Tidak ada gempa dirasakan dengan magnitudo setinggi itu."


@mcp.resource("gempa://sumber")
def sumber() -> str:
    """Keterangan sumber data gempa."""
    return "Sumber data: BMKG (Badan Meteorologi, Klimatologi, dan Geofisika), data.bmkg.go.id"


@mcp.prompt()
def ringkas_untuk_keluarga() -> str:
    """Template ringkasan gempa untuk grup keluarga."""
    return ("Ambil info gempa terkini, lalu tulis ringkasan maksimal 3 kalimat yang tenang "
            "untuk grup WhatsApp keluarga. Sebutkan BMKG sebagai sumber dan jangan "
            "menambahkan informasi yang tidak ada di data.")


if __name__ == "__main__":
    mcp.run()
