def rssi_to_distance(rssi, tx_power=-40, path_loss_exponent=2.7):
    # Simple log-distance path loss model
    return 10 ** ((tx_power - rssi) / (10 * path_loss_exponent))
