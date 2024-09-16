################################################################
# This is a sample model without interventions.
# It is used for demonstrate the "Hypothetical Behavior" part
################################################################


import numpy as np
import pandas as pd
import time
import logging
import math
import matplotlib.pyplot as plt
from collections import deque

import Model0Config as config
import Model0Utils as utils
import Model0Initializer as initializer

logger = logging.getLogger("Model0")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s \n',
                    datefmt='%Y/%m/%d %I:%M:%S',
                    filename=f'D:\\BlueSkyProgram\\pythonProject\\model\\log\\{int(time.time())}.log',
                    encoding='utf-8',
                    level=logging.INFO)


def main():
    logger.info("Simulation start.")

    # price list
    price_list = []
    initial_money_amount_in_pool = config.initial_money_amount_in_pool
    initial_stablecoin_amount_in_pool = config.initial_stablecoin_amount_in_pool

    # read the initial data from config
    (now_simulation_time,
     simulation_end_time,
     simulation_time_interval,
     general_risk_window_span,
     simulation_time_unit_timedelta,
     risk_horizon_fundamentalists,
     risk_horizon_long_term,
     risk_horizon_short_term) = initializer.initialize_time(config)
    (stablecoin_amount_in_pool,
     money_amount_in_pool,
     price) = initializer.initialize_pool(config)
    (stablecoin_amount_in_chartists_wallet,
     money_amount_in_chartists_wallet,
     stablecoin_amount_in_fundamentalists_wallet,
     money_amount_in_fundamentalists_wallet) = initializer.initialize_wealth(config)
    (xi_fc, xi_fe, xi_cf, xi_ce, xi_fS, xi_fM, xi_cS, xi_cM) = initializer.initialize_noise(config)
    (Fr_N, Fr_R, U_min_f, U_min_c) = initializer.initialize_upper_bound(config)
    (chi_f, v_f, chi_c, v_c) = initializer.initialize_coefficients(config)

    Delta_t_in_number = simulation_time_interval / simulation_time_unit_timedelta

    # initialize the risk queue
    risk_queue_general = utils.RiskQueue(simulation_time_interval, general_risk_window_span, simulation_time_unit_timedelta)
    risk_queue_fundamentalist = utils.RiskQueue(simulation_time_interval, risk_horizon_fundamentalists, simulation_time_unit_timedelta)
    risk_queue_long_term = utils.RiskQueue(simulation_time_interval, risk_horizon_long_term, simulation_time_unit_timedelta)
    risk_queue_short_term = utils.RiskQueue(simulation_time_interval, risk_horizon_short_term, simulation_time_unit_timedelta)

    # start the simulation
    while now_simulation_time < simulation_end_time:
        # Intervention is zero in this version
        I_bar = 0

        # Inflow is zero
        Rl_fS = 0
        Rl_fM = 0
        Rl_cS = 0
        Rl_cM = 0

        price = utils.calculate_price(stablecoin_amount_in_pool, money_amount_in_pool)

        price_list.append(price)

        # Record some information to the log
        logger.info(f"Model0: \n"
                    f"    Simulation time: {now_simulation_time}\n"
                    f"    Stage: Initialize\n"
                    f"        Stablecoin amount in pool: {stablecoin_amount_in_pool}\n"
                    f"        Money amount in pool: {money_amount_in_pool}\n"
                    f"        Price: {price}\n"
                    f"        Stablecoin in chartists wallet: {stablecoin_amount_in_chartists_wallet}\n"
                    f"        Money in chartists wallet: {money_amount_in_chartists_wallet}\n"
                    f"        Stablecoin in fundamentalists wallet: {stablecoin_amount_in_fundamentalists_wallet}\n"
                    f"        Money in fundamentalists wallet: {money_amount_in_fundamentalists_wallet}")


        #################################################
        # calculate current risk level, aka Q(t)        #
        #################################################
        risk_queue_general.add(now_simulation_time, max(price - 1, -1))
        risk_queue_fundamentalist.add(now_simulation_time, max(price - 1, -1))
        risk_queue_long_term.add(now_simulation_time, max(price - 1, -1))
        risk_queue_short_term.add(now_simulation_time, max(price - 1, -1))

        risk_level_general = risk_queue_general.get_average(now_simulation_time)
        risk_level_fundamentalist = risk_queue_fundamentalist.get_average(now_simulation_time)
        risk_level_long_term = risk_queue_long_term.get_average(now_simulation_time)
        risk_level_short_term = risk_queue_short_term.get_average(now_simulation_time)

        logger.info(f"Model0: \n"
                    f"    Simulation time: {now_simulation_time}\n"
                    f"    Stage: Risk Calculation\n"
                    f"        General risk level: {risk_level_general}\n"
                    f"        Fundamentalist risk level: {risk_level_fundamentalist}\n"
                    f"        Long-term risk level: {risk_level_long_term}\n"
                    f"        Short-term risk level: {risk_level_short_term}")


        #################################################
        # calculate the conversion and exit proportion  #
        #################################################

        # The fraction of fundamentalists leaving the system per time
        P_fe_t = min(xi_fe.sample(), Fr_N / Delta_t_in_number)

        # The fraction of fundamentalists converting to chartists per time
        P_fc_t = min(xi_fc.sample() / (1 + chi_f * I_bar) * (1 + v_f * max(-U_min_f - risk_level_fundamentalist, 0)),
                     Fr_N / Delta_t_in_number - P_fe_t)

        # The fraction of chartists leaving the system per time
        P_ce_t = min(xi_ce.sample(), Fr_N / Delta_t_in_number)

        # The fraction of chartists converting to fundamentalists per time
        P_cf_t = min(xi_cf.sample() * (1 + chi_c * I_bar) * (1 + v_c * max(U_min_c + risk_level_long_term, 0)),
                     Fr_N / Delta_t_in_number - P_ce_t)

        logger.info(f"Model0: \n"
                    f"    Simulation time: {now_simulation_time}\n"
                    f"    Stage: Conversion and Exit Proportion Calculation\n"
                    f"        p_fe_t: {P_fe_t}\n"
                    f"        p_fc_t: {P_fc_t}\n"
                    f"        p_ce_t: {P_ce_t}\n"
                    f"        p_cf_t: {P_cf_t}")


        #################################################
        # calculate the money and stablecoin supply     #
        #################################################

        # Fundamentalist-supplied total stablecoin to the liquidity pool per time
        W_fS_t = min(xi_fS.sample() * max(risk_level_fundamentalist, 0) * stablecoin_amount_in_fundamentalists_wallet,
                     (Fr_R/Delta_t_in_number - P_fc_t - P_fe_t) * stablecoin_amount_in_fundamentalists_wallet)

        # Fundamentalist-supplied total money to the liquidity pool per time
        W_fM_t = min(xi_fM.sample() * max(-risk_level_fundamentalist, 0) * money_amount_in_fundamentalists_wallet,
                     (Fr_R/Delta_t_in_number - P_fc_t - P_fe_t) * money_amount_in_fundamentalists_wallet)

        # Chartist-supplied total stablecoin to the liquidity pool per time
        W_cS_t = min(xi_cS.sample() * max(risk_level_long_term - risk_level_short_term, 0) * stablecoin_amount_in_chartists_wallet,
                     (Fr_R/Delta_t_in_number - P_cf_t - P_ce_t) * stablecoin_amount_in_chartists_wallet)

        # Chartist-supplied total money to the liquidity pool per time
        W_cM_t = 0
        if risk_level_short_term < 0:
            W_cM_t = min(xi_cM.sample() * max(risk_level_short_term - risk_level_long_term, 0) * money_amount_in_chartists_wallet,
                         (Fr_R/Delta_t_in_number - P_cf_t - P_ce_t) * money_amount_in_chartists_wallet)
        else:
            W_cM_t = 0

        logger.info(f"Model0: \n"
                    f"    Simulation time: {now_simulation_time}\n"
                    f"    Stage: Money and Stablecoin Supply Calculation\n"
                    f"        W_fS_t: {W_fS_t}\n"
                    f"        W_fM_t: {W_fM_t}\n"
                    f"        W_cS_t: {W_cS_t}\n"
                    f"        W_cM_t: {W_cM_t}")


        #################################################
        # Settlement and Distribution                   #
        #################################################

        dR_S_Delta_t_t = (W_fS_t + W_cS_t) * Delta_t_in_number
        dR_M_Delta_t_t = (W_fM_t + W_cM_t + I_bar) * Delta_t_in_number

        # This is the real price given by Pan-Jun Kim, not guaranteed to be correct
        real_price_pj = (money_amount_in_pool + dR_M_Delta_t_t) / (stablecoin_amount_in_pool + dR_S_Delta_t_t)

        new_stablecoin_in_pool = stablecoin_amount_in_pool + dR_S_Delta_t_t - (1) / (real_price_pj) * dR_M_Delta_t_t
        new_money_in_pool = money_amount_in_pool + dR_M_Delta_t_t - real_price_pj * dR_S_Delta_t_t

        # R_{fS}(t+\Delta t) : The total stablecoin in the wallet of fundamentalists
        new_stablecoin_amount_in_fundamentalists_wallet = \
            stablecoin_amount_in_fundamentalists_wallet + (
                1/(real_price_pj) * W_fM_t + P_cf_t * stablecoin_amount_in_chartists_wallet + Rl_fS
                - W_fS_t - (P_fc_t + P_fe_t) * stablecoin_amount_in_fundamentalists_wallet
            ) * Delta_t_in_number

        # R_{fM}(t+\Delta t) : The total money in the wallet of fundamentalists
        new_money_amount_in_fundamentalists_wallet = \
            money_amount_in_fundamentalists_wallet + (
                real_price_pj * W_fS_t + P_cf_t * money_amount_in_chartists_wallet + Rl_fM
                - W_fM_t - (P_fc_t + P_fe_t) * money_amount_in_fundamentalists_wallet
            ) * Delta_t_in_number

        # R_{cS}(t+\Delta t) : The total stablecoin in the wallet of chartists
        new_stablecoin_amount_in_chartists_wallet = \
            stablecoin_amount_in_chartists_wallet + (
                1/(real_price_pj) * W_cM_t + P_fc_t * stablecoin_amount_in_fundamentalists_wallet + Rl_cS
                - W_cS_t - (P_cf_t + P_ce_t) * stablecoin_amount_in_chartists_wallet
            ) * Delta_t_in_number

        # R_{cM}(t+\Delta t) : The total money in the wallet of chartists
        new_money_amount_in_chartists_wallet = \
            money_amount_in_chartists_wallet + (
                real_price_pj * W_cS_t + P_fc_t * money_amount_in_fundamentalists_wallet + Rl_cM
                - W_cM_t - (P_cf_t + P_ce_t) * money_amount_in_chartists_wallet
            ) * Delta_t_in_number

        logger.info(f"Model0: \n"
                    f"    Simulation time: {now_simulation_time}\n"
                    f"    Stage: Settlement and Distribution\n"
                    f"        new_stablecoin_in_pool: {new_stablecoin_in_pool}\n"
                    f"        new_money_in_pool: {new_money_in_pool}\n"
                    f"        new_stablecoin_amount_in_fundamentalists_wallet: {new_stablecoin_amount_in_fundamentalists_wallet}\n"
                    f"        new_money_amount_in_fundamentalists_wallet: {new_money_amount_in_fundamentalists_wallet}\n"
                    f"        new_stablecoin_amount_in_chartists_wallet: {new_stablecoin_amount_in_chartists_wallet}\n"
                    f"        new_money_amount_in_chartists_wallet: {new_money_amount_in_chartists_wallet}")

        #################################################
        # Final Confirmation                            #
        #################################################

        stablecoin_amount_in_pool = new_stablecoin_in_pool
        money_amount_in_pool = new_money_in_pool

        stablecoin_amount_in_fundamentalists_wallet = new_stablecoin_amount_in_fundamentalists_wallet
        money_amount_in_fundamentalists_wallet = new_money_amount_in_fundamentalists_wallet

        stablecoin_amount_in_chartists_wallet = new_stablecoin_amount_in_chartists_wallet
        money_amount_in_chartists_wallet = new_money_amount_in_chartists_wallet

        new_price = utils.calculate_price(stablecoin_amount_in_pool, money_amount_in_pool)

        logger.info(f"Model0: \n"
                    f"    Simulation time: {now_simulation_time}\n"
                    f"    Stage: Final Confirmation\n"
                    f"        new_price: {new_price}")

        # update the time
        now_simulation_time += simulation_time_interval

    price_list_x = range(len(price_list))
    plt.plot(price_list_x, price_list)
    plt.title("Price Trend")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.annotate(f"initial_money_amount_in_pool = {initial_money_amount_in_pool}\n"
                 f"initial_stablecoin_amount_in_pool = {initial_stablecoin_amount_in_pool}", xy=(1, 1), xytext=(0.9, 0.9), textcoords="axes fraction", ha="right", va="top", fontsize=12)
    plt.show()



if __name__ == "__main__":
    main()
