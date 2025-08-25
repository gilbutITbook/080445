from llama_cpp import Llama
# 다운로드한 모델 지정 
llm = Llama(model_path='vicuna-7b-v1.5.Q4_0.gguf')
# 프롬프트 지정 
prompt = 'Q:한국에서 가장 높은 산은? \nA:'
# 언어 모델로부터 응답을 받는다 
output = llm(prompt, temperature=0.1, stop='\n\n', echo=False)
print('-----')
print(output["choices"][0]["text"])