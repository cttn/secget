# SEC Filings Downloader

Librería en Python para buscar, descargar y combinar automáticamente documentos presentados ante la SEC (como 10-K, 10-Q, 8-K) para uno o varios tickers en un rango de fechas determinado.

## 🚀 Características

- Conversión automática de **ticker** a **CIK**.
- Uso de la **EDGAR Full-Text Search API** para buscar documentos.
- Descarga de archivos HTML y conversión a PDF.
- Unión de todos los PDFs en un único archivo final por ticker.
- Interfaz por línea de comandos (`cli.py`).
- Tests automatizados con `pytest`.

## 📦 Requisitos

- Python 3.8+
- [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) instalado en el sistema (necesario para `pdfkit`)

## 🛠 Instalación

```bash
pip install -r requirements.txt
```

Asegurate también de tener `wkhtmltopdf` disponible en el PATH del sistema.

## 🧪 Ejemplo de uso

### Modo script

```bash
python main.py
```

Esto descargará los documentos 10-K, 10-Q y 8-K del ticker `AAPL` en el año 2023 y los combinará en un único PDF dentro de `output/AAPL/AAPL_merged.pdf`.

### Modo CLI (línea de comandos)

```bash
python cli.py --tickers AAPL MSFT --start 2023-01-01 --end 2023-12-31 --forms 10-K 10-Q
```

Podés omitir `--forms` y usará por defecto `10-K`, `10-Q` y `8-K`.

## 🤖 Bot de Telegram

El proyecto incluye un bot de Telegram para solicitar y recibir archivos PDF de filings desde un chat.  
Cada usuario mantiene su propio estado de consulta (ticker y rango de fechas) y el bot genera el PDF utilizando las mismas funciones que el script principal.

### Configuración

1. Crea un bot con [@BotFather](https://t.me/BotFather) y obtén el token.
2. Exporta el token en la variable de entorno `TELEGRAM_BOT_TOKEN`:
   ```bash
   export TELEGRAM_BOT_TOKEN="TU_TOKEN"
   ```
3. Instala las dependencias listadas en `requirements.txt` (incluye `python-telegram-bot`).
4. Opcionalmente podés modificar `DEFAULT_START` en `telegram_bot.py` para cambiar la fecha inicial por defecto.

### Comandos disponibles

- `/ini YYYY-MM-DD` — establece la fecha inicial. Por defecto se usa `2023-01-01`.
- `/fin YYYY-MM-DD` — establece la fecha final. Si no se define, se usa la fecha actual.
- `/ticker TICKER` — define el ticker a consultar (se almacena en mayúsculas).
- `/get` — descarga los filings 10-K, 10-Q y 8-K del período y envía un único PDF.

### Ejemplo de conversación

```
/ini 2023-01-01
/fin 2023-03-31
/ticker AAPL
/get
```

El bot responderá enviando un archivo PDF con los documentos disponibles para el ticker en el rango de fechas indicado.

### Ejecutar el bot

Iniciá el servicio con:

```bash
python telegram_bot.py
```

El bot quedará escuchando mensajes y responderá a los comandos anteriores.

## 🧪 Testing automatizado

Instalá dependencias:

```bash
pip install pytest fpdf
```

Ejecutá todos los tests:

```bash
pytest
```

Tests incluidos:
- `test_fetch.py` — Verifica CIKs y búsqueda de filings reales
- `test_merge.py` — Prueba combinación de PDFs

## 🧱 Estructura del proyecto

```
sec_filings_downloader/
├── fetch.py                 # Buscar CIK y documentos desde EDGAR
├── download.py              # Descargar HTML y convertir a PDF
├── merge.py                 # Unir PDFs en uno solo
├── main.py                  # Script orquestador
├── cli.py                   # Interfaz CLI con argparse
├── requirements.txt         # Dependencias
├── README.md                # Documentación
├── tests/                   # Tests automatizados (pytest)
│   ├── test_fetch.py
│   └── test_merge.py
├── output/                  # PDFs generados por ticker
│   └── AAPL/                # Ejemplo: carpeta AAPL
└── .gitignore
```

## 🔍 Funcionalidades disponibles

- `get_cik_from_ticker(ticker)` — convierte ticker a CIK
- `search_sec_filings(cik, forms, start, end)` — busca documentos por tipo y fecha
- `download_html_and_convert_to_pdf(url, output_path)` — descarga y convierte HTML a PDF
- `merge_pdfs(list_of_pdfs, output_path)` — combina PDFs en uno solo
- `download_and_merge_sec_filings(ticker, start, end, forms)` — proceso completo para un ticker
- `cli.py` — interfaz amigable desde terminal

## ✅ TODO (próximas versiones)

- Salida en otros formatos (JSON, TXT)
- Uso de multiprocessing para acelerar conversiones
- Indexado y búsqueda de texto dentro de los PDFs
- Interfaz web
- Publicación como paquete en PyPI

## 📄 Licencia

MIT License
