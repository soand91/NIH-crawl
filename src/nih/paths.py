# reads .env, returns Path objects
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()

# Required environment variable
DATA_ROOT = os.getenv('DATA_ROOT')
if DATA_ROOT is None:
  raise RuntimeError(
    'DATA_ROOT is not set.'
    'Create a .env file or export DATA_ROOT.'
  )

DATA_ROOT = Path(DATA_ROOT)

# Core directories
RAW_DIR       = DATA_ROOT / 'raw'
INTERIM_DIR   = DATA_ROOT / 'interim'
PROCESSED_DIR = DATA_ROOT / 'processed'
EXTERNAL_DIR  = DATA_ROOT / 'external'

# Subdirectories
EXPORTER_ZIPS_DIR   = RAW_DIR / 'exporter_zips'
PROJECTS_ZIPS_DIR   = EXPORTER_ZIPS_DIR / 'projects'
ABSTRACTS_ZIPS_DIR  = EXPORTER_ZIPS_DIR / 'abstracts'

CORPUS_DIR      = PROCESSED_DIR / 'corpus'
EMBEDDINGS_DIR  = PROCESSED_DIR / 'embeddings'

def ensure_dirs():
  """Create expected directories if they don't exist."""
  for d in [
    RAW_DIR, INTERIM_DIR, PROCESSED_DIR, EXTERNAL_DIR, 
    EXPORTER_ZIPS_DIR, PROJECTS_ZIPS_DIR, ABSTRACTS_ZIPS_DIR, 
    CORPUS_DIR, EMBEDDINGS_DIR
  ]:
    d.mkdir(parents=True, exist_ok=True)