API_KEY = 'bg_80b6837153d312b042744c8f34e854c6'
SECRET_KEY = ''
PASSWORD = ''

usdt_available = None

for currency_info in data['info']:
    if currency_info['currency'] == 'USDT':
        usdt_available = currency_info['available']
        break

print("USDT 可用余额:", usdt_available)

# BGB/USDT 最新报价 1.1064
# {'info': {'orderId': '1231023321824796672',
#            'clientOid': 'd0d37e42-be0c-4e99-bcea-c516e2603157'},
#              'id': '1231023321824796672', 'clientOrderId': 'd0d37e42-be0c-4e99-bcea-c516e2603157',
#                'timestamp': None, 'datetime': None, 'lastTradeTimestamp': None, 
#                'lastUpdateTimestamp': None, 'symbol': 'BGB/USDT', 'type': None, 
#                'side': None, 'price': None, 'amount': None, 'cost': None,
#                  'average': None, 'filled': None, 'remaining': None, 
#                  'timeInForce': None, 'postOnly': None, 'reduceOnly': None, 
#                  'stopPrice': None, 'triggerPrice': None, 'takeProfitPrice': None, 
#                  'stopLossPrice': None, 'status': None, 'fee': None, 'trades': [], 'fees': []}


# USDT 可用余额: 10.000990033166
# 购买时间: 2024-10-18 17:00:00.988
# An error occurred during buying: gateio {"label":"INVALID_PRICE","message":"Market SFT_USDT has no latest price, please try later"}
# 请求耗时（延迟）: 0.018707 秒
# USDT 可用余额: 10.000990033166
# 购买时间: 2024-10-18 17:00:01.111
# An error occurred during buying: gateio {"label":"INVALID_PRICE","message":"Market SFT_USDT has no latest price, please try later"}
# 请求耗时（延迟）: 0.010026 秒
# USDT 可用余额: 10.000990033166
# 购买时间: 2024-10-18 17:00:01.227
# 请求耗时（延迟）: 0.547550 秒
# Buy Order: {'id': '701135123549', 'clientOrderId': 'apiv4', 'timestamp': 1729242001609, 
#             'datetime': '2024-10-18T09:00:01.609Z', 'lastTradeTimestamp': 1729242001772,
#               'status': 'closed', 'symbol': 'SFT/USDT', 'type': 'market', 
#               'timeInForce': 'IOC', 'postOnly': False, 'reduceOnly': None, 
#               'side': 'buy', 'price': 1.32, 'stopPrice': None, 'triggerPrice': None, 
#               'average': 1.32, 'amount': 7.575757575757576, 'cost': 10.0, 'filled': 7.57,
#                 'remaining': 0.005757575757575757, 'fee': None, 'fees': [{'currency': 'GT', 'cost': 0.0}, 
#                 {'currency': 'SFT', 'cost': 0.00757}, {'currency': 'USDT', 'cost': 0.0}], 'trades': [], 
#                 'info': {'id': '701135123549', 'text': 'apiv4', 'amend_text': '-', 
#                          'create_time': '1729242001', 'update_time': '1729242001', 
#                          'create_time_ms': '1729242001609', 'update_time_ms': '1729242001772', 
#                          'status': 'closed', 'currency_pair': 'SFT_USDT', 'type': 'market', 
#                          'account': 'spot', 'side': 'buy', 'amount': '10', 'price': '0', 
#                          'time_in_force': 'ioc', 'iceberg': '0', 'left': '0.0076', 
#                          'filled_amount': '7.57', 'fill_price': '9.9924', 'filled_total': '9.9924',
#                            'avg_deal_price': '1.32', 'fee': '0.00757', 'fee_currency': 'SFT', 'point_fee': '0', 'gt_fee': '0', 'gt_maker_fee': '0', 'gt_taker_fee': '0', 'gt_discount': False, 'rebated_fee': '0', 'rebated_fee_currency': 'USDT', 'finish_as': 'filled'}, 'lastUpdateTimestamp': None, 'takeProfitPrice': None, 'stopLossPrice': None}
# 请求耗时（延迟）: 0.115269 秒
# USDT 可用余额: 0.008590033166
# 请求耗时（延迟）: 0.087478 秒
# Current size: 7.56243
# 出售时间: 2024-10-18 17:00:02.377
# 请求耗时（延迟）: 0.020700 秒
# Sell Order: {'id': '701135128032', 'clientOrderId': 'apiv4', 'timestamp': 1729242002383, 'datetime': '2024-10-18T09:00:02.383Z', 'lastTradeTimestamp': 1729242002385, 'status': 'closed', 'symbol': 'SFT/USDT', 'type': 'market', 'timeInForce': 'IOC', 'postOnly': False, 'reduceOnly': None, 'side': 'sell', 'price': 1.05, 'stopPrice': None, 'triggerPrice': None, 'average': 1.05, 'amount': 7.56, 'cost': 7.938, 'filled': 7.56, 'remaining': 0.0, 'fee': None, 'fees': [{'currency': 'GT', 'cost': 0.0}, {'currency': 'USDT', 'cost': 0.007938}, {'currency': 'SFT', 'cost': 0.0}], 'trades': [], 'info': {'id': '701135128032', 'text': 'apiv4', 'amend_text': '-', 'create_time': '1729242002', 'update_time': '1729242002', 'create_time_ms': '1729242002383', 'update_time_ms': '1729242002385', 'status': 'closed', 'currency_pair': 'SFT_USDT', 'type': 'market', 'account': 'spot', 'side': 'sell', 'amount': '7.56', 'price': '0', 'time_in_force': 'ioc', 'iceberg': '0', 'left': '0', 'filled_amount': '7.56', 'fill_price': '7.938', 'filled_total': '7.938', 'avg_deal_price': '1.05', 'fee': '0.007938', 'fee_currency': 'USDT', 'point_fee': '0', 'gt_fee': '0', 'gt_maker_fee': '0', 'gt_taker_fee': '0', 'gt_discount': False, 'rebated_fee': '0', 'rebated_fee_currency': 'SFT', 'finish_as': 'filled'}, 'lastUpdateTimestamp': None, 'takeProfitPrice': None, 'stopLossPrice': None}


# 程序启动时间: 2024-10-18 17:59:58.489
# Executing trading strategy...
# 请求耗时（延迟）: 2.172498 秒
# USDT 可用余额: 7.938652033166
# 请求耗时（延迟）: 0.046010 秒
# USDT 可用余额: 7.938652033166
# 购买时间: 2024-10-18 18:00:00.708
# Buy Order: {'id': '701165804616', 'clientOrderId': 'apiv4', 'timestamp': 1729245600721, 'datetime': '2024-10-18T10:00:00.721Z', 'lastTradeTimestamp': 1729245600721, 'status': 'open', 'symbol': 'PUFF/USDT', 'type': 'limit', 'timeInForce': 'GTC', 'postOnly': False, 'reduceOnly': None, 'side': 'buy', 'price': 0.06, 'stopPrice': None, 'triggerPrice': None, 'average': None, 'amount': 100.0, 'cost': 0.0, 'filled': 0.0, 'remaining': 100.0, 'fee': None, 'fees': [{'currency': 'GT', 'cost': 0.0}, {'currency': 'PUFF', 'cost': 0.0}, {'currency': 'USDT', 'cost': 0.0}], 'trades': [], 'info': {'id': '701165804616', 'text': 'apiv4', 'amend_text': '-', 'create_time': '1729245600', 'update_time': '1729245600', 'create_time_ms': '1729245600721', 'update_time_ms': '1729245600721', 'status': 'open', 'currency_pair': 'PUFF_USDT', 'type': 'limit', 'account': 'spot', 'side': 'buy', 'amount': '100', 'price': '0.06', 'time_in_force': 'gtc', 'iceberg': '0', 'left': '100', 'filled_amount': '0', 'fill_price': '0', 'filled_total': '0', 'fee': '0', 'fee_currency': 'PUFF', 'point_fee': '0', 'gt_fee': '0', 'gt_maker_fee': '0', 'gt_taker_fee': '0', 'gt_discount': False, 'rebated_fee': '0', 'rebated_fee_currency': 'USDT', 'finish_as': 'open'}, 'lastUpdateTimestamp': None, 'takeProfitPrice': None, 'stopLossPrice': None}
# 请求耗时（延迟）: 0.013158 秒
# USDT 可用余额: 1.938652033166
# 请求耗时（延迟）: 0.031618 秒
# Current size: 10496.28405421

# 购买时间: 2024-10-18 18:00:00.708
# Buy Order: {'id': '701165804616', 'clientOrderId': 'apiv4', 'timestamp': 1729245600721, 'datetime': '2024-10-18T10:00:00.721Z', 'lastTradeTimestamp': 1729245600721, 'status': 'open', 'symbol': 'PUFF/USDT', 'type': 'limit', 'timeInForce': 'GTC', 'postOnly': False, 'reduceOnly': None, 'side': 'buy', 'price': 0.06, 'stopPrice': None, 'triggerPrice': None, 'average': None, 'amount': 100.0, 'cost': 0.0, 'filled': 0.0, 'remaining': 100.0, 'fee': None, 'fees': [{'currency': 'GT', 'cost': 0.0}, {'currency': 'PUFF', 'cost': 0.0}, {'currency': 'USDT', 'cost': 0.0}], 'trades': [], 'info': {'id': '701165804616', 'text': 'apiv4', 'amend_text': '-', 'create_time': '1729245600', 'update_time': '1729245600', 'create_time_ms': '1729245600721', 'update_time_ms': '1729245600721', 'status': 'open', 'currency_pair': 'PUFF_USDT', 'type': 'limit', 'account': 'spot', 'side': 'buy', 'amount': '100', 'price': '0.06', 'time_in_force': 'gtc', 'iceberg': '0', 'left': '100', 'filled_amount': '0', 'fill_price': '0', 'filled_total': '0', 'fee': '0', 'fee_currency': 'PUFF', 'point_fee': '0', 'gt_fee': '0', 'gt_maker_fee': '0', 'gt_taker_fee': '0', 'gt_discount': False, 'rebated_fee': '0', 'rebated_fee_currency': 'USDT', 'finish_as': 'open'}, 'lastUpdateTimestamp': None, 'takeProfitPrice': None, 'stopLossPrice': None}
# 请求耗时（延迟）: 0.013158 秒
# USDT 可用余额: 1.938652033166
# 请求耗时（延迟）: 0.031618 秒
# Current size: 10496.28405421
# 出售时间: 2024-10-18 18:00:01.172
# An error occurred during selling: 
# gateio {"label":"INVALID_PRICE","message":"Market PUFF_USDT has no latest price, please try later"}

Buy Order: {'id': '704136235168', 'clientOrderId': 'apiv4', 'timestamp': 1729584000545, 'datetime': '2024-10-22T08:00:00.545Z', 'lastTradeTimestamp': 1729584000737, 'status': 'closed', 'symbol': 'SCR/USDT', 'type': 'limit', 'timeInForce': 'GTC', 'postOnly': False, 'reduceOnly': None, 'side': 'buy', 'price': 1.375, 'stopPrice': None, 'triggerPrice': None, 'average': 1.34, 'amount': 7.0, 'cost': 9.38, 'filled': 7.0, 'remaining': 0.0, 'fee': None, 'fees': [{'currency': 'GT', 'cost': 0.0}, {'currency': 'SCR', 'cost': 0.007}, {'currency': 'USDT', 'cost': 0.0}], 'trades': [], 'info': {'id': '704136235168', 'text': 'apiv4', 'amend_text': '-', 'create_time': '1729584000', 'update_time': '1729584000', 'create_time_ms': '1729584000545', 'update_time_ms': '1729584000737', 'status': 'closed', 'currency_pair': 'SCR_USDT', 'type': 'limit', 'account': 'spot', 'side': 'buy', 'amount': '7', 'price': '1.375', 'time_in_force': 'gtc', 'iceberg': '0', 'left': '0', 'filled_amount': '7', 'fill_price': '9.38', 'filled_total': '9.38', 'avg_deal_price': '1.34', 'fee': '0.007', 'fee_currency': 'SCR', 'point_fee': '0', 'gt_fee': '0', 'gt_maker_fee': '0', 'gt_taker_fee': '0', 'gt_discount': False, 'rebated_fee': '0', 'rebated_fee_currency': 'USDT', 'finish_as': 'filled'}, 'lastUpdateTimestamp': None, 'takeProfitPrice': None, 'stopLossPrice': None}

Sell Order: {'id': '704136258038', 'clientOrderId': 'apiv4', 'timestamp': 1729584004581, 'datetime': '2024-10-22T08:00:04.581Z', 'lastTradeTimestamp': 1729584004612, 'status': 'closed', 'symbol': 'SCR/USDT', 'type': 'market', 'timeInForce': 'IOC', 'postOnly': False, 'reduceOnly': None, 'side': 'sell', 'price': 1.3716774, 'stopPrice': None, 'triggerPrice': None, 'average': 1.3716774, 'amount': 6.99, 'cost': 9.588025, 'filled': 6.99, 'remaining': 0.0, 'fee': None, 'fees': [{'currency': 'GT', 'cost': 0.0}, {'currency': 'USDT', 'cost': 0.009588025}, {'currency': 'SCR', 'cost': 0.0}], 'trades': [], 'info': {'id': '704136258038', 'text': 'apiv4', 'amend_text': '-', 'create_time': '1729584004', 'update_time': '1729584004', 'create_time_ms': '1729584004581', 'update_time_ms': '1729584004612', 'status': 'closed', 'currency_pair': 'SCR_USDT', 'type': 'market', 'account': 'spot', 'side': 'sell', 'amount': '6.99', 'price': '0', 'time_in_force': 'ioc', 'iceberg': '0', 'left': '0', 'filled_amount': '6.99', 'fill_price': '9.588025', 'filled_total': '9.588025', 'avg_deal_price': '1.3716774', 'fee': '0.009588025', 'fee_currency': 'USDT', 'point_fee': '0', 'gt_fee': '0', 'gt_maker_fee': '0', 'gt_taker_fee': '0', 'gt_discount': False, 'rebated_fee': '0', 'rebated_fee_currency': 'SCR', 'finish_as': 'filled'}, 'lastUpdateTimestamp': None, 'takeProfitPrice': None, 'stopLossPrice': None}
卖出操作已完成，程序终止。

orderer = exchange.fetch_order( orderId,symbols)

{'info': {'userId': '6828086469', 'symbol': 'CANTOUSDT', 'orderId': '1232918849877614599', 'clientOid': 'c9950ff3-2f51-4c5b-90cb-e970f5676596', 'price': '0', 'size': '4.0000000000000000', 'orderType': 'market', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.0260005767320262', 'baseVolume': '153.0000000000000000', 'quoteVolume': '3.9780882400000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":-0.0027620817496963,"deduction":false,"r":0,"t":-0.153,"totalDeductionFee":0},"BGB":{"deduction":true,"feeCoinCode":"BGB","totalDeductionFee":-0.0027620817496963,"totalFee":-0.0027620817496963}}', 'orderSource': 'market', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'CANTO', 'cancelReason': '', 'cTime': '1729676681012', 'uTime': '1729676681087'}, 'id': '1232918849877614599', 'clientOrderId': 'c9950ff3-2f51-4c5b-90cb-e970f5676596', 'timestamp': 1729676681012, 'datetime': '2024-10-23T09:44:41.012Z', 'lastTradeTimestamp': 1729676681087, 'lastUpdateTimestamp': 1729676681087, 'symbol': 'CANTO/USDT', 'type': 'market', 'side': 'buy', 'price': 0.0260005767320262, 'amount': 4.0, 'cost': 3.97808824, 'average': 0.0260005767320262, 'filled': 153.0, 'remaining': -149.0, 'timeInForce': 'IOC', 'postOnly': None, 'reduceOnly': None, 'stopPrice': None, 'triggerPrice': None, 'takeProfitPrice': None, 'stopLossPrice': None, 'status': 'closed', 'fee': {'cost': 0.0027620817496963, 'currency': 'BGB'}, 'trades': [], 'fees': [{'cost': 0.0027620817496963, 'currency': 'BGB'}]}

USDT 可用余额: 4.491437933563
JANET/USDT 最新报价 0.00779
JANET/USDT 准备买入价格: 0.00779
JANET/USDT 准备买入数量: 576
程序启动时间: 2024-10-24 11:59:18.070
Executing trading strategy...
请求耗时（延迟）: 0.061962 秒
USDT 可用余额: 4.491437933563
请求耗时（延迟）: 0.023995 秒
USDT 可用余额: 4.491437933563
购买时间: 2024-10-24 11:59:18.156

Buy Order: {'id': '705645894489', 'clientOrderId': 'apiv4', 'timestamp': 1729742400244, 'datetime': '2024-10-24T04:00:00.244Z', 'lastTradeTimestamp': 1729742400245, 'status': 'closed', 'symbol': 'JANET/USDT', 'type': 'limit', 'timeInForce': 'GTC', 'postOnly': False, 'reduceOnly': None, 'side': 'buy', 'price': 0.00779, 'stopPrice': None, 'triggerPrice': None, 'average': 0.0066, 'amount': 576.0, 'cost': 3.8016, 'filled': 576.0, 'remaining': 0.0, 'fee': None, 'fees': [{'currency': 'GT', 'cost': 0.0003859057071960298}, {'currency': 'JANET', 'cost': 0.0}, {'currency': 'USDT', 'cost': 0.0}], 'trades': [], 'info': {'id': '705645894489', 'text': 'apiv4', 'amend_text': '-', 'create_time': '1729742400', 'update_time': '1729742400', 'create_time_ms': '1729742400244', 'update_time_ms': '1729742400245', 'status': 'closed', 'currency_pair': 'JANET_USDT', 'type': 'limit', 'account': 'spot', 'side': 'buy', 'amount': '576', 'price': '0.00779', 'time_in_force': 'gtc', 'iceberg': '0', 'left': '0', 'filled_amount': '576', 'fill_price': '3.8016', 'filled_total': '3.8016', 'avg_deal_price': '0.0066', 'fee': '0', 'fee_currency': 'JANET', 'point_fee': '0', 'gt_fee': '0.00038590570719602977', 'gt_maker_fee': '0.0009', 'gt_taker_fee': '0.0009', 'gt_discount': True, 'rebated_fee': '0', 'rebated_fee_currency': 'USDT', 'finish_as': 'filled'}, 'lastUpdateTimestamp': None, 'takeProfitPrice': None, 'stopLossPrice': None}
请求耗时（延迟）: 0.083004 秒
USDT 可用余额: 0.689837933563
请求耗时（延迟）: 0.045042 秒
Current size: 576.0
JANET/USDT 最新报价 0.007189
当前买入价格是: 0.0066
更新最大价格: 0.007189
当前价格 0.007189 满足卖出条件，准备卖出。触发条件：最大价格曾经高于买入价的 5%
出售时间: 2024-10-24 12:00:00.920
An error occurred during selling: gateio {"label":"INVALID_PRICE","message":"Market JANET_USDT has no latest price, please try later"}
请求耗时（延迟）: 0.050302 秒
USDT 可用余额: 0.689837933563
请求耗时（延迟）: 0.125947 秒
Current size: 576.0
JANET/USDT 最新报价 0.0073
当前买入价格是: 0.0066
更新最大价格: 0.0073
当前价格 0.0073 满足卖出条件，准备卖出。触发条件：最大价格曾经高于买入价的 5%
出售时间: 2024-10-24 12:00:01.523
An error occurred during selling: gateio {"label":"INVALID_PRICE","message":"Market JANET_USDT has no latest price, please try later"}
请求耗时（延迟）: 0.017156 秒
USDT 可用余额: 0.689837933563
请求耗时（延迟）: 0.076413 秒
Current size: 576.0
JANET/USDT 最新报价 0.0072
当前买入价格是: 0.0066
当前价格 0.0072 满足卖出条件，准备卖出。触发条件：最大价格曾经高于买入价的 5%
出售时间: 2024-10-24 12:00:02.107
An error occurred during selling: gateio {"label":"INVALID_PRICE","message":"Market JANET_USDT has no latest price, please try later"}
请求耗时（延迟）: 0.070848 秒
USDT 可用余额: 0.689837933563
请求耗时（延迟）: 0.023449 秒
Current size: 576.0
JANET/USDT 最新报价 0.0073
当前买入价格是: 0.0066
当前价格 0.0073 满足卖出条件，准备卖出。触发条件：最大价格曾经高于买入价的 5%
出售时间: 2024-10-24 12:00:02.652
An error occurred during selling: gateio {"label":"INVALID_PRICE","message":"Market JANET_USDT has no latest price, please try later"}
请求耗时（延迟）: 0.189173 秒
USDT 可用余额: 0.689837933563
请求耗时（延迟）: 0.184747 秒
Current size: 576.0
JANET/USDT 最新报价 0.0073
当前买入价格是: 0.0066
当前价格 0.0073 满足卖出条件，准备卖出。触发条件：最大价格曾经高于买入价的 5%
出售时间: 2024-10-24 12:00:03.539
请求耗时（延迟）: 0.383605 秒
Sell Order: {'id': '705645916046', 'clientOrderId': 'apiv4', 'timestamp': 1729742403843, 'datetime': '2024-10-24T04:00:03.843Z', 'lastTradeTimestamp': 1729742403919, 'status': 'closed', 'symbol': 'JANET/USDT', 'type': 'market', 'timeInForce': 'IOC', 'postOnly': False, 'reduceOnly': None, 'side': 'sell', 'price': 0.0066, 'stopPrice': None, 'triggerPrice': None, 'average': 0.0066, 'amount': 576.0, 'cost': 3.8016, 'filled': 576.0, 'remaining': 0.0, 'fee': None, 'fees': [{'currency': 'GT', 'cost': 0.00038564472497745717}, {'currency': 'USDT', 'cost': 0.0}, {'currency': 'JANET', 'cost': 0.0}], 'trades': [], 'info': {'id': '705645916046', 'text': 'apiv4', 'amend_text': '-', 'create_time': '1729742403', 'update_time': '1729742403', 'create_time_ms': '1729742403843', 'update_time_ms': '1729742403919', 'status': 'closed', 'currency_pair': 'JANET_USDT', 'type': 'market', 'account': 'spot', 'side': 'sell', 'amount': '576', 'price': '0', 'time_in_force': 'ioc', 'iceberg': '0', 'left': '0', 'filled_amount': '576', 'fill_price': '3.8016', 'filled_total': '3.8016', 'avg_deal_price': '0.0066', 'fee': '0', 'fee_currency': 'USDT', 'point_fee': '0', 'gt_fee': '0.00038564472497745716', 'gt_maker_fee': '0', 'gt_taker_fee': '0.0009', 'gt_discount': True, 'rebated_fee': '0', 'rebated_fee_currency': 'JANET', 'finish_as': 'filled'}, 'lastUpdateTimestamp': None, 'takeProfitPrice': None, 'stopLossPrice': None}
卖出操作已完成，程序终止。
root@ip-172-26-4-230:/www/wwwroot/musk/test#