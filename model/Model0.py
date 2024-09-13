################################################################
# This is a sample model without interventions.
# It is used for demonstrate the "Hypothetical Behavior" part
################################################################

import numpy as np
import pandas as pd
import time
import logging
import Model0Config as config
import Model0Utils as utils

logger = logging.getLogger("Model0")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s \n',
                    datefmt='%Y/%m/%d %I:%M:%S',
                    filename=f'D:\\BlueSkyProgram\\pythonProject\\model\\log\\{int(time.time())}.log',
                    encoding='utf-8',
                    level=logging.INFO)


def initialize_time(config):
    return config.simulation_start_time, config.simulation_end_time, config.simulation_time_interval


def initialize_pool(config):
    return (config.initial_stablecoin_amount_in_pool,
            config.initial_money_amount_in_pool,
            utils.calculate_price(config.initial_stablecoin_amount_in_pool, config.initial_money_amount_in_pool))


def initialize_wealth(config):
    return (config.initial_stablecoin_amount_in_chartists_wallet,
            config.initial_money_amount_in_chartists_wallet,
            config.initial_stablecoin_amount_in_fundamentalists_wallet,
            config.initial_money_amount_in_fundamentalists_wallet)


def main():
    logger.info("Simulation start.")

    # read the initial data from config
    now_simulation_time, simulation_end_time, simulation_time_interval = initialize_time(config)
    stablecoin_amount_in_pool, money_amount_in_pool, price = initialize_pool(config)
    (stablecoin_amount_in_chartists_wallet,
     money_amount_in_chartists_wallet,
     stablecoin_amount_in_fundamentalists_wallet,
     money_amount_in_fundamentalists_wallet) = initialize_wealth(config)

    # start the simulation
    while now_simulation_time < simulation_end_time:
        logger.info(f"Model0: \n"
                    f"    Simulation time: {now_simulation_time}\n"
                    f"        Stablecoin amount in pool: {stablecoin_amount_in_pool}\n"
                    f"        Money amount in pool: {money_amount_in_pool}\n"
                    f"        Price: {price}\n"
                    f"        Stablecoin in chartists wallet: {stablecoin_amount_in_chartists_wallet}\n"
                    f"        Money in chartists wallet: {money_amount_in_chartists_wallet}\n"
                    f"        Stablecoin in fundamentalists wallet: {stablecoin_amount_in_fundamentalists_wallet}\n"
                    f"        Money in fundamentalists wallet: {money_amount_in_fundamentalists_wallet}")
        now_simulation_time += simulation_time_interval

    pass


if __name__ == "__main__":
    main()
