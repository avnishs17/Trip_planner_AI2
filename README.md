uv venv -p python3.10.18
.venv/Scripts/activate

uv add -r requirements.txt
or
uv pip install -r requirements.txt
or 
uv pip install .[dev]  # you must have the pyproject.toml with all the dependencies [ for replicability]

# you can also do this if you have the pyproejct.toml
uv pip compile > requirements.txt
uv pip install -r requirements.txt

streamlit run streamlit_app.py

uvicorn main:app --reload --port 8000