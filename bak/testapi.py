import requests
import traceback

def test_bitget_contracts_api():
    url = 'https://api.bitget.com/api/mix/v1/market/contracts'
    params = {
        'productType': 'umcbl'  # Example product type, you might need to adjust this based on your needs
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        print("API Response:", response.json())
    except requests.exceptions.SSLError as e:
        print("SSL Exception in test_bitget_contracts_api:", e)
        traceback.print_exc()
    except requests.exceptions.RequestException as e:
        print("Request Exception in test_bitget_contracts_api:", e)
        traceback.print_exc()
    except Exception as e:
        print("General Exception in test_bitget_contracts_api:", e)
        traceback.print_exc()

if __name__ == '__main__':
    test_bitget_contracts_api()
