from prosody import process_gujarati_text
from typing import Dict, List, Any

def visualize_results(results: Dict[str, Any], test_case_num: int):
    """Visualize the processing results"""
    print(f"\n=== Test Case {test_case_num} ===")
    print(f"Original Text: {results['original_text']}")
    print(f"Normalized Text: {results['normalized_text']}")
    print(f"Sentence Type: {results['prosody']['sentence_type']}")
    
    print("\nGrapheme-to-Phoneme Mapping:")
    print("Graphemes:", " ".join(results['graphemes']))
    print("Phonemes: ", " ".join(results['phonemes']))
    
    print("\nDetailed Prosodic Analysis:")
    print("Idx | Grapheme | Phoneme    | Type            | Position    | Stress | Duration | Pitch")
    print("-" * 80)
    
    prosody_index = 0
    for i, (grapheme, phoneme, detail) in enumerate(zip(
        results['graphemes'],
        results['phonemes'],
        results['phoneme_details']
    )):
        if detail['type'] == 'punctuation':
            print(f"{i:3} | {grapheme:8} | {phoneme:10} | {detail['type']:15} | {'N/A':11} | {'N/A':6} | {'N/A':8} | {'N/A':5}")
        else:
            prosody = results['prosody']['phonemes'][prosody_index]
            print(f"{i:3} | {grapheme:8} | {phoneme:10} | {detail['type']:15} | {prosody['position']:11} | {prosody['stress']:6.2f} | {prosody['duration']:8.2f} | {prosody['pitch']:5.2f}")
            prosody_index += 1
    
    rhythm = results['prosody']['rhythm']
    print("\nRhythm Metrics:")
    print(f"Average Duration: {rhythm['avg_duration']:.2f}")
    print(f"Duration Variance: {rhythm['duration_variance']:.2f}")
    print(f"Average Pitch: {rhythm['avg_pitch']:.2f}")
    print(f"Pitch Range: {rhythm['pitch_range']:.2f}")
    print(f"Speech Rate: {rhythm['speech_rate']:.2f} phonemes/sec")
    print("="*60)

def run_test_cases():
    """Run multiple test cases through the pipeline"""
    test_cases = [
        {
            "text": "હેલો, તમે કેમ છો?",
            "type": "question"
        },
        {
            "text": "મને ગુજરાતી ભાષા ગમે છે!",
            "type": "exclamation"
        },
        {
            "text": "આજે હવામાન સારું છે.",
            "type": "statement"
        },
        {
            "text": "તમારું નામ શું છે?",
            "type": "question"
        },
        {
            "text": "ચાલો ફરવા જઈએ!",
            "type": "exclamation"
        },
        {
            "text": "કમલ",
            "type": "statement"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        results = process_gujarati_text(test_case["text"], test_case["type"])
        visualize_results(results, i)

if __name__ == "__main__":
    print("=== Gujarati Text Processing with Prosody Analysis ===")
    print("Running multiple test cases...\n")
    run_test_cases()
