import torch
import einops
import numpy as np
import pandas as pd
from typing import List, Optional
from spectral_encoding.datamodel import Sensor


def get_encoding(
    dataset: pd.DataFrame,
    sensor: str
) -> Optional[List[float]]:
    """ This function returns the encoding of the sensor

    Args:
        dataset (pd.DataFrame): The dataset with the sensors information
        sensor (str): The sensor to get the encoding

    Returns:
        Optional[List[float]]: The encoding of the sensor
    """
    # Filter the dataset by the sensor
    sensor_data = dataset[dataset["Sensor"] == sensor]
    sensor_data_summary = []

    # Obtaint the FWHM values for the bands
    #band = "CoastalAerosol"
    for band in sensor_data["band_name"].unique():
        # Filter the dataset by the band
        dfs = sensor_data[
            sensor_data["band_name"] == band].loc[:, ["Wavelength", "SRF"]
        ]
        dfs.sort_values("Wavelength", inplace=True)
        dfs.reset_index(drop=True, inplace=True)
        
        # reference wavelengths
        all_wavelengths = pd.Series(
            range(
                dfs.Wavelength.min(),
                dfs.Wavelength.max() + 1,
            )
        )
        dfs = pd.merge(
            all_wavelengths.to_frame(name="Wavelength"),
            dfs,
            on="Wavelength",
            how="left",
        ).interpolate(method="linear", limit_direction="both")
        dfs.sort_values("Wavelength", inplace=True)

        # Get the FWHM values
        fwhm_lower = dfs[dfs["SRF"] >= 0.5].iloc[0].Wavelength
        fwhm_upper = dfs[dfs["SRF"] >= 0.5].iloc[-1].Wavelength

        # Get the FWHM area ratio
        fwhm_area = dfs[dfs.Wavelength.between(fwhm_lower, fwhm_upper)].SRF.sum()
        fwhm_ratio = normalize_and_adjust(
            fwhm_area / (fwhm_upper - fwhm_lower + 1), 1.0
        )

        row = {
            "band_name": band,
            "fwhm_min": int(fwhm_lower),
            "fwhm_max": int(fwhm_upper),
            "fwhm_area_ratio": int(fwhm_ratio  * 1000),
            "gsd": sensor_data[sensor_data["band_name"] == band]["GSD"].values[0]*10,
        }
        sensor_data_summary.append(row)        
    return pd.DataFrame(sensor_data_summary)


def normalize_and_adjust(values, temperature):
    """
    Normalize values originally between 0.7 and 1 to the range [0, 1] and
    adjust them using a temperature parameter.
    
    Args:
    - values (np.array): Array of values between 0.7 and 1.
    - temperature (float): Temperature parameter to adjust the 
    normalized values.
    
    Returns:
    - np.array: Adjusted values in the range [0, 1].
    """
    # if values is lower than 0.5, change it to 0.5
    values = np.where(values < 0.5, 0.5, values)

    # Normalize values to range [0, 1]
    normalized_values = (values - 0.5) / (1.0 - 0.5)
    
    # Apply the temperature parameter
    adjusted_values = normalized_values ** temperature
    
    return adjusted_values



class FourierEncoding(torch.nn.Module):
    def __init__(self, d_model, max_freq=10000):
        super(FourierEncoding, self).__init__()
        self.d_model = d_model
        self.max_freq = max_freq

    def forward(self, x):
        # x is a 1D tensor of GSD values
        batch_size = x.size(0)
        
        # Calculate the positional encodings
        pe = torch.zeros(batch_size, self.d_model)
        position = x.unsqueeze(1)
        
        div_term = torch.exp(
            torch.arange(0, self.d_model, 2).float() * -(np.log(self.max_freq) / self.d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        return pe


def sensor_encoder(
    object: Sensor,
    encoding_dim: int = 64,
    max_freq: int = 10000
) -> torch.Tensor:
    """
    Encode the sensor object using the Fourier encoding.
    
    Args:
    - object (Sensor): Sensor object to encode.
    
    Returns:
    - torch.Tensor: Encoded sensor object.
    """
    # Set the encoding dimension model
    fourier_encoder = FourierEncoding(
        d_model=encoding_dim,
        max_freq=max_freq
    )

    sensor_encoded = torch.zeros(len(object.bands), encoding_dim*4)
    for band in object.bands:

        # Get the values to encode
        to_encode = torch.tensor(
            [band.fwhm_min, band.fwhm_max, band.fwhm_ratio, band.gsd],
            dtype=torch.float32
        )

        # Encode the values
        encoded_values = fourier_encoder(to_encode).flatten()
        sensor_encoded[object.bands.index(band)] = encoded_values

    return sensor_encoded