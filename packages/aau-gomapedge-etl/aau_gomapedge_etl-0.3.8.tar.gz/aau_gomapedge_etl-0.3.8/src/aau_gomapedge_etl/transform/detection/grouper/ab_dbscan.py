from duckdb import DuckDBPyConnection, DuckDBPyRelation

from aau_gomapedge_etl.services import AngleBalancingDBSCAN

from .protocol import Grouper


class ABDBSCAN(Grouper):
    __slots__ = ["__con", "__max_dist", "__max_angle", "__min_samples"]

    def __init__(
        self,
        con: DuckDBPyConnection,
        max_dist: float,
        max_angle: float,
        min_samples: int,
    ) -> None:
        self.__con = con
        self.__max_dist = max_dist
        self.__max_angle = max_angle
        self.__min_samples = min_samples
        self.__ensure_db_function()

    @property
    def max_dist(self) -> float:
        return self.__max_dist

    @property
    def max_angle(self) -> float:
        return self.__max_angle

    @property
    def min_samples(self) -> int:
        return self.__min_samples

    @staticmethod
    def __cluster(
        data: list[tuple[float, float, float]],
        max_dist: float,
        max_angle: float,
        min_samples: int,
    ) -> list[int]:
        cluster = AngleBalancingDBSCAN(max_dist, max_angle, min_samples, degrees=True)
        return cluster.fit_predict(data).tolist()

    def __ensure_db_function(self):
        function_name = "ab_dbscan"
        result = self.__con.query(
            """
SELECT function_name
FROM duckdb_functions()
WHERE function_name = $fname;
""",
            params={"fname": function_name},
        ).fetchone()

        if result is None:
            self.__con.create_function(function_name, self.__cluster)

    def group(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        self.__con.execute(
            """
CREATE OR REPLACE TABLE detection AS
    WITH data_tbl AS (
        SELECT cls,
               list(id                                        ORDER BY id) AS ids,
               list([ST_X(location), ST_Y(location), heading] ORDER BY id) AS dimensions,
        FROM tbl
        GROUP BY cls
    ), cluster_tbl AS (
        SELECT unnest(ids)                   AS id,
               unnest(ab_dbscan(dimensions, $max_dist, $max_angle, $min_samples)) AS cid
        FROM data_tbl
    )
    SELECT id,
           cluster_tbl.cid,
           trip_no,
           img_seq_id,
           heading,
           width,
           height,
           score,
           cls,
           location
    FROM cluster_tbl
        INNER JOIN detection USING (id);
""",
            parameters={
                "max_dist": self.max_dist,
                "max_angle": self.max_angle,
                "min_samples": self.min_samples,
            },
        )
        return self.__con.table("detection").filter("cid > -1")
