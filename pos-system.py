import pandas as pd
import datetime

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master
    
    def add_item_order(self,item_code):
        self.item_order_list.append(item_code)
        
    def view_item_list(self):
        search_result = False
        for item in self.item_master:
            for order_item in self.item_order_list:
                if int(order_item) == item.item_code:
                    print("オーダーは\n商品コード:{}、商品名:{}、価格:{}円ですね。".format(item.item_code, item.item_name, item.price))
                    search_result = True
                    calc(item)
        if search_result:
            return True
        return False

def calc(item):
    mount = input("数量を入力してください：")
    mount = num_check(mount, "数量")

    total_price = item.price * int(mount)      
    print("【注文確認】\n商品コード:{}、商品名:{}、個数{}、合計金額:{}円ですね。".format(item.item_code, item.item_name, mount, total_price))
    
    pay = input("お支払い金額を入力してください:")
    pay = pay_check(pay, total_price)

    change = int(pay) - total_price
    print("お釣りは{}円です。".format(change))
    # レシートファイル出力
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    receipt_file_name = "{}.txt".format(now)
    with open(receipt_file_name,'w', encoding='utf_8-sig') as f:
        f.write("商品コード:{}\n商品名:{}\n数量:{}個\n合計金額:{}円\nお支払い金額:{}円\nお釣り:{}円".format(item.item_code, item.item_name, mount, total_price, pay, change))

    print("ありがとうございました。")

# 入力値が文字列なので、数値変換が可能な値なら変換した値を返す
def num_check(num_object, message_item):
    check = False
    while(check == False):
        if not num_object or not num_object.isdecimal():
            num_object = input("不正な値です{}は半角数字で入力してください：".format(message_item))
        else:
            check = True
    return num_object

def pay_check(pay_object, total_price):
    pay_object = num_check(pay_object, "金額")
    check = False
    while(check == False):
        if (int(pay_object) - total_price) < 0:
            pay_object = input("金額が足りません。もう一度入力してください：")
        else:
            check = True
    return pay_object
      
### メイン処理
def main():
    # マスタ登録
    item_master=[]
    source = pd.read_csv("item.csv").values.tolist()
    for row in source:
        item_master.append(Item(row[0], row[1], row[2]))
    
    # オーダー登録
    order=Order(item_master)

    # オーダー表示
    order_result = False
    while(order_result == False):
        custommer_order = input("ご注文を商品番号でどうぞ：")
        order.add_item_order(custommer_order)
        if order.view_item_list():
            order_result = True
        else:
            print("ご注文の商品はありません。もう一度やり直してください")
    
if __name__ == "__main__":
    main()