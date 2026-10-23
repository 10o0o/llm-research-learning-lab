from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[3]

INPUT_PATH = LAB_ROOT / "materials/private/ax-inquiries/inquiries.json"
DOCUMENTS_PATH = LAB_ROOT / "materials/private/ax-policies/documents.json"
RUNS_PATH = LAB_ROOT / "tmp/ax-inquiry-runs.jsonl"
DEV_QUERIES_PATH = LAB_ROOT / "materials/private/ax-retrieval-eval/dev_queries.json"
ACCOUNT_STATUS_PATH = LAB_ROOT / "materials/private/ax-account-state/accounts.json"

MODEL_NAME = "qwen3:4b-instruct-2507-q4_K_M"
