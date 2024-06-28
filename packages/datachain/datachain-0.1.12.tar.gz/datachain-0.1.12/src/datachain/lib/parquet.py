from collections.abc import Iterator
from typing import Callable, Optional

import pandas as pd
from pydantic import Field

from datachain.lib.feature import Feature
from datachain.lib.file import File


class BasicParquet(Feature):
    file: File
    index: Optional[int] = Field(default=None)


def process_parquet(spec: type[BasicParquet]) -> Callable:
    def process(file: File) -> Iterator[spec]:  # type: ignore[valid-type]
        with file.open() as fd:
            df = pd.read_parquet(fd)
            df["index"] = df.index

            for pq_dict in df.to_dict("records"):
                pq_dict["file"] = File(
                    name=str(pq_dict["index"]),
                    source=file.source,
                    parent=file.get_full_name(),
                    version=file.version,
                    etag=file.etag,
                )
                yield spec(**pq_dict)

    return process
