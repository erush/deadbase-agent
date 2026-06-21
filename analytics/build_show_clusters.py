from pathlib import Path

import duckdb
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


DB_PATH = (
    Path(__file__)
    .parent.parent
    / "data"
    / "duckdb"
    / "deadbase.duckdb"
)


N_CLUSTERS = 10


def main():

    con = duckdb.connect(str(DB_PATH))

    df = con.execute(
        """
        select
            se.show_uuid,
            se.show_date,
            se.era,
            se.show_length,
            se.set_count,
            se.segue_ratio,
            se.historian_score
        from show_embeddings se
        """
    ).df()

    features = df[
        [
            "show_length",
            "set_count",
            "segue_ratio",
            "historian_score",
        ]
    ]

    scaler = StandardScaler()

    X = scaler.fit_transform(features)

    model = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=42,
        n_init=20,
    )

    df["cluster_id"] = model.fit_predict(X)

    show_clusters = df[
        [
            "show_uuid",
            "show_date",
            "era",
            "cluster_id",
        ]
    ].copy()

    cluster_profiles = (
        df.groupby("cluster_id")
        .agg(
            cluster_size=(
                "show_uuid",
                "count"
            ),
            avg_show_length=(
                "show_length",
                "mean"
            ),
            avg_set_count=(
                "set_count",
                "mean"
            ),
            avg_segue_ratio=(
                "segue_ratio",
                "mean"
            ),
            avg_historian_score=(
                "historian_score",
                "mean"
            ),
        )
        .reset_index()
    )

    dominant_eras = []

    for cluster_id, group in df.groupby(
        "cluster_id"
    ):

        dominant_era = (
            group["era"]
            .value_counts()
            .idxmax()
        )

        dominant_eras.append(
            {
                "cluster_id": cluster_id,
                "dominant_era": dominant_era,
            }
        )

    dominant_eras = pd.DataFrame(
        dominant_eras
    )

    cluster_profiles = (
        cluster_profiles.merge(
            dominant_eras,
            on="cluster_id",
            how="left"
        )
    )

    cluster_profiles[
        "avg_show_length"
    ] = (
        cluster_profiles[
            "avg_show_length"
        ].round(2)
    )

    cluster_profiles[
        "avg_set_count"
    ] = (
        cluster_profiles[
            "avg_set_count"
        ].round(2)
    )

    cluster_profiles[
        "avg_segue_ratio"
    ] = (
        cluster_profiles[
            "avg_segue_ratio"
        ].round(3)
    )

    cluster_profiles[
        "avg_historian_score"
    ] = (
        cluster_profiles[
            "avg_historian_score"
        ].round(4)
    )

    con.register(
        "show_clusters_df",
        show_clusters
    )

    con.register(
        "cluster_profiles_df",
        cluster_profiles
    )

    con.execute(
        """
        create or replace table show_clusters as
        select *
        from show_clusters_df
        """
    )

    con.execute(
        """
        create or replace table cluster_profiles as
        select *
        from cluster_profiles_df
        """
    )

    print()
    print(
        f"show_clusters={len(show_clusters)}"
    )
    print()

    print(
        con.execute(
            """
            select *
            from cluster_profiles
            order by cluster_id
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()