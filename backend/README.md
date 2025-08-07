# Backend

## ⚙️ Sozlash

1. Create a `.env` file:

```bash
cp example_env .env
```

2. Create venv

```bash
python -m venv .venv
. .venv/bin/activate
```

Install libraries

```bash
pip3 install -r requirements.txt
```

3. Run the server

```bash
cd backend
uvicorn main:app --reload
```

4. Testing
```bash
pytest .
```