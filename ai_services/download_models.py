from huggingface_hub import snapshot_download

# Descargar XTTS para clonación de voz
snapshot_download(
    repo_id="coqui/XTTS-v2",
    local_dir="./models/xtts",
    ignore_patterns=["*.gitattributes", "*.md"]
)

# Descargar DistilBERT para procesamiento de texto
snapshot_download(
    repo_id="distilbert-base-uncased",
    local_dir="./models/distilbert"
)