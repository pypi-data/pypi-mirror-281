import math
from collections import Counter


def calculate_entropy(byte_array):
    """Calculate the entropy of a byte array."""
    file_size = len(byte_array)
    if file_size == 0:
        return 0.0

    freq_list = Counter(byte_array)

    entropy = 0.0
    for freq in freq_list.values():
        p = freq / file_size
        entropy -= p * math.log2(p)

    return entropy


def calculate_enhanced_entropy(file_path, section_size=4096, window_size=2048):
    """Calculate global, section-wise, and sliding window entropy for a file."""
    with open(file_path, 'rb') as f:
        file_content = f.read()

    global_entropy = calculate_entropy(file_content)

    section_entropies = []
    for i in range(0, len(file_content), section_size):
        section = file_content[i:i + section_size]
        section_entropy = calculate_entropy(section)
        section_entropies.append(section_entropy)

    sliding_window_entropies = []
    for i in range(0, len(file_content) - window_size + 1, window_size):
        window = file_content[i:i + window_size]
        window_entropy = calculate_entropy(window)
        sliding_window_entropies.append(window_entropy)

    return {
        "global_entropy": global_entropy,
        "section_entropies": section_entropies,
        "sliding_window_entropies": sliding_window_entropies
    }
