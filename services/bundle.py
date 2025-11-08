#!/usr/bin/env python3
import os

output_file = "bundle.txt"

with open(output_file, "w", encoding="utf-8") as out:
    for root, _, files in os.walk("."):
        for file in files:
            # Skip the output file itself to avoid recursion
            if file == output_file:
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"[Could not read file: {e}]"

            rel_path = os.path.relpath(file_path, ".")
            out.write(f"\n# ===== {rel_path} =====\n")
            out.write(content)
            out.write("\n# ===== END OF FILE =====\n")

print(f"All files bundled into {output_file}")
