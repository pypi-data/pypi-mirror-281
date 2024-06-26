import uuid
from datetime import datetime

import pandas as pd
import pyarrow as pa


def validate_df_and_convert_to_arrow(df: pd.DataFrame) -> pa.Table:
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    current_time = pd.Timestamp(datetime.now()).floor("ms").tz_localize("UTC")
    if "created_at" in df.columns:
        if df["created_at"].isnull().values.any():
            df["created_at"].fillna(current_time, inplace=True)
    else:
        df["created_at"] = current_time

    if "updated_at" in df.columns:
        if df["updated_at"].isnull().values.any():
            df["updated_at"].fillna(current_time, inplace=True)
    else:
        df["updated_at"] = current_time

    if "id" in df.columns:
        # check if there is any missing value in the id column
        if df["id"].isnull().values.any():
            df["id"] = df["id"].apply(lambda x: str(uuid.uuid4()) if pd.isnull(x) else x)
        # check if the id column is unique
        if not df["id"].is_unique:
            raise ValueError("Column 'id' must be unique")
    else:
        df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]

    df["__time"] = "1970-01-01T00:00:00.000Z"
    df["__time"] = pd.to_datetime(df["__time"], utc=True)

    pa_schema = pa.Schema.from_pandas(df)
    new_schema = pa.schema(
        [
            (field.name, pa.timestamp("ms", tz="UTC"))
            if field.name in ["__time", "created_at", "updated_at"]
            else field
            for field in pa_schema
        ]
    )

    tbl = pa.Table.from_pandas(df, schema=new_schema)

    return tbl
