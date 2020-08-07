import logging
import numpy as np
from itertools import product
from rhino_lp.logs.utils import GetterClass
from rhino_lp.logs.constants import (
    COMPONENTS,
    FEATURES,
    RECIPES,
    TEMPLATE,
    WINDOWS,
    get_feature_string,
)

logger = logging.getLogger(__name__)


def _is_rhino_dataframe(df):
    return any(
        [
            ("J1-" in c) or ("K0-" in c) or ("B0-" in c) or ("J2-" in c) or ("J0-" in c)
            for c in df.columns
        ]
    )


def iterate_features():
    for i in product(RECIPES, COMPONENTS, WINDOWS, FEATURES):
        yield TEMPLATE.format(
            **dict(zip(["recipe", "component", "window", "feature"], i))
        )


class RhinoPhysics(object):
    """
    """

    def __init__(
        self, dataframe, config={}, use_recipe="J2", components_to_process=None
    ):

        # dataframe = amplitude_zero_to_nan(dataframe)

        self.dataframe = dataframe
        self.config = config
        self.current_recipe = use_recipe
        self._is_populated = False

        recipes = GetterClass(*RECIPES)

        if components_to_process is not None:
            self.components_to_process = components_to_process
        else:
            self.components_to_process = COMPONENTS

        for recipe in RECIPES:
            components = GetterClass(recipe)
            for component in self.components_to_process:
                windows = GetterClass(recipe, component)
                for window in WINDOWS:
                    features = GetterClass(recipe, component, window)
                    for feature in FEATURES:
                        string = get_feature_string(
                            recipe=recipe,
                            component=component,
                            window=window,
                            feature=feature,
                        )
                        if string in self.dataframe.columns:
                            setattr(features, feature, self.dataframe[string].view())
                        elif feature == "time_pick":
                            for replace_string in [
                                "maximum_time",
                                "max_time",
                                "zero_crossing_time",
                                "zero_crossing_positive_slope",
                                "zero_crossing_negative_slope",
                                "minimum_time",
                                "min_time",
                            ]:

                                replaced_string = string.replace(
                                    "time_pick", replace_string
                                )
                                if replaced_string in self.dataframe.columns:
                                    setattr(
                                        features,
                                        feature,
                                        self.dataframe[replaced_string].view(),
                                    )
                                    break
                        elif feature == "amplitude":
                            for replace_string in [
                                "integrated_absolute_amplitude",
                                "maximum_amplitude",
                                "max_amplitude",
                            ]:

                                replaced_string = string.replace(
                                    "amplitude", replace_string
                                )
                                if replaced_string in self.dataframe.columns:
                                    setattr(
                                        features,
                                        feature,
                                        self.dataframe[replaced_string].view(),
                                    )
                                    break
                    setattr(windows, window, features)
                setattr(components, component, windows)
            setattr(recipes, recipe, components)

        self.recipes = recipes
        for component in self.components_to_process:
            setattr(self, component, getattr(recipes[self.current_recipe], component))

    def __getitem__(self, name):
        return self.dataframe[name].values

    def __setitem__(self, name, value):
        self.dataframe[name] = value

    @property
    def _is_rhino(self):
        """
        Check if this is a Rhino dataframe.
        """
        return _is_rhino_dataframe(self.dataframe)

    @property
    def a_delay_1(self):
        return self.axial.multiple_1.time_pick - self.axial.primary.time_pick

    @property
    def a_delay_2(self):
        return self.axial.multiple_2.time_pick - self.axial.multiple_1.time_pick

    @property
    def a_density(self):
        return self.a_modulus_r_1 / (self.a_modulus_v_1 ** 2)

    @property
    def a_ratio(self):
        return self.axial.primary.amplitude / self.axial.multiple_1.amplitude

    @property
    def a_ratio_1(self):
        return self.a_ratio

    @property
    def a_ratio_2(self):
        return self.axial.multiple_1.amplitude / self.axial.multiple_2.amplitude

    @property
    def a_jazz_left(self):
        try:
            return (
                self.axial.multiple_1.jazz1_left_integrated_amplitude
            )
        except:
            return np.nan

    @property
    def a_jazz_right(self):
        try:
            return (
                self.axial.multiple_1.jazz1_right_integrated_amplitude
            )
        except:
            return np.nan

    @property
    def a_jazz_difference(self):
        try:
            return (
                self.a_jazz_right
                - self.a_jazz_left
            )
        except:
            return np.nan

    @property
    def a_phase_indicator(self):
        try:
            return (
                self.a_jazz_difference
                / self.axial.primary.integrated_absolute_amplitude
            )
        except:
            return np.nan

    @property
    def a_modulus_p(self):
        try:
            return (
                self.a_jazz_difference
                - self.axial.multiple_1.integrated_absolute_amplitude
            ) / self.axial.primary.integrated_absolute_amplitude
        except:
            return np.nan

    @property
    def c_modulus_p(self):
        try:
            x = (self.a_modulus_p - 0.4) / 3
            return (
                1105 * (x ** 4) + 2314 * (x ** 3) + 1778 * (x ** 2) + 732.4 * x + 135.6
            )
        except:
            return np.nan

    @property
    def a_jazz_ratio(self):
        try:
            return (
                self.a_jazz_left
                / self.a_jazz_right
            )
        except:
            return np.nan

    @property
    def a_modulus_r_1(self):
        return (1 - self.a_ratio_1) / (1 + self.a_ratio_1)

    @property
    def a_modulus_r_2(self):
        return (1 - self.a_ratio_2) / (1 + self.a_ratio_2)

    @property
    def a_reflection_coef(self):
        return self.a_modulus_r_1

    @property
    def a_strength(self):
        return np.sqrt(self.axial.primary.amplitude.astype(float))

    @property
    def a_modulus_v_1(self):
        return 1.0 / self.a_delay_1

    @property
    def a_modulus_v_2(self):
        return 1.0 / self.a_delay_2

    @property
    def t_delay_1(self):
        return self.tangential.multiple_1.time_pick - self.tangential.primary.time_pick

    @property
    def t_delay_2(self):
        return (
            self.tangential.multiple_2.time_pick - self.tangential.multiple_1.time_pick
        )

    @property
    def t_density(self):
        return self.t_modulus_r_1 / (self.t_modulus_v_1 ** 2)

    @property
    def t_ratio(self):
        return self.tangential.primary.amplitude / self.tangential.multiple_1.amplitude

    @property
    def t_ratio_1(self):
        return self.t_ratio

    @property
    def t_ratio_2(self):
        return (
            self.tangential.multiple_1.amplitude / self.tangential.multiple_2.amplitude
        )

    @property
    def t_modulus_r_1(self):
        return (1 - self.t_ratio) / (1 + self.t_ratio)

    @property
    def t_modulus_r_2(self):
        return (1 - self.t_ratio_2) / (1 + self.t_ratio_2)

    @property
    def t_reflection_coef(self):
        return self.t_modulus_r_1

    @property
    def t_strength(self):
        return np.sqrt(self.tangential.primary.amplitude.astype(float))

    @property
    def t_modulus_v_1(self):
        return 1.0 / self.t_delay_1

    @property
    def t_modulus_v_2(self):
        return 1.0 / self.t_delay_2

    @property
    def t_jazz_left(self):
        try:
            return (
                self.tangential.multiple_1.jazz1_left_integrated_amplitude
            )
        except:
            return np.nan

    @property
    def t_jazz_right(self):
        try:
            return (
                self.tangential.multiple_1.jazz1_right_integrated_amplitude
            )
        except:
            return np.nan

    @property
    def t_jazz_difference(self):
        try:
            return (
                self.tangential.multiple_1.jazz1_right_integrated_amplitude
                - self.tangential.multiple_1.jazz1_left_integrated_amplitude
            )
        except:
            return np.nan

    @property
    def t_phase_indicator(self):
        try:
            return (
                self.t_jazz_difference
                / self.tangential.primary.integrated_absolute_amplitude
            )
        except:
            return np.nan

    @property
    def t_jazz_ratio(self):
        try:
            return (
                self.tangential.multiple_1.jazz1_left_integrated_amplitude
                / self.tangential.multiple_1.jazz1_right_integrated_amplitude
            )
        except:
            return np.nan

    @property
    def t_modulus_p(self):
        try:
            return (
                self.t_jazz_difference
                - self.tangential.multiple_1.integrated_absolute_amplitude
            ) / self.tangential.primary.integrated_absolute_amplitude
        except:
            return np.nan

    def _populate(self):
        """
        Populates dataframe with all the physical properties defined in this
        class.
        """
        skip = (
            dir(type("dummy", (object,), {}))
            + [
                "_is_rhino",
                "dataframe",
                "_populate",
                "config",
                "recipes",
                "_drop_features",
                "current_recipe",
            ]
            + RECIPES
            + COMPONENTS
        )

        attrs = (
            item
            for item in dir(RhinoPhysics)
            if (item not in skip)
            and (("__" not in item))
            and (not item.startswith("_"))
            # and (not np.isnan(getattr(self, item)))
            # and (not getattr(self, item) is None)
            and (
                (not item.startswith("a_"))
                if "axial" not in self.components_to_process
                else True
            )
            and (
                (not item.startswith("t_"))
                if "tangential" not in self.components_to_process
                else True
            )
            and (
                (not item.startswith("r_"))
                if "radial" not in self.components_to_process
                else True
            )
        )

        for col in attrs:
            logger.debug("Adding {} to dataframe.".format(col))
            try:
                self.dataframe[col] = getattr(self, col)
            except Exception as e:
                logger.debug("Failed to add {} to dataframe, ERROR: {}".format(col, e))

        self._is_populated = True

    def _drop_features(self):
        """
        Drop extracted features. For now, it looks for matches of J0 and J1
        in the headers.
        """

    def __repr__(self):
        return "< Rhino | Recipe: {} | Populated: {} >".format(
            self.current_recipe, self._is_populated
        )
