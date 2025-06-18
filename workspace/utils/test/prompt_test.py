import json

from utils.create_prompt import replace_values, compress_json

json_data = """
{
  "data": [
    {
      "id": "1",
      "name": "John Doe",
      "age": 35,
      "isMember": true,
      "preferences": {
        "colors": ["blue", "green", "red"],
        "food": {
          "favorite": "pizza",
          "dislike": "broccoli"
        }
      },
      "contacts": [
        {
          "type": "email",
          "details": "johndoe@example.com"
        },
        {
          "type": "phone",
          "details": "+123456789"
        }
      ],
      "transactions": [
        {
          "date": "2023-10-01",
          "amount": 150.75,
          "items": [
            {"name": "book", "price": 25.5, "quantity": 2},
            {"name": "pen", "price": 2.5, "quantity": 5}
          ]
        },
        {
          "date": "2023-10-15",
          "amount": 299.99,
          "items": [
            {"name": "headphones", "price": 299.99, "quantity": 1}
          ]
        }
      ]
    },
    {
      "id": "2",
      "name": "Jane Smith",
      "age": 28,
      "isMember": false,
      "preferences": {
        "colors": ["purple", "yellow"],
        "food": {
          "favorite": "sushi",
          "dislike": "cheese"
        }
      },
      "contacts": [
        {
          "type": "email",
          "details": "janesmith@example.com"
        }
      ],
      "transactions": [
        {
          "date": "2023-09-22",
          "amount": 45.0,
          "items": [
            {"name": "notebook", "price": 15.0, "quantity": 3}
          ]
        }
      ]
    }
  ],
  "meta": {
    "recordCount": 2,
    "generatedAt": "2024-11-01T12:34:56Z"
  }
}

"""

json_data2 = """
{
  "feeds": [
    {"id": 1, "title": "title_1", "description": "description_1", "url": "url_1"},
    {"id": 2, "title": "title_2", "description": "description_2", "url": "url_2"}
  ]
}
"""
json_data4 = """
{
  "ttt": [
    {
      "id": "101",
      "type": "news",
      "title": "Breaking News Headline",
      "content": "Summary of the news goes here.",
      "images": [
        {
          "url": "https://example.com/news1.jpg",
          "description": "News Image 1"
        },
        {
          "url": "https://example.com/news2.jpg",
          "description": "News Image 2"
        }
      ],
      "details": {
        "author": "Reporter A",
        "pubTime": "2023-11-01T10:30:00Z",
        "comments": [
          {
            "user": "User1",
            "text": "Great article!",
            "likes": 25
          },
          {
            "user": "User2",
            "text": "Interesting perspective.",
            "likes": 18
          }
        ]
      }
    },
    {
      "id": "202",
      "type": "blog",
      "title": "A Guide to Coding Practices",
      "content": "This blog post discusses best practices in coding.",
      "author": {
        "name": "Tech Blogger",
        "profileUrl": "https://example.com/profile/techblogger"
      },
      "tags": ["coding", "best practices", "development"],
      "stats": {
        "views": 1500,
        "likes": 300,
        "shares": 75
      }
    },
    {
      "id": "303",
      "type": "product",
      "title": "New Smartphone Release",
      "description": "The latest model with advanced features.",
      "product": {
        "name": "SmartPhone X",
        "price": "¥9999",
        "features": [
          "6.7-inch display",
          "Triple-lens camera",
          "5G connectivity"
        ]
      },
      "media": {
        "imageUrl": "https://example.com/phone.jpg",
        "videoUrl": "https://example.com/phone_video.mp4"
      }
    }
  ]
}

"""


def test():
    json_obj = json.loads(json_data4)
    old_json = str(json.dumps(replace_values(json_obj), ensure_ascii=False, indent=4))
    new_json = str(json.dumps(replace_values(json_obj), ensure_ascii=False, indent=1))
    compress_json_str = compress_json(new_json)
    compress_json_str2 = str(json.dumps(replace_values(json_obj), ensure_ascii=False, indent=0))
    compress_json_str3 = compress_json(str(json.dumps(replace_values(json_obj), ensure_ascii=False, indent=0)))
    # print(new_json)
    # print(compress_json_str2)
    print(compress_json_str3)
    print(len(old_json), len(compress_json_str3))
    # print("compress_json_str:" + compress_json_str)
    # json_str = decompress_json(compress_json_str)
    # print("json_str:" + json_str)
    print(json.loads(compress_json_str3))

test()
# create_prompt(json_data4)
