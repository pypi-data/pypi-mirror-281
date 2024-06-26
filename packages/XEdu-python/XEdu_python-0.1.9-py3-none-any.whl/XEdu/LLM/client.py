from .llms import Moonshot,Deepseek,Openrouter,GLM,ERNIE,BaseURL,Qwen
import os
import sys,subprocess
import requests
import random
provider_id_map = {
        "openrouter": Openrouter,
        "moonshot": Moonshot,
        "deepseek": Deepseek,
        "glm": GLM,
        "ernie": ERNIE,
        "qwen":Qwen,
    }
provider_id_map_zh = {
    "openrouter":"openrouter",
    "月之暗面-Kimi":"moonshot",
    "幻方-深度求索":"deepseek",
    "智谱-智谱清言":"glm",
    "百度-文心一言":"ernie",
    "阿里-通义千问":"qwen",
}
default_model_map = {
        "openrouter": "mistralai/mistral-7b-instruct:free",
        "moonshot": "moonshot-v1-8k",
        "deepseek": "deepseek-chat",
        "glm":"glm-4",
        "ernie":"ERNIE_speed_8k",
        "qwen":"qwen-long",
    }
class Client:
    """docstring for Client
    """

    def __init__(self, provider=None,base_url=None,api_key=None,model=None,secret_key=None,xedu_url=None):
        self.provider = provider
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        if provider:
            if provider in provider_id_map_zh.keys():
                provider = provider_id_map_zh[provider]

            index =[ i  for i in provider_id_map_zh.keys() if provider in i]
            if len(index) != 0:
                provider = provider_id_map_zh[index[0]]
            # self.base_url = ServiceProvider.BASE_URL[provider] 
            if not self.model:
                self.model = default_model_map[provider]
            if provider in ['ernie']:
                self.client = provider_id_map[provider](api_key=self.api_key,secret_key=secret_key,model=self.model)
            else:
                self.client = provider_id_map[provider](api_key=self.api_key,model=self.model)
            print(f"|| Selected provider: {self.provider} || Current model: {self.model} ||")
        elif base_url:
            self.client = BaseURL(base_url=base_url,api_key=self.api_key,model=self.model)
        elif xedu_url:
            self.base_url = xedu_url
            from .llms.gradioapi import GradioClient as gc
            self.client = gc(xedu_url)
            # 选择合适的model
            try:
                model_list = self.try_list_models()
                if len(model_list) == 0:
                    raise Exception("No model available")
                free_model_list = [i for i in model_list if 'free' in i]
                if len(free_model_list) > 0:
                    self.model = random.choice(free_model_list)
                else:
                    self.model = random.choice(model_list)
            except:
                pass
            if self.model is not None:
                print(f"|| Selected base URL: {self.base_url} || Current model: {self.model} ||")
            # else:
            #     print(f"|| Selected base URL: {self.base_url} ||")
        # if self.model not in self.client.list_models():
        #     try:
        #         self.model = self.support_model()[0]
        #     except:
        #         pass


    def inference(self, message, stream=False,**kwargs):
        return self.client.inference(message, stream=stream, **kwargs)

    def support_model(self):
        return self.client.list_models()
    
    def try_list_models(self):
        url = self.base_url + "/models"
        payload={}
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.api_key),
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        id_list = []
        try:
            for i in response.json()['data']:
                id_list.append(i['id'])
        except:
            raise Exception(response.json())
        return id_list
    
    def support_provider(lang='en'):
        if lang == "zh":
            return list(provider_id_map_zh.keys())
        return list(provider_id_map.keys())

    def _restart_script(self):
        """Restarts the current script."""
        current_script = sys.argv[0]
        subprocess.run([sys.executable, current_script])

    def upgrade_env(self):
        try:
            import gradio as gr
            if gr.__version__ < "4.0.0":
                raise ImportError
            block = gr.Blocks()
        except:
            subprocess.run([sys.executable, "-m", "pip", "install", "gradio", "-U"], check=True)
            self._restart_script()
            import importlib
            importlib.invalidate_caches()  # 清理导入缓存
            import gradio as gr
            # 重新加载模块
            importlib.reload(gr)

    def run(self,host='0.0.0.0',port=7860,share=False):
        if host == "0.0.0.0":
            from .utils import find_available_port,get_local_ip
            port = find_available_port(port)
            ip = get_local_ip()
            print(f"Running on local URL:  http://{ip}:{port}")
            print(f"Running on local URL:  http://127.0.0.1:{port}")

        self.upgrade_env()
        import gradio as gr
        block = gr.Blocks( theme=gr.themes.Monochrome())
        
        def predict(message, history):
            history_openai_format = []
            for human, assistant in history:
                history_openai_format.append({"role": "user", "content": human })
                history_openai_format.append({"role": "assistant", "content":assistant})
            history_openai_format.append({"role": "user", "content": message})
        
            response = self.client.inference(
                message=history_openai_format,
                stream=True,
            )
            partial_message = ""
            for i in response:
                partial_message += i
                yield partial_message
                # if chunk.choices[0].delta.content is not None:
                #     partial_message = partial_message + chunk.choices[0].delta.content
                #     yield partial_message
        block = gr.Blocks( theme=gr.themes.Monochrome())
        with block:
            gr.Markdown(f"""<h1><center>🤖️ LLM Chatbot 🤖️</center></h1>
                        <h2><center>by XEdu</center></h2>
            """)
            provider = self.provider if self.provider else self.base_url
            # 横向排列两个文本框,不可编辑
            with gr.Row():
                gr.Textbox(label='provider', value=provider,interactive=False)
                gr.Textbox(label='model', value=self.model, interactive=False)
            # gr.Text(label='provider',value=f"{provider},  model: {self.model}")
            # with gr.Row():
            #     with gr.Column(visible=False,scale=1) as sidebar_left:
            #         gr.Slider(label='Max New Tokens', minimum=10, maximum=100,interactive=True)     
            #         gr.Slider(label='Temperature', minimum=0.1, maximum=1.0)
            #         gr.Slider(label='Top-p', minimum=0.1, maximum=1.0)
                # with gr.Column(scale=2):
            gr.ChatInterface(
                predict,
                retry_btn="🔄重试",undo_btn="↩️撤回",clear_btn="🗑️清空",
                # examples=["hi,how are you","你好，我是小红，你叫什么名字？"]
            )

                
            # sidebar_state = gr.State(False)
            # btn_toggle_sidebar = gr.Button("Toggle Sidebar")
            # btn_toggle_sidebar.click(toggle_sidebar, [sidebar_state], [sidebar_left, sidebar_state])
        if port:
            block.launch(server_name=host, share=share, server_port=port)
        else:
            block.launch(server_name=host, share=share)
