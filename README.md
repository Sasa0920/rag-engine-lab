# rag-engine-lab

## Run the backend

Use the bundled launcher so Windows picks a free local port:

```powershell
conda activate rag-eval
python run_backend.py
```

The frontend will automatically use the selected backend URL if the `BACKEND_URL` environment variable is set.