# LGP-Sentence-Composition
A MediaPipe project that allows anyone to write a sentence using gestual language from the LGP (Linguagem Gestual Portuguesa) easily. Custom gestures can be made without knowledge of MediaPipe or Python, just by using a simple UI.

## ⚡️ Quick start
Run via local Python:
```bash
cd src
pip install -r requirements.txt
python3 main.py
```

Run via docker:
```bash
docker compose build
```

## 🤔 Usage
Open the app.
```bash
python3 main.py
```

How to create a new gesture:
```bash
Inside the UI, press the "C" button to create a new gesture using our Gesture Creator UI.
```

If you want to create a new gesture using code, head to ``src/gestures/``, create a new gesture inside letters, numbers, saudations or verbs and add it to the dictionary on ``lgp_recognition.py``.

Run via docker:
```bash
docker compose build
```

## 📖 Additional information
This project was done in a university course, so it is not production ready. It is a proof of concept that MediaPipe can be used to create a gestual language detection and sentence building app. If you wish to research this matter, feel free to contact us to collaborate or ask any questions.

## 👥 Initial contributors
- João Ferreira [@Xurape](https://github.com/xurape)
- Hugo Guimarães [@Guimaraes04](https://github.com/Guimaraes04)