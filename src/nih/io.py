# load projects/abstracts, join, save parquet
from __future__ import annotations
from pathlib import Path
import re
import pandas as pd

from nih.paths import PROJECTS_ZIPS_DIR, ABSTRACTS_ZIPS_DIR

FY_RE = re.compile(r'FY(\d{4})', re.IGNORECASE)

def _fy_from_name(path: Path) -> int | None:
  m = FY_RE.search(path.name)
  return int(m.group(1)) if m else None

def list_zips_by_fy(zip_dir: Path) -> dict[int, Path]:
  """Return mapping FY -> zip path for all ZIPs in a directory."""
  out: dict[int, Path] = {}
  for p in sorted(zip_dir.glob('*.zip')):
    fy = _fy_from_name(p)
    if fy is not None:
      out[fy] = p
  return out

def read_exporter_zip(zip_path: Path) -> pd.DataFrame:
  """Read the single CSV inside an ExPORTER ZIP directly (no unzip)."""
  try: 
    df = pd.read_csv(zip_path, compression='zip', low_memory=False, encoding='utf-8')
    df.attrs['encoding_used'] = 'utf-8'
    return df
  except UnicodeDecodeError:
    df = pd.read_csv(zip_path, compression='zip', low_memory=False, encoding='cp1252', encoding_errors='replace')
    df.attrs['encoding_used'] = 'cp1252+replace'
    return df

def load_projects_fy(fy: int) -> pd.DataFrame:
  zips = list_zips_by_fy(PROJECTS_ZIPS_DIR)
  if fy not in zips:
    raise FileNotFoundError(f'No Projects ZIP found for FY{fy} in {PROJECTS_ZIPS_DIR}')
  return read_exporter_zip(zips[fy])

def load_abstracts_fy(fy: int) -> pd.DataFrame:
  zips = list_zips_by_fy(ABSTRACTS_ZIPS_DIR)
  if fy not in zips:
    raise FileNotFoundError(f'No Abstracts ZIP found for FY{fy} in {ABSTRACTS_ZIPS_DIR}')
  return read_exporter_zip(zips[fy])

def join_projects_abstracts_fy(fy: int) -> pd.DataFrame:
  """
  Load Projects + Abstracts for a fiscal year and left-join abstracts onto projects.
  Assumes join key is APPLICATION_ID and abstracts column is ABSTRACT_TEXT.
  """
  df_p = load_projects_fy(fy)
  df_a = load_abstracts_fy(fy)
  
  needed = {'APPLICATION_ID'}
  if not needed.issubset(df_p.columns):
    raise KeyError(f'Projects FY{fy} missing columns: {needed - set(df_p.columns)}')
  if not needed.issubset(df_a.columns):
    raise KeyError(f'Abstracts FY{fy} missing columns: {needed - set(df_a.columns)}')
  if 'ABSTRACT_TEXT' not in df_a.columns:
    raise KeyError(f'Abstracts FY{fy} missing ABSTRACT_TEXT. Columns: {list(df_a.columns)}')
  
  df = df_p.merge(df_a[['APPLICATION_ID', 'ABSTRACT_TEXT']], on='APPLICATION_ID', how='left')
  df['FY'] = pd.to_numeric(df['FY'], errors='coerce').astype('Int64')

  return df