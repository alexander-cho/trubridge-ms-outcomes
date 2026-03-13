import asyncio

import polars as pl

from analytics.setup import get_feature_table


async def get_correlations_async():
    table = await get_feature_table()
    df = pl.DataFrame(table).select(pl.col(pl.Float64))
    correlation = df.corr()
    return correlation


async def get_vulnerability_scores_async():
    table = await get_feature_table()
    df = pl.DataFrame(table)
    features = [
        "no_doctor_visit_routine_checkup_past_year",
        "food_insecurity_past_year",
        "uninsured",
        "no_internet_access",
        "below_poverty",
        "no_vehicle",
    ]

    df_scored = df.with_columns([
        ((pl.col(f) - pl.col(f).mean()) / pl.col(f).std()).alias(f"z_{f}")
        for f in features
    ]).with_columns(
        pl.sum_horizontal([f"z_{f}" for f in features]).alias("vulnerability_score")
    )

    return df_scored.select(["census_tract_id", "vulnerability_score"]).write_json()


async def main():
    return await asyncio.create_task(get_vulnerability_scores_async())


if __name__ == '__main__':
    asyncio.run(main())
