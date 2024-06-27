import hashlib
import os
import json


def malhasher_hash(byte_array):
    """Generate a hash of the byte array using MALHasher algorithm."""
    return hashlib.sha256(byte_array).hexdigest()


def context_aware_hash(file_path):
    """Generate a context-aware hash for a file."""
    with open(file_path, 'rb') as f:
        file_content = f.read()

    file_hash = malhasher_hash(file_content)

    # Extract contextual features
    file_stats = os.stat(file_path)
    context = {
        "file_path": file_path,
        "file_size": file_stats.st_size,
        "creation_time": file_stats.st_ctime,
        "modification_time": file_stats.st_mtime,
        "permissions": file_stats.st_mode,
    }
    context_str = json.dumps(context, sort_keys=True)
    context_hash = hashlib.sha256(context_str.encode()).hexdigest()

    # Combine the file hash and context hash
    combined_hash = hashlib.sha256((file_hash + context_hash).encode()).hexdigest()

    return combined_hash
