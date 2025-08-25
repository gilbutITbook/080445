from sentence_transformers import SentenceTransformer, util

# 모델을 사용해 임베딩을 계산한다 --- (*1)
model = SentenceTransformer('stsb-xlm-r-multilingual')
# 더 가벼운 모델로 시험해보고 싶은 경우에는 아래를 사용 --- (*1a)
# model = SentenceTransformer('all-MiniLM-L6-v2')

# 샘플 문장 --- (*2)
sentences = [
    '오늘 일기예보에 따르면 비가 온다고 한다.',
    '이 회사는 고등어 통조림을 수출한다.',
    'Python을 사용해 Embedding을 계산한다.',
    '하늘을 보니 구름이 많아서 우산을 갖고 나가자.']
# 문장을 임베딩으로 변환 --- (*3)
embeddings = model.encode(sentences)
# 각각의 유사도를 계산 --- (*4)
cosine_scores = util.cos_sim(embeddings, embeddings)
# 결과를 표시 --- (*4)
result = []
for i, sentence in enumerate(sentences):
    # 최초의 문장과의 유사도를 가져옴 --- (*5)
    score = cosine_scores[0][i]
    embedding = embeddings[i]
    result.append({'score': score, 'sentence': sentence})
    print("문장:", sentence)
    print("Embedding:", embedding[:5], '...')
    print("유사도:", score)
    print("---------")
# 최초의 문장과 가까운 순으로 표시 --- (*5)
result = list(sorted(result, key=lambda x: x['score'], reverse=True))
print("=== 최초의 문장과 가까운 순으로 표시 ===")
for e in result:
    print(f"(유사도:{e['score']:.3f}) {e['sentence']}")

