# agents/research_agent.py

from pathlib import Path

import duckdb

from agents.similarity_agent import SimilarityAgent
from agents.song_agent import SongAgent
from agents.venue_agent import VenueAgent
from agents.synthesis_agent import execute as synthesize


DB_PATH = (
    Path(__file__)
    .parent.parent
    / "data"
    / "duckdb"
    / "deadbase.duckdb"
)


class ResearchAgent:

    def __init__(self):

        self.con = duckdb.connect(str(DB_PATH))

        self.song_agent = SongAgent()

        self.venue_agent = VenueAgent()

        self.similarity_agent = SimilarityAgent()

    def investigate_show(
        self,
        show_date: str
    ):

        show = self.con.execute(
            f"""
            select
                s.show_uuid,
                s.show_date,
                s.venue,
                s.city,
                s.state,
                h.historian_score,
                h.historian_rank,
                h.historian_percentile,
                a.primary_archetype,
                a.secondary_archetype
            from shows s

            join show_historical_significance h
                on s.show_uuid = h.show_uuid

            left join show_archetypes a
                on s.show_uuid = a.show_uuid

            where s.show_date = '{show_date}'
            """
        ).df()

        if len(show) == 0:

            return {
                "found": False,
                "answer": (
                    f"No show found for "
                    f"{show_date}."
                )
            }

        show = show.iloc[0]

        songs = self.con.execute(
            f"""
            select
                song_name
            from performances p

            join shows s
                on p.show_uuid = s.show_uuid

            where s.show_date = '{show_date}'

            order by
                set_number,
                song_position
            """
        ).df()

        song_names = (
            songs["song_name"]
            .drop_duplicates()
            .tolist()
        )

        top_song_context = []

        for song in song_names[-5:]:

            result = (
                self.song_agent
                .analyze(song)
            )

            if result["found"]:

                top_song_context.append(
                    {
                        "song": song,
                        "performances":
                            result[
                                "performance_count"
                            ]
                    }
                )

        venue_context = (
            self.venue_agent.analyze(
                show["venue"]
            )
        )

        neighbors = (
            self.similarity_agent.analyze(
                show_date,
                top_n=5
            )
        )

        synthesis = synthesize(
            {
                "show_date":
                    show_date,

                "historian_rank":
                    int(
                        show[
                            "historian_rank"
                        ]
                    ),

                "historian_percentile":
                    float(
                        show[
                            "historian_percentile"
                        ]
                    ),

                "primary_archetype":
                    show[
                        "primary_archetype"
                    ],

                "secondary_archetype":
                    show[
                        "secondary_archetype"
                    ],
            }
        )

        report = f"""
Historical Investigation: {show_date}
========================================

Location
--------
{show["venue"]} ({show["city"]}, {show["state"]})

Historical Profile
------------------
Historian Rank:
{int(show["historian_rank"])} of 1822

Percentile:
{round(show["historian_percentile"], 2)}

Historian Score:
{round(show["historian_score"], 4)}

Archetypes
----------
Primary:
{show["primary_archetype"]}

Secondary:
{show["secondary_archetype"]}

Venue Context
-------------
{venue_context["answer"]}

Nearest Neighbor Shows
----------------------
"""

        for rec in neighbors["recommendations"]:

            report += (
                f"- "
                f"{rec['show_date']} "
                f"({rec['venue']}) "
                f"| similarity "
                f"{rec['similarity']}\n"
            )

        report += """

Song Context
------------
"""

        for song in top_song_context:

            report += (
                f"- "
                f"{song['song']} "
                f"({song['performances']} "
                f"performances)\n"
            )

        report += """

Interpretation
--------------
This show's historical standing is
derived from venue profile,
repertoire,
archetype classification,
historian ranking,
and nearest-neighbor relationships
across the archive.

Synthesis
---------
"""

        report += synthesis["answer"]

        return {
            "agent":
                "research-agent",

            "show_date":
                show_date,

            "historian_rank":
                int(
                    show[
                        "historian_rank"
                    ]
                ),

            "historian_percentile":
                float(
                    show[
                        "historian_percentile"
                    ]
                ),

            "historian_score":
                float(
                    show[
                        "historian_score"
                    ]
                ),

            "primary_archetype":
                show[
                    "primary_archetype"
                ],

            "secondary_archetype":
                show[
                    "secondary_archetype"
                ],

            "synthesis":
                synthesis,

            "answer":
                report
        }


agent = ResearchAgent()


def execute(
    show_date: str
):

    return (
        agent
        .investigate_show(
            show_date
        )
    )