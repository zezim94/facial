
# Sistema de Login com Reconhecimento Facial + Agenda de Avisos

Este sistema foi desenvolvido com Flask e reconhecimento facial (OpenCV), utilizando PostgreSQL como banco de dados e pronto para deploy no [Render](https://render.com).

## Funcionalidades

- Captura de rostos (`capture_faces.py`)
- Treinamento do modelo (`train_model.py`)
- Login por reconhecimento facial (`face_login.py`)
- Agenda dinâmica para adicionar avisos (Flask)
- Banco de dados PostgreSQL
- Pronto para deploy com `gunicorn` + `Procfile`

## Requisitos

- Python 3.8+
- PostgreSQL
- `haarcascade_frontalface_default.xml` (já incluso)
- Biblioteca OpenCV (`opencv-python`)

## Deploy no Render

Configure as variáveis de ambiente no Render conforme o `.render.yaml`.

---
Desenvolvido com ❤️
