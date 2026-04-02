# Smart File Analysis Web App

A Streamlit app to analyze files, summarize `.txt` content, visualize file counts, and export results to Excel.

## Features

- Analyze files from:
  - Local folder path (desktop usage)
  - Uploaded files (cloud hosting usage)
- Summarize `.txt` files
- Show file analysis graph (TXT vs Other)
- Preview processed table
- Download Excel output
- Optionally save `output.xlsx` to local folder (local mode)

## Run locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start app:

```bash
streamlit run web_app.py
```

3. Open browser:

`http://localhost:8501`

## GitHub push

```bash
git init
git add .
git commit -m "Initial Smart File Analysis web app"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Host on Streamlit Community Cloud

1. Push this project to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from your repo.
4. Set main file path to `web_app.py`.
5. Deploy.

After deploy, use **Upload files** mode in the hosted app.
