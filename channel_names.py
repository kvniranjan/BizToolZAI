import random
adjectives = ["Echoes", "Shadows", "Whispers", "Chronicles", "Archives", "Enigmas", "Relics", "Secrets"]
nouns = ["History", "Time", "Past", "Unknown", "Abyss", "Void", "Ages", "Dust"]
for i in range(5):
    print(f"Option {i+1}: {random.choice(adjectives)} of the {random.choice(nouns)}")
print("\nOr the single-word punchy ones:")
print("- The Anomaly")
print("- Obscured")
print("- Unearthed")
