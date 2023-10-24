import pandas as pd
import streamlit as st
import numpy as np

st.title("Data Analyst Task")
trade_data = pd.read_csv('tradelog.csv')
trade_data.drop(columns='Unnamed: 0', inplace=True)
print(trade_data.isnull().sum())
st.write(trade_data)

initial_portfolio_value = 6500
risk_free_rate = 0.05

# Calculate the required parameters
total_trades = len(trade_data)
profitable_trades = len(trade_data[trade_data['Exit Price'] > trade_data['Entry Price']])
loss_making_trades = total_trades - profitable_trades
win_rate = profitable_trades / total_trades

trade_data['Trade Profit'] = trade_data['Exit Price'] - trade_data['Entry Price']
average_profit_per_trade = trade_data['Trade Profit'].mean()
average_loss_per_trade = -trade_data[trade_data['Trade Profit'] < 0]['Trade Profit'].mean()
risk_reward_ratio = average_profit_per_trade / average_loss_per_trade
loss_rate = 1 - win_rate
expectancy = (win_rate * average_profit_per_trade) - (loss_rate * average_loss_per_trade)

portfolio_values = [initial_portfolio_value]
for i in range(total_trades):
    if trade_data['Trade Profit'][i] > 0:
        portfolio_values.append(portfolio_values[-1] + trade_data['Trade Profit'][i])
    else:
        portfolio_values.append(portfolio_values[-1])

daily_returns = np.diff(portfolio_values) / portfolio_values[:-1]
average_ror_per_trade = (np.mean(daily_returns) - risk_free_rate) / np.std(daily_returns)

sharpe_ratio = (average_ror_per_trade - risk_free_rate) / np.std(daily_returns)

# Calculate Max Drawdown
cumulative_returns = np.cumsum(daily_returns)
peak, trough = cumulative_returns.max(), cumulative_returns.min()
max_drawdown = peak - trough
max_drawdown_percentage = (max_drawdown / peak) * 100

# Calculate CAGR
cagr = ((portfolio_values[-1] / initial_portfolio_value) ** (1 / total_trades)) - 1

# Calculate Calmar Ratio
calmar_ratio = cagr / max_drawdown_percentage

st.subheader("Calculated Parameters")
st.write(f"Total Trades: {total_trades}")
st.write(f"Profitable Trades: {profitable_trades}")
st.write(f"Loss-Making Trades: {loss_making_trades}")
st.write(f"Win Rate: {win_rate}")
st.write(f"Average Profit per Trade: {average_profit_per_trade}")
st.write(f"Average Loss per Trade: {average_loss_per_trade}")
st.write(f"Risk Reward Ratio: {risk_reward_ratio}")
st.write(f"Expectancy: {expectancy}")
st.write(f"Average ROR per Trade: {average_ror_per_trade}")
st.write(f"Sharpe Ratio: {sharpe_ratio}")
st.write(f"Max Drawdown: {max_drawdown}")
st.write(f"Max Drawdown Percentage: {max_drawdown_percentage}%")
st.write(f"CAGR: {cagr}")
st.write(f"Calmar Ratio: {calmar_ratio}")

decision_criteria_met = (
    win_rate > 0.5 and
    expectancy > 0 and
    risk_reward_ratio > 1.5 and
    calmar_ratio > 0
)

st.subheader("Decision")
if decision_criteria_met:
    st.write(f"Based on the calculated parameters, the decision is to: Execute")
else:
    st.write(f"Based on the calculated parameters, the decision is to: Do Not Execute")
