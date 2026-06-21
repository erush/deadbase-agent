from agents.song_evolution_agent import execute


for song in [
    "Dark Star",
    "Scarlet Begonias",
    "Fire On The Mountain",
    "Saint Stephen"
]:

    result = execute(song)

    print()
    print("=" * 80)
    print(song)
    print("=" * 80)
    print()
    print(result["answer"])