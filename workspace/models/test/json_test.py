import json

json_str = """
{
	"t": "d",
	"a": "s=d:block",
	"c": [{
				"t": "d",
				"a": "s=d:block",
				"c": [{
					"t": "d",
					"a": "s=d:block",
					"c": [{
						"t": "d",
						"a": "s=d:block",
						"c": [{
							"t": "im",
							"a": "src=url_request-example.com/h1.jpg"
						}]
					}, {
						"t": "d",
						"a": "s=d:block",
						"c": [{
							"t": "im",
							"a": "src=url_request-example.com/h2.jpg"
						}]
					}]
				}, {
					"t": "d",
					"a": "s=d:block",
					"c": [{
						"t": "d",
						"a": "s=d:block",
						"c": [{
							"t": "d",
							"a": "s=d:block",
							"c": [{
								"t": "d",
								"a": "s=d:block",
								"c": [{
									"t": "im",
									"a": "src=url_request-example.com/icon1.png"
								}]
							}, {
								"t": "d",
								"a": "s=d:block",
								"c": [{
									"t": "im",
									"a": "src=url_request-example.com/icon2.png"
								}]
							}]
						}]
					}, {
						"t": "d",
						"a": "s=d:block",
						"c": [{
							"t": "d",
							"a": "s=d:block",
							"c": [{
								"t": "d",
								"a": "s=d:block",
								"c": [{
									"t": "d",
									"a": "s=d:block",
									"c": [{
										"t": "im",
										"a": "src=url_request-example.com/photo1.jpg"
									}]
								}]
							}, {
								"t": "d",
								"a": "s=d:block",
								"c": [{
									"t": "d",
									"a": "s=d:block",
									"c": [{
										"t": "im",
										"a": "src=url_request-example.com/photo2.jpg"
									}]
								}]
							}]
						}]
					}, {
						"t": "d",
						"a": "s=d:block",
						"c": [{
							"t": "d",
							"a": "s=d:block",
							"c": [{
								"t": "d",
								"a": "s=d:block",
								"c": [{
									"t": "d",
									"a": "s=d:block",
									"c": [{
										"t": "im",
										"a": "src=url_request-example.com/icon3.png"
									}]
								}, {
									"t": "d",
									"a": "s=d:block",
									"c": [{
										"t": "im",
										"a": "src=url_request-example.com/icon4.png"
									}]
								}]
							}]
						}]
					}]
				}, {
					"t": "d",
					"a": "s=d:block",
					"c": [{
						"t": "d",
						"a": "s=d:block",
						"c": [{
							"t": "d",
							"a": "s=d:block",
							"c": [{
								"t": "a",
								"a": "l=url_request-example.com/about"
							}]
						}, {
							"t": "d",
							"a": "s=d:block",
							"c": [{
								"t": "a",
								"a": "l=url_request-example.com/contact"
							}]
						}, {
							"t": "d",
							"a": "s=d:block",
							"c": [{
								"t": "a",
								"a": "l=url_request-example.com/privacy"
							}]
						}]
					}]
				}]
			}
        """

from half_json.core import JSONFixer

# 一个不完整的 JSON 字符串（缺少右括号）
invalid_json = '{"name": "John", "age": 30'
f = JSONFixer()
# 使用 jsonfixer 来修复它
fixed_json = f.fix(json_str)
if fixed_json.success:
    print(json.loads(fixed_json.line))
