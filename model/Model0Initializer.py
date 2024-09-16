import Model0Utils as utils

def initialize_time(config):
    return (config.simulation_start_time,
            config.simulation_end_time,
            config.simulation_time_interval,
            config.general_risk_window_span,
            config.simulation_time_unit_timedelta,
            config.risk_horizon_fundamentalists,
            config.risk_horizon_long_term,
            config.risk_horizon_short_term)


def initialize_pool(config):
    return (config.initial_stablecoin_amount_in_pool,
            config.initial_money_amount_in_pool,
            utils.calculate_price(config.initial_stablecoin_amount_in_pool, config.initial_money_amount_in_pool))


def initialize_wealth(config):
    return (config.initial_stablecoin_amount_in_chartists_wallet,
            config.initial_money_amount_in_chartists_wallet,
            config.initial_stablecoin_amount_in_fundamentalists_wallet,
            config.initial_money_amount_in_fundamentalists_wallet)


def initialize_noise(config):
    xi_fc = utils.LogNormalVariable(config.phi_fc_xi, config.omega_fc_xi)
    xi_fe = utils.LogNormalVariable(config.phi_fe_xi, config.omega_fe_xi)
    xi_cf = utils.LogNormalVariable(config.phi_cf_xi, config.omega_cf_xi)
    xi_ce = utils.LogNormalVariable(config.phi_ce_xi, config.omega_ce_xi)

    xi_fS = utils.LogNormalVariable(config.phi_fS_xi, config.omega_fS_xi)
    xi_fM = utils.LogNormalVariable(config.phi_fM_xi, config.omega_fM_xi)
    xi_cS = utils.LogNormalVariable(config.phi_cS_xi, config.omega_cS_xi)
    xi_cM = utils.LogNormalVariable(config.phi_cM_xi, config.omega_cM_xi)

    return xi_fc, xi_fe, xi_cf, xi_ce, xi_fS, xi_fM, xi_cS, xi_cM


def initialize_upper_bound(config):
    return (config.Fr_N,
            config.Fr_R,
            config.U_min_f,
            config.U_min_c)


def initialize_coefficients(config):
    return (config.chi_f,
            config.v_f,
            config.chi_c,
            config.v_c)