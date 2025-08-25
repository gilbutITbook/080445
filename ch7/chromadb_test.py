import chromadb
from chromadb.utils import embedding_functions

# 임베딩을 위해 이용할 모델 --- (*1)
embedding_model_name = 'stsb-xlm-r-multilingual'
# 임베딩을 계산할 임베딩을 계산하는 함수를 생성 --- (*2)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=embedding_model_name)
# ChromaDB의의 클라이언트를 생성 --- (*3)
chroma_client = chromadb.EphemeralClient() # 메모리 내에 저장하는 경우
# 컬렉션을 작성 --- (*4)
collection = chroma_client.get_or_create_collection(
    name='test',
    embedding_function=embedding_fn)
# 샘플 문장 --- (*5)
sentences = [
    '오늘 일기예보에 따르면 비가 온다고 한다.',
    '이 회사는 고등어 통조림을 수출한다.',
    'Python을 사용해 Embedding을 계산한다.',
    '하늘을 보니 구름이 많아서 우산을 갖고 나가자.']
# 문장을 컬렉션에 추가 --- (*6)
collection.add(
    ids=[str(i) for i in range(len(sentences))], # 적당히 ID를 부여 
    documents=sentences)
# 유사한 문장을 검색 --- (*7)
query = '비가 오네. 어쩌지, 우산이 없어'
docs = collection.query(
    query_texts=[query],
    n_results=3,
    include=['documents', 'distances', 'embeddings'])
# 결과를 표시 --- (*8)
docs0 = zip(
    docs['documents'][0], 
    docs['distances'][0], 
    docs['embeddings'][0])
for doc, dist, emb in docs0:
    print(f'(거리:{dist:.1f}) {doc}', emb[:3], '...')
