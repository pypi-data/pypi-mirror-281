import time
from typing import List, Tuple, Dict,Any,Union
import httpx
from openai import OpenAI
import base64
import io    
import json
import ray
from byzerllm.utils.types import BlockVLLMStreamServer,StreamOutputs,SingleOutput,SingleOutputMeta,BlockBinaryStreamServer
from byzerllm.utils.langutil import asyncfy_with_semaphore
import threading
import asyncio
import traceback
import uuid

class CustomSaasAPI:    

    def __init__(self, infer_params: Dict[str, str]) -> None:
             
        self.api_key = infer_params["saas.api_key"]        
        self.model = infer_params.get("saas.model","gpt-3.5-turbo-1106")
        
        other_params = {}

        if "saas.api_base" in infer_params:
            other_params["api_base"] = infer_params["saas.api_base"]
        
        if "saas.api_version" in infer_params:
            other_params["api_version"] = infer_params["saas.api_version"]
        
        if "saas.api_type" in infer_params:
            other_params["api_type"] = infer_params["saas.api_type"]

        if "saas.base_url" in infer_params:
            other_params["base_url"] = infer_params["saas.base_url"]    

        if "saas.timeout" in infer_params:
            other_params["timeout"] = float(infer_params["saas.timeout"]    )
        
        self.max_retries = int(infer_params.get("saas.max_retries",10))

        self.meta = {
            "model_deploy_type": "saas",
            "backend":"saas",
            "support_stream": True,
            "model_name": self.model,

        }

        self.meta["embedding_mode"] = "embedding"  in  self.model.lower()
                    
        self.proxies = infer_params.get("saas.proxies", None)
        self.local_address = infer_params.get("saas.local_address", "0.0.0.0")
                
        
        if not self.proxies:
            self.client = OpenAI(**other_params,api_key=self.api_key)  
        else:
            self.client = OpenAI(**other_params,api_key=self.api_key,http_client=httpx.Client(
                proxies=self.proxies,
                transport=httpx.HTTPTransport(local_address=self.local_address)))         
    
        try:
            ray.get_actor("BLOCK_VLLM_STREAM_SERVER") 
        except ValueError:  
            try:          
                ray.remote(BlockVLLMStreamServer).options(name="BLOCK_VLLM_STREAM_SERVER",lifetime="detached",max_concurrency=1000).remote()
            except Exception as e:
                pass    
        try:
            ray.get_actor("BlockBinaryStreamServer")    
        except ValueError:  
            try:          
                ray.remote(BlockBinaryStreamServer).options(name="BlockBinaryStreamServer",lifetime="detached",max_concurrency=1000).remote()
            except Exception as e:
                pass        
    
    # saas/proprietary
    def get_meta(self):
        return [self.meta]

    def process_input(self, ins: Union[str, List[Dict[str, Any]],Dict[str, Any]]):
        
        if isinstance(ins, list) or isinstance(ins, dict):
            return ins
        
        content = []
        try:
            ins_json = json.loads(ins)
        except:            
            return ins
        
        ## speech
        if isinstance(ins_json, dict):
            return ins_json
        
        content = []
    #     [
    #     {"type": "text", "text": "What’s in this image?"},
    #     {
    #       "type": "image_url",
    #       "image_url": {
    #         "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
    #         "detail": "high"
    #       },
    #     },
    #   ],
        for item in ins_json:
            # for format like this: {"image": "xxxxxx", "text": "What’s in this image?","detail":"high"}
            # or {"image": "xxxxxx"}, {"text": "What’s in this image?"}
            if ("image" in item or "image_url" in item) and "type" not in item:
                image_data = item.get("image",item.get("image_url",""))
                ## "data:image/jpeg;base64," 
                if not image_data.startswith("data:"):
                    image_data = "data:image/jpeg;base64," + image_data 

                ## get the other fields except image/text/image_url
                other_fields = {k:v for k,v in item.items() if k not in ["image","text","image_url"]}
                content.append({"image_url": {"url":image_data,**other_fields},"type": "image_url"})
            if "text" in item and "type" not in item:
                text_data = item["text"]
                content.append({"text": text_data,"type":"text"})
            
            ## for format like this: {"type": "text", "text": "What’s in this image?"},
            ## {"type": "image_url", "image_url": {"url":"","detail":"high"}}
            ## this is the standard format, just return it
            if "type" in item and item["type"] == "text":
                content.append(item)

            if "type" in item and item["type"] == "image_url":                
                content.append(item)

        if not content:
            return ins
        
        return content   
    
    async def async_embed_query(self, ins: str, **kwargs):                     
        resp = await asyncfy_with_semaphore(lambda:self.client.embeddings.create(input = [ins], model=self.model))()
        embedding = resp.data[0].embedding
        usage = resp.usage
        return (embedding,{"metadata":{
                "input_tokens_count":usage.prompt_tokens,
                "generated_tokens_count":0}})

    def embed_query(self, ins: str, **kwargs):                     
        resp = self.client.embeddings.create(input = [ins], model=self.model)
        embedding = resp.data[0].embedding
        usage = resp.usage
        return (embedding,{"metadata":{
                "input_tokens_count":usage.prompt_tokens,
                "generated_tokens_count":0}})
    
    async def async_text_to_speech(self,stream:bool, ins: str, voice:str,chunk_size:int=None,**kwargs):
        if stream:
            server = ray.get_actor("BlockBinaryStreamServer")
            request_id = [None]
            
            def writer():
                try:                                                     
                    request_id[0] = str(uuid.uuid4())                
                    with self.client.with_streaming_response.audio.speech.create(
                                model=self.model,
                                voice=voice,
                                input=ins,**kwargs) as response:               
                        for chunk in response.iter_bytes(chunk_size):                                                                                                                          
                            input_tokens_count = 0
                            generated_tokens_count = 0                                               
                            ray.get(server.add_item.remote(request_id[0], 
                                                            StreamOutputs(outputs=[SingleOutput(text=chunk,metadata=SingleOutputMeta(
                                                                input_tokens_count=input_tokens_count,
                                                                generated_tokens_count=generated_tokens_count,
                                                            ))])
                                                            ))                                                   
                except:
                    traceback.print_exc()            
                ray.get(server.mark_done.remote(request_id[0]))

            
            threading.Thread(target=writer,daemon=True).start()            
                            
            time_count= 10*100
            while request_id[0] is None and time_count > 0:
                time.sleep(0.01)
                time_count -= 1
            
            if request_id[0] is None:
                raise Exception("Failed to get request id")
            
            def write_running():
                return ray.get(server.add_item.remote(request_id[0], "RUNNING"))
                        
            await asyncio.to_thread(write_running)
            return [("",{"metadata":{"request_id":request_id[0],"stream_server":"BlockBinaryStreamServer"}})]                   
    
        start_time = time.monotonic()
        with io.BytesIO() as output:
            async with asyncfy_with_semaphore(lambda:self.client.with_streaming_response.audio.speech.create(
                    model=self.model,
                    voice=voice,
                    input=ins, **kwargs))() as response:                
                for chunk in response.iter_bytes():
                    output.write(chunk)

            base64_audio = base64.b64encode(output.getvalue()).decode()
            time_cost = time.monotonic() - start_time        
            return [(base64_audio,{"metadata":{
                            "request_id":"",
                            "input_tokens_count":0,
                            "generated_tokens_count":0,
                            "time_cost":time_cost,
                            "first_token_time":0,
                            "speed":0,        
                        }})]                               

    def speech_to_text(self, ins: str, **kwargs):
        pass

    def image_to_text(self, ins: str, **kwargs):
        pass

    async def async_text_to_image(self, stream:bool, input: str,size:str,quality:str,n:int, **kwargs): 
        if stream:
            raise Exception("Stream not supported for text to image")
        start_time = time.monotonic()       
        response = await asyncfy_with_semaphore(lambda:self.client.images.generate(
                                    model=self.model,
                                    prompt=input,
                                    size=size,
                                    quality=quality,
                                    n=1,
                                    response_format="b64_json",
                                    **kwargs
                                    ))()
        time_cost = time.monotonic() - start_time
        base64_image = response.data[0].b64_json
        return [(base64_image,{"metadata":{
                            "request_id":"",
                            "input_tokens_count":0,
                            "generated_tokens_count":0,
                            "time_cost":time_cost,
                            "first_token_time":0,
                            "speed":0,        
                        }})]


    def text_to_text(self, ins: str, **kwargs):
        pass

    async def async_stream_chat(self, tokenizer, ins: str, his: List[Dict[str, Any]] = [],
                    max_length: int = 4096,
                    top_p: float = 0.7,
                    temperature: float = 0.9, **kwargs):

        model = self.model        

        if "model" in kwargs:
            model = kwargs["model"] 
        
        messages = [{"role":message["role"],"content":self.process_input(message["content"])} for message in his] + [{"role": "user", "content": self.process_input(ins)}]

        stream = kwargs.get("stream",False)
        
        ## content = [
        ##    "voice": "alloy","input": "Hello, World!",response_format: "mp3"]
        last_message = messages[-1]["content"]
        
        if isinstance(last_message,dict) and "voice" in last_message:
            voice = last_message["voice"]
            response_format = last_message.get("response_format","mp3")
            chunk_size = last_message.get("chunk_size",None)
            input = last_message["input"]            
            return await self.async_text_to_speech(stream=stream,
                                             ins=input,
                                             voice=voice,
                                             chunk_size=chunk_size,
                                             response_format=response_format)
        
        if isinstance(last_message,dict) and "input" in last_message:
            input = last_message["input"]
            size = last_message.get("size","1024x1024")
            quality = last_message.get("quality","standard")
            n = last_message.get("n",1)            
            return await self.async_text_to_image(stream=stream,input=input,size=size,quality=quality,n=n)        

        
        server = ray.get_actor("BLOCK_VLLM_STREAM_SERVER")
        request_id = [None]
        
        def writer():
            try:
                r = ""       
                response = self.client.chat.completions.create(
                                    messages=messages,
                                    model=model,
                                    stream=True, 
                                    max_tokens=max_length,
                                    temperature=temperature,
                                    top_p=top_p                                                                        
                                )    
                # input_tokens_count = 0     
                # generated_tokens_count = 0
                
                request_id[0] = str(uuid.uuid4())                

                for chunk in response:                                                              
                    content = chunk.choices[0].delta.content or ""
                    r += content        
                    if hasattr(chunk,"usage") and chunk.usage:
                        input_tokens_count = chunk.usage.prompt_tokens
                        generated_tokens_count = chunk.usage.completion_tokens
                    else:
                        input_tokens_count = 0
                        generated_tokens_count = 0
                    ray.get(server.add_item.remote(request_id[0], 
                                                    StreamOutputs(outputs=[SingleOutput(text=r,metadata=SingleOutputMeta(
                                                        input_tokens_count=input_tokens_count,
                                                        generated_tokens_count=generated_tokens_count,
                                                    ))])
                                                    ))                                                   
            except:
                traceback.print_exc()            
            ray.get(server.mark_done.remote(request_id[0]))

        if stream:
            threading.Thread(target=writer,daemon=True).start()            
                            
            time_count= 10*100
            while request_id[0] is None and time_count > 0:
                time.sleep(0.01)
                time_count -= 1
            
            if request_id[0] is None:
                raise Exception("Failed to get request id")
            
            def write_running():
                return ray.get(server.add_item.remote(request_id[0], "RUNNING"))
                        
            await asyncio.to_thread(write_running)
            return [("",{"metadata":{"request_id":request_id[0],"stream_server":"BLOCK_VLLM_STREAM_SERVER"}})]
        else:
            try:
                start_time = time.monotonic()
                response = await asyncfy_with_semaphore(lambda:self.client.chat.completions.create(
                                    messages=messages,
                                    model=model,
                                    max_tokens=max_length,
                                    temperature=temperature,
                                    top_p=top_p                            
                                ))()

                generated_text = response.choices[0].message.content
                generated_tokens_count = response.usage.completion_tokens
                input_tokens_count = response.usage.prompt_tokens
                time_cost = time.monotonic() - start_time
                return [(generated_text,{"metadata":{
                            "request_id":response.id,
                            "input_tokens_count":input_tokens_count,
                            "generated_tokens_count":generated_tokens_count,
                            "time_cost":time_cost,
                            "first_token_time":0,
                            "speed":float(generated_tokens_count)/time_cost,        
                        }})]
            except Exception as e:
                print(f"Error: {e}")
                raise e