from llama_cpp import Llama
# 다운로드한 모델을 지정한다.  
llm = Llama(model_path='Meta-Llama-3.1-8B-Instruct-Q4_K_L.gguf', verbose=False)
# 프롬프트를 지정한다             
prompt = '한국어로 대답해줘. \nQ:대한민국에서 제일 높은 산은?\nA:'
# 언어 모델로부터 응답을 받는다 
output = llm(prompt, temperature=0.1, stop='\n', echo=False)
print('-----')
print(output["choices"][0]["text"])
