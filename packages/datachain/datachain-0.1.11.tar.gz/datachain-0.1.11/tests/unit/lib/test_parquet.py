import pandas as pd

from datachain.lib.file import File
from datachain.lib.parquet import BasicParquet, process_parquet


def test_parquet_generator(tmp_path, catalog):
    ids = [12345, 67890, 34, 0xF0123]
    texts = ["28", "22", "we", "hello world"]
    df = pd.DataFrame({"id": ids, "text": texts})

    class _MyPq(BasicParquet):
        id: int
        text: str

    name = "111.parquet"
    pq_path = tmp_path / name
    df.to_parquet(pq_path)
    stream = File(name=name, parent=str(tmp_path))
    with open(pq_path) as fd:
        stream._set_stream(catalog, fd, caching_enabled=False)

        func = process_parquet(_MyPq)
        objs = list(func(stream))

    unixpath = pq_path.as_posix()
    assert len(objs) == len(ids)
    for o, id, text in zip(objs, ids, texts):
        assert isinstance(o, _MyPq)
        assert isinstance(o.file, File)
        assert o.file.parent == unixpath
        assert o.id == id
        assert o.text == text
