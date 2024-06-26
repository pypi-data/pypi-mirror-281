from .disassembly import hybrid_disassembly_decompilation
from .code_flow_analysis import generate_control_flow_graph, capture_dynamic_execution_trace, \
    combine_static_dynamic_analysis
from .string_resource_extraction import extract_strings, analyze_string_context, extract_resources, \
    analyze_resource_context
from .obfuscation_removal import identify_obfuscation_patterns, remove_obfuscation, verify_deobfuscation
from .model import SimpleObfuscationModel  # Import the model here
import torch
import os

# Ensure the models directory is correctly referenced
model_dir = os.path.join(os.path.dirname(__file__), 'models')
obfuscation_model_path = os.path.join(model_dir, 'obfuscation_model.pth')

# Load the AI model for obfuscation detection when the module is loaded
if os.path.exists(obfuscation_model_path):
    obfuscation_model = SimpleObfuscationModel()
    obfuscation_model.load_state_dict(torch.load(obfuscation_model_path))
    obfuscation_model.eval()
else:
    raise FileNotFoundError(f"Model file not found: {obfuscation_model_path}")


def reverse_engineering_analysis(file_path):
    """Perform comprehensive reverse engineering analysis on a file."""

    # Step 1: Hybrid Disassembly and Decompilation
    combined_output = hybrid_disassembly_decompilation(file_path)

    # Step 2: Behavioral Code Flow Analysis
    cfg = generate_control_flow_graph(combined_output["disassembly"])
    dynamic_trace = capture_dynamic_execution_trace(file_path)
    combined_analysis = combine_static_dynamic_analysis(cfg, dynamic_trace)

    # Step 3: Contextual String and Resource Extraction
    extracted_strings = extract_strings(file_path)
    string_context = analyze_string_context(extracted_strings, combined_output["disassembly"])
    extracted_resources = extract_resources(file_path)
    resource_context = analyze_resource_context(extracted_resources, combined_output["disassembly"])

    # Step 4: AI-Enhanced Obfuscation Removal
    obfuscation_patterns = identify_obfuscation_patterns(file_path, obfuscation_model)
    deobfuscated_code = remove_obfuscation(file_path, obfuscation_model)
    verification_result = verify_deobfuscation(deobfuscated_code)

    return {
        "combined_output": combined_output,
        "combined_analysis": combined_analysis,
        "string_context": string_context,
        "resource_context": resource_context,
        "obfuscation_patterns": obfuscation_patterns,
        "deobfuscated_code": deobfuscated_code,
        "verification_result": verification_result
    }
