
RHINO_CATEGORICAL_COLUMNS = [
    "bench_name",
    "bench",
    "hole",
    "hole_id",
    "hole_name",
    "hole_type_id",
    "rig_id",
    "mine_name",
    "sensor_id",
    "digitizer_id",
    "rhino_sensor_uid",
    "acorr_file_id",
    "operator_name",
    "pit",
    "pit_name",
    "pattern_name",
    "pattern",
    "rod_sequence",
    "rock_type_id",
    "rock_type",
    "drill_string_resonant_length",
    "hole_start",
    "bit_type",
    "operator_name",
    "splits",
]


RHINO_BASIC_COLUMNS = [
    "bench_name",
    "pattern_name",
    "hole_name",
    "depth",
    "easting",
    "northing",
    "elevation",
    "collar_elevation",
    "sensor_id",
    "timestamp",
    "mse",
]

MWD_COLUMNS = [
    "pit",
    "hole",
    "bench",
    "pattern",
    "X",
    "Y",
    "Z",
    "measured_depth",
    "true_vertical_depth",
    "hole_angle",
    "hole_azimuth",
    "rod_sequence",
    "hole_start",
    "time_start",
    "time_end",
    "start_depth",
    "end_depth",
    "rpm",
    "weight_on_bit",
    "torque",
    "rop",
    "air_pressure",
    "vibration",
    "blastability",
    "collar_elevation",
    "computed_elevation",
    "easting",
    "northing",
    "mse",
    "hole_profile_id",
    "machine_id",
    "hole_start",
    "time_start",
    "time_end",
]

RECIPES = ["J0", "J1", "K0", "J2"]

COMPONENTS = ["axial", "tangential", "radial"]

WINDOWS = [
    "primary",
    "multiple_1",
    "multiple_2",
    "noise_1",
    "noise_2",
    "multiple",
    "multiple_3",
]
FEATURES = [
    "time_pick",
    "amplitude",
    "maximum_time",
    "maximum_amplitude",
    "minimum_time",
    "minimum_amplitude",
    "integrated_absolute_amplitude",
    "additional_pick_based_left_integrated_absolute_amplitude",
    "additional_pick_based_right_integrated_absolute_amplitude",
    "zero_crossing_time",
    "zero_crossing_negative_slope",
    "zero_crossing_positive_slope",
    "jazz1_left_integrated_amplitude",
    "jazz1_right_integrated_amplitude",
    "jazz1_center_integrated_amplitude",
]

PRIMARY_AMPLITUDES = [
    "J2-axial-primary-integrated_absolute_amplitude",
    "J2-tangential-primary-integrated_absolute_amplitude",
    "J2-tangential-primary-additional_pick_based_right_integrated_absolute_amplitude",
    "J2-axial-primary-additional_pick_based_right_integrated_absolute_amplitude",
    "J2-tangential-primary-additional_pick_based_left_integrated_absolute_amplitude",
    "J2-axial-primary-additional_pick_based_left_integrated_absolute_amplitude",
]

MULTIPLE_TO_NOISE_WINDOW_MAP = {"primary": "noise_1", "multiple_1": "noise_1"}

TEMPLATE = "{recipe}-{component}-{window}-{feature}"

def get_feature_string(
    recipe="K0", component="axial", window="multiple_1", feature="maximum_amplitude"
):

    return TEMPLATE.format(
        recipe=recipe, component=component, window=window, feature=feature
    )


__all__ = [
    COMPONENTS,
    FEATURES,
    RECIPES,
    TEMPLATE,
    WINDOWS,
    get_feature_string,
    MULTIPLE_TO_NOISE_WINDOW_MAP,
    RHINO_CATEGORICAL_COLUMNS,
]
