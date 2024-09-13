from datetime import datetime, timedelta

###########################################
# Simulation Timespan Config
###########################################

# The time when the simulation starts
simulation_start_time = datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# The time when the simulation starts
simulation_end_time = datetime.strptime("2024-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# The time interval of each simulation step
# Also known as $\Delta t$
simulation_time_interval = timedelta(hours=1)


###########################################
# Initial Wealth Config
###########################################

# Initial amount of stablecoin and money in the liquidity pool (unit: a million)
initial_stablecoin_amount_in_pool = 10000
initial_money_amount_in_pool = 10000

# Initial amount of stablecoin and money in Chartists' wallet (unit: a million)
initial_stablecoin_amount_in_chartists_wallet = 100000
initial_money_amount_in_chartists_wallet = 100000

# Initial price of stablecoin and money in Fundamentalists' wallet (unit: a million)
initial_stablecoin_amount_in_fundamentalists_wallet = 100000
initial_money_amount_in_fundamentalists_wallet = 100000
