import base
import pandas as pd
import sklearn.preprocessing
import utils
import numpy as np
import random
import electricity

np.random.seed(21)
random.seed(21)

ElectricityFormatter = electricity.ElectricityFormatter
DataTypes = base.DataTypes
InputTypes = base.InputTypes


class AirQualityFormatter(ElectricityFormatter):

    _column_definition = [
        ('hours_from_start', DataTypes.REAL_VALUED, InputTypes.TIME),
        ('CO', DataTypes.REAL_VALUED, InputTypes.TARGET),
        ('PM2.5', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('PM10', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('SO2', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('NO2', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('O3', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('TEMP', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('PRES', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('DEWP', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('RAIN', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('WSPM', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('day_of_week', DataTypes.REAL_VALUED, InputTypes.KNOWN_INPUT),
        ('id', DataTypes.REAL_VALUED, InputTypes.ID),
    ]

    def get_fixed_params(self):
        """Returns fixed model parameters for experiments."""

        fixed_params = {
            'total_time_steps': 8 * 24,
            'num_encoder_steps': 7 * 24,
            'num_epochs': 100,
            'early_stopping_patience': 5,
            'multiprocessing_workers': 5
        }

        return fixed_params

    def get_default_model_params(self):
        """Returns default optimised model parameters."""

        model_params = {
            'dropout_rate': 0.3,
            'hidden_layer_size': 320,
            'learning_rate': 0.001,
            'minibatch_size': 128,
            'max_gradient_norm': 100.,
            'num_heads': 4,
            'stack_size': 1
        }

        return model_params

    def get_num_samples_for_calibration(self):
        """Gets the default number of training and validation samples.
        Use to sub-sample the data for network calibration and a value of -1 uses
        all available samples.
        Returns:
          Tuple of (training samples, validation samples)
        """
        return 38400, 480
