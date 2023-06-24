from datetime import date as dt, timedelta, datetime, timedelta
import pandas as pd
import os
import numpy as np
import statsmodels.api as sm
from pandas_datareader import data as pdr
import yfinance as yf
import statistics
from statistics import mean, stdev
import math
import copy
import os
import json
# from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from joblib import Parallel, delayed
from collections import OrderedDict
yf.pdr_override()


class Backtest:
    def __init__(self, symbol_1, symbol_2, start_date, end_date, max_position, risk_free):
        self.symbol_2 = symbol_2
        self.symbol_1 = symbol_1
        self.start_date = start_date
        self.end_date = end_date
        self.max_position = max_position
        self.risk_free = risk_free
        self.hedge_ratio_count_limit = 9
        self.moving_average = 0
        self.standard_deviation = 0
        self.standard_deviation_div = 3
        self.initial_investment = 100000
        self.comms_value = 0.001195
        self.reinvest = False
        self.qty_multiplier_1_string = f'{self.symbol_1}_qty_multiplier'
        self.qty_multiplier_2_string = f'{self.symbol_2}_qty_multiplier'
        self.days_to_wait = max(
            [self.moving_average, self.standard_deviation, self.hedge_ratio_count_limit])
        self.df_runtime = OrderedDict()
        self.df = pd.DataFrame({})
        self.df_analysis = pd.DataFrame({})

    def fetch_data(self):
        data = pdr.get_data_yahoo(
            [self.symbol_1, self.symbol_2], start=self.start_date, end=self.end_date)
        self.df[self.symbol_1] = data['Adj Close'][self.symbol_1]
        self.df[self.symbol_2] = data['Adj Close'][self.symbol_2]
        self.df = self.df.reset_index()
        # rounded by 3
        self.df[self.symbol_1] = self.df.apply(
            lambda row: round(row[self.symbol_1], 2), axis=1)
        self.df[self.symbol_2] = self.df.apply(
            lambda row: round(row[self.symbol_2], 2), axis=1)

    def custom_round(self, division_result, index):
        ratio = str(division_result).split('.')[0]
        after_decimal = str(division_result).split('.')[1]
        after_decimal = float('0.'+after_decimal)
        round_up = 0
        if after_decimal >= 0.0 and after_decimal <= 0.34:
            ratio = float(ratio)
            round_up = 0
        elif after_decimal > 0.34 and after_decimal <= 0.66:
            ratio = float(ratio) + 0.5
            round_up = 0.5
        else:
            ratio = float(ratio) + 1
            round_up = 1
        if division_result < 1:
            ratio = round(1/division_result, 0)
        return ratio, round_up
    
    def calculate(self,date,symbol1_price,symbol2_price,index):
        ratio=''
        ratio_list = 0
        ratio_2d = 0
        ratio_2d_value_band = 0
        ratio_trade = 0
        hedge_ratio_count = 0
        symbol_1_qty_multipier = 0
        symbol_2_qty_multipier = 0
        
        #----------ratio calculation  --------------
        division_result = round(float(symbol1_price)/float(symbol2_price),2)  
        ratio_2d = division_result
        round_up = 0
        ratio,round_up = self.custom_round(division_result,index)
        ratio_list = ratio
        ratio_2d_value_band = round_up
        if index+1 < self.hedge_ratio_count_limit:
            ratio_trade = ratio
        else:
                #print(index, index+1-hedge_ratio_count_limit,index+1, date,list(df_runtime["hedge_ratio_calc"][index+1-hedge_ratio_count_limit: index+1] ),ratio)
                #print(date,list(df_runtime["hedge_ratio_calc"][index+1-hedge_ratio_count_limit: index+1]),round(mean(df_runtime["hedge_ratio_calc"][index+1-hedge_ratio_count_limit: index+1]),0))
                if self.df_runtime[ index - 1 ]['rolling_net_open'] == 0 and ratio == mean( [  self.df_runtime[val]["hedge_ratio_calc"] for val  in range(index+1-self.hedge_ratio_count_limit, index) ] ) :
                    ratio_trade = mean([ self.df_runtime[val]["hedge_ratio_calc"] for val in range ( index+1-self.hedge_ratio_count_limit, index ) ] )
                else: 
                    ratio_trade = self.df_runtime[index-1]["hedge_ratio_trade"]
        if index != 0:
                hedge_ratio_count = self.df_runtime[index-1]["hedge_ratio_change_count"]+1 if self.df_runtime[index-1]["hedge_ratio_trade"] == ratio_trade else 1

        #----------if reinvest enabled ------------
        if  index > 0:
            initial_investment =  initial_investment_plus_strategy_net_cum_pnl if self.reinvest else self.df_runtime[index-1]["initial_investment"]
            
        #----------quantity multiplier calculation ----------------
        if index == 0:
                if ratio_2d <1:
                    symbol_1_qty_multipier = ratio_trade
                    symbol_2_qty_multipier = symbol_1_qty_multipier/ratio_trade
                else:
                    if ratio_2d_value_band == 0.5:
                        symbol_1_qty_multipier = 2
                    else:
                        symbol_1_qty_multipier = 1 
                    symbol_2_qty_multipier = symbol_1_qty_multipier * ratio_trade          
        else:
                if ratio_2d < 1:
                        symbol_1_qty_multipier =ratio_trade
                        symbol_2_qty_multipier = symbol_1_qty_multipier/ratio_trade   
                else:
                            if ratio_2d_value_band == 0.5 and self.df_runtime[index-1]['rolling_net_open'] == 0:
                                symbol_1_qty_multipier = 2
                            else:
                                symbol_1_qty_multipier = self.df_runtime[index-1] [self.qty_multiplier_1_string]
                            symbol_2_qty_multipier = symbol_1_qty_multipier * ratio_trade
                            
        #----------Position Size multiplier Calculation -------------------------------
        
        position_size_calculation = self.initial_investment / (symbol_1_qty_multipier * symbol1_price + symbol_2_qty_multipier * symbol2_price)/self.max_position
        position_size_calculation = math.floor(position_size_calculation)
        position_size_trade = 0
        if index == 0:
                position_size_trade = position_size_calculation
        else:
                position_size_trade = position_size_calculation if  self.df_runtime[index-1]['rolling_net_open'] == 0 else self.df_runtime[index-1]['position_size_trade']

        #----------demat requirement -------------------
        stock_1_demat_req = symbol_1_qty_multipier * position_size_trade * self.max_position
        stock_2_demat_req = symbol_2_qty_multipier * position_size_trade * self.max_position
        
        #----------trade execution quantity --------------
        stock_1_trade_exec_qty = stock_1_demat_req/self.max_position
        stock_2_trade_exec_qty = stock_2_demat_req/self.max_position
        
        #----------spread -----------------------
        spread= round(( symbol1_price * symbol_1_qty_multipier ) - ( symbol2_price * symbol_2_qty_multipier ),2)
        
        #----------moving average & standard deviation -----------
        ma=0
        sd=0
        if index >= self.moving_average-1:
            spread_list= [ self.df_runtime[val]['spread'] for val in   range((index+1-self.moving_average),index ) ]
            spread_list.append( spread )
            ma=round(mean(spread_list),2)  

        if index >= self.standard_deviation-1 :
            spread_list=[ self.df_runtime[val]['spread'] for val in range((index+1-self.standard_deviation),index) ]
            spread_list.append( spread )
            sd=round(stdev(spread_list)/self.standard_deviation_div,2)
        
        #----------lower bound & upper bound --------------------
        lower_bound = 0
        upper_bound = 0
        if index >= self.days_to_wait - 1:
            lower_bound = ma-sd
            upper_bound = ma+sd
        #----------check for buy and sell ----------------
        buy_signal_generated = 0
        sell_signal_generated = 0
        buy_signal_accepted = 0
        sell_signal_accepted = 0
        net_open = 0
        rolling_net_open = 0
        
        if index >= self.days_to_wait-1:

                #check for buy
                if spread < lower_bound:
                    buy_signal_generated = 1
                    if self.df_runtime[index-1]["rolling_net_open"] < self.max_position  and hedge_ratio_count >= self.moving_average and hedge_ratio_count >= self.standard_deviation:
                        buy_signal_accepted = spread
                        net_open = 1
                    
                #check for sell
                if spread > upper_bound:
                    sell_signal_generated = 1
                    if (self.df_runtime[index-1]["rolling_net_open"] * -1) < self.max_position and hedge_ratio_count >= self.moving_average and hedge_ratio_count>=self.standard_deviation:
                        sell_signal_accepted = spread
                        net_open=-1
        
        #----------rolling net open -------------
        if index == 0:
            rolling_net_open = net_open
        else:
            rolling_net_open = net_open+self.df_runtime[index-1]['rolling_net_open']
            
        #----------strategy day gross pnl  --------------------
        strategy_day_gross_pnl = (sell_signal_accepted * 1) - ( buy_signal_accepted * 1) + net_open*spread 
        strategy_gross_cum_pnl = copy.deepcopy( strategy_day_gross_pnl )
        if index != 0:
            prev_rolling_net_open = self.df_runtime[index-1]["rolling_net_open"]
            strategy_day_gross_pnl = round(((strategy_day_gross_pnl)+prev_rolling_net_open * self.df_runtime[index-1]["spread"] *-1
                                    + prev_rolling_net_open * spread) * position_size_trade,2)
            strategy_gross_cum_pnl = strategy_day_gross_pnl + self.df_runtime[index-1]["strategy_gross_cum_pnl"]
        
        #----------turnover : ask question about round up------------
        turnover = abs(net_open) * (stock_1_trade_exec_qty * symbol1_price + stock_2_trade_exec_qty * symbol2_price)
        turnover = round(turnover,2)
        
        #----------Comms : whats the full form, round up ?------------------------
        comms = round(turnover * self.comms_value,2)
        
        #----------dp charges----------------
        dp_charges = abs(net_open)*16
        
        #----------cum. transaction costs------------
        cum_transaction_costs = (comms+dp_charges) * -1
        if index != 0:
            cum_transaction_costs = round(cum_transaction_costs + self.df_runtime[index-1]["cum_transaction_costs"],2)
        
        #----------strategy net cum pnl ----------------
        strategy_net_cum_pnl= round(strategy_gross_cum_pnl+cum_transaction_costs,2)
        
        #----------net_withdraw_reinvestable_calculation -----------
        net_withdraw_reinvestabe_calculation=0
        if index >= 2:
            net_withdraw_reinvestabe_calculation = strategy_net_cum_pnl if rolling_net_open==0 else self.df_runtime[index-1]["net_withdraw_reinvestabe_calculation"]
            net_withdraw_reinvestabe_calculation = round(net_withdraw_reinvestabe_calculation,2)
        
        #-----------Net P&L (Withdraw / Reinvest able) Trade by Trade P&L Closed Trades  ---------------------
        net_pnl_tradebytrade_closedtrades = 0
        if index >= 2:
            net_pnl_tradebytrade_closedtrades = (net_withdraw_reinvestabe_calculation-self.df_runtime[index-1]["net_pnl_tradebytrade_closedtrades"] ) if rolling_net_open==0 else 0
            net_pnl_tradebytrade_closedtrades = round(net_pnl_tradebytrade_closedtrades,2)

        #-----------initial_investment_plus_strategy_net_cum_pnl ----------------
        initial_investment_plus_strategy_net_cum_pnl = round(strategy_net_cum_pnl + self.initial_investment, 2)
        
        #-----------daily % change in net pnl : about division --------------------------
        daily_percent_change_net_pnl = 0
        if index > 0:
            daily_percent_change_net_pnl= initial_investment_plus_strategy_net_cum_pnl/self.df_runtime[index-1]["initial_investment_plus_strategy_net_cum_pnl"]-1
            daily_percent_change_net_pnl = round(daily_percent_change_net_pnl*100,2)
        
        #-----------initial investment plus strategy net cum pnl drawdown -----------------
        initial_investment_plus_cum_pnl_drawdown=0
        if index > 0 :
            initial_investment_plus_cum_pnl_drawdown = initial_investment_plus_strategy_net_cum_pnl / max( [ self.df_runtime[val]["initial_investment_plus_strategy_net_cum_pnl"] for val in range(0,index)] +[ initial_investment_plus_strategy_net_cum_pnl] )
            initial_investment_plus_cum_pnl_drawdown= round(( initial_investment_plus_cum_pnl_drawdown -1 ) * 100, 2)
        
        #-----------total strategy return till sharpe ratio net ----------------------
        total_strategy_return = 0 
        CAGR_strategy_return = 0
        volatility_annualized = 0
        downside_volatility = 0
        max_drawdown = 0
        sharpe_ratio_net_pnl = 0
        if index >= 60:
            
            #round up by 1
            total_strategy_return =initial_investment_plus_strategy_net_cum_pnl/self.df_runtime[index-60]["initial_investment_plus_strategy_net_cum_pnl"]-1
            total_strategy_return = round((total_strategy_return)*100,1)
            
            #round up by 1, there is some minor difference because of ^252 
            CAGR_strategy_return = initial_investment_plus_strategy_net_cum_pnl/self.df_runtime[index-60]["initial_investment_plus_strategy_net_cum_pnl"]
            CAGR_strategy_return = (CAGR_strategy_return**(252/60) )-1
            CAGR_strategy_return = round(CAGR_strategy_return*100,1)
            #print(CAGR_strategy_return)
            
                
            volatility_annualized = stdev( [ self.df_runtime[val]["daily_percent_change_net_pnl"] for val in range(index-60, index) ] + [ daily_percent_change_net_pnl ])
            volatility_annualized = round(volatility_annualized*math.sqrt(252),1)
            
            downside_volatility = [x for x in [ self.df_runtime[val]["daily_percent_change_net_pnl"] for val in range(index-60, index) ] + [ daily_percent_change_net_pnl ] if x<0]
            downside_volatility = round(stdev(downside_volatility)*math.sqrt(252),1)
            
            max_drawdown = round(abs(min( [ self.df_runtime[val]["initial_investment_plus_cum_pnl_drawdown"] for val in range(index-60,index) ]+[initial_investment_plus_cum_pnl_drawdown])), 1)
            
            sharpe_ratio_net_pnl =round(( CAGR_strategy_return - volatility_annualized  ) / 1,1)
            
        #----------b&H calculation for Leg 1 and leg 2 -------------
        
        #leg 1
        bnh_buy_symbol1_qty = copy.deepcopy( stock_1_demat_req )
        bnh_sell_symbol1_qty = 0
        bnh_net_open_symbol1 = bnh_buy_symbol1_qty - bnh_sell_symbol1_qty
        bnh_rolling_net_open_symbol1 = bnh_net_open_symbol1
        bnh_day_gross_pnl_symbol1 = 0
        bnh_day_gross_pnl_symbol1_cum = 0
        
        #leg 2 
        bnh_buy_symbol2_qty = copy.deepcopy( stock_2_demat_req )
        bnh_sell_symbol2_qty = 0
        bnh_net_open_symbol2 = bnh_buy_symbol2_qty - bnh_sell_symbol2_qty
        bnh_rolling_net_open_symbol2 = bnh_net_open_symbol2
        bnh_day_gross_pnl_symbol2 = 0
        bnh_day_gross_pnl_symbol2_cum = 0
        
        if index > 0:
            
            #leg1 calculation
            diff = stock_1_demat_req - self.df_runtime[index-1]["stock_1_demat_req"]
            bnh_buy_symbol1_qty = diff if diff > 0 else 0
            bnh_sell_symbol1_qty = abs(diff) if diff < 0 else 0
            bnh_net_open_symbol1 = bnh_buy_symbol1_qty - bnh_sell_symbol1_qty
            bnh_rolling_net_open_symbol1 = bnh_net_open_symbol1 + self.df_runtime[index-1]["bnh_rolling_net_open_symbol1"]
            bnh_day_gross_pnl_symbol1 = bnh_sell_symbol1_qty * symbol1_price - bnh_buy_symbol1_qty * symbol1_price + \
                                        bnh_net_open_symbol1 * symbol1_price + self.df_runtime[index-1]["bnh_rolling_net_open_symbol1"] \
                                        * self.df_runtime[index-1][self.symbol_1] * -1 +  self.df_runtime[index-1]["bnh_rolling_net_open_symbol1"] \
                                        * symbol1_price
            bnh_day_gross_pnl_symbol1 = round(bnh_day_gross_pnl_symbol1, 2)
            bnh_day_gross_pnl_symbol1_cum = bnh_day_gross_pnl_symbol1 +  self.df_runtime[index-1]["bnh_day_gross_pnl_symbol1_cum"]
            
            #leg2 calculation 
            diff_2 = stock_2_demat_req - self.df_runtime[index-1]["stock_2_demat_req"]
            bnh_buy_symbol2_qty = diff_2 if diff_2 > 0 else 0
            bnh_sell_symbol2_qty = abs(diff_2) if diff_2 < 0 else 0
            bnh_net_open_symbol2 = bnh_buy_symbol2_qty - bnh_sell_symbol2_qty
            bnh_rolling_net_open_symbol2 = bnh_net_open_symbol2 + self.df_runtime[index-1]["bnh_rolling_net_open_symbol2"]
            bnh_day_gross_pnl_symbol2 = bnh_sell_symbol2_qty * symbol2_price - bnh_buy_symbol2_qty * symbol2_price + \
                                        bnh_net_open_symbol2 * symbol2_price + self.df_runtime[index-1]["bnh_rolling_net_open_symbol2"] \
                                        * self.df_runtime[index-1][self.symbol_2] * -1 +  self.df_runtime[index-1]["bnh_rolling_net_open_symbol2"] \
                                        * symbol2_price
            bnh_day_gross_pnl_symbol2 = round(bnh_day_gross_pnl_symbol2, 2)
            bnh_day_gross_pnl_symbol2_cum = bnh_day_gross_pnl_symbol2 +  self.df_runtime[index-1]["bnh_day_gross_pnl_symbol2_cum"]
        
        bnh_day_total_gross_pnl = bnh_day_gross_pnl_symbol1 + bnh_day_gross_pnl_symbol2
        bnh_day_total_gross_pnl_cum = bnh_day_gross_pnl_symbol1_cum +bnh_day_gross_pnl_symbol2_cum
        bnh_plus_strategy_gross_pnl_cum = round( strategy_net_cum_pnl + bnh_day_total_gross_pnl_cum , 2 )
            
        #appending into df
        record={"Date":date,
                self.symbol_1:symbol1_price, 
                self.symbol_2:symbol2_price, 
                'ratio_2d':ratio_2d,
                'ratio_2d_value_band':ratio_2d_value_band,
                "hedge_ratio_calc":ratio,
                "hedge_ratio_trade":ratio_trade,
                'hedge_ratio_change_count':hedge_ratio_count,
                "initial_investment" : self.initial_investment,
                self.qty_multiplier_1_string:symbol_1_qty_multipier,
                self.qty_multiplier_2_string:symbol_2_qty_multipier,
            "position_size_calc":position_size_calculation,
                "position_size_trade":position_size_trade,
            "stock_1_demat_req":stock_1_demat_req,
                "stock_2_demat_req":stock_2_demat_req,
                "stock_1_trade_exec_qty":stock_1_trade_exec_qty,
                "stock_2_trade_exec_qty":stock_2_trade_exec_qty,
                "spread":spread,"Mavg":ma,"Stdev":sd,
            "lower_bound":lower_bound,
                "upper_bound":upper_bound,
                "buy_signal_generated":buy_signal_generated,
                "sell_signal_generated":sell_signal_generated,
                "buy_signal_accepted": buy_signal_accepted,
                "sell_signal_accepted":sell_signal_accepted,
                "net_open":net_open,
                "rolling_net_open":rolling_net_open,
                "strategy_day_gross_pnl":strategy_day_gross_pnl,
                "strategy_gross_cum_pnl":strategy_gross_cum_pnl,
                "turnover":turnover,
                "comms":comms,
                "dp_charges":dp_charges,
                "cum_transaction_costs":cum_transaction_costs,
                "strategy_net_cum_pnl":strategy_net_cum_pnl,
                "net_withdraw_reinvestabe_calculation":net_withdraw_reinvestabe_calculation,
                "net_pnl_tradebytrade_closedtrades":net_pnl_tradebytrade_closedtrades,
                "initial_investment_plus_strategy_net_cum_pnl":initial_investment_plus_strategy_net_cum_pnl,
                "daily_percent_change_net_pnl":daily_percent_change_net_pnl,
                "initial_investment_plus_cum_pnl_drawdown":initial_investment_plus_cum_pnl_drawdown,
                "total_strategy_return":total_strategy_return,
                "CAGR_strategy_return" : CAGR_strategy_return,
                "volatility_annualized" :volatility_annualized,
                "downside_volatility" : downside_volatility,
                "max_drawdown" : max_drawdown,
                "sharpe_ratio_net_pnl" :sharpe_ratio_net_pnl,
                "bnh_buy_symbol1_qty" : bnh_buy_symbol1_qty ,
                "bnh_sell_symbol1_qty" : bnh_sell_symbol1_qty, 
                "bnh_net_open_symbol1" : bnh_net_open_symbol1, 
                "bnh_rolling_net_open_symbol1" : bnh_rolling_net_open_symbol1,
                "bnh_day_gross_pnl_symbol1" : bnh_day_gross_pnl_symbol1,
                "bnh_day_gross_pnl_symbol1_cum" :bnh_day_gross_pnl_symbol1_cum,
                "bnh_buy_symbol2_qty" : bnh_buy_symbol2_qty,
                "bnh_sell_symbol2_qty" : bnh_sell_symbol2_qty, 
                "bnh_net_open_symbol2" : bnh_net_open_symbol2, 
                "bnh_rolling_net_open_symbol2" : bnh_rolling_net_open_symbol2, 
                "bnh_day_gross_pnl_symbol2" : bnh_day_gross_pnl_symbol2,
                "bnh_day_gross_pnl_symbol2_cum" : bnh_day_gross_pnl_symbol2_cum,
                "bnh_day_total_gross_pnl" : bnh_day_total_gross_pnl, 
                "bnh_day_total_gross_pnl_cum" : bnh_day_total_gross_pnl_cum, 
                "bnh_plus_strategy_gross_pnl_cum" : bnh_plus_strategy_gross_pnl_cum 
            }
        self.df_runtime[index] = record

    def build_table(self):
        numpy_df = self.df.to_numpy()
        i=0
        columns = list(self.df.columns)
        for row in numpy_df:
            self.calculate ( row[columns.index('Date')], row[columns.index(self.symbol_1)], row[columns.index(self.symbol_2)], i)
            i+=1 
        self.df_runtime = pd.DataFrame.from_dict(self.df_runtime, "index")

    def build_df_analysis(self):
        days = self.df_runtime.shape[0]
        total_strategy_return_net_pnl = round(list(self.df_runtime['initial_investment_plus_strategy_net_cum_pnl'])[
            -1]/self.df_runtime['initial_investment_plus_strategy_net_cum_pnl'][0]-1, 2) * 100
        #rename to net
        cagr_strategy_return_net_pnl = round(((list(self.df_runtime['initial_investment_plus_strategy_net_cum_pnl'])[
                                               -1]/self.df_runtime['initial_investment_plus_strategy_net_cum_pnl'][0])**(252/self.df_runtime.shape[0])-1)*100, 2)
        volatility_anualized = round(statistics.stdev(
            list(self.df_runtime["daily_percent_change_net_pnl"]))*math.sqrt(252), 2)
        downside_volatility_annualized = round(statistics.stdev([x for x in list(
            self.df_runtime["daily_percent_change_net_pnl"]) if x < 0])*math.sqrt(252), 2)
        max_drawdon = round(
            abs(min(list(self.df_runtime["initial_investment_plus_cum_pnl_drawdown"]))), 2)
        sharpe_ratio = round(
            (cagr_strategy_return_net_pnl-self.risk_free)/volatility_anualized, 2)
        sortino_ratio = round((cagr_strategy_return_net_pnl -
                              self.risk_free)/downside_volatility_annualized, 2)
        calmar_ratio = round(cagr_strategy_return_net_pnl/max_drawdon, 2)
        transaction_costs_gross_pnl = round( ( list(self.df_runtime["cum_transaction_costs"])[
            -1] / list(self.df_runtime["strategy_gross_cum_pnl"])[-1] ) * -1 * 100, 2)
        strategy_net_cum_pnl = round(list(
            self.df_runtime["strategy_net_cum_pnl"])[-1],0)
        strategy_gross_cum_pnl = round(list(
            self.df_runtime["strategy_gross_cum_pnl"])[-1], 0)

        self.df_analysis = self.df_analysis.append(
            {'analysis': 'strategy gross cum pnl', 'value': strategy_gross_cum_pnl}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'transaction costs gross pnl %', 'value':  transaction_costs_gross_pnl}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'strategy net cum pnl', 'value': strategy_net_cum_pnl}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'CAGR strategy return net pnl %', 'value': cagr_strategy_return_net_pnl}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'assumed risk free rate %', 'value': self.risk_free}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'total strategy return net pnl %', 'value': total_strategy_return_net_pnl}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'volatility annualized %', 'value': volatility_anualized}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'downside volatility annualized %', 'value': downside_volatility_annualized}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'max draw down %', 'value': max_drawdon}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'sharpe ratio', 'value': sharpe_ratio}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'sortino ratio', 'value': sortino_ratio}, ignore_index=True)
        self.df_analysis = self.df_analysis.append(
            {'analysis': 'calmar ratio', 'value': calmar_ratio}, ignore_index=True)

    def tojson(self):
        print(self.moving_average, self.standard_deviation)
        self.df_runtime_json = json.loads(self.df_runtime.to_json(
            orient='records'))  # date=iso removed
        self.df_analysis_json = json.loads(
            self.df_analysis.to_json(orient='records'))
