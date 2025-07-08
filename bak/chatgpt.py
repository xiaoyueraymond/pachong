import test.bit2 as bit2
import json
import csv

class BitgetTrader:
    def __init__(self, bSymbolPathExists=False, pathSymbol="D:\\python\\appifyers\\symbols.csv"):
        self.bSymbolPathExists = bSymbolPathExists
        self.pathSymbol = pathSymbol
        self._exchange = self.CreateExchange()  # 初始化交易所实例

    # 创建交易所实例
    def CreateExchange(self):
        with open('D:\\python\\appifyers\\configuration.json', 'r') as f:
            data = json.load(f)
        return bit2.bitget({
            'apikey': data["APIKEY"],
            'secret': data['SECRET'],
            'password': data['PASSWORD'],
            "options": {
                'defaultType': 'swap',
                'adjustForTimeDifference': True
            }
        })

    # 获取交易对信息
    def FetchSymbols(self, bSave=False):
        symbols = None
        string = '_UMCBL'
        try:
            data = self._exchange.fetch_markets()
            symbols = [pair['id'] for pair in data if string in pair['id']]
            if bSave:
                self.SaveSymbols(symbols)
        except Exception as e:
            print("Exception in fetching market symbols:", e)
        return symbols

    # 把交易货币列表存入本地csv
    def SaveSymbols(self, symbols):
        with open(self.pathSymbol, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Symbols"])
            for symbol in symbols:
                writer.writerow([symbol])
        print(f"Symbols have been saved to {self.pathSymbol}")

    # 读取本地货币列表csv
    def ReadSymbols(self):
        with open(self.pathSymbol, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过标题行
            symbols = [row[0] for row in reader]
        return symbols

    def printtest(self):
        print('work')

if __name__ == '__main__':
    bgTrader = BitgetTrader()
    symbols = bgTrader.FetchSymbols(bSave=True)
    print(symbols)
    bgTrader.printtest()
