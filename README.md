# 🎨 RGB Color Studio

An interactive RGB color mixer built with Python and Streamlit.

Adjust Red, Green, and Blue values to create colors in real time.
Explore color harmonies, compare text contrast, and export your
favorite colors as CSS or JSON files.

## ✨ Features

- **Live RGB color mixer:** Adjust Red, Green, and Blue from 0 to 255.
- **Instant color preview:** See your selected color update immediately.
- **HEX and RGB values:** View the exact color codes.
- **Preset color gallery:** Explore ready-made colors.
- **Color harmonies:** Generate complementary, analogous, triadic,
  split-complementary, and tetradic combinations.
- **Contrast checker:** Compare white and black text on your color.
- **CSS export:** Download reusable CSS variables and classes.
- **JSON export:** Save your color information and palette.
- **Responsive layout:** Use the app on desktop or mobile.

## 🛠️ Technologies

- Python
- Streamlit
- HTML and CSS
- Python standard library

## 📁 Project Structure

```text
rgb-color-studio/
├── app.py
├── requirements.txt
└── README.md
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/SukainaZaidi21/rgb-color-studio.git
cd rgb-color-studio
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS or Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

Open this URL in your browser:

http://localhost:8501

## ☁️ Deploy on Streamlit Community Cloud

1. Create a repository on GitHub.
2. Upload `app.py`, `requirements.txt`, and `README.md` to the repository root.
3. Visit https://share.streamlit.io/
4. Sign in using your GitHub account.
5. Create a new app and select your repository.
6. Choose the `main` branch.
7. Set the main file path to `app.py`.
8. Click **Deploy**.

Streamlit will install the dependencies and launch your application.

## 🎨 Understanding RGB

RGB stands for Red, Green, and Blue.

Each channel accepts a value between 0 and 255.

| Color | RGB | HEX |
|---|---|---|
| Red | (255, 0, 0) | `#FF0000` |
| Green | (0, 255, 0) | `#00FF00` |
| Blue | (0, 0, 255) | `#0000FF` |
| White | (255, 255, 255) | `#FFFFFF` |
| Black | (0, 0, 0) | `#000000` |

Combining different channel values produces approximately 16.7 million
possible RGB colors.

## 📤 Export Formats

### CSS

Export your selected color as CSS variables and a reusable class.

### JSON

Export the color's HEX value, RGB channels, text color, selected harmony,
and palette information.

## 📄 License

This project is available under the MIT License. To distribute it under
that license, add a `LICENSE` file containing the MIT License text.
