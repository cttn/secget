# test_bot.py
# Tests para telegram_bot handlers

import os
import sys
import types
import asyncio
import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

# Asegurar que la raíz del proyecto está en sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Crear stubs mínimos de telegram para evitar dependencias externas
tg_module = types.ModuleType("telegram")
tg_module.Update = object
sys.modules["telegram"] = tg_module

ext_module = types.ModuleType("telegram.ext")
class DummyApplication: ...
class DummyCommandHandler: ...
class DummyContextTypes:
    DEFAULT_TYPE = object
ext_module.Application = DummyApplication
ext_module.CommandHandler = DummyCommandHandler
ext_module.ContextTypes = DummyContextTypes
sys.modules["telegram.ext"] = ext_module

# Stub para main.download_and_merge_sec_filings
def _dummy_download(*args, **kwargs):
    raise NotImplementedError
main_module = types.ModuleType("main")
main_module.download_and_merge_sec_filings = _dummy_download
sys.modules["main"] = main_module

import telegram_bot
from telegram_bot import ini, fin, ticker, get_docs


def test_ini_actualiza_start_date():
    user_data = {}
    update = SimpleNamespace(message=SimpleNamespace(reply_text=AsyncMock()))
    context = SimpleNamespace(args=["2023-05-01"], user_data=user_data)
    asyncio.run(ini(update, context))
    assert user_data["start_date"] == "2023-05-01"


def test_fin_actualiza_end_date():
    user_data = {"start_date": "2023-01-01"}
    update = SimpleNamespace(message=SimpleNamespace(reply_text=AsyncMock()))
    context = SimpleNamespace(args=["2023-06-30"], user_data=user_data)
    asyncio.run(fin(update, context))
    assert user_data["end_date"] == "2023-06-30"


def test_ticker_actualiza_ticker():
    user_data = {}
    update = SimpleNamespace(message=SimpleNamespace(reply_text=AsyncMock()))
    context = SimpleNamespace(args=["msft"], user_data=user_data)
    asyncio.run(ticker(update, context))
    assert user_data["ticker"] == "MSFT"


def test_get_docs_invoca_descarga(monkeypatch, tmp_path):
    user_data = {
        "ticker": "AAPL",
        "start_date": "2023-01-01",
        "end_date": "2023-02-01",
    }
    pdf_path = tmp_path / "dummy.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%%EOF")

    mock_download = Mock(return_value=str(pdf_path))
    monkeypatch.setattr(telegram_bot, "download_and_merge_sec_filings", mock_download)

    mock_reply = AsyncMock()
    update = SimpleNamespace(message=SimpleNamespace(reply_document=mock_reply, reply_text=AsyncMock()))
    context = SimpleNamespace(args=[], user_data=user_data)

    asyncio.run(get_docs(update, context))

    mock_download.assert_called_once_with("AAPL", "2023-01-01", "2023-02-01")
    assert mock_reply.called
