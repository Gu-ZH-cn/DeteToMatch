import requests
import json
import unittest
from unittest.mock import patch

def send_post(url, data, customerCode, storeCode):
    '''
    以POTS请求方式将检测结果和一些配置类Code以json字符串格式发送
    :param url: 服务端地址
    :param data: （dict数据类型）检测结果对象
    :param customerCode: 由配置文件定义的customerCode，随时可以更换
    :param storeCode: 由配置文件定义的storeCode，随时可以更换
    :return: :class:`Response <Response>` 由匹配端传输过来的响应结果确认信息（HTTP状态码）
    :rtype: requests.Response
    '''

    url = url + '/genai/goods/prevention'

    # add 'the code' in configuration to the detection json result
    content = json.loads(data)
    code = {"customerCode":customerCode,"storeCode":storeCode}
    content.update(code)
    content = json.dumps(content)

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=content, headers=headers,timeout=10, allow_redirects=False)
    # print(response)
    return response

# 单元测试案例
class TestSendPost(unittest.TestCase):
    @patch('requests.post')
    def test_send_post(self, mock_post):
        '''
        该测试用例需要首先使用app.py启动flask服务器，再进行测试访问
        '''
        # 设置mock返回值
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"success": true}'
        mock_post.return_value = mock_response
        mock_request = {"goodsInfo": [{"ean": [11,12],"prob": [0.3,0.8]},
                              {"ean": [11,14,15],"prob": [0.3,0.5,0.8]}],
                        "customerCode": "genai",
                        "storeCode": "beijing"
                        }
        mock_json = json.dumps(mock_request)

        '''测试案例使用如下'''
        # 测试数据
        ## 测试地址URL
        url = 'http://127.0.0.1:5000'
        ## （以字典对象形式存储）检测模型的检测结果
        data = {"goodsInfo": [{"ean": [11,12],"prob": [0.3,0.8]},
                              {"ean": [11,14,15],"prob": [0.3,0.5,0.8]}]}
        data = json.dumps(data)
        ## 配置好的一些Code
        customerCode = 'genai'
        storeCode = 'beijing'

        # 调用函数
        response = send_post(url, data, customerCode, storeCode)

        # 验证请求是否正确
        mock_post.assert_called_once_with(
            url + '/genai/goods/prevention',
            json= mock_json,
            headers={'Content-Type': 'application/json'},
            timeout=10,
            allow_redirects=False
        )

        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"success": true}')

if __name__ == '__main__':
    unittest.main()