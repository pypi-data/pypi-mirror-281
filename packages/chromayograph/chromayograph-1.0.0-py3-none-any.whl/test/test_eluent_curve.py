import datetime
import unittest
import requests
import json
from app import create_app


class TestEluentCurveAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # self.url = 'http://127.0.0.1:5000/api/eluent/get_curve'  # 根据你的实际API URL进行调整

    def test_get_curve(self):
        print("-------------------")
        response = self.client.get('/api/eluent/get_curve')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()  # 使用 get_json() 方法解析响应数据
        self.assertIn('message', data)
        self.assertIn('point', data)

        eluent_point = data['point']
        self.assertIn('time', eluent_point)
        self.assertIn('value', eluent_point)

        # 验证时间格式
        try:
            datetime.datetime.strptime(eluent_point['time'], "%H:%M:%S")
        except ValueError:
            self.fail("Incorrect time format")

        # 验证 value 是否在 [0, 1] 范围内
        value = float(eluent_point['value'])
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 100)


if __name__ == '__main__':
    unittest.main()
