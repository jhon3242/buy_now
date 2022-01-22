from op import *

# 기본 정보 입력
print("기본 정보를 입력하세요. ")
ticker = input("티커를 대문자로 입력하세요(ex. APPL). :")
date = input("시작날을 입력하세요( ex. 2021-04-01 ). :")
asset =  int(input("시작 자산을 달러 단위로 입력하세요. :"))

person = stock_fn(asset)
fngu_data = return_dataframe(ticker, date)
if_used(fngu_data, person)
