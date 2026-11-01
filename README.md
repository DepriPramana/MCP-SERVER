# mcp-gempa-bmkg

Contoh MCP server sederhana dengan Python. Server ini mengambil info gempa dari data terbuka BMKG, lalu bisa dipakai di Claude Desktop dan Antigravity.

Repo ini pendamping video **"Bikin MCP Server Sendiri dari Nol"** di kanal Tips Unix.

> ⚠️ **Hanya untuk belajar, bukan sistem peringatan dini resmi.** Untuk info gempa dan tsunami resmi, pakai kanal resmi BMKG, misalnya aplikasi **InfoBMKG** atau https://www.bmkg.go.id.

## Isi server

| Jenis | Nama | Fungsi |
| --- | --- | --- |
| Tool | `gempa_terkini` | Gempa terbaru (satu kejadian), lengkap dengan keterangan potensi tsunami dari BMKG |
| Tool | `gempa_dirasakan` | Daftar gempa yang dirasakan warga (maks. 15 terbaru), bisa difilter `min_magnitudo` |
| Resource | `gempa://sumber` | Keterangan sumber data |
| Prompt | `ringkas_untuk_keluarga` | Template ringkasan gempa yang tenang untuk grup keluarga |

Semuanya ada di satu file, `server.py`, dan memakai SDK resmi `mcp` versi 2 (`MCPServer`).

## Syarat

- Python 3.11 atau lebih baru
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Node.js, hanya untuk MCP Inspector (`mcp dev`)

## Install

```bash
git clone https://github.com/<akun-kamu>/mcp-gempa-bmkg.git
cd mcp-gempa-bmkg
uv sync
```

Kalau mau membangun dari nol seperti di video:

```bash
uv init mcp-gempa-bmkg
cd mcp-gempa-bmkg
uv add "mcp[cli]" httpx
```

Lalu buat `server.py`. `httpx` harus ditambahkan sendiri karena tidak ikut terpasang bersama `mcp` versi 2.

> Catatan: `uv init` versi baru juga membuat folder `src/`. Folder itu tidak dipakai di proyek ini dan boleh dihapus.

## Uji dengan MCP Inspector

```bash
uv run mcp dev server.py
```

Inspector terbuka di browser. Klik **Connect**, lalu coba tab **Tools**, **Resources**, dan **Prompts**.

## Sambungkan ke aplikasi AI

Ketiga aplikasi memakai entri yang sama. Ganti `/PATH/LENGKAP/mcp-gempa-bmkg` dengan path lengkap folder proyek. Di Windows, tulis path dengan `\\`, misalnya `C:\\Users\\kamu\\mcp-gempa-bmkg`.

```json
{
  "mcpServers": {
    "gempa-bmkg": {
      "command": "uv",
      "args": ["--directory", "/PATH/LENGKAP/mcp-gempa-bmkg", "run", "server.py"]
    }
  }
}
```

### Claude Desktop

Buka **Settings → Developer → Edit Config**. File config ada di:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Tambahkan entri di atas, simpan, lalu **keluar penuh** dari Claude Desktop dan buka lagi.

### Antigravity CLI (`agy`) dan aplikasi Antigravity

Keduanya memakai file config global yang sama: `~/.gemini/config/mcp_config.json`.

- Dari aplikasi Antigravity: menu **…** di panel agent → **MCP Servers** → **Manage MCP Servers** → **View raw config**.
- Dari Antigravity CLI: edit file di atas, jalankan ulang `agy`, lalu ketik `/mcp` untuk melihat status server.

### Gemini CLI

Gemini CLI tidak lagi melayani akun Google gratis sejak 18 Juni 2026 (penggantinya Antigravity CLI). Kalau kamu masih memakainya dengan API key atau lisensi enterprise, tambahkan entri yang sama di `~/.gemini/settings.json`.

## 3 kesalahan paling umum

1. **Memakai `print()`.** Lewat stdio, stdout khusus untuk pesan JSON-RPC, jadi `print()` biasa bisa memutus koneksi. Pakai `logging`, yang menulis ke stderr, atau `print(..., file=sys.stderr)`.
2. **Path relatif di config.** Aplikasi AI tidak tahu folder proyekmu. Tulis path **lengkap** ke folder proyek. Kalau `uv` tidak ditemukan, tulis juga path lengkap ke `uv` (cek dengan `which uv` di macOS/Linux atau `where uv` di Windows).
3. **Lupa restart.** Setelah config diubah, keluar penuh dari aplikasinya (bukan sekadar menutup jendela), lalu buka lagi.

## Sumber data

Data gempa: **BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)**, https://data.bmkg.go.id. Sesuai ketentuan BMKG, cantumkan BMKG sebagai sumber data dan tampilkan di aplikasi atau sistemmu.

## Lisensi

[MIT](LICENSE)
"# MCP-SERVER" 
