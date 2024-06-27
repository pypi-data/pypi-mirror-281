from .entropy import calculate_enhanced_entropy
from .context_hashing import context_aware_hash
from .fuzzy_hashing import generate_fuzzy_hash
from .anomaly_detection import detect_anomalies
from .indexing import create_index
from .obfuscation_detection import create_code_graph, detect_obfuscation


def adaptive_analysis(file_path, model, known_malware_hashes):
    """Perform real-time adaptive analysis on a file."""
    # Step 1: Initial Analysis
    entropy_results = calculate_enhanced_entropy(file_path)
    context_hash = context_aware_hash(file_path)

    with open(file_path, 'rb') as f:
        file_content = f.read()

    # Extract file metadata for anomaly detection
    file_metadata = [entropy_results["global_entropy"], context_hash]

    # Step 2: Intermediate Analysis
    if entropy_results["global_entropy"] > 7.0:
        # Apply more intensive analysis
        fuzzy_hash = generate_fuzzy_hash(model, file_content)
        anomaly_score = detect_anomalies(model, file_metadata)

    if context_hash in known_malware_hashes:
        # Flag as potential malware
        return True

    # Step 3: Adaptive Techniques
    if anomaly_score > 0.5:
        # Apply additional analysis techniques
        index = create_index(model, file_metadata)
        code_graph = create_code_graph(file_content)
        is_obfuscated = detect_obfuscation(code_graph)
        if is_obfuscated:
            return True

    return False
