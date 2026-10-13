import json
import colorsys
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="RGB Color Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .hero {
        padding: 1.8rem;
        border-radius: 20px;
        background: linear-gradient(120deg, #171923, #303650);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: white;
        margin-bottom: 0.3rem;
    }

    .hero p {
        color: #d7dcef;
        font-size: 1.05rem;
    }

    .color-preview {
        min-height: 300px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        padding: 2rem;
        transition: background-color 0.15s ease;
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    }

    .color-preview h2 {
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: 2px;
    }

    .color-preview p {
        font-size: 1.05rem;
        margin-top: 0.7rem;
    }

    .swatch {
        height: 95px;
        border-radius: 12px;
        margin-bottom: 8px;
        border: 1px solid rgba(128,128,128,0.2);
    }

    div[data-testid="stMetric"] {
        padding: 12px;
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# COLOR UTILITIES
# --------------------------------------------------
def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(
        int(hex_color[i:i + 2], 16)
        for i in (0, 2, 4)
    )


def text_color_for_background(r, g, b):
    """Choose black or white text for readability."""
    channels = [r, g, b]
    linear = []

    for value in channels:
        value = value / 255
        if value <= 0.04045:
            linear.append(value / 12.92)
        else:
            linear.append(((value + 0.055) / 1.055) ** 2.4)

    luminance = (
        0.2126 * linear[0]
        + 0.7152 * linear[1]
        + 0.0722 * linear[2]
    )

    return "#000000" if luminance > 0.179 else "#FFFFFF"


def contrast_ratio(rgb1, rgb2):
    def luminance(rgb):
        values = []
        for value in rgb:
            value = value / 255
            if value <= 0.04045:
                values.append(value / 12.92)
            else:
                values.append(((value + 0.055) / 1.055) ** 2.4)

        return (
            0.2126 * values[0]
            + 0.7152 * values[1]
            + 0.0722 * values[2]
        )

    l1, l2 = luminance(rgb1), luminance(rgb2)
    lighter, darker = max(l1, l2), min(l1, l2)

    return (lighter + 0.05) / (darker + 0.05)


def harmony_colors(r, g, b):
    """Generate complementary and analogous color combinations."""
    h, s, v = colorsys.rgb_to_hsv(
        r / 255, g / 255, b / 255
    )

    combinations = {
        "Complementary": [h + 0.5],
        "Analogous": [h - 1 / 12, h + 1 / 12],
        "Triadic": [h + 1 / 3, h + 2 / 3],
        "Split Complementary": [h + 5 / 12, h + 7 / 12],
        "Tetradic": [
            h + 0.25,
            h + 0.5,
            h + 0.75,
        ],
    }

    result = {}

    for name, hues in combinations.items():
        result[name] = []

        for hue in hues:
            rr, gg, bb = colorsys.hsv_to_rgb(
                hue % 1, s, v
            )

            result[name].append(
                (
                    round(rr * 255),
                    round(gg * 255),
                    round(bb * 255),
                )
            )

    return result


# --------------------------------------------------
# PRESET COLORS
# --------------------------------------------------
PRESETS = {
    "Custom": "#6C63FF",
    "Pure Red": "#FF0000",
    "Pure Green": "#00FF00",
    "Pure Blue": "#0000FF",
    "Purple": "#8B5CF6",
    "Sunset Orange": "#FF6B35",
    "Ocean Blue": "#0077B6",
    "Mint Green": "#06D6A0",
    "Golden Yellow": "#FFD166",
    "Rose Pink": "#FF4D8D",
    "Dark Mode": "#1E1E2F",
    "White": "#FFFFFF",
    "Black": "#000000",
}


def load_preset():
    preset = st.session_state.get("preset", "Custom")
    hex_color = PRESETS[preset]
    r, g, b = hex_to_rgb(hex_color)

    st.session_state.red = r
    st.session_state.green = g
    st.session_state.blue = b


# Initialize widget state before rendering widgets.
if "red" not in st.session_state:
    st.session_state.red = 108
if "green" not in st.session_state:
    st.session_state.green = 99
if "blue" not in st.session_state:
    st.session_state.blue = 255


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🎨 RGB Color Studio</h1>
        <p>
            Mix Red, Green and Blue. Discover beautiful colors,
            explore harmonies, and export your perfect palette.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "An interactive playground for designers, developers, "
    "artists and color enthusiasts."
)


# --------------------------------------------------
# SIDEBAR: COLOR CONTROLS
# --------------------------------------------------
with st.sidebar:
    st.header("🎛️ Color Mixer")
    st.write("Adjust the RGB channels from 0 to 255.")

    st.selectbox(
        "Choose a preset",
        options=list(PRESETS.keys()),
        key="preset",
        on_change=load_preset,
    )

    st.slider(
        "🔴 Red",
        min_value=0,
        max_value=255,
        key="red",
    )

    st.slider(
        "🟢 Green",
        min_value=0,
        max_value=255,
        key="green",
    )

    st.slider(
        "🔵 Blue",
        min_value=0,
        max_value=255,
        key="blue",
    )

    st.divider()

    st.caption("Tip: Combine all three channels to create millions of colors.")

    if st.button("Reset to default", use_container_width=True):
        st.session_state.red = 108
        st.session_state.green = 99
        st.session_state.blue = 255
        st.session_state.preset = "Custom"
        st.rerun()


# --------------------------------------------------
# CURRENT COLOR
# --------------------------------------------------
r = st.session_state.red
g = st.session_state.green
b = st.session_state.blue

hex_color = rgb_to_hex(r, g, b)
rgb_color = f"rgb({r}, {g}, {b})"
text_color = text_color_for_background(r, g, b)

white_contrast = contrast_ratio((r, g, b), (255, 255, 255))
black_contrast = contrast_ratio((r, g, b), (0, 0, 0))


# --------------------------------------------------
# LIVE PREVIEW AND COLOR VALUES
# --------------------------------------------------
st.subheader("Your live color")

preview_col, info_col = st.columns([1.35, 1], gap="large")

with preview_col:
    st.markdown(
        f"""
        <div class="color-preview"
             style="background-color:{hex_color}; color:{text_color};">
            <h2>{hex_color}</h2>
            <p>{rgb_color}</p>
            <p>Live color preview</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with info_col:
    st.markdown("#### Color information")

    st.metric("HEX", hex_color)
    st.metric("RGB", f"{r}, {g}, {b}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Red", r)
    c2.metric("Green", g)
    c3.metric("Blue", b)

    st.markdown("**Channel proportions**")

    st.progress(r / 255, text=f"Red: {r}/255")
    st.progress(g / 255, text=f"Green: {g}/255")
    st.progress(b / 255, text=f"Blue: {b}/255")


# --------------------------------------------------
# CONTRAST CHECKER
# --------------------------------------------------
st.divider()
st.subheader("♿ Text contrast checker")

contrast_col1, contrast_col2 = st.columns(2)

with contrast_col1:
    st.markdown(
        f"""
        <div style="background:{hex_color}; color:#FFFFFF;
                    padding:22px; border-radius:12px;">
            <strong>White text</strong>
            <p>The quick brown fox jumps over the lazy dog.</p>
            <small>Contrast ratio: {white_contrast:.2f}:1</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

with contrast_col2:
    st.markdown(
        f"""
        <div style="background:{hex_color}; color:#000000;
                    padding:22px; border-radius:12px;">
            <strong>Black text</strong>
            <p>The quick brown fox jumps over the lazy dog.</p>
            <small>Contrast ratio: {black_contrast:.2f}:1</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "WCAG guidance: 4.5:1 for normal text and 3:1 for large text. "
    "The ratios above help you compare white and black text."
)


# --------------------------------------------------
# COLOR HARMONIES
# --------------------------------------------------
st.divider()
st.subheader("🌈 Explore color combinations")

st.write(
    "Color harmonies create coordinated colors from your current selection."
)

harmonies = harmony_colors(r, g, b)

selected_harmony = st.selectbox(
    "Select a color harmony",
    options=list(harmonies.keys()),
)

palette = [(r, g, b)] + harmonies[selected_harmony]

st.markdown("**Palette preview**")

palette_columns = st.columns(len(palette))

for index, (pr, pg, pb) in enumerate(palette):
    palette_hex = rgb_to_hex(pr, pg, pb)

    with palette_columns[index]:
        st.markdown(
            f"""
            <div class="swatch"
                 style="background-color:{palette_hex};"></div>
            """,
            unsafe_allow_html=True,
        )

        st.code(palette_hex, language=None)
        st.caption(f"RGB {pr}, {pg}, {pb}")


# --------------------------------------------------
# PRESET GALLERY
# --------------------------------------------------
st.divider()
st.subheader("✨ Color inspiration gallery")

gallery_names = [
    name for name in PRESETS if name != "Custom"
]

gallery_columns = st.columns(4)

for index, name in enumerate(gallery_names):
    gallery_hex = PRESETS[name]

    with gallery_columns[index % 4]:
        st.markdown(
            f"""
            <div style="background:{gallery_hex}; height:75px;
                        border-radius:10px; margin-bottom:6px;
                        border:1px solid rgba(128,128,128,0.2);">
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"**{name}**")
        st.code(gallery_hex, language=None)

        if st.button(
            f"Use {name}",
            key=f"gallery_{name}",
            use_container_width=True,
        ):
            rr, gg, bb = hex_to_rgb(gallery_hex)
            st.session_state.red = rr
            st.session_state.green = gg
            st.session_state.blue = bb
            st.session_state.preset = name
            st.rerun()


# --------------------------------------------------
# EXPORT COLOR DATA
# --------------------------------------------------
st.divider()
st.subheader("📥 Export your color")

color_data = {
    "name": "My RGB Color",
    "hex": hex_color,
    "rgb": {
        "red": r,
        "green": g,
        "blue": b,
    },
    "css_rgb": rgb_color,
    "text_color": text_color,
    "harmony": selected_harmony,
    "palette": [
        {
            "hex": rgb_to_hex(pr, pg, pb),
            "rgb": {"red": pr, "green": pg, "blue": pb},
        }
        for pr, pg, pb in palette
    ],
}

css_content = f"""/* Generated by RGB Color Studio */

:root {{
    --primary-color: {hex_color};
    --primary-rgb: {r}, {g}, {b};
    --text-color: {text_color};
}}

.primary-background {{
    background-color: var(--primary-color);
    color: var(--text-color);
}}
"""

json_content = json.dumps(color_data, indent=2)

export_col1, export_col2 = st.columns(2)

with export_col1:
    st.download_button(
        "⬇️ Download CSS",
        data=css_content,
        file_name="my-color.css",
        mime="text/css",
        use_container_width=True,
    )

with export_col2:
    st.download_button(
        "⬇️ Download JSON",
        data=json_content,
        file_name="my-color.json",
        mime="application/json",
        use_container_width=True,
    )

st.code(css_content, language="css")

st.caption(
    "RGB Color Studio · Built with Python and Streamlit"
)
