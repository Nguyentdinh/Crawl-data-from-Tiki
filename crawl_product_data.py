import pandas as pd
import requests
import time
import random
from tqdm import tqdm

cookies = {'_trackity': '53347a54-a007-ed47-cacc-d4c0707b92df', 'delivery_zone': 'Vk4wMzQwMjQwMTM', '_ga': 'GA1.1.1259996088.1728841653', '_gcl_au': '1.1.1188771562.1728841657', '_fbp': 'fb.1.1728841659550.40172164066093682', '__uidac': '35a750269dae4c10554548ac772fa161', '__iid': '749', '__su': '0', '__RC': '4', '__R': '1', '__tb': '0', 'tiki_client_id': '1259996088.1728841653', '_hjSessionUser_522327': 'eyJpZCI6IjY0OTQyMTBlLWViYWMtNWRjYi04ZmJiLTRmZTBjNjQ2NWMxNiIsImNyZWF0ZWQiOjE3Mjg4NDE2NTkzNTUsImV4aXN0aW5nIjp0cnVlfQ', 'TOKENS': '{%22access_token%22:%22P4oSj26vzQLr7qcnWGCTluh1d5VxwKUB%22}', '__utm': 'source%3Dgoogle%7Cmedium%3Dcpc%7Ccampaign%3DSEA_NBR_GGL_PMA_DAP_ALL_VN_ALL_UNK_UNK_C.PMAX_X.21434089152_Y.167617706789_V._W.DT_A._O.CIR', 'dtdz': '_PID.1.3a28f3f072015b29', '_gcl_gs': '2.1.k1$i1732182078$u165506106', '_gcl_aw': 'GCL.1732182082.CjwKCAiArva5BhBiEiwA-oTnXQMAkrQjEJeqFEuGD5U2UDsOzehsSjOpDIm61rcpYy5Y_8SgJ80hshoCE88QAvD_BwE', 'cto_bundle': 'CTZVI19LYlZsSndOMkJPNzNJdDFWbXRMVUJzT2ZVZk0zZXUydjclMkZaelNkU1h6TWxYMHBaVVZxdHJyV2NUJTJGZ2NXc0Q0MVhub0xUcEtDS1B6T3JwbGhKTlhFVnlEVTN1UzkxVEcyTzBKNkdkbG5GWGZhNDklMkJSVmROMmFXSk5zNU5tTVdjTVFGUHJnN3pqVEZ4THNpbnYlMkJvRnQ3JTJCYXlDcHdhS2s5NTBwdU5BSjAza2N6TVMlMkJpSGc4VSUyRllVQVJON3NRU2F1WFolMkZuNFA0SlN2UnQ5aFNZblVsbFQ4USUzRCUzRA', '_hjSession_522327': 'eyJpZCI6IjczY2FiNWEyLWRjNjYtNDNjYS1iODgzLWZkZTk5YzFjM2I0MCIsImMiOjE3MzI0OTg4ODcxNTQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0', '_dtdcTime': '1732498887', '__adm_upl': 'eyJ0aW1lIjoxNzMyNTAwNjg4LCJfdXBsIjoiMC0zMjU0NTkyMDIzMTA5MDg0NjUyIn0', '__IP': '457740975', '__uif': '__uid%3A3254592023109084652%7C__ui%3A-1%7C__create%3A1675459202', '_ga_S9GLR1RQFJ': 'GS1.1.1732498883.16.1.1732499902.60.0.0', 'amp_99d374': 'mBmGfKaP6wLDG393rzEevM...1idgflv1k.1idggl4g8.d4.hv.v3}'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi',
    'Referer': 'https://tiki.vn/api/v2/reviews?product_id=71345381&include=comments&page=1&limit=-1&top=true&spid=77026805&seller_id=26874',
    'x-guest-token': 'P4oSj26vzQLr7qcnWGCTluh1d5VxwKUB',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = (
    ('platform', 'web'),
    ('spid', 77026805)
)

def parser_product(json):
    d = {}
    d['id'] = json.get('id', None)
    d['sku'] = json.get('sku', None)
    d['name'] = json.get('name', None)
    d['price'] = json.get('price', None)
    d['short_url'] = json.get('short_url', None)
    d['original_price'] = json.get('original_price', None)
    d['discount'] = json.get('discount', None)
    d['discount_rate'] = json.get('discount_rate', None)
    d['review_count'] = json.get('review_count', None)
    d['rating_average'] = json.get('rating_average', None)
    return d

df_id = pd.read_csv('crawled.csv')
p_ids = df_id.id.to_list()
print(p_ids)
result = []
for pid in tqdm(p_ids, total=len(p_ids)):
    response = requests.get(
            'https://tiki.vn/api/v2/products/{}'.format(pid),
            headers=headers,
            cookies=cookies,
            params=params,
        )

    # Kiểm tra nếu phản hồi trống hoặc không phải JSON hợp lệ
    if not response.text.strip():
        print(f"Phản hồi trống cho sản phẩm {pid}, bỏ qua.")
        continue
    
    try:
        # Kiểm tra phản hồi có phải JSON hợp lệ không
        data = response.json()
        print('Crawl data {} success !!!'.format(pid))
        result.append(parser_product(data))
    except requests.exceptions.JSONDecodeError:
        print(f"Lỗi phân tích cú pháp JSON cho sản phẩm {pid}, bỏ qua.")

    # time.sleep(random.randrange(3, 5))

# Tạo DataFrame từ kết quả
df_product = pd.DataFrame(result)
print(df_product)
df_product.to_csv('data.csv', index=False)
