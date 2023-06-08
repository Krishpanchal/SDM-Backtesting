import pandas as pd
import numpy as np
import datetime
import statistics
# import pandas_datareader as pdr
from pandas_datareader import data as pdr
import datetime as dt
import math
import copy
import time
import yfinance as yf
yf.pdr_override()
import json
class SDMCalculator():
    def __init__(self,symbol_1,symbol_2,start_date,end_date,max_position,risk_free):
        self.symbol_1=symbol_1
        self.symbol_2=symbol_2
        self.start_date=start_date
        self.end_date=end_date
        self.max_position=max_position
        self.risk_free=risk_free
        self.df=pd.DataFrame({})
        self.df_summary=pd.DataFrame({'Output':[],'Buy':[],'Sell':[],'total':[]})
        self.df_analysis=pd.DataFrame({'analysis':[],'value':[]})
        self.strategy_capital=0
        #greater_sd_ma stores the max value between sd and ma.
        self.greater_sd_ma=0
        #store the symbol having the greater price in first record -> greater_price in jupyter base 
        self.greater_symbol=""
        self.lesser_symbol=""
        self.ratio={'greater':0,'lesser':0}
        self.moving_average=0
        self.standard_deviation=0
        self.strategy_peak_count=0
        self.ratio_data={}
        yf.pdr_override()
        
    
    def fetch_data(self):

        data = pdr.get_data_yahoo([self.symbol_1,self.symbol_2], start=self.start_date,end=self.end_date)
        self.df[self.symbol_1]=data['Close'][self.symbol_1]
        self.df[self.symbol_2]=data['Close'][self.symbol_2]
        self.df=self.df.reset_index()
        #rounded by 3
        self.df[self.symbol_1]=self.df.apply( lambda row : round(row[self.symbol_1],2),axis=1)
        self.df[self.symbol_2]=self.df.apply( lambda row : round(row[self.symbol_2],2),axis=1)
        
    def build_spread(self):
        spread_list=[]
        ratio=''
        greater=""
        lesser=""
        for index,row in self.df.iterrows():
            print(greater)
            print(lesser)
            isdouble=False
            if index==0:
                greater= self.symbol_1 if row[self.symbol_1] > row[self.symbol_2] else self.symbol_2
                lesser=self.symbol_2 if self.symbol_1==greater else self.symbol_1
                division_result=row[greater]/row[lesser]
                ratio=str(division_result).split('.')[0]
                print(f"--{ratio}")
                after_decimal=str(division_result).split('.')[1]
                if len(after_decimal)==1:
                    after_decimal=after_decimal+'0'
                else :
                    after_decimal=after_decimal[0:2]
                after_decimal=float('0.'+after_decimal)
                if after_decimal>=0.00 and after_decimal<=0.33:
                    ratio=float(ratio)
                elif after_decimal>=0.331 and after_decimal<=0.67:
                    ratio=float(ratio)+0.5
                    isdouble=True
                else :
                    ratio=float(ratio)+1
            print(f"-----{ratio}")
            
            spread=0
            if self.symbol_1==greater:
                spread=round(row[self.symbol_1]-((ratio)*row[self.symbol_2]),2)
            else:
                spread=round(((ratio)*row[self.symbol_1])-(row[self.symbol_2]),2)
            if isdouble: # if ratio is 0.5 then double the spread
                spread=spread*2
            # spread=round(row[greater]-((ratio)*row[lesser]), 2)
            print(f"spread={row[greater]}-({ratio}*{row[lesser]})")
            print(f"{row['Date']} {row[self.symbol_1]}----{row[self.symbol_2]} | round:{after_decimal}---ratio:{ratio}={spread}")
            spread_list.append(spread)      
        return spread_list
        
    def build_moving_average(self):
        moving_average_list=[0]*(self.moving_average-1)
        start=0
        end=start+self.moving_average
        for index in range(0,len(self.df['spread'])-self.moving_average+1):
            moving_average_list.append(round(statistics.mean(list(self.df['spread'][start:end])),2))
            start+=1
            end+=1
        print(moving_average_list)
        return moving_average_list
    
    def build_standard_deviation(self):
        standard_deviation_list=[0]*(self.standard_deviation-1)
        start=0
        end=start+self.standard_deviation
        for index in range(0,len(self.df['spread'])-self.standard_deviation+1):
            standard_deviation_list.append(round(statistics.stdev(list(self.df['spread'][start:end])),2))
            start+=1
            end+=1
        print(standard_deviation_list)
        return standard_deviation_list
    
    def build_lower_bound(self):
        lower_bound=self.df['moving_average']-self.df['standard_dev'][self.greater_sd_ma-1:] 
        return lower_bound

    def build_upper_bound(self):
        upper_bound=self.df['moving_average']+self.df['standard_dev'][self.greater_sd_ma-1:]
        return upper_bound

    def build_buy_signal(self):
        buy_signal=self.df.apply( lambda row : 1 if row['spread']<=row['lower_bound'] else 0,axis=1)
        return buy_signal

    def build_sell_signal(self):
        sell_signal=self.df.apply( lambda row : 1 if row['spread']>=row['upper_bound'] else 0,axis=1)
        return sell_signal

    
    def build_rolling_net_open(self):
        df_copy=self.df
        column_length=len(self.df['lower_bound'])
        rolling_net_open=0
        buy=[0]*column_length
        sell=[0]*column_length
        sell_price=[0]*column_length
        sell_quantity=[0]*column_length
        buy_price=[0]*column_length
        buy_quantity=[0]*column_length
        net_open=[0]*column_length
        rolling_net_open_list=[]
        for index,row in self.df.iterrows():
                #sell invalid when rolling_net_open == -1  (max_position)
                if row['sell_signal']==1 and -(self.max_position) != rolling_net_open :
                        rolling_net_open-=1
                        sell[index]= row['spread']
                        sell_price[index]=row['spread']
                        sell_quantity[index]=1
                        rolling_net_open_list.append(rolling_net_open) 
                        net_open[index]= (-1)
                #buy invalid when rolling_net_open =1
                elif row['buy_signal']==1 and  self.max_position != rolling_net_open :
                        rolling_net_open+=1
                        buy[index]= row['spread']
                        buy_price[index]=row['spread']
                        buy_quantity[index]=1
                        rolling_net_open_list.append(rolling_net_open) 
                        net_open[index]=1
                else:
                    rolling_net_open_list.append(rolling_net_open) 
        df_copy['buy']=buy
        df_copy['sell']=sell
        df_copy['sell_price']=sell_price
        df_copy['sell_quantity']=sell_quantity
        df_copy['buy_price']=buy_price
        df_copy['buy_quantity']=buy_quantity
        df_copy['net_open']=net_open
        df_copy['rolling_net_open']=rolling_net_open_list
        return df_copy
    
    def build_day_pnl(self):
        day_pnl_list=[0]*(self.standard_deviation-1)
        for index,row in self.df.iterrows():
            if index>= self.standard_deviation-1:
                day_pnl=((row['sell_price']*row['sell_quantity'] - row['buy_price']*row['buy_quantity'] + row['net_open'] * row['spread'] )
                + self.df['rolling_net_open'][index-1] * self.df['spread'][index-1] *-1+self.df['rolling_net_open'][index-1]*row['spread'])
                day_pnl_list.append(round( day_pnl,2))
        return day_pnl_list
    
    def build_trade_by_trade_pnl(self):
        trade_by_trade_pnl=[0]*(self.standard_deviation-1)
        for index , row in self.df.iterrows():
            if index>=self.standard_deviation-1:
                if self.df['rolling_net_open'][index-1]==0:
                    trade_by_trade_pnl.append(row['day_pnl'])
                else:
                    res=round(row['day_pnl']+trade_by_trade_pnl[index-1],2)
                    trade_by_trade_pnl.append(res)
        return trade_by_trade_pnl
    
    def build_trade_pnl_closed_trade(self):
        result=[]
        for index , row in self.df.iterrows():
            if self.df['rolling_net_open'][index]==0:
                result.append(self.df['trade_by_trade_pnl'][index])
            else:
                result.append(0)
        return result
    
    def build_buy_sell(self):
        result=[]
        length=len(self.df['lower_bound'])
        buy_trade_pnl_maxpos=[0]*length
        sell_trade_pnl_maxpos=[0]*length
        peak_strategy_cum_pnl=[self.df['cumulative_pnl'][0]]
        for index, row in self.df.iterrows():
            if index>0 :
                peak_strategy_cum_pnl.append(round(max(self.df['cumulative_pnl'][:index+1]),2))
            if self.df['trade_pnl_closed_trade'][index]==0:
                result.append("")
            else:
                if self.df['rolling_net_open'][index-1]==-1:
                    result.append("Sell")
                    sell_trade_pnl_maxpos[index]=self.df['trade_pnl_closed_trade'][index]
                else:
                    result.append("Buy")
                    buy_trade_pnl_maxpos[index]=self.df['trade_pnl_closed_trade'][index] 
        print(buy_trade_pnl_maxpos)
        return result,buy_trade_pnl_maxpos,sell_trade_pnl_maxpos,peak_strategy_cum_pnl
    
    def build_entry_trade_counts(self):
        length=len(self.df['lower_bound'])
        entry_buy_trade_count=[0]*length
        entry_sell_trade_count=[0]*length
        for index,row in self.df.iterrows():
            if index==0:
                continue
            else:
                if not self.df['rolling_net_open'][index-1]<0:
                    entry_buy_trade_count[index]=self.df['buy_quantity'][index]
                if not self.df['rolling_net_open'][index-1]>0:
                    entry_sell_trade_count[index]=self.df['sell_quantity'][index]
        entry_buy_trade_count[0]=sum(entry_buy_trade_count)
        entry_sell_trade_count[0]=sum(entry_sell_trade_count)
        return entry_buy_trade_count,entry_sell_trade_count
    def build_entry_average3(self):
        length=len(self.df['lower_bound'])
        entry_buy_average_price=[0.0]*length
        entry_sell_average_price=[0.0]*length
        sell_column =[ "" if cell==0 else cell  for cell in list(self.df['sell'])]
        buy_column =[ "" if cell==0 else cell  for cell in list(self.df['buy'])]
        for index,row in self.df.iterrows():
            if index==0:
                continue     
            else:
                try:
                    sell_average=((sell_column[index] if self.df['rolling_net_open'][index]<0 else 0.0)+entry_sell_average_price[index-1]*abs(self.df['rolling_net_open'][index-1]))/abs(self.df['rolling_net_open'][index])
                    entry_sell_average_price[index]=(round(entry_sell_average_price[index-1],3)  if math.isnan(sell_average) or math.isinf(sell_average)  else round(sell_average,3))
                except:
                    entry_sell_average_price[index]=entry_sell_average_price[index-1]
                try:
                    buy_average=((buy_column[index] if self.df['rolling_net_open'][index]>0 else 0.0)+entry_buy_average_price[index-1]*abs(self.df['rolling_net_open'][index-1]))/abs(self.df['rolling_net_open'][index])
                    entry_buy_average_price[index]=(round(entry_buy_average_price[index-1],3)  if math.isnan(buy_average) or math.isinf(buy_average) else round(buy_average,3))
                except:
                    entry_buy_average_price[index]=entry_buy_average_price[index-1]
        return entry_buy_average_price,entry_sell_average_price
   
    def build_exit_price(self):
        length=len(self.df['lower_bound'])
        exit_buy_price=[0.0]*length
        exit_sell_price=[0.0]*length
        buy=[0]*length
        sell=[0]*length
        for index,row in self.df.iterrows():
            if index==0:
                continue
            if self.df['rolling_net_open'][index-1]>0 and self.df['sell_quantity'][index]==1:
                exit_buy_price[index]=self.df['sell'][index]
                buy[index]=round(exit_buy_price[index]-self.df['entry_buy_average_price'][index],2)

            if self.df['rolling_net_open'][index-1]<0 and self.df['buy_quantity'][index]==1:
                exit_sell_price[index]=self.df['buy'][index]
                sell[index]=round(self.df['entry_sell_average_price'][index]-exit_sell_price[index],2)            

        return exit_buy_price,exit_sell_price,buy,sell
    
    def build_strategy_capital_plus_strategy_pnl_peak(self):
        quotient=round(self.df[self.greater_symbol][0]/self.df[self.lesser_symbol][0],2)
        after_decimal=str(float(quotient)).split('.')

        if int(after_decimal[1])>67:
            self.ratio['greater']=1
            self.ratio['lesser']=int(after_decimal[0])+1
        elif int(after_decimal[1])<=35:
            self.ratio['greater']=1
            self.ratio['lesser']=int(after_decimal[0])
        elif int(after_decimal[1])>=36 and int(after_decimal[1])<=67:
            new_quotient=float(after_decimal[0])+0.5
            self.ratio['greater']=2
            self.ratio['lesser']=new_quotient*2.0
        else:
            self.ratio['greater']=1
            self.ratio['lesser']=int(after_decimal[0])
        self.ratio_data={self.greater_symbol:self.ratio['greater'] ,self.lesser_symbol:self.ratio['lesser'] }
        self.strategy_capital=((self.df[self.greater_symbol][0]*self.ratio['greater'])+(self.df[self.lesser_symbol][0]*self.ratio['lesser']))*self.max_position   
        result=self.df.apply( lambda row : int(row['peak_strategy_cum_pnl']+self.strategy_capital),axis=1)  
        return result
    
    def build_starting_capital_plus_strategy_cum_pnl(self):
        initial=self.df['strategy_capital_plus_strategy_peak'][0]
        result=self.df.apply( lambda row : int(initial+row['cumulative_pnl']),axis=1)  
        return result

    def build_starting_capital_plus_strategy_pnl_drawdown(self):
        result=self.df.apply( lambda row : round(((row['starting_capital_plus_strategy_cum_pnl']-row['strategy_capital_plus_strategy_peak'])/row['strategy_capital_plus_strategy_peak'])*100,1) ,axis=1)  
        return result

    def build_strategy_pnl_percentage(self):
        result=[]
        counter=-1
        for data in list(self.df['starting_capital_plus_strategy_cum_pnl']):
            if counter==-1 :
                result.append(0)
                counter+=1
                continue
            elif counter==0:
                counter+=1
                result.append(0)
                continue
            else:
                #print(str(data) + "/" +str(df['starting_capital_plus_strategy_cum_pnl'][counter]))
                x=round((((data+1)/self.df['starting_capital_plus_strategy_cum_pnl'][counter])-1)*100,3)
                result.append(float(f"{x:.3f}"))
                counter+=1
        return result

    def build_b_and_h_value(self):
        result=self.df.apply(lambda row : round(((row[self.lesser_symbol]*self.ratio['lesser'])+(row[self.greater_symbol]*self.ratio['greater']))*self.max_position),axis=1)
        peak=[]
        max_value=result[0]
        for value in result:
            if value>max_value:
                max_value=value
            peak.append(max_value)
        return result,peak
    
    def build_b_and_h_drawdown(self):
        result=self.df.apply(lambda row:round(((row['b_and_h_value']-row['b_and_h_peak'])/row['b_and_h_peak'])*100,1),axis=1)
        return result

    def build_bh_plus_strategy_cum_pnl(self):
        result= self.df.apply(lambda row : row['cumulative_pnl']+row['b_and_h_value'],axis=1) 
        return result

    def build_overall_peak(self):
        result=self.df.apply(lambda row:round(row['b_and_h_peak']+row['peak_strategy_cum_pnl']),axis=1)
        return result

    def build_overall_mdd(self):
        result=self.df.apply(lambda row: round(((row['bh_plus_strategy_cum_pnl']-row['overall_peak'])/row['overall_peak'])*100,1),axis=1)
        return result

    def build_main_df(self):
        #df=df.reset_index()
        self.greater_symbol= self.symbol_1 if self.df[self.symbol_1][0] > self.df[self.symbol_2][0] else self.symbol_2
        self.lesser_symbol=self.symbol_2 if self.symbol_1==self.greater_symbol else self.symbol_1
        #corr=find_corelation(df[self.symbol_1],df[self.symbol_2])
#         self.df['spread']=self.build_spread()
        self.df['moving_average']=self.build_moving_average()
        self.df['standard_dev']=self.build_standard_deviation()
        self.df['lower_bound']=self.build_lower_bound()
        self.df['upper_bound']=self.build_upper_bound()
        self.df['buy_signal']=self.build_buy_signal()
        self.df['sell_signal']=self.build_sell_signal()
        self.df=self.build_rolling_net_open()
        self.df['day_pnl']=self.build_day_pnl()
        self.df['cumulative_pnl']=self.df['day_pnl'].cumsum()
        self.df['trade_by_trade_pnl']=self.build_trade_by_trade_pnl()
        self.df['trade_pnl_closed_trade']=self.build_trade_pnl_closed_trade()
        self.df['buy_sell'],self.df['buy_trade_pnl_maxpos'],self.df['sell_trade_pnl_maxpos'],self.df['peak_strategy_cum_pnl']=self.build_buy_sell()
        self.df['entry_buy_trade_count'],self.df['entry_sell_trade_count']=self.build_entry_trade_counts()
        self.df['entry_buy_average_price'],self.df['entry_sell_average_price']=self.build_entry_average3()
        self.df['exit_buy_price'],self.df['exit_sell_price'],self.df["buy_tradepl_maxpos"],self.df["sell_tradepl_maxpos"]=self.build_exit_price()
        self.df['strategy_capital_plus_strategy_peak']=self.build_strategy_capital_plus_strategy_pnl_peak()
        self.df['starting_capital_plus_strategy_cum_pnl']=self.build_starting_capital_plus_strategy_cum_pnl()
        self.df['starting_capital_plus_strategy_pnl_drawdown']=self.build_starting_capital_plus_strategy_pnl_drawdown()
        self.df['strategy_pnl_percentage']=self.build_strategy_pnl_percentage()
        self.df['b_and_h_value'],self.df['b_and_h_peak']=self.build_b_and_h_value()
        self.df['b_and_h_drawdown']=self.build_b_and_h_drawdown()
        self.df['bh_plus_strategy_cum_pnl']=self.build_bh_plus_strategy_cum_pnl()
        self.df['overall_peak']=self.build_overall_peak()
        self.df['overall_mdd']=self.build_overall_mdd()
        
    def build_summary_df(self):
        self.df_summary=pd.DataFrame({'Output':[],'Buy':[],'Sell':[],'total':[]})
        self.df_analysis=pd.DataFrame({'analysis':[],'value':[]})
        trades_buy=self.df['entry_buy_trade_count'][0]
        trades_sell=self.df['entry_sell_trade_count'][0]
        trades_total=trades_buy+trades_sell
        win_buy= len(self.df[self.df["buy_tradepl_maxpos"]>0])
        win_sell=len(self.df[self.df["sell_tradepl_maxpos"]>0])
        win_total=win_buy+win_sell

        winpercentage_buy=(win_buy/trades_buy)*100  if trades_buy != 0 else  0
        winpercentage_sell=(win_sell/trades_sell)*100 if trades_sell !=0 else 0
        winpercentage_total=(win_total/trades_total)*100 if trades_total !=0 else 0

        totalwin_buy=0
        totalwin_sell=0
        totallose_buy=0
        totallose_sell=0
        for index in range(0,len(self.df['lower_bound'])):
            if self.df['buy_tradepl_maxpos'][index]>0.0:
                totalwin_buy+=self.df['buy_tradepl_maxpos'][index]
            if self.df['sell_tradepl_maxpos'][index]>0.0:
                totalwin_sell+=self.df['sell_tradepl_maxpos'][index]
            if self.df['buy_tradepl_maxpos'][index]<0.0:
                totallose_buy+=self.df['buy_tradepl_maxpos'][index]
            if self.df['sell_tradepl_maxpos'][index]<0.0:
                totallose_sell+=self.df['sell_tradepl_maxpos'][index]
        totalwin_total=totalwin_buy+totalwin_sell
        totallose_total=totallose_buy+totallose_sell

        biggestwin_buy=max(self.df["buy_tradepl_maxpos"])
        biggestwin_sell=max(self.df["sell_tradepl_maxpos"])
        biggestwin_total=max([biggestwin_buy,biggestwin_sell])

        biggestlose_buy=min(self.df["buy_tradepl_maxpos"])
        biggestlose_sell=min(self.df["sell_tradepl_maxpos"])
        biggestlose_total=min([biggestlose_buy,biggestlose_sell])

        avgwin_buy=round(totalwin_buy/win_buy,1) if win_buy!=0 else 0
        avgwin_sell=round(totalwin_sell/win_sell,1) if win_sell!=0 else 0
        avgwin_total=round(totalwin_total/win_total,1) if win_total!=0 else 0

        avglose_buy=round(totallose_buy/(trades_buy-win_buy),1) if (trades_buy-win_buy)!=0 else 0
        avglose_sell=round(totallose_sell/(trades_sell-win_sell),1) if (trades_sell-win_sell)!=0 else 0
        avglose_total=round(totallose_total/(trades_total-win_total),1) if (trades_total-win_total)!=0 else 0

        totalpnl_buy=totalwin_buy+totallose_buy
        totalpnl_sell=totalwin_sell+totallose_sell
        #round to 1
        totalpnl_total=round(totalpnl_buy+totalpnl_sell)

        profitfactor_buy=round(totalwin_buy/abs(totallose_buy),1) if abs(totallose_buy)!=0 else 0
        profitfactor_sell=round(totalwin_sell/abs(totallose_sell),1) if abs(totallose_sell)!=0 else 0
        profitfactor_total=round(totalwin_total/abs(totallose_total),2) if abs(totallose_total)!=0 else 0
        
        trades= {'Output': 'trades', 'Buy': trades_buy, 'Sell':trades_sell ,'total':trades_total}
        win= {'Output': 'win', 'Buy': win_buy, 'Sell': win_sell,"total":win_total}
        p_win= {'Output': '% win', 'Buy':winpercentage_buy, 'Sell':winpercentage_sell ,"total":round(winpercentage_total,1)}
        total_win= {'Output': 'total win', 'Buy': totalwin_buy, 'Sell': totalwin_sell,'total':totalwin_total}
        total_lose= {'Output': 'total lose', 'Buy': totallose_buy, 'Sell': totallose_sell ,'total':totallose_total}
        biggest_win= {'Output': 'biggest win', 'Buy': biggestwin_buy, 'Sell': biggestwin_sell,'total':biggestwin_total}
        biggest_lose= {'Output': 'biggest  lose', 'Buy': biggestlose_buy, 'Sell': biggestlose_sell,'total':biggestlose_total}
        avg_win= {'Output': 'avg win', 'Buy': avgwin_buy, 'Sell':avgwin_sell,'total':round(avgwin_total)}
        avg_lose= {'Output': 'avg lose', 'Buy': avglose_buy, 'Sell': avglose_sell,"total":round(avglose_total)}
        total_pnl= {'Output': 'total pnl', 'Buy': totalpnl_buy, 'Sell': totalpnl_sell,"total":totalpnl_total}
        profit_factor= {'Output': 'profit factor', 'Buy': profitfactor_buy, 'Sell': profitfactor_sell,"total":profitfactor_total}
        self.df_summary=self.df_summary.append([trades,win,p_win,total_win,total_lose,biggest_win,biggest_lose,avg_win,avg_lose,total_pnl,profit_factor], ignore_index = True)
        
        #analysis table
        strategy_mdd=round(min(self.df['starting_capital_plus_strategy_pnl_drawdown']))
        b_and_h_mdd=round(min(self.df['b_and_h_drawdown']))
        overall_mdd=min(self.df['overall_mdd'])
        strategy_return_percent=round((totalpnl_total/self.strategy_capital)*100) if self.strategy_capital!=0 else 0
        diff=self.end_date-self.start_date
        return_pa=strategy_return_percent/(diff.days/365)
        return_mdd=return_pa/abs(strategy_mdd) if abs(strategy_mdd)!=0 else 0
        gross_pnl_per_trade=round(totalpnl_total/trades_total,1)
        #harsh shivlani update
        total_strategy_return_gross_pnl=round(list(self.df['starting_capital_plus_strategy_cum_pnl'])[-1]/self.df['starting_capital_plus_strategy_cum_pnl'][0]-1,2)
        cagr_strategy_return_gross_pnl=round(((list(self.df['starting_capital_plus_strategy_cum_pnl'])[-1]/self.df['starting_capital_plus_strategy_cum_pnl'][0])**(252/len(self.df['Date']))-1)*100,2)
        volatility_anualized=round(statistics.stdev(list(self.df['strategy_pnl_percentage']))*math.sqrt(252),2)
        downside_volatility_annualized=round( statistics.stdev ([ x for x in list(self.df['strategy_pnl_percentage']) if x<0 ])*math.sqrt(252),2)
        assumed_risk_free_rate=self.risk_free
        max_drawdon=round(abs( min(list(self.df['starting_capital_plus_strategy_pnl_drawdown']))),2)
        sharpe_ratio=round((cagr_strategy_return_gross_pnl-assumed_risk_free_rate)/volatility_anualized,2)
        sortino_ratio=round((cagr_strategy_return_gross_pnl-assumed_risk_free_rate)/downside_volatility_annualized,2)
        calmar_ratio=round(cagr_strategy_return_gross_pnl/max_drawdon,2)
        #adding in df
        self.df_analysis=self.df_analysis.append(  {'analysis':'strategy mdd','value':strategy_mdd},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'bnh_mdd','value':b_and_h_mdd} ,ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'overall mdd','value':overall_mdd},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'strategy return %','value':strategy_return_percent},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'return pa','value':return_pa},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'return mdd','value':return_mdd},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'gross pnl per trade','value':gross_pnl_per_trade},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'total_strategy_return_gross_pnl %','value':total_strategy_return_gross_pnl},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'CAGR strategt return gross pnl %','value':cagr_strategy_return_gross_pnl},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'volatility annualized %','value':volatility_anualized},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'downside volatility annualized %','value':downside_volatility_annualized},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'assumed risk free rate %','value':assumed_risk_free_rate},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'max draw down %','value':max_drawdon},ignore_index=True)
        self.df_analysis=self.df_analysis.append(  {'analysis':'sharpe ratio','value':sharpe_ratio},ignore_index=True)  
        self.df_analysis=self.df_analysis.append(  {'analysis':'sortino ratio','value':sortino_ratio},ignore_index=True)  
        self.df_analysis=self.df_analysis.append(  {'analysis':'calmar ratio','value':calmar_ratio},ignore_index=True)   
        #added ratio to return
        #added strategy peak count 
        self.strategy_peak_count=round((sum(list(self.df.apply(lambda row : 0 if (row['cumulative_pnl']==0 or row['peak_strategy_cum_pnl']==0) else (1 if round(row['cumulative_pnl'],2)/round(row['peak_strategy_cum_pnl'],2)==1 else 0) ,axis=1)))/len(self.df['lower_bound']))*100,1) 
        #harsh shivlani
    
    
    def tojson(self):
        self.df_json=json.loads(self.df.to_json(orient='records'))#date=iso removed
        self.df_summary_json=json.loads(self.df_summary.to_json(orient='records'))
        self.df_analysis_json=json.loads(self.df_analysis.to_json(orient='records'))