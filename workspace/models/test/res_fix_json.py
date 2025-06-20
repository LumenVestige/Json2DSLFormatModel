import json

from utils.json_compress import flatten_json

json_data = """
{
    "articles": [
        {
            "slug": "Ill-quantify-the-redundant-TCP-bus-that-should-hard-drive-the-ADP-bandwidth!-553",
            "title": "Ill quantify the redundant TCP bus, that should hard drive the ADP bandwidth!",
            "description": "Aut facilis qui. Cupiditate sit ratione eum sunt rerum impedit. Qui suscipit debitis et et voluptates voluptatem voluptatibus. Quas voluptatum quae corporis corporis possimus.",
            "body": "Quis nesciunt ut est eos.\\nQui reiciendis doloribus.\\nEst quidem ullam reprehenderit.\\nEst omnis eligendi quis quis quo eum officiis asperiores quis. Et sed dicta eveniet accusamus consequatur.\\nUllam voluptas consequatur aut eos ducimus.\\nId officia est ut dicta provident beatae ipsa. Pariatur quo neque est perspiciatis non illo rerum expedita minima.\\nEt commodi voluptas eos ex.\\nUnde velit delectus deleniti deleniti non in sit.\\nAliquid voluptatem magni. Iusto laborum aperiam neque delectus consequuntur provident est maiores explicabo. Est est sed itaque necessitatibus vitae officiis.\\nIusto dolores sint eveniet quasi dolore quo laborum esse laboriosam.\\nModi similique aut voluptates animi aut dicta dolorum.\\nSint explicabo autem quidem et.\\nNeque aspernatur assumenda fugit provident. Et fuga repellendus magnam dignissimos eius aspernatur rerum. Dolorum eius dignissimos et magnam voluptate aut voluptatem natus.\\nAut sint est eum molestiae consequatur officia omnis.\\nQuae et quam odit voluptatum itaque ducimus magni dolores ab.\\nDolorum sed iure voluptatem et reiciendis. Eveniet sit ipsa officiis laborum.\\nIn vel est omnis sed impedit quod magni.\\nDignissimos quis illum qui atque aut ut quasi sequi. Eveniet sit ipsa officiis laborum.\\nIn vel est omnis sed impedit quod magni.\\nDignissimos quis illum qui atque aut ut quasi sequi. Sapiente vitae culpa ut voluptatem incidunt excepturi voluptates exercitationem.\\nSed doloribus alias consectetur omnis occaecati ad placeat labore.\\nVoluptate consequatur expedita nemo recusandae sint assumenda.\\nQui vel totam quia fugit saepe suscipit autem quasi qui.\\nEt eum vel ut delectus ut nesciunt animi.",
            "tagList": [
                "sit",
                "reiciendis",
                "consequuntur",
                "nihil"
            ],
            "createdAt": "2024-01-04T00:52:58.601Z",
            "updatedAt": "2024-01-04T00:52:58.601Z",
            "favorited": false,
            "favoritesCount": 697,
            "author": {
                "username": "Maksim Esteban",
                "bio": null,
                "image": "https://api.realworld.io/images/demo-avatar.png",
                "following": false
            }
        },
        {
            "slug": "quantifying-the-circuit-wont-do-anything-we-need-to-parse-the-back-end-FTP-interface!-553",
            "title": "quantifying the circuit wont do anything, we need to parse the back-end FTP interface!",
            "description": "Quo voluptatem quia numquam laudantium sit quibusdam aut. Veritatis omnis neque ea saepe hic enim. Nam odit dolor non consequuntur perspiciatis inventore ut sint. Velit quod praesentium adipisci modi.",
            "body": "Quos pariatur tenetur.\\nQuasi omnis eveniet eos maiores esse magni possimus blanditiis.\\nQui incidunt sit quos consequatur aut qui et aperiam delectus.\\nPraesentium quas culpa.\\nEaque occaecati cumque incidunt et. Laborum est maxime enim accusantium magnam.\\nRerum dolorum minus laudantium delectus eligendi necessitatibus quia.\\nDeleniti consequatur explicabo aut nobis est vero tempore.\\nExcepturi earum quo quod voluptatem quo iure vel sapiente occaecati.\\nConsectetur consequatur corporis doloribus omnis harum voluptas esse amet. Quia quo iste et aperiam voluptas consectetur a omnis et.\\nDolores et earum consequuntur sunt et.\\nEa nulla ab voluptatem dicta vel. Officia consectetur quibusdam velit debitis porro quia cumque.\\nSuscipit esse voluptatem cum sit totam consequatur molestiae est.\\nMollitia pariatur distinctio fugit. Officia consectetur quibusdam velit debitis porro quia cumque.\\nSuscipit esse voluptatem cum sit totam consequatur molestiae est.\\nMollitia pariatur distinctio fugit. Ab rerum eos ipsa accusantium nihil voluptatem.\\nEum minus alias.\\nIure commodi at harum.\\nNostrum non occaecati omnis quisquam. Sapiente maxime sequi. Quia quo iste et aperiam voluptas consectetur a omnis et.\\nDolores et earum consequuntur sunt et.\\nEa nulla ab voluptatem dicta vel. Similique et quos maiores commodi exercitationem laborum animi qui. Consequatur exercitationem asperiores quidem fuga rerum voluptas pariatur.\\nRepellendus sit itaque nam.\\nDeleniti consectetur vel aliquam vitae est velit.\\nId blanditiis ullam sed consequatur omnis.",
            "tagList": [
                "at",
                "quasi",
                "ullam",
                "nemo"
            ],
            "createdAt": "2024-01-04T00:52:58.600Z",
            "updatedAt": "2024-01-04T00:52:58.600Z",
            "favorited": false,
            "favoritesCount": 292,
            "author": {
                "username": "Maksim Esteban",
                "bio": null,
                "image": "https://api.realworld.io/images/demo-avatar.png",
                "following": false
            }
        }
    ],
    "articlesCount": 251
}
"""

res = flatten_json(json.loads(json_data))
print(res)
