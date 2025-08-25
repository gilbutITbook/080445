import os, openai, wikipediaapi

# 텍스트를 청크로 분할 --- (*1)
def split_text(text, chunk_size=2000):
    chunks = []
    text = text.replace('. ', '.\n')  # 마침표 뒤에 줄바꿈 추가
    cur = ''
    for s in text.split('\n'):
        cur += s + '\n'
        if len(cur) > chunk_size:
            chunks.append(cur)
            cur = ''
    if cur != '': chunks.append(cur)
    return chunks

# 텍스트를 요약한다 --- (*2)
def summarize(text, max_len=800):
    # 텍스트를 청크로 분할
    chunks = split_text(text)
    print(f'=== 요약: 청크 수: {len(chunks)} ===')
    # 요약을 위한 프롬프트 템플릿 --- (*3)
    summarize_template = \
        '### 지시:\n다음 입력을 간결하게 요약해 줘.\n' + \
        '### 입력:\n```{chunk}```\n'
    # 청크별로 요약한다 --- (*4)
    result_all = ''
    for chunk in chunks:
        prompt = summarize_template.format(chunk=chunk)
        print('--- 요약 프롬프트 ---\n' + prompt)
        result = call_chatgpt(prompt) + '\n'
        print('--- 요약 결과 ---\n' + result)
        result_all += result + '\n'
    # 문자수 이상이면 재귀적으로 요약 --- (*5)
    if len(result_all) > max_len:
        result_all = summarize(result_all, max_len)
    return result_all

# ChatGPT API를 호출하는 함수  --- (*6)
use_azure=False
def call_chatgpt(prompt):
    if use_azure:
        client = openai.AzureOpenAI()
        completion = client.chat.completions.create(
            model='test-gpt-35-turbo',
            messages=[{'role': 'user', 'content': prompt}])
    else:
        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}])
    return completion.choices[0].message.content

# 위키백과에서 본문을 가져온다 --- (*7)
def get_wikitext(wiki_title):
    wiki = wikipediaapi.Wikipedia('llm-wiki-search', 'ko')
    wiki_file = os.path.join('./', f'__{wiki_title}.txt')
    if not os.path.exists(wiki_file):
        page = wiki.page(wiki_title) # 페이지를 가져온다 
        if not page.exists(): return f'{wiki_title}가 존재하지 않습니다.'
        with open(wiki_file, 'w', encoding='utf-8') as f:
            f.write(page.text) # 본문을 저장
    with open(wiki_file, 'r', encoding='utf-8') as f:
        text = f.read()
        print(f'=== Wikipedia: {wiki_title} ({len(text)}자) ===')
        return text

if __name__ == '__main__':
    # Wikipedia에서 텍스트를 가져와서 요약 --- (*8)
    wiki_text = get_wikitext('태양')
    result = summarize(wiki_text)
    print(f'=== 결과:{len(result)} 문자 ===\n{result}')

