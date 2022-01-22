from numpy import NaN
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import ta

class stock_fn:

	def __init__(self, cash):
		self.first = cash	# 초기 자산
		self.cash = cash	# 시작 자산
		self.stock = 0		# 주식 자산
		pass

	def buy_fn(self, price, count):
		""" 주식을 매수하는 함수 """
		if (self.cash < price * count):
			print("돈이 충분하지 않습니다.")
			return
		self.cash -= price * count
		self.stock += count
		pass

	def sell_fn(self, price, count):
		""" 주식을 매도하는 함수 """
		if (self.stock < count):
			print('그 정도 주식을 가지고 있지 않습니다.')
			return
		self.stock -= count
		self.cash += price * count
		pass

	def print_profit(self):
		print("{0:->30}".format(""))
		print(f"순이익 : {self.cash - self.first}")
		print(f"수익률 : {(self.cash / self.first) * 100 - 100}")



def return_dataframe(ticker, start_day):
	""" 사용할 데이터 프레임을 리턴하는 함수"""

	start_30days_before = str(datetime(*map(int,start_day.split('-'))) - timedelta(days=33)).split()[0]		# 시작날을 입력 받으면 그 이후 33일 정도 기록누락 발생
	data = yf.download(ticker,start = start_30days_before) 													# 시작일 33일 이전의 데이터부터 가져오기 위한 날짜 생성
	if start_day not in data.index:
		print('해당 날은 주가 기록이 없습니다.')
		return
	data = data.reset_index()						# 날짜 인덱스를 열로 바꾸고 숫자 인덱스 사용
	return data


def if_used(data, person):
	""" 만약 내가 정한 조건에 맞춰 매수, 매도시 수익률 확인 함수"""

	rsi = ta.momentum.rsi(data['Close'])
	mfi = ta.volume.money_flow_index(data['High'],data['Low'],data['Close'],data['Volume'])
	macd = ta.trend.macd(data['Close'])
	macd_sig = ta.trend.macd_signal(data['Close'])
	buy_condition = (rsi <= 35) & (mfi <= 35) & (macd - macd_sig < -0.5)		# 매수하는 조건  default : RIS=35 / MFI=35 / macd 차이=-0.5
	sell_condition = (rsi >= 65) & (mfi >= 65) & (macd - macd_sig >= 0.6)		# 매도하는 조건  default : RIS=65 / MFI=65 / macd 차이=0.6
	buy_data = data[buy_condition].copy()			# 매수할 날에 대한 데이터 프레임, 수정시 기존에 파일을 수정할지 아니면 복사본만 수정할지 정해줘야 해서 copy() 시용하여 복사본을 만들어 수정한다고 명시
	sell_data = data[sell_condition].copy()			# 매도할 날에 대한 데이터 프레임
	buy_data['state'] = 'buy'				# 상태 열 추가
	sell_data['state'] = 'sell'				# 상태 열 추가
	data = pd.concat([buy_data, sell_data]).sort_index()
	flag = 0								# 매수 여부 flag
	for row in data.itertuples():			# 한 줄씩 가져오기
		price = row[5]						# 종가
		state = row[8]						# 매수 / 매도
		if flag == 0 and state == 'buy':
			person.buy_fn(price, person.cash // price)	# 전량 매수
			flag = 1
			pass
		elif flag == 1 and state == 'sell':
			person.sell_fn(price, person.stock)	# 전량 매도
			person.print_profit()
			flag = 0
			pass
