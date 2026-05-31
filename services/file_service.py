from datetime import datetime

def save_translation(mt_provider: str, lines: list[str]) -> str:

    curdate = datetime.now().strftime("%y_%m_%d_%H_%M") 
    filepath = f"./data/{mt_provider}_{curdate}.txt" 
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    
    return f"Translation file saved to {filepath}"