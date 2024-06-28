from .tools import now
from .tools import logger

__all__ = [
    "connect_to_mongodb",
    "mongodb",
    "mongo_sample",
    "mongo_tongji",
]


def mongodb(host, database, port: int | None = None, **kwargs):
    """
    连接 MongoDB

    host: mongo 链接
    database: 数据库名称
    port: mongo 端口

    host 有密码格式: "mongodb://username:password@192.168.0.1:27017/"
    host 无密码格式: "mongodb://192.168.0.1:27017/"
    """
    from pymongo import MongoClient

    try:
        # 连接到 MongoDB
        client = MongoClient(host, port, **kwargs)
        db = client[database]
        db.list_collection_names()
        logger.success(f"MongoDB 成功连接到 {database}")
        return db
    except Exception as e:
        logger.error("MongoDB 连接失败:", str(e))
        return None


connect_to_mongodb = mongodb


def mongo_sample(
    mongodb,
    table: str,
    size: int = 1000,
) -> list:
    """
    mongodb 随机样本抽样

    mongodb: mongo 库
    table: mongo 表(集合)名称
    size: 随机样本数量
    """
    results = list(mongodb[table].aggregate([{"$sample": {"size": size}}]))
    return results


def mongo_tongji(
    mongodb,
    prefix: str = "",
    tongji_table: str = "tongji",
) -> dict:
    """
    统计 mongodb 每个集合的`文档数量`

    mongodb: mongo 库
    prefix: mongo 表(集合)前缀, 默认空字符串可以获取所有表, 字段名称例如 `统计_20240101`。
    tongji_table: 统计表名称，默认为 tongji
    """

    tongji = mongodb[tongji_table]
    key = prefix if prefix else f"统计_{now(7)}"
    collection_count_dict = {
        **(
            tongji.find_one({"key": key}).get("count")
            if tongji.find_one({"key": key})
            else {}
        ),
        **(
            {
                i: mongodb[i].estimated_document_count()
                for i in mongodb.list_collection_names()
                if i.startswith(prefix)
            }
        ),
    }
    tongji.update_one(
        {"key": prefix if prefix else f"统计_{now(7)}"},
        {"$set": {"count": collection_count_dict}},
        upsert=True,
    )
    return dict(sorted(collection_count_dict.items()))
