from agents.research_agent import execute as research_show
from agents.similarity_agent import execute as similarity_agent
from agents.song_agent import execute as song_agent
from agents.venue_agent import execute as venue_agent


def print_section(title):

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)
    print()


def main():

    show_date = "1977/05/08"

    print_section("DeadBase Capstone Demo")
    print("Question: Was Cornell 1977 actually unique?")

    print_section("1. Multi-Agent Historical Investigation")

    research = research_show(show_date)

    print(research["answer"])

    print_section("2. Similarity Agent")

    similarity = similarity_agent(show_date, top_n=5)

    for item in similarity["recommendations"]:
        print(
            f"{item['show_date']} | {item['venue']} | "
            f"similarity={item['similarity']} | "
            f"shared_songs={item['shared_song_count']}"
        )

    print_section("3. Venue Agent")

    venue = venue_agent("Barton Hall")

    print(venue["answer"])
    print(
        f"Shows: {venue['show_count']}\n"
        f"First Show: {venue['first_show']}\n"
        f"Last Show: {venue['last_show']}\n"
        f"Average Show Length: {venue['avg_show_length']}\n"
        f"Average Segue Ratio: {venue['avg_segue_ratio']}"
    )

    print_section("4. Song Agents")

    songs = [
        "Scarlet Begonias",
        "Fire On The Mountain",
        "Morning Dew",
        "Saint Stephen",
    ]

    for song in songs:
        result = song_agent(song)

        print(
            f"{result['song']}: "
            f"{result['performance_count']} performances | "
            f"first={result['first_performance']['date']} | "
            f"last={result['last_performance']['date']}"
        )

    print_section("5. Demo Conclusion")

    print(
        "DeadBase separates cultural reputation from measurable archive signals. "
        "Cornell 1977 is culturally legendary, but the current archive model ranks "
        "it as notable rather than extreme by setlist structure, song rarity, "
        "venue weight, and nearest-neighbor similarity. That tension is exactly "
        "why a multi-agent historical research system is useful."
    )


if __name__ == "__main__":
    main()