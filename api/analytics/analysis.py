import asyncio

import polars as pl

from analytics.setup import get_feature_table


async def get_correlations():
    table = await get_feature_table()
    df = pl.DataFrame(table).select(pl.col(pl.Float64))
    correlation = df.corr()
    print(correlation)
    return correlation


async def main():
    return await asyncio.create_task(get_correlations())


if __name__ == '__main__':
    asyncio.run(main())
