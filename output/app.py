import gradio as gr
from accounts import Account, get_share_price

# Initialize a global account for demonstration purposes
user_account = Account(account_id="user123", initial_deposit=10000.0)

def create_account(initial_deposit):
    global user_account
    user_account = Account(account_id="user123", initial_deposit=initial_deposit)
    return "Account created with initial deposit of ${}".format(initial_deposit)

def deposit_funds(amount):
    try:
        amount = float(amount)
        user_account.deposit(amount)
        return "Deposited ${}. New balance: ${}".format(amount, user_account.balance)
    except ValueError:
        return "Invalid amount. Please enter a valid number."

def withdraw_funds(amount):
    try:
        amount = float(amount)
        if amount <= 0:
            return "Please enter a positive amount."
        success = user_account.withdraw(amount)
        if success:
            return "Withdrew ${}. New balance: ${}".format(amount, user_account.balance)
        return "Withdrawal failed. Insufficient funds."
    except ValueError:
        return "Invalid amount. Please enter a valid number."

def buy_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return "Please enter a positive quantity."
        success = user_account.buy_shares(symbol, quantity)
        if success:
            return "Bought {} shares of {}. Remaining balance: ${}".format(quantity, symbol, user_account.balance)
        return "Purchase failed. Insufficient funds."
    except ValueError:
        return "Invalid quantity. Please enter a valid number."

def sell_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return "Please enter a positive quantity."
        success = user_account.sell_shares(symbol, quantity)
        if success:
            return "Sold {} shares of {}. New balance: ${}".format(quantity, symbol, user_account.balance)
        return "Sale failed. Insufficient shares."
    except ValueError:
        return "Invalid quantity. Please enter a valid number."

def portfolio_value():
    return "Total portfolio value: ${}".format(user_account.get_portfolio_value())

def profit_loss():
    return "Profit/Loss: ${}".format(user_account.get_profit_or_loss())

def holdings():
    return "Holdings: {}".format(user_account.get_holdings())

def transaction_history():
    return "Transaction History: {}".format(user_account.get_transaction_history())

with gr.Blocks() as app:
    gr.Markdown("# Stock Trading Account Interface")
    
    with gr.Tab("Account Management"):
        initial_deposit = gr.Slider(minimum=0, maximum=100000, step=1000, label="Initial Deposit")
        create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Account Creation")
        create_btn.click(create_account, inputs=initial_deposit, outputs=create_output)
        
        deposit_amount = gr.Number(label="Deposit Amount", precision=2)
        deposit_btn = gr.Button("Deposit")
        deposit_output = gr.Textbox(label="Deposit Result")
        deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
        
        withdraw_amount = gr.Number(label="Withdrawal Amount", precision=2)
        withdraw_btn = gr.Button("Withdraw")
        withdraw_output = gr.Textbox(label="Withdrawal Result")
        withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    
    with gr.Tab("Trading"):
        buy_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Share Symbol")
        buy_quantity = gr.Number(label="Quantity to Buy", precision=0)
        buy_btn = gr.Button("Buy Shares")
        buy_output = gr.Textbox(label="Buy Result")
        buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
        
        sell_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Share Symbol")
        sell_quantity = gr.Number(label="Quantity to Sell", precision=0)
        sell_btn = gr.Button("Sell Shares")
        sell_output = gr.Textbox(label="Sell Result")
        sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
    
    with gr.Tab("Portfolio"):
        portfolio_btn = gr.Button("Get Portfolio Value")
        portfolio_output = gr.Textbox(label="Portfolio Value")
        portfolio_btn.click(portfolio_value, outputs=portfolio_output)
        
        profit_loss_btn = gr.Button("Get Profit/Loss")
        profit_loss_output = gr.Textbox(label="Profit/Loss")
        profit_loss_btn.click(profit_loss, outputs=profit_loss_output)
        
        holdings_btn = gr.Button("Get Holdings")
        holdings_output = gr.Textbox(label="Holdings")
        holdings_btn.click(holdings, outputs=holdings_output)
        
        history_btn = gr.Button("Get Transaction History")
        history_output = gr.Textbox(label="Transaction History")
        history_btn.click(transaction_history, outputs=history_output)

if __name__ == "__main__":
    app.launch()
