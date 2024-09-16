from datetime import datetime, timedelta

###########################################
# Precision Config                        #
###########################################

# The precision of the model
# If the difference between two numbers is less than this value,
# they are considered to be equal
eps = 1e-6


###########################################
# Simulation Timespan Config              #
###########################################

# The time when the simulation starts
simulation_start_time = datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# The time when the simulation end
simulation_end_time = datetime.strptime("2024-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# The time interval of each simulation step
# Also known as $\Delta t$
# Note: This is a timedelta object, rather than a number
simulation_time_interval = timedelta(hours=1)

# The longest time span of the general risk queue
# Also known as $\tau_q$
# Note: This is a timedelta object, rather than a number
general_risk_window_span = timedelta(hours=4)

# This unit is used for some numerical calculation
# e.g. calculate the average risk per time
simulation_time_unit_timedelta = timedelta(hours=1)

# Risk horizon of fundamentalists, long term and short term
# Also known as $\tau_f, \tau_{c_st}, \tau_{c_lt}$
risk_horizon_fundamentalists = timedelta(hours=4) ## !NOTE: This horizon should be shorter??
risk_horizon_long_term = timedelta(hours=12)
risk_horizon_short_term = timedelta(hours=4)

###########################################
# Initial Pool Config                     #
###########################################

# Initial amount of stablecoin and money in the liquidity pool (unit: a million)
initial_stablecoin_amount_in_pool = 10000
initial_money_amount_in_pool = 1000


###########################################
# Initial Wealth Config                   #
###########################################

# Initial amount of stablecoin and money in Chartists' wallet (unit: a million)
initial_stablecoin_amount_in_chartists_wallet = 100000
initial_money_amount_in_chartists_wallet = 100000

# Initial price of stablecoin and money in Fundamentalists' wallet (unit: a million)
initial_stablecoin_amount_in_fundamentalists_wallet = 100000
initial_money_amount_in_fundamentalists_wallet = 100000

###########################################
# Noise Config                            #
###########################################

# the noise in $P_{fc}(t)$
phi_fc_xi = 0.1
omega_fc_xi = 0

# the noise in $P_{fe}(t)$
phi_fe_xi = 0
omega_fe_xi = 0

# the noise in $P_{cf}(t)$
phi_cf_xi = 0.1
omega_cf_xi = 0

# the noise in $P_{ce}(t)$
phi_ce_xi = 0
omega_ce_xi = 0

# the noise in $W_{fS}(t)$
phi_fS_xi = 0.05
omega_fS_xi = 0

# the noise in $W_{fM}(t)$
phi_fM_xi = 0.05
omega_fM_xi = 0

# the noise in $W_{cS}(t)$
phi_cS_xi = 0.05
omega_cS_xi = 0

# the noise in $W_{cM}(t)$
phi_cM_xi = 0.05
omega_cM_xi = 0

###########################################
# Upperbound Config                       #
###########################################

# the upper bound of the fraction of fundamentalists (chartists)
# converting to chartists (fundamentalist) and leaving the system during the time interval
Fr_N = 0.6
# the upper bound of the fraction of the stablecoin or money in the wallet of fundamentalists (chartists)
# supplied to the liquidity pool, converting to that in the wallet of chartists (fundamentalist),
# and leaving the system during the time interval
Fr_R = 0.8

# the unpegging threshold where extra Fundamentalists begins to fear and convert to Chartists
U_min_f = 0.05

# the unpegging threshold where extra Chartists begins to believe and convert to Fundamentalists
U_min_c = 0.05

###########################################
# Coefficient Config                      #
###########################################

# the constant coefficients in the function of $P_{fc}(t)$
chi_f = 1
v_f = 10

# the constant coefficients in the function of $P_{cf}(t)$
chi_c = 1
v_c = 10
