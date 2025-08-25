import select_tool_wikipedia as select_tool

if __name__ == '__main__':
    prompt = '서울에 얼마나 많은 사람이 살고 있어?'
    res = select_tool.select_tool(prompt)
    print('=== 결과 ===\n' + res)