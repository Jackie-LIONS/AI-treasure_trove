import chromadb

# 存在内存当中，程序运行完时会丢失
# client = chromadb.Client();
# 创建client时，设置数据持久化路径，默认存储在内存中，程序运行完时会丢失
client = chromadb.PersistentClient(path=r"./chroma_db")
# 存在这个集合就返回，不存在就创建
collection = client.get_or_create_collection(name="test")
# chroma数据库表作用：embeddings表：存向量信息，embeddings_metadata表:存放元数据，embeddings_metadata_array表：转换成向量的元数据

# 添加数据
collection.add(
    documents= ["Article by john","Article by jack","Article by jim"],
    embeddings=[[1,2,3],[4, 5, 6],[7,8,9]],
    ids=["1","2","3"]
)

# 查数据
get_result = collection.get(
    # ids=["1"]                    根据id获取
    # 模糊查询
    where_document= {"$contains":"john"},
    # include=["embeddings"]   默认不展示转成的向量数据，因为很长，如果想看则打开这个配置
)
print(get_result)

# 删除数据信息
collection.delete(
    ids=["1"]
)
print(collection.get(include=["embeddings"]))

# 修改数据
collection.update(
    documents= ["Article by john","Article by jack","Article by jim"],
    embeddings=[[10,2,3],[40, 5, 6],[70,8,9]],
    ids=["1","2","3"]
)
print(collection.get(include=["embeddings"]))
