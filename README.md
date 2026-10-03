# 🔊 Text to Voice

A simple text-to-speech web app built with **Streamlit** and **Google Text-to-Speech (gTTS)**. Type or upload text, convert it to natural-sounding speech in many languages (including Indian languages), then play it in the browser or download it as an MP3. No API key required.

## Features

- **14 languages:** English, Hindi, Telugu, Tamil, Bengali, Marathi, Kannada, Malayalam, Gujarati, Urdu, French, Spanish, German, Japanese
- **English accents:** Indian, American, British, Australian
- **Slow speech** option for clearer pronunciation
- **Type text or upload a `.txt` file**
- **Sample text** prefilled for English, Hindi and Telugu
- **Play in browser** and **download as MP3**
- Character counter, with a 5,000-character limit for typed text
- Custom styled UI (gradient theme, pill-style radios, rounded cards)

## Requirements

- Python 3.9+
- **Internet connection** (gTTS calls Google's text-to-speech service)

## Installation

```bash
# 1. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install streamlit gtts
```

Or save this as `requirements.txt`:

```
streamlit
gTTS
```

and run `pip install -r requirements.txt`.

## Usage

```bash
streamlit run tts_app.py
```

The app opens at `http://localhost:8501`.

1. Pick a **language** in the sidebar. For English, you can also choose an **accent**.
2. Optionally tick **Slow speech**.
3. Choose **Type text** or **Upload .txt**.
4. Click **🔊 Convert to speech**.
5. Play the audio, or click **⬇️ Download MP3**.

> Tip: write the text in the same language you select. For example, use Devanagari script for Hindi, otherwise the pronunciation will be wrong.

## Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | `en` | Gujarati | `gu` |
| Hindi | `hi` | Urdu | `ur` |
| Telugu | `te` | French | `fr` |
| Tamil | `ta` | Spanish | `es` |
| Bengali | `bn` | German | `de` |
| Marathi | `mr` | Japanese | `ja` |
| Kannada | `kn` | Malayalam | `ml` |

## Customization

- **Add languages:** add an entry to the `LANGUAGES` dictionary using any [gTTS language code](https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang).
- **Change sample text:** edit the `SAMPLES` dictionary.
- **Change the character limit:** adjust `max_chars` in `st.text_area`.
- **Styling:** edit the `CUSTOM_CSS` block near the top of the file (colors are CSS variables under `:root`).

## Limitations

- **Requires internet.** The app will show an error if it can't reach Google's service.
- **Accents only apply to English.** Other languages use a single default voice.
- **No voice selection.** gTTS provides one voice per language/accent.
- Very long text may be slow to process, and uploaded `.txt` files are not limited to 5,000 characters, so keep them reasonably short.
- gTTS is an unofficial wrapper around Google Translate's TTS, so heavy use may be rate-limited.

## Project Structure

```
.
├── tts_app.py      # Streamlit application
└── README.md
```

## Tech Stack

[Streamlit](https://streamlit.io) · [gTTS](https://gtts.readthedocs.io)
