from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

save_dir = PROJECT_ROOT / "data" 

def save_translation(mt_provider: str, lines: list[str]) -> str:

    curdate = datetime.now().strftime("%y_%m_%d_%H_%M") 
    filepath = save_dir / f"{mt_provider}_{curdate}.txt" 
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    
    return f"Translation file saved to {filepath}"