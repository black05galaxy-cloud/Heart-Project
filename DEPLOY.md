# Deploy Heart Collaborative — Public Link for Everyone

Deploy this app so **anyone** can open it from any device (phone, tablet, laptop) with a single link — no installation needed.

**Don’t want to sign in or deploy?** You can run the app on your PC with **no sign-in**: double-click **`run_app.bat`** (Windows) or run `streamlit run app.py` in this folder, then open **http://localhost:8501** in your browser.

## Get Your Public Link (Free)

Use **Streamlit Community Cloud** (free, official Streamlit hosting):

### Step 1: Put your code on GitHub

1. Create a GitHub account if you don’t have one: [github.com](https://github.com).
2. Create a **new repository** (e.g. `Heart-Project`).
3. Upload your project folder:
   - Your repo must contain at least: `app.py`, `requirements.txt`.
   - Optional: `README.md`, `DEPLOY.md`.

### Step 2: Deploy on Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**.
2. Click **“Sign up”** or **“Sign in”** and log in with **GitHub**.
3. Click **“New app”**.
4. Choose:
   - **Repository:** your GitHub username / `Heart-Project` (or the repo name you used).
   - **Branch:** `main` (or the branch where your code is).
   - **Main file path:** `app.py`.
5. Click **“Deploy!”**.

### Step 3: Your public link

After a few minutes, your app will be live at a URL like:

**`https://heart-project-xxxx.streamlit.app`**

*(The "xxxx" part will be unique to your deployment)*

- This link works from **any device** and **any network** (phone, tablet, laptop, anywhere in the world).
- You can share it by email, chat, or social media.
- No need for others to install Python or run anything.
- **Copy this URL** — you'll need it for Step 4 (optional).

### Step 4 (Optional): Use your public link inside the app

To show this public link in the app’s “Application link” section:

1. In the Streamlit Cloud dashboard, open your app → **“Settings”** (or **“Manage app”**).
2. Go to **“Secrets”** or **“Environment variables”**.
3. Click **"Add new secret"** or **"New environment variable"**.
4. Add:
   - **Key:** `PUBLIC_APP_URL`
   - **Value:** your full URL (copy from Step 3), e.g. `https://heart-project-xxxx.streamlit.app`
5. Click **"Save"** and let the app redeploy (usually takes 1-2 minutes).

After that, the app will automatically display this public link in the sidebar and footer, so anyone using the app knows the shareable link.

**Note:** The app may also auto-detect the Streamlit Cloud URL. If it doesn't, use Step 4 above.

---

## Summary

| Where you run the app | Who can open it | Link |
|----------------------|------------------|------|
| **Your computer** (`streamlit run app.py`) | Only you (same machine) | `http://localhost:8501` |
| **Streamlit Community Cloud** (after deploy) | **Everyone, any device** | `https://your-app-name.streamlit.app` |

For a link that is **open for everyone and every system**, deploy to Streamlit Community Cloud and share the `https://....streamlit.app` link.
