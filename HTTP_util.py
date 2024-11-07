import requests
import json

def send_post(url, data, customerCode, storeCode):
    '''
    以POTS请求方式将检测结果和一些配置类Code以json字符串格式发送
    :param url: 服务端地址
    :param data: 由检测端发送过来的json字符串内容
    :param customerCode: 由配置文件定义的customerCode，随时可以更换
    :param storeCode: 由配置文件定义的storeCode，随时可以更换
    :return: :class:`Response <Response>` 由匹配端传输过来的响应结果确认信息（HTTP状态码）
    :rtype: requests.Response
    '''

    url = url + '/genai/goods/prevention'

    # add 'the code' in configuration to the detection json result
    content = json.load(data)
    code = {"customerCode":customerCode,"storeCode":storeCode}
    content.update(code)
    content = json.dumps(content)

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=content, headers=headers,timeout=10, allow_redirects=False)
    # print(response)
    return response
