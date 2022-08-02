import re
from bs4 import BeautifulSoup as bs
import requests
import json


cost_gaps = ['do-3-mln', 'do-1500000', 'do-800000', 'do-500000']
total = []
region = []
url_stock_segments = {
    'do-3-mln': ['X', 'MzAwMDAwMH0'],
    'do-1500000': ['X','MTUwMDAwMH0'],
    'do-800000': ['W','ODAwMDAwfQ'],
    'do-500000': ['W','NTAwMDAwfQ']
}
value_stock_segments = {
    'do-3-mln': '',
    'do-1500000': '',
    'do-800000': '',
    'do-500000': ''
}

fix_value_stock_segments = {
    'over-3-mln': '',
    'do-3-mln': '',
    'do-1500000': '',
    'do-800000': '',
    'do-500000': ''
}
headers = {'accept': '*/*',
           'user-agent':
               'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36'}


def get_total(url: str) -> None:
    # https://www.avito.ru/sim-yaroslavl/yaroslavl?page_from=from_shops_list
    get_region = url.split('/')[-1]
    region.append(get_region)
    r = requests.get(url, headers).text
    soup = bs(r, 'html.parser')
    soups = soup.find('span', class_='breadcrumbs-link-count js-breadcrumbs-link-count')
    select = re.findall('\d', str(soups))
    total_numb = int(''.join(select))
    print(f'total: {total_numb}')
    total.append(total_numb)
    split_stock_in_costs(url)


def split_stock_in_costs(url: str) -> None:
    middle_url = '-rubley-ASgCAgECAUXGmgw'
    end_url = 'eyJmcm9tIjowLCJ0byI6'
    for k, v in url_stock_segments.items():
        final_url = f'{url}/avtomobili/{k}{middle_url}{v[0]}{end_url}{v[1]}'
        try:
            r = requests.get(final_url, headers).text
            soup = bs(r, 'html.parser')
            soups = soup.find('span', class_='breadcrumbs-link-count js-breadcrumbs-link-count')
            select_numb = re.findall('\d', str(soups))
            select = int(''.join(select_numb))
            if select:
                value_stock_segments[k] = select
            else:
                value_stock_segments[k] = 0
        except:
            value_stock_segments[k] = 0
    print(f'value_stock {value_stock_segments}')


def calculate_func() -> int:
    with open('tarif_net.json', 'r') as json_obj:
        json_data = json.load(json_obj)
        price_for_region = json_data[region[0]]
    sum_without_sale = 0
    for k, v in fix_value_stock_segments.items():
        print(f'k {k}')
        print(f'v {v}')
        if v or k is not None:
            x = price_for_region.get(k)# * v
            print(x)
            # sum_without_sale += int(x)
            # print(type(x), x)
    return sum_without_sale


def fix_count_in_segments() -> None:
    for k, v in value_stock_segments.items():
        if k == 'do-3-mln':
            fix_value_stock_segments['over-3-mln'] = total[0] - v
        elif k == 'do-1500000':
            fix_value_stock_segments['do-3-mln'] = value_stock_segments['do-3-mln'] - v
        elif k == 'do-800000':
            fix_value_stock_segments['do-1500000'] = value_stock_segments['do-1500000'] - v
        elif k == 'do-500000':
            fix_value_stock_segments['do-800000'] = value_stock_segments['do-800000'] - v
            fix_value_stock_segments['do-500000'] = value_stock_segments['do-500000']
    print(f'fix_value {fix_value_stock_segments}')


if __name__ == '__main__':
    print(fix_value_stock_segments)
    url = input("Введи ссылку на магазин и нажми Enter: ")
    get_total(url)
    fix_count_in_segments()
    print(f' total sum {calculate_func()}')

