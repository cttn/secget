# cli.py
# Interfaz de línea de comandos para la herramienta de descarga de filings SEC

import argparse
from main import download_and_merge_sec_filings

def main():
    parser = argparse.ArgumentParser(
        description="Descarga y combina documentos de la SEC para uno o más tickers."
    )
    parser.add_argument(
        "--tickers",
        nargs='+',
        required=True,
        help="Uno o más tickers separados por espacio (ej: AAPL MSFT TSLA)"
    )
    parser.add_argument(
        "--start",
        required=True,
        help="Fecha de inicio en formato YYYY-MM-DD"
    )
    parser.add_argument(
        "--end",
        required=True,
        help="Fecha de fin en formato YYYY-MM-DD"
    )
    parser.add_argument(
        "--forms",
        nargs='*',
        default=[],
        help="Tipos de formularios SEC a incluir (ej: 10-K 10-Q 8-K). Por defecto incluye todos."
    )

    args = parser.parse_args()

    for ticker in args.tickers:
        print(f"\n========== Procesando {ticker} ==========")
        download_and_merge_sec_filings(
            ticker=ticker,
            start=args.start,
            end=args.end,
            forms=args.forms
        )

if __name__ == "__main__":
    main()
