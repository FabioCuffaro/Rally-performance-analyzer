.PHONY: install run-api run-dashboard test help

# ── Setup ──────────────────────────────────────────────────────────
install:
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	cp -n .env.example .env || true
	@echo "✅  Entorno listo. Activa con: source venv/bin/activate"

# ── Run ────────────────────────────────────────────────────────────
run-api:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

run-dashboard:
	streamlit run dashboard/app.py --server.port 8501

# ── Tests ──────────────────────────────────────────────────────────
test:
	pytest backend/tests/ -v

# ── Help ───────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make install        Crea venv e instala dependencias"
	@echo "  make run-api        Arranca FastAPI en localhost:8000"
	@echo "  make run-dashboard  Arranca Streamlit en localhost:8501"
	@echo "  make test           Ejecuta los tests"
	@echo ""
