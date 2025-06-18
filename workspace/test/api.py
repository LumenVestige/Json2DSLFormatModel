import json

import requests

url = "http://172.18.15.169:8099/dsl2"

data = {
	"a": {
		"b": "图片",
		"c": [{
			"d": "https://example.com/image1.jpg",
			"e": "风景",
			"f": {
				"g": "自然",
				"h": "山景"
			}
		}, {
			"d": "https://example.com/image2.jpg",
			"e": "人物",
			"f": {
				"g": "肖像",
				"h": "微笑"
			},
			"i": {
				"j": "摄影师",
				"k": "张三"
			}
		}]
	},
	"l": {
		"m": "新闻",
		"n": [{
			"o": "国际",
			"p": " 俄乌冲突",
			"q": "最新进展",
			"r": "紧张局势升级"
		}, {
			"o": "科技",
			"p": "AI发展",
			"q": "突破",
			"s": "自动驾驶"
		}],
		"t": {
			"u": "国内",
			"v": "经济",
			"w": "政策调整",
			"x": "促进增长"
		}
	},
	"y": {
		"z": "关于我们",
		"aa": "公司简介",
		"ab": "我们是一家专注于科技创新的公司",
		"ac": {
			"ad": "团队",
			"ae": "精英",
			"af": "专业",
			"ag": "热情"
		},
		"ah": {
			"ai": "联系方式",
			"aj": "电话",
			"ak": "123-456-7890",
			"al": "邮箱",
			"am": "info@example.com"
		}
	},
	"an": {
		"ao": "产品列表",
		"ap": [{
			"aq": "产品1",
			"ar": "智能音箱",
			"as": "https://example.com/product1.jpg",
			"at": "语音助手"
		}, {
			"aq": "产品2",
			"ar": "智能手表",
			"as": "https://example.com/product2.jpg",
			"at": "健康监测"
		}, {
			"aq": "产品3",
			"ar": "智能眼镜",
			"as": "https://example.com/product3.jpg",
			"at": "AR体验",
			"au": {
				"av": "特色",
				"aw": "高清显示"
			}
		}]
	}
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(url, data={"data": json.dumps(data, ensure_ascii=True)})
print(response.status_code)
print(response.text)
