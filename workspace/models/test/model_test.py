from models.index import create_main_eval_model, create_backup_eval_model

json_data = """
{
  "page_title": "探索美丽的巴黎",
  "header": {
    "title": "欢迎来到巴黎",
    "subtitle": "探索浪漫与文化的城市"
  },
  "sections": [
    {
      "type": "text",
      "content": "巴黎，被誉为‘光之城’，是一座充满历史、艺术和文化的城市，吸引了无数游客前来探索。无论是参观世界著名的卢浮宫，还是在塞纳河畔漫步，巴黎总能给您带来难忘的体验。"
    },
    {
      "type": "image",
      "src": "https://example.com/images/paris.jpg",
      "alt": "巴黎景观"
    },
    {
      "type": "video",
      "src": "https://example.com/videos/paris_tour.mp4",
      "alt": "巴黎旅行视频"
    },
    {
      "type": "list",
      "title": "巴黎的必游景点",
      "items": [
        "埃菲尔铁塔",
        "卢浮宫博物馆",
        "巴黎圣母院",
        "塞纳河游船",
        "蒙马特高地"
      ]
    },
    {
      "type": "text",
      "content": "在巴黎，您不仅能享受美丽的景点，还能品尝到顶级的法式美食。每一条街道、每一个角落都充满了魅力。"
    },
    {
      "type": "card",
      "title": "旅游套餐",
      "content": "提供专属巴黎旅游套餐，包括一日游、奢华酒店住宿、私人导游等。",
      "cta": {
        "text": "立即预订",
        "href": "https://example.com/book-now"
      }
    }
  ],
  "footer": {
    "contact": {
      "phone": "+33 1 23 45 67 89",
      "email": "contact@paristour.com"
    },
    "social_links": [
      {
        "platform": "Facebook",
        "href": "https://facebook.com/paristour"
      },
      {
        "platform": "Instagram",
        "href": "https://instagram.com/paristour"
      }
    ]
  }
}

"""

main_model = create_main_eval_model()
print('main_model', main_model.get_result(json_data))
backup_model = create_backup_eval_model()
print('model', backup_model.get_result(json_data))
