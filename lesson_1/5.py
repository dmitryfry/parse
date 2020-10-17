import json
import requests
import pdb
import time

# {
# "name": "имя категории",
# "code": "Код соответсвующий категории (используется в запросах)",
# "products": [{PRODUCT},  {PRODUCT}........] # список словарей товаров соответсвующих данной категории
# }

class Parser5ka:
    __params = {
        'records_per_page': 50,
    }

    def __init__(self, start_url, categories_url):
        self.start_url = start_url
        self.categories_url = categories_url

    def categories(self, url=None):
        if not url:
            url = self.categories_url
        response = requests.get(url)
        categories: dict = response.json()
        return categories

    def parse(self, url=None, categories=None):
        if not url:
            url = self.start_url
        params = self.__params
        for category in categories:
            category_data = []
            while url:
                # pdb.set_trace()
                params['categories'] = int(category['parent_group_code'])

                response = requests.get(url, params=params)
                if params:
                    params = {}
                data: dict = response.json()
                if data['next'] == None:
                    print(category['parent_group_name'])
                    print('break')
                    break
                elif data['next']:
                    print(category['parent_group_name'])
                    print(data['next'])
                    url = data['next']
                    category_data.append(data['results'])
                time.sleep(0.1)
            json_data = {
                "name": category['parent_group_name'],
                "code": category['parent_group_code'],
                "products": category_data
            }
            self.save_to_json_file(json_data, category['parent_group_name'])

    def save_to_json_file(self, json_data, category_name):
        with open(f'products/{category_name}.json', 'w', encoding='UTF-8') as file:
            json.dump(json_data, file, ensure_ascii=False)


if __name__ == '__main__':
    parser = Parser5ka('https://5ka.ru/api/v2/special_offers/', 'https://5ka.ru/api/v2/categories/')
    parser.categories()
    parser.parse(categories=parser.categories())
