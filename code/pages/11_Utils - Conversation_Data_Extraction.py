import streamlit as st
import os
import traceback
from utilities.helper import LLMHelper

def clear_summary():
    st.session_state['summary'] = ""

def get_custom_prompt():
    customtext = st.session_state['customtext']
    customprompt = "{}".format(customtext)
    return customprompt

def customcompletion():
    response = llm_helper.get_completion(get_custom_prompt())
    st.session_state['conv_result'] = response.encode().decode()

try:
    # Set page layout to wide screen and menu item
    menu_items = {
    'Get help': None,
    'Report a bug': None,
    'About': '''
     ## Embeddings App
     Embedding testing application.
    '''
    }
    st.set_page_config(layout="wide", menu_items=menu_items)

    llm_helper = LLMHelper()

    st.markdown("## Conversation data extraction")

    conversation_prompt = """   用户：您好，我在8月25日到9月11日之间休息。为了这次愉快的旅行，我存了4000英镑。如果我从旧金山飞出去，你对我去哪里有什么建议？
        代理商：如果有这个预算，你可以去美国、墨西哥、巴西、意大利或日本的城市旅行。有什么偏好吗？
        用户：太好了，我一直想去日本看看。我能期待什么样的酒店？？
        代理商：太好了，让我检查一下我有什么。首先，我可以和你确认一下，这是一个成年人的旅行吗？
        用户：是的
        代理商：太好了，谢谢。那样的话，我可以给你15天的住宿时间，这是一家靠近皇宫的三星级酒店。你将在8月25日至9月7日期间住在那里。他们提供免费无线网络，客人的评分为8.49/10。整个套餐价格为2024.25美元。我应该为您预订吗？
        用户：这听起来真的很好。比方说我有一个约会我想带…那么日本会超出我的价格范围吗？
        代理商：是的，很遗憾，我在日本的两个包裹不符合你们的预算。然而，我可以在圣多明各的三星级玫瑰塞拉酒店为您提供为期13天的海滩度假。你对这样的东西感兴趣吗？
        用户：那个地方的客人评分如何？
        代理商：7.06/10，所以客人似乎对这个地方很满意。
        用户：真。你知道吗，我还不确定我是否准备好邀请她和我一起旅行。给Sugoi预定我就行了
        代理商：我可以帮你做！
        用户：谢谢！
        代理商：我今天能帮你预订其他房间吗？
        用户：不用了，谢谢！


        执行以下任务：
        -	总结对话，关键：总结
        -      如果未检测到客户预算，则无，关键字：预算
        -      出发城市，关键字：出发
        -      目的地城市，关键字：目的地
        -      所选国家/地区，关键字：国家/地区
        -      客户选择哪家酒店？，关键字：酒店
        -	代理商是否提醒客户评估调查, 关键字:评估调查 true or false as bool
        -	客户是否提到了产品竞争对手？, key: 竞争对手 true or false as bool
        -	客户要求折扣了吗？, 关键字:折扣 true or false as bool
        - 代理商询问了其他客户需求. key: additional_requests
        - 客户对解决方案满意吗? key: 满意

        Answer in JSON machine-readable format, using the keys from above.
        Format the ouput as JSON object called "results". Pretty print the JSON and make sure that is properly closed at the end."""

    # displaying a box for a custom prompt
    st.session_state['customtext'] = st.text_area(label="Prompt",value=conversation_prompt, height=400)
    st.button(label="Execute tasks", on_click=customcompletion)
    # displaying the summary
    result = ""
    if 'conv_result' in st.session_state:
        result = st.session_state['conv_result']
    st.text_area(label="OpenAI result", value=result, height=200)

except Exception as e:
    st.error(traceback.format_exc())
