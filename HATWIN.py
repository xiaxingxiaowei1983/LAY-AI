import streamlit as st
import time

# 模拟后端逻辑与状态机
class LayAI_Backend:
    def __init__(self):
        if "state" not in st.session_state:
            st.session_state.state = "IDLE" # 初始状态
        if "history" not in st.session_state:
            st.session_state.history = []
    
    def get_response(self, user_input):
        # 状态机逻辑 (对应 PRD 6.1)
        current_state = st.session_state.state
        
        # 1. IDLE -> DIAGNOSTIC (智商税测试启动)
        if current_state == "IDLE":
            st.session_state.state = "DIAGNOSTIC_WAITING"
            return """
            (LAY 正在审视你的投资计划...)
            
            我是 LAY，你的风控参谋。在谈投资之前，先看你能不能过这关。
            
            **【智商税测试】**
            你是一个外行，想在二线城市老城区接手一家看起来装修还可以的转让店。房东说：“这店以前生意很好的，我就是累了想休息。”
            你的第一反应是？
            
            A. 捡漏了，装修省一大笔钱，赶紧签。
            B. 要求看过去三年的流水和OTA后台数据。
            C. 觉得有猫腻，但相信自己的运营能力能做起来。
            
            (请输入 A, B 或 C)
            """
            
        # 2. DIAGNOSTIC -> ANALYSIS (测试反馈与分析)
        elif current_state == "DIAGNOSTIC_WAITING":
            if user_input.upper() not in ["A", "B", "C"]:
                return "别想糊弄过去。选 A, B 还是 C？这是你的真金白银。"
            
            response = ""
            if user_input.upper() == "B":
                response = "**勉强及格。** 但你知道流水可以造假吗？你知道OTA差评可以被“技术处理”吗？不过你至少没那么天真。\n\n"
            else:
                response = "**典型韭菜。** 选A的是给房东接盘装修垃圾的；选C的是患了'自信幻觉症'的。记住：好店不需要转让，转让的都是坑。\n\n"
            
            st.session_state.state = "ANALYSIS"
            response += "测试结束。现在告诉我，**你想在哪个城市，投资多少钱，做什么类型的酒店？** (例如：我想在长沙开一家以电竞为主题的酒店，预算200万)"
            return response

        # 3. ANALYSIS -> GENERATING (城市路由与生成)
        elif current_state == "ANALYSIS":
            city = self.extract_city(user_input)
            tier = self.get_city_tier(city)
            
            template_type = "【一线城市高周转模板】" if tier == "Tier1" else "【通用生存模板】"
            
            st.session_state.state = "GENERATING"
            
            return f"""
            收到。识别城市：**{city}**
            判定等级：**{tier}** -> 调用 {template_type}
            
            正在根据“智商税破壁模型”检索 {city} 的竞品数据...
            正在调用“系统性废弃”模型优化成本结构...
            
            --------------------------------
            **《{city}酒店投资分析底稿 (P1-P3)》**
            
            ### P1. 宏观环境与劝退预警
            **【反直觉判断】**
            你认为{city}是网红城市，流量大？错了。
            根据 {city} 2024年文旅数据，过夜游客人均消费仅为...
            
            (此处模拟流式输出 800字...)
            
            ...
            
            *(篇幅已达上限，系统已暂停。请输入“继续”查看 P4 财务测算表)*
            """
        
        # 4. PAUSED -> RESUMED (断点续写)
        elif current_state == "GENERATING":
             return """
             ### P4. 财务测算 (FMEA风控版)
             
             **【风险对冲分析】**
             你的回本周期模型建立在入住率 85% 的假设上。
             如果不幸遇到不可抗力（参考2020年），入住率跌至 40%，你的现金流能撑几个月？
             
             ... (模拟生成 P4-P9) ...
             """
             
        return "系统异常，请刷新。"

    # 模拟 PRD 4.2.2 的城市路由逻辑
    def extract_city(self, text):
        # 简单模拟实体抽取
        if "北京" in text or "上海" in text: return "上海"
        if "长沙" in text: return "长沙"
        return "未知城市"

    def get_city_tier(self, city):
        tier1 = ["北京", "上海", "广州", "深圳"]
        if city in tier1: return "Tier1"
        return "General"

# --- Streamlit 前端界面 ---

def main():
    st.set_page_config(page_title="LAY AI - 酒店投资风控参谋", layout="wide")

    # 侧边栏：配置与导航
    with st.sidebar:
        st.title("LAY AI v1.0")
        st.markdown("---")
        st.markdown("**当前模式**: 投资风控 (Risk Control)")
        st.markdown("**加载模型库**: 52个 (Active)")
        st.markdown("**数据源**: 2024 实时联网")
        st.markdown("---")
        st.info("💡 提示：LAY 说话很难听，但能帮你省几百万。")

    # 主界面标题
    st.header("LAY AI：您的酒店投资风控参谋")
    st.markdown("> *“在投前阶段规避毁灭性风险，输出可落地的属地化投资方案。”*")

    # 初始化后端
    backend = LayAI_Backend()

    # 聊天记录显示
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 首次加载自动触发 Hook (PRD 4.2.1)
    if not st.session_state.history:
        initial_msg = backend.get_response("")
        st.session_state.history.append({"role": "assistant", "content": initial_msg})
        st.rerun()

    # 用户输入
    if prompt := st.chat_input("输入你的想法..."):
        # 显示用户消息
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 显示 AI 正在思考 (模拟)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("*(LAY 正在调用 50+ 模型库进行演算...)*")
            time.sleep(1) # 模拟延迟
            
            # 获取后端回复
            full_response = backend.get_response(prompt)
            
            # 模拟打字机效果
            displayed_response = ""
            for chunk in full_response.split():
                displayed_response += chunk + " "
                message_placeholder.markdown(displayed_response + "▌")
                time.sleep(0.05)
            message_placeholder.markdown(full_response)
        
        # 记录 AI 消息
        st.session_state.history.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()