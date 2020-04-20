from woocommerce import API
import csv

wcapi = API(
  url="http://server764802.nazwa.pl/wordpress",
  consumer_key="ck_28c44a0b2526deeac2791f629e51a394f281b1ad",
  consumer_secret="cs_30e4817bbba122d6cf28c694d14f58f4c061bdbe",
  wp_api=True,
  version="wc/v3",
  timeout=120
)

def get_baselinker_products():
    products = []
    with open('bs.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            product = {}
            data = {}
            product_id = row['products_id']
            data['auction_id'] = row['auction_id']
            data['products_variant_id'] = row['products_variant_id']
            product[product_id] = data
            products.append(product)
    return products

def update_simple_product_woo(product_id, auction_id):
    data = {}
    meta_data_list = []

    allegro_meta = {}

    allegro_meta['key'] = '_allegro_auction_id'
    allegro_meta['value'] = auction_id

    meta_data_list.append(allegro_meta)

    data['meta_data'] = meta_data_list

    try:
        response = wcapi.put("products/{}".format(product_id), data).json()
        if response['status'] == 'publish':
            print('product_id: {} successfully added'.format(product_id))
        else:
            print('Problem occurred while trying to add product_id: {}'.format(product_id))
    except Exception:
        print('Problem occurred while trying to add product_id: {}'.format(product_id))

def update_product_with_variation_woo(product_id, products_variant_id, auction_id):
    data = {}
    meta_data_list = []

    allegro_meta = {}

    allegro_meta['key'] = '_allegro_auction_id'
    allegro_meta['value'] = auction_id

    meta_data_list.append(allegro_meta)

    data['meta_data'] = meta_data_list
    try:
        response = wcapi.put('products/{}/variations/{}'.format(product_id, products_variant_id), data).json()
        if response['status'] == 'publish':
            print('product_id: {} successfully added'.format(product_id))
        else:
            print('Problem occurred while trying to add product_id: {}'.format(product_id))
            print(response)
    except Exception:
        print('Problem occurred while trying to add product_id: {}'.format(product_id))
        print(response)

def sync_auction_id_with_woocommerce_products(bs_products):
    for product in bs_products:
        for key, val in product.items():
            if val['products_variant_id'] == '0':
                update_simple_product_woo(key, val['auction_id'])
            else:
                update_product_with_variation_woo(key, val['products_variant_id'], val['auction_id'])

if __name__ == "__main__":
    products = get_baselinker_products()
    sync_auction_id_with_woocommerce_products(products)