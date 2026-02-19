Large NIH data lives in NIH_DATA_ROOT (see .env).

raw/       - original ZIP downloads from NIH ExPORTER (immutable)
interim/   - temporary extracted and joined files (safe to delete)
processed/ - cleaned corpus, embeddings, and model outputs
external/  - reference metadata and dictionaries