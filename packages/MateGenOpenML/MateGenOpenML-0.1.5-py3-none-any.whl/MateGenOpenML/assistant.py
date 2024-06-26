# MateGenOpenML/assistant.py

from IPython.display import display, Code, Markdown, Image
import time
import openai
import os
import json
from openai import OpenAI
from openai import OpenAIError
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime
from pathlib import Path

assistant_id = 'asst_Zy0x3doFWmTXpSd97qbF1ANG'
base_url = 'https://ai.devtool.tech/proxy/v1'
project = 'proj_U6UhUrseV68t8VGv6ZvHdHAR'

home_dir = str(Path.home())
log_dir = os.path.join(home_dir, ".my_agent_logs")
os.makedirs(log_dir, exist_ok=True)
token_log_file = os.path.join(log_dir, "token_usage_log.json")
thread_log_file = os.path.join(log_dir, "thread_log.json")

client = None
thread = None

def log_thread_id(thread_id):
    try:
        with open(thread_log_file, "r") as file:
            thread_log = json.load(file)
    except FileNotFoundError:
        thread_log = []

    # 添加新的线程 ID
    thread_log.append(thread_id)

    with open(thread_log_file, "w") as file:
        json.dump(thread_log, file)
        
def get_latest_thread():
    global assistant_id, client, thread  
    try:
        with open(thread_log_file, "r") as file:
            thread_log = json.load(file)
    except FileNotFoundError:
        thread_log = []

    if thread_log:
        # 获取最新的线程 ID 并将其设置为全局变量
        thread_id = thread_log[-1]
        thread = client.beta.threads.retrieve(thread_id=thread_id)
        return thread
    else:
        # 如果没有线程，则创建一个新的线程
        thread = client.beta.threads.create()
        log_thread_id(thread.id)
        return thread
    
def log_token_usage(thread_id, tokens):
    try:
        with open(token_log_file, "r") as file:
            token_log = json.load(file)
    except FileNotFoundError:
        token_log = {"total_tokens": 0}

    today = datetime.utcnow().date().isoformat()

    if today not in token_log:
        token_log[today] = {}

    if thread_id not in token_log[today]:
        token_log[today][thread_id] = 0
    token_log[today][thread_id] += tokens

    # 更新累计 token 总数
    if "total_tokens" not in token_log:
        token_log["total_tokens"] = 0
    token_log["total_tokens"] += tokens

    with open(token_log_file, "w") as file:
        json.dump(token_log, file)
        
def check_daily_token_limit():
    try:
        with open(token_log_file, "r") as file:
            token_log = json.load(file)
    except FileNotFoundError:
        return False

    today = datetime.utcnow().date().isoformat()

    total_tokens_today = sum(token_log.get(today, {}).values())
    
    if total_tokens_today >= 500000:
        return True
    
    return False

def check_total_token_limit():
    try:
        with open(token_log_file, "r") as file:
            token_log = json.load(file)
    except FileNotFoundError:
        return False

    total_tokens = token_log.get("total_tokens", 0)
    
    if total_tokens > 3000000:
        return True
    
    return False

def print_token_usage():
    try:
        with open(token_log_file, "r") as file:
            token_log = json.load(file)
    except FileNotFoundError:
        print("目前没有token消耗")
        return
    
    today = datetime.utcnow().date().isoformat()
    
    # 打印今日 token 使用情况
    if today in token_log:
        total_tokens_today = sum(token_log[today].values())
        print(f"今日已消耗的 token 数量：{total_tokens_today}")
    else:
        print("今日没有消耗 token。")
    
    # 打印累计 token 使用情况
    total_tokens = token_log.get("total_tokens", 0)
    print(f"总共消耗的 token 数量：{total_tokens}")
    
def python_inter(py_code, g='globals()'):
    """
    专门用于执行python代码，并获取最终查询或处理结果。
    :param py_code: 字符串形式的Python代码，
    :param g: g，字符串形式变量，表示环境变量，无需设置，保持默认参数即可
    :return：代码运行的最终结果
    """    
    try:
        # 尝试如果是表达式，则返回表达式运行结果
        return str(eval(py_code, g))
    # 若报错，则先测试是否是对相同变量重复赋值
    except Exception as e:
        global_vars_before = set(g.keys())
        try:            
            exec(py_code, g)
        except Exception as e:
            return f"代码执行时报错{e}"
        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        # 若存在新变量
        if new_vars:
            result = {var: g[var] for var in new_vars}
            return str(result)
        else:
            return "已经顺利执行代码"
        
python_inter_tool =  {
    "type": "function",
    "function": {
        "name": "python_inter",
        "description": "Execute general Python code and return the result. ",
        "parameters": {
            "type": "object",
            "properties": {
                "py_code": {
                    "type": "string",
                    "description": "The Python code to execute."
                },
                "g": {
                    "type": "string",
                    "description": "Global environment variables, default to globals().",
                    "default": "globals()"
                }
            },
            "required": ["py_code"]
        }
    }
}

def function_to_call(run_details):
    global assistant_id, client, thread, run
    # 仅有一个自定义的外部函数
    available_functions = {
        "python_inter": python_inter,
    }
    
    # 初始化一个空列表，用于存储所有工具调用的输出
    tool_outputs = []
    
    # 提取所有工具调用
    tool_calls = run_details.required_action.submit_tool_outputs.tool_calls
    
    for tool_call in tool_calls:
        # 获取调用外部函数的函数名称
        function_name = tool_call.function.name
        
        # 根据函数名称获取对应的外部函数对象
        function_to_call = available_functions.get(function_name)
        
        if function_to_call is None:
            # 如果函数不存在，则跳过
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": f"函数 {function_name} 不存在"
            })
            continue
        
        # 提取function_call_message中调用外部函数的函数参数
        function_args = tool_call.function.arguments
        
        def is_json(myjson):
            """
            检查字符串是否为JSON格式
            """
            try:
                json_object = json.loads(myjson)
            except ValueError as e:
                return False
            return True

        def convert_to_json(code_str):
            """
            如果字符串不是JSON格式，将其转换为键为 "py_code" 的JSON对象
            """
            if is_json(code_str):
                return code_str
            else:
                return json.dumps({"py_code": code_str})
        
        # 转化为json格式字符串
        function_args = convert_to_json(function_args)
        # 转化为json
        function_args = json.loads(function_args)
        
        # 打印代码    
        # 创建convert_to_markdown内部函数，用于辅助打印代码结果
        def convert_to_markdown(code, language):
            return f"```{language}\n{code}\n```"

        # 提取代码部分参数
        code = function_args['py_code']
        markdown_code = convert_to_markdown(code, 'python')
        print("即将执行以下代码：")
        display(Markdown(markdown_code))
        
        # 将参数带入到外部函数中并运行
        try:
            # 将当前操作空间中的全局变量添加到外部函数中
            function_args['g'] = globals()
            
            # 运行外部函数
            function_response = function_to_call(**function_args)
          
        # 若外部函数运行报错，则提取报错信息
        except Exception as e:
            function_response = "函数运行报错如下:" + str(e)
            #print(function_response)
            
        tool_outputs.append({
            "tool_call_id": tool_call.id,
            "output": function_response
        })

    return tool_outputs

def run_status():
    global assistant_id, client, thread, run
    # 创建计数器
    i = 0
    try:
        # 轮询检查运行状态
        while True:
            run_details = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            status = run_details.status

            if status in ['completed', 'expired', 'cancelled']:
                log_token_usage(thread.id, run_details.usage.total_tokens)
                return run_details
            if status in ['requires_action']:
                return run_details

            i += 1
            if i == 30:
                print("响应超时，请稍后再试。")
                return None

            # 等待一秒后再检查状态
            time.sleep(1)

    except OpenAIError as e:
        print(f"An error occurred: {e}")
        return None
        
    return None

def chat_base(user_input, 
              first_input=True, 
              function_res=False, 
              tool_outputs=None):
    
    global assistant_id, client, thread, run
    
    # 创建消息
    if first_input:
        message = client.beta.threads.messages.create(
          thread_id=thread.id,
          role="user",
          content=user_input
        )
        
    if tool_outputs == None:
        # 执行对话
        run = client.beta.threads.runs.create(
          thread_id=thread.id,
          assistant_id=assistant_id
        )
        
    else:
        # Function calling第二轮对话，更新run的状态
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    
    # 判断运行状态
    run_details = run_status()
    # 若无结果，则打印报错信息
    if run_details.status == None:
        print('当前应用无法运行，请稍后再试')
        
    # 若消息创建完成，则返回模型返回信息
    elif run_details.status == 'completed':
        messages_check = client.beta.threads.messages.list(thread_id=thread.id)
        display(Markdown(messages_check.data[0].content[0].text.value))
        
    # 若外部函数响应超时，则根据用户反馈制定执行流程
    elif run_details.status == 'expired' or run_details.status == 'cancelled' :
        user_res = input('当前编程环境响应超时或此前任务已取消，是否继续？1.继续，2.重新输入需求')
        if user_res == '1':
            print('好的，正在重新创建响应')
            chat_base(user_input=user_input, first_input=False, tool_outputs=None)
        else:
            user_res1 = input('请输入新的问题：')
            chat_base(user_input=user_res1, first_input=True, tool_outputs=None)
            
    # 若调用外部函数，则开启Function calling
    elif run_details.status == 'requires_action':
        # 创建外部函数输出结果
        tool_outputs = function_to_call(run_details)
        chat_base(user_input=user_input, first_input=False, tool_outputs=tool_outputs)
        
class MateGenMLClass:
    def __init__(self, api_key):
        """
        初始参数解释：
        api_key：必选参数，表示调用OpenAI模型所必须的字符串密钥，没有默认取值，需要用户提前设置才可使用MateGen；
        """
        global client, thread, assistant_id
        
        # 基础属性定义
        self.api_key = api_key
        
        # 创建openai客户端
        self.client = OpenAI(api_key = self.api_key, 
                             base_url = 'https://ai.devtool.tech/proxy/v1', 
                             project = 'proj_U6UhUrseV68t8VGv6ZvHdHAR')
        
        print("正在初始化，请稍后...")
        # 验证API-Key和网络环境，并选择模型
        try:
            self.models = self.client.models.list()
            
            if self.models:
                print("初始化成功，网络环境无误，API-KEY通过验证...")
                print("公开课API每日限额50万token，总计限额300万token，用完即止。正式付费课程将提供更多Agent额度及更强模型的功能支持，付费课程信息添加客服小可爱微信：littlecat_1201回复“机器学习”详询哦~")
            else:
                print("当前网络环境无法连接服务器，请检查网络并稍后重试...")
                
        except openai.AuthenticationError:
            print("API-KEY未通过验证，请添加客服小可爱微信：littlecat_1201，加入课程并领取API-KEY")
        except openai.APIConnectionError:
            print("当前网络环境无法连接服务器，请检查网络并稍后重试...")
        except openai.RateLimitError:
            print("API-KEY账户已达到RateLimit上限，请添加客服小可爱微信：littlecat_1201，加入课程并领取API-KEY")
        except openai.OpenAIError as e:
            print(f"An error occurred: {e}")
        client =  self.client    
        thread = get_latest_thread()
            
    def chat(self, question=None):
        head_str = "▌MateGen（机器学习公开课版）初始化完成，欢迎使用！"
        display(Markdown(head_str))
        
        if question != None:
            if check_daily_token_limit():
                print("MateGen今日试用额度已用完，请明日再试，或添加客服小可爱微信：littlecat_1201，加入课程即可获赠更高额度及更强模型的功能支持~")
            elif check_total_token_limit():
                print("MateGen总试用额度已用完，或添加客服小可爱微信：littlecat_1201，加入课程即可获赠更高额度及更强模型的功能支持~")
            else:
                chat_base(user_input=question)
        else:
            print("你好，我是你的机器学习公开课课程助理，有任何问题都可以问我哦~")
            while True:
                question = input("请输入您的问题(输入退出以结束对话): ")
                if question == "退出":
                    break
                elif check_daily_token_limit():
                    print("MateGen今日试用额度已用完，请明日再试，或添加客服小可爱微信：littlecat_1201，加入课程即可获赠更高额度及更强模型的功能支持~")
                    break
                elif check_total_token_limit():
                    print("MateGen总试用额度已用完，或添加客服小可爱微信：littlecat_1201，加入课程即可获赠更高额度及更强模型的功能支持~")
                    break
                else:
                    chat_base(user_input=question)
                    
    def reset(self):
        global client, thread, assistant_id, run
        try:
            client.beta.threads.runs.cancel(thread_id=thread.id, run_id=run.id)
        except Exception as e:
            pass
        client.beta.threads.delete(thread_id=thread.id)
        thread = client.beta.threads.create()
        log_thread_id(thread.id)
        print("已经清理历史消息")
        
    def message_history(self):
        global client, thread, assistant_id, run
        messages_check = client.beta.threads.messages.list(thread_id=thread.id)
        print(messages_check.data)
        
    def print_usage(self):
        print_token_usage()

def export_variables():
    return globals()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="MateGen ML Assistant")
    parser.add_argument('--api_key', required=True, help="MateGen API KEY")
    args = parser.parse_args()
    assistant = MateGenMLClass(api_key=args.api_key)
    print("成功实例化MateGen Agent")