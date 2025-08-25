import chromadb, os, wikipediaapi, openai
from chromadb.utils import embedding_functions

# 임베딩에 이용할 모델을 지정 --- (*1)
embedding_model_name = 'stsb-xlm-r-multilingual'
# ChromaDB를 초기화하고 컬렉션을 생성 --- (*2)
os.environ["TOKENIZERS_PARALLELISM"] = "false"
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=embedding_model_name)
chroma_client = chromadb.EphemeralClient()
collection = chroma_client.get_or_create_collection(
    name='test', embedding_function=embedding_fn)

# Wikipedia 본문 가져오기 --- (*3)
def get_wikitext(wiki_title):
    wiki = wikipediaapi.Wikipedia('llm-wiki-search', 'ko')
    wiki_file = os.path.join('./', f'__{wiki_title}.txt')
    if not os.path.exists(wiki_file):
        page = wiki.page(wiki_title) # 페이지 획득 
        if not page.exists(): return f'{wiki_title}가 존재하지 않습니다.'
        with open(wiki_file, 'w', encoding='utf-8') as f:
            f.write(page.text) # 본문을 저장장
    with open(wiki_file, 'r', encoding='utf-8') as f:
        text = f.read()
        print(f'=== Wikipedia: {wiki_title} ({len(text)}자) ===')
        return text

# 데이터베이스에 텍스트 추가 --- (*4)
def insert_text(text, chunk_size=500):
    # 문장을 일정량의 청크로 분할
    chunks = []
    paragraphs = text.split('\n')
    cur = ''
    for s in paragraphs:
        cur += s + '\n'
        if len(cur) > chunk_size:
            chunks.append(cur)
            cur = ''
    if cur != '': chunks.append(cur)
    print(f'=== 청크 수: {len(chunks)} ===\n')
    # print('----\n'.join(chunks))
    # 문장을 컬렉션에 추가 --- (*5)
    collection.add(
        ids=[f'{text[0:5]}{i+1}' for i in range(len(chunks))], # 적당히 ID 부여 
        documents=chunks)

# 데이터베이스에서 유사 텍스트 가져오기 --- (*6)
def query_text(query, max_len=1500):
    # 유사한 문장을 검색 --- (*7)
    docs = collection.query(
        query_texts=[query],
        n_results=10,
        include=['documents'])
    doc_list = docs['documents'][0]
    # 결과에서 max_len만큼 추출 --- (*8)
    doc_result = ''
    for doc in doc_list:
        if len(doc_result + doc) > max_len: break
        doc_result += doc.strip() + '\n-----\n'
    return doc_result

# 텍스트를 요약한다다 --- (*9)
def llm_summarize(text, query):
    # 텍스트를 데이터베이스에 추가
    insert_text(text)
    # 데이터베이스에서 유사 텍스트 가져오기
    doc_result = query_text(query)
    # 대규모 언어 모델을 사용해서 요약한다
    prompt = \
        f'### 지시:\n아래 정보를 참고해서 요약해줘.\n' + \
        f'특히"{query}"에 주목해줘.\n' + \
        f'### 정보:\n```{doc_result}```\n'
    print('=== 응답 프롬프트 ===\n' + prompt)
    result = call_chatgpt(prompt)
    print('=== 결과 ===\n' + result)
    return result

# ChatGPT API를 호출하는 함수 --- (*10)
def call_chatgpt(prompt):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}])
    return completion.choices[0].message.content

if __name__ == '__main__':
    # 위키백과에서 텍스트를 가져와 포인트를 지정하여 요약 --- (*11)
    title = '서울시'
    query = '인구 변화'
    wiki_text = get_wikitext(title)
    llm_summarize(wiki_text, query)
