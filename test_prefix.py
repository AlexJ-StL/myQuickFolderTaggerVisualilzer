import os

paths = [
    r"C:\Users\AlexJ\Documents\Coding\Repos\my-repos\ProjectA",
    r"C:\Users\AlexJ\Documents\Coding\Repos\work-repos\ProjectB",
    r"C:\Users\AlexJ\Documents\Coding\.archived-repos\old-repos\ProjectC"
]

split_paths = [p.replace("/", os.sep).replace("\\", os.sep).split(os.sep) for p in paths]
common_parts = []
min_len = min(len(p) for p in split_paths)
for i in range(min_len):
    if all(p[i] == split_paths[0][i] for p in split_paths):
        common_parts.append(split_paths[0][i])
    else:
        break

print(f"Common parts: {common_parts}")

if len(common_parts) > 0:
    min_remaining = min(len(p) - len(common_parts) for p in split_paths)
    print(f"Min remaining before pop: {min_remaining}")
    if min_remaining <= 1 and len(common_parts) > 1:
        common_parts.pop()

print(f"Final Common parts: {common_parts}")

for p in paths:
    parts = p.replace("/", os.sep).replace("\\", os.sep).split(os.sep)
    idx = len(common_parts)
    clean = os.sep.join(parts[idx:])
    root = parts[idx] if idx < len(parts) else "Unknown"
    print(f"Path: {p}\n  Clean: {clean}\n  Root: {root}\n")

# Single root case
print("--- Single Root Case ---")
paths2 = [
    r"C:\Projects\my-repos\ProjectA",
    r"C:\Projects\my-repos\ProjectB"
]
split_paths2 = [p.replace("/", os.sep).replace("\\", os.sep).split(os.sep) for p in paths2]
common_parts2 = []
min_len2 = min(len(p) for p in split_paths2)
for i in range(min_len2):
    if all(p[i] == split_paths2[0][i] for p in split_paths2):
        common_parts2.append(split_paths2[0][i])
    else:
        break

if len(common_parts2) > 0:
    min_remaining2 = min(len(p) - len(common_parts2) for p in split_paths2)
    print(f"Min remaining before pop: {min_remaining2}")
    if min_remaining2 <= 1 and len(common_parts2) > 1:
        common_parts2.pop()

for p in paths2:
    parts = p.replace("/", os.sep).replace("\\", os.sep).split(os.sep)
    idx = len(common_parts2)
    clean = os.sep.join(parts[idx:])
    root = parts[idx] if idx < len(parts) else "Unknown"
    print(f"Path: {p}\n  Clean: {clean}\n  Root: {root}\n")
