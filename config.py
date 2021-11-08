from acconeer.exptool import configs

sensorconfig = {}
updaterate = 60
bin_short_config = configs.PowerBinServiceConfig()
bin_short_config.profile = bin_short_config.Profile.PROFILE_1
bin_short_config.update_rate = updaterate
bin_short_config.bin_count = 5
bin_short_config.range_interval = [0.05, 0.2]
bin_short_config.hw_accelerated_average_samples = 50

bin_long_config = configs.PowerBinServiceConfig()
bin_long_config.profile = bin_long_config.Profile.PROFILE_3
bin_long_config.update_rate = updaterate
bin_long_config.bin_count = 7
bin_long_config.range_interval = [0.3, 0.6]
bin_long_config.hw_accelerated_average_samples = 50

env_short_config = configs.EnvelopeServiceConfig()
env_short_config.profile = env_short_config.Profile.PROFILE_1
env_short_config.update_rate = 30
env_short_config.range_interval = [0.05, 0.25]
env_short_config.hw_accelerated_average_samples = 50

env_long_config = configs.EnvelopeServiceConfig()
env_long_config.profile = env_long_config.Profile.PROFILE_3
env_long_config.update_rate = 30 
env_long_config.range_interval = [0.2, 0.5]
env_long_config.hw_accelerated_average_samples = 50

env_xlong_config = configs.EnvelopeServiceConfig()
env_xlong_config.profile = env_long_config.Profile.PROFILE_4
env_xlong_config.update_rate = 30
env_xlong_config.range_interval = [0.5, 1.0]
env_xlong_config.hw_accelerated_average_samples = 30

env_mid_config = configs.EnvelopeServiceConfig()
env_mid_config.profile = env_long_config.Profile.PROFILE_2
env_mid_config.update_rate = 30
env_mid_config.range_interval = [0.1, 0.6]
env_mid_config.hw_accelerated_average_samples = 50

env_wastebin_config = configs.EnvelopeServiceConfig()
env_wastebin_config.profile = env_long_config.Profile.PROFILE_4
env_wastebin_config.update_rate = 30
env_wastebin_config.range_interval = [0.4, 0.8]
env_wastebin_config.hw_accelerated_average_samples = 50


off_config = configs.EnvelopeServiceConfig()
off_config.tx_disable = True
off_config.update_rate = updaterate
off_config.range_interval = [0.2, 0.5]

sensorconfig["bins_short_range"] = bin_short_config
sensorconfig["bins_long_range"] = bin_long_config
sensorconfig["env_short_range"] = env_short_config
sensorconfig["env_long_range"] = env_long_config
sensorconfig["env_xlong_range"] = env_xlong_config
sensorconfig["env_mid_range"] = env_mid_config
sensorconfig["env_wastebin_config"] = env_wastebin_config
sensorconfig["off"] = off_config