import torch
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d

# =============================================================================================
# Modifying Datasets =============================================================================================
# =============================================================================================


def shape_factor(spec_vals, ekin, params):
    """Introduces a polynomial shapefactor to a beta spectrum

    Parameters
    -----------
    spec_vals: array
        Values of the beta spectrum

    params: array
        Parameters for the polynomial in order of increasing degree i.e. (1, 2) give 1 + 2*x
    """
    x = (ekin - ekin.max()) / ekin.max()
    p = 1
    for c, i in enumerate(params):
        p += i * x ** (c + 1)
    shaped_beta = p * spec_vals
    return shaped_beta


# =============================================================================================
# Processing Datasets =============================================================================================
# =============================================================================================


class Preprocessing:
    """
    Preprocessing class for preparing training datasets.

    This class provides methods for preprocessing spectra data, including feature standardization,
    min-max normalization, and data modification.

    Attributes:
    -----------
        seed (int): Random seed for reproducibility.
        rng (Generator): Random number generator.
        outputs (str): Type of output data.
        num_ref_spec (int): Number of reference spectra.
        modifications (dict): Dictionary specifying modifications to apply to the data.
        spectrum_type (str): Type of spectrum data.
        ms_range (tuple): Range of sterile mass values.
        s2t_log_range (tuple): Range of sin^2(2*theta) values.
        x_sterile (pd.Series): Sterile spectrum data.
        x_ref (pd.Series): Reference spectrum data.
        bin_width (int): Width of energy bins.
        e_range (tuple): Energy range.
        ekin (np.ndarray): Array of kinetic energies.
        y_sterile (np.ndarray): Labels for sterile spectrum data.
        y_ref (np.ndarray): Labels for reference spectrum data.
        m_s (np.ndarray): Sterile mass values.
        s2t (np.ndarray): Sin^2(2*theta) values.
        x (pd.Series or np.ndarray): Combined spectrum data.
        y (np.ndarray): Combined labels.
        m (np.ndarray): Combined mass values.
        s (np.ndarray): Combined sin^2(2*theta) values.

    Methods:
    --------
        scale(just_var=False): Perform feature standardization.
        min_max_scale(logscale=True): Perform min-max normalization.
        modify(): Apply modifications to the data.
        create_train_test_dataset(validation_split=0.5, scale=True, min_max_scale=True): Create training and validation datasets.
    """

    def __init__(self, spectra_df, use_case, seed=42):

        self.seed = seed
        self.rng = np.random.default_rng(seed)

        self.outputs = use_case["outputs"]
        self.num_ref_spec = use_case["num_ref_spec"]
        self.modifications = use_case["modifications"]
        self.spectrum_type = use_case["spectrum_type"]

        self.ms_range = (
            0,
            18600,
        )  # for parametrized models & correct min / max scaling
        self.s2t_log_range = (
            -8,
            -0.5,
        )  # for parametrized models & correct min / max scaling
        if self.spectrum_type == "both":
            self.x_sterile = spectra_df["sterile_noise"]
            self.x_ref = spectra_df["reference_noise"].iloc[: self.num_ref_spec]
            self.y_sterile = np.ones_like(self.x_sterile)
            self.y_ref = np.zeros_like(self.x_ref)
            self.bins = self.x_sterile.iloc[0].shape[0]
        if self.spectrum_type == "ref":
            self.x_ref = spectra_df["reference_noise"].iloc[: self.num_ref_spec]
            self.y_ref = np.zeros_like(self.x_ref)
            self.bins = self.x_ref.iloc[0].shape[0]
        if self.spectrum_type == "ster":
            self.x_sterile = spectra_df["sterile_noise"]
            self.y_sterile = np.ones_like(self.x_sterile)
            self.bins = self.x_sterile.iloc[0].shape[0]

        # for key in use_case.keys():
        #     if key == "no_noise":
        #         if use_case[key]:
        #             self.x_sterile = spectra_df["sterile_scaled"]
        #             self.x_ref = spectra_df["reference_scaled"].iloc[
        #                 : self.num_ref_spec
        #             ]

        for key in use_case.keys():
            if key == "no_noise":
                if use_case[key]:
                    self.x_sterile = spectra_df["sterile"]
                    self.x_ref = spectra_df["reference"].iloc[: self.num_ref_spec]

        # self.bin_width = 100  # eV
        self.e_range = (0, 18600)  # eV
        self.bin_width = (self.e_range[1] - self.e_range[0]) / self.bins
        self.ekin = np.linspace(
            self.e_range[0],
            self.e_range[1],
            int((self.e_range[1] - self.e_range[0]) / self.bin_width),
        )

        self.m_s = spectra_df["m_sterile"].to_numpy()
        # self.m_s_ref = np.zeros_like(self.m_s)
        self.s2t = spectra_df["sin2theta"].to_numpy()
        # self.s2t_ref = np.zeros_like(self.s2t)

        # updates after scaling and modification

        if self.spectrum_type == "both":
            self.x = pd.concat([self.x_sterile, self.x_ref])
            self.y = np.concatenate((self.y_sterile, self.y_ref))
            self.m = np.concatenate([self.m_s, self.m_s])
            self.s = np.concatenate([self.s2t, self.s2t])

        if self.spectrum_type == "ref":
            self.x = self.x_ref
            self.y = self.y_ref
            self.m = self.m_s
            self.s = self.s2t

        if self.spectrum_type == "ster":
            self.x = self.x_sterile
            self.y = self.y_sterile
            self.m = self.m_s
            self.s = self.s2t

    def scale(self, just_var=False):
        """
        Performes feature standardization. (Z-score Normalisation). Scales energy bin counts of beta decay spectra to have zero mean and unit variance:
        s = variance of spectrum
        u = mean of spectrum
        x_scaled = (x - u) / s
        if just_var:
            Normalization of data is changed to have unit variance
        """
        l = []
        for spectrum in self.x:
            if just_var:
                temp = (spectrum) / spectrum.std()
            else:
                temp = (spectrum - spectrum.mean()) / spectrum.std()

            l.append(temp)

        self.x = np.array(l, dtype=np.float64)

        return self.x

    def min_max_scale(self, logscale=True):
        """
        Perform min-max normalization with respect to the full sterile mass and mixing angle range.

        Args:
            logscale (bool, optional): If True, apply log scaling to sin^2(theta). Defaults to True.
        """

        if logscale:
            self.s = np.log10(self.s)

        self.m = -1 + (self.m - self.ms_range[0]) * 2 / (
            self.ms_range[1] - self.ms_range[0]
        )
        self.s = -1 + (self.s - self.s2t_log_range[0]) * 2 / (
            self.s2t_log_range[1] - self.s2t_log_range[0]
        )

    def modify(self):
        """
        Apply modifications to the data according to specified use case.

        This method allows for applying various modifications to the spectrum data, such as shape factor adjustments,
        energy range shifts, response matrices, or combinations thereof, as specified in the modifications dictionary.

        Supported modifications:
            - Shape Factor (shape_factor): Adjust the shape of the spectra by applying a shape factor (polynomial). For more info see the 'shape_factor' function.
            - Post-Analysis Energy (PAE): Shift the energy range of the spectra.
            - Response Matrix (RM): Apply a response matrix to the spectra.
            - List of Respone Matrices (RM_list): Apply a list of response matrices to each spectrum individually.
            - Dictionary of Pesponse Matrices (RM_dict): Apply different response matrices specified by keys.

        Returns:
            None
        """
        if self.modifications != None:
            for i in self.modifications.keys():
                if i == "shape_factor":
                    shape_fac_arr = self.modifications["shape_factor"]
                    if "idxs" in self.modifications:
                        shape_fac_arr = shape_fac_arr[self.modifications["idxs"]]
                    self.x = np.array(
                        [
                            shape_factor(
                                self.x.iloc[i],
                                self.ekin,
                                shape_fac_arr[i],
                            )
                            for i in range(shape_fac_arr.shape[0])
                        ],
                        dtype=np.float64,
                    )

                if i == "PAE":
                    E_PAE, e_range_post = self.modifications["PAE"]
                    num_bins_prev = int(
                        (self.e_range[1] - self.e_range[0]) / self.bin_width
                    )
                    num_bins_new = int(
                        (e_range_post[1] - e_range_post[0]) / self.bin_width
                    )
                    num_bins_shift = int(E_PAE / self.bin_width)
                    # update energy range
                    self.e_range = e_range_post
                    # update ekin
                    self.ekin = np.linspace(
                        self.e_range[0],
                        self.e_range[1],
                        int((self.e_range[1] - self.e_range[0]) / self.bin_width),
                    )
                    self.x = np.array(
                        [
                            np.concatenate(
                                (
                                    np.zeros(num_bins_shift),
                                    spectrum,
                                    np.zeros(
                                        num_bins_new - num_bins_shift - num_bins_prev
                                    ),
                                )
                            )
                            for spectrum in self.x
                        ],
                        dtype=np.float64,
                    )

                if i == "smoothing_kernel":
                    sigma = self.modifications["smoothing_kernel"]
                    self.x = np.array(
                        [gaussian_filter1d(i, sigma) for i in self.x], dtype=np.float64
                    )

                if i == "RM":
                    R = self.modifications["RM"]
                    self.x = np.array(
                        [i @ R for i in self.x], dtype=np.float64
                    )  # TODO: Account for different energy range after RM

                if i == "RM_list":  # slow
                    if len(self.modifications["RM_list"]) == self.x.shape[0]:
                        self.x = np.array(
                            [
                                i @ self.modifications["RM_list"][c]
                                for c, i in enumerate(self.x)
                            ],
                            dtype=np.float64,
                        )

                if i == "RM_dict":
                    keys = self.modifications["RM_dict"]["keys"]
                    if len(keys) == self.x.shape[0]:
                        self.x = np.array(
                            [
                                i @ self.modifications["RM_dict"][keys[c]]
                                for c, i in enumerate(self.x)
                            ],
                            dtype=np.float64,
                        )

                if i == "RM_interp":
                    dead_mean = self.modifications["RM_interp"]["dead_mean"]
                    dead_sigma = self.modifications["RM_interp"]["dead_sigma"]
                    interp_vals = dead_mean + dead_sigma * self.rng.standard_normal(
                        self.x.shape[0]
                    )

                    self.x = np.array(
                        [
                            i
                            @ self.modifications["RM_interp"]["interp_obj"](
                                interp_vals[c]
                            )
                            for c, i in enumerate(self.x)
                        ],
                        dtype=np.float64,
                    )

    def create_train_test_dataset(
        self, validation_split=0.5, scale=True, min_max_scale=True, chisq=False
    ):
        """
        Create training and validation datasets.

        Args:
            validation_split (float, optional): Fraction of data to use for validation. Defaults to 0.5.
            scale (bool, optional): If True, perform feature standardization. Defaults to True.
            min_max_scale (bool, optional): If True, perform min-max scaling on the additional parameters for a parametrized NN. Defaults to True.

        Returns:
            tuple: Depending on the specified outputs, returns training and validation datasets.
        """

        rng_idxs = self.rng.choice(np.arange(self.x.shape[0]), self.x.shape[0])
        rng_idx_val = rng_idxs[: int(self.x.shape[0] * validation_split)]
        rng_idx_train = rng_idxs[int(self.x.shape[0] * validation_split) :]

        if scale:
            self.scale()

        if self.outputs == "xy":
            x_train = self.x[rng_idx_train]
            y_train = self.y[rng_idx_train]
            x_val = self.x[rng_idx_val]
            y_val = self.y[rng_idx_val]
            return (
                x_train,
                y_train,
                x_val,
                y_val,
            )  # maybe need to change this to numpy array

        if self.outputs == "xyms":
            if min_max_scale:
                self.min_max_scale()
            x_train = self.x[rng_idx_train]
            y_train = self.y[rng_idx_train]
            m_s_train = self.m[rng_idx_train]
            s2t_train = self.s[rng_idx_train]
            x_val = self.x[rng_idx_val]
            y_val = self.y[rng_idx_val]
            m_s_val = self.m[rng_idx_val]
            s2t_val = self.s[rng_idx_val]
            return (
                x_train,
                y_train,
                m_s_train,
                s2t_train,
                x_val,
                y_val,
                m_s_val,
                s2t_val,
            )

        if self.outputs == "xy_no_split":
            if chisq:  # failsafe for case of single spectra in chisq scan
                return self.x, self.y

            x = self.x[rng_idxs]
            y = self.y[rng_idxs]
            return x, y

        if self.outputs == "xyms_no_split":
            if min_max_scale:
                self.min_max_scale()
            x = self.x[rng_idxs]
            y = self.y[rng_idxs]
            m = self.m[rng_idxs]
            s = self.s[rng_idxs]
            return x, y, m, s


# =============================================================================================
# Creating Datasets =============================================================================================
# =============================================================================================


class Dataset:
    def __init__(self, x, y, seed):
        self.x, self.y = x, y

        self.seed = seed
        self.rng = np.random.default_rng(self.seed)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return self.x[i], self.y[i]

    def shuffle(self):
        rng_idxs = self.rng.choice(
            np.arange(self.x.shape[0]), self.x.shape[0], replace=False
        )
        self.x = self.x[rng_idxs]
        self.y = self.y[rng_idxs]


class DataLoader:
    def __init__(self, dataset, batch_size, device):
        self.ds, self.bs = dataset, batch_size
        self.device = device

    def __iter__(self):
        for i in range(0, len(self.ds), self.bs):
            x, y = self.ds[i : i + self.bs]
            x, y = torch.FloatTensor(x.astype(np.float64)), torch.FloatTensor(
                y.astype(np.float64)
            ).unsqueeze(-1)
            batch = x.to(self.device), y.to(self.device)
            yield batch


class Dataset_Parametrized(Dataset):
    def __init__(self, x, y, m_s, s2t, seed=42):
        super().__init__(x, y, seed)
        self.m_s, self.s2t = m_s, s2t

    def __getitem__(self, i):
        return self.x[i], self.y[i], self.m_s[i], self.s2t[i]

    def shuffle_parametrized(self):
        rng_idxs = self.rng.choice(
            np.arange(self.x.shape[0]), self.x.shape[0], replace=False
        )
        self.x = self.x[rng_idxs]
        self.y = self.y[rng_idxs]
        self.m_s = self.m_s[rng_idxs]
        self.s2t = self.s2t[rng_idxs]


class DataLoader_Parametrized(DataLoader):
    def __init__(self, dataset, batch_size, device):
        super().__init__(dataset, batch_size, device)

    def __iter__(self):
        for i in range(0, len(self.ds), self.bs):
            x, y, m_s, s2t = self.ds[i : i + self.bs]
            x, y, m_s, s2t = (
                torch.FloatTensor(x.astype(np.float64)),
                torch.FloatTensor(y.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s2t.astype(np.float64)).unsqueeze(-1),
            )
            batch = (
                x.to(self.device),
                y.to(self.device),
                m_s.to(self.device),
                s2t.to(self.device),
            )
            yield batch


# old 10.04.24
# class Dataset:
#     def __init__(self, x, y):
#         self.x, self.y = x, y

#     def __len__(self):
#         return len(self.x)

#     def __getitem__(self, i):
#         return self.x[i], self.y[i]


# class DataLoader:
#     def __init__(self, dataset, batch_size, device):
#         self.ds, self.bs = dataset, batch_size
#         self.device = device

#     def __iter__(self):
#         for i in range(0, len(self.ds), self.bs):
#             x, y = self.ds[i : i + self.bs]
#             x, y = torch.FloatTensor(x.astype(np.float64)), torch.FloatTensor(
#                 y.astype(np.float64)
#             ).unsqueeze(-1)
#             batch = x.to(self.device), y.to(self.device)
#             yield batch


# old old
# class Dataset:
#     def __init__(self, x, y):
#         self.x, self.y = x, y

#     def __len__(self):
#         return len(self.x)

#     def __getitem__(self, i):
#         return self.x[i], self.y[i]


# class DataLoader:
#     def __init__(self, dataset, batch_size, device):
#         self.ds, self.bs = dataset, batch_size
#         self.device = device

#     def __iter__(self):
#         for i in range(0, len(self.ds), self.bs):
#             x, y = self.ds[i : i + self.bs]
#             x, y = torch.FloatTensor(x), torch.FloatTensor(y).unsqueeze(-1)
#             batch = x.to(self.device), y.to(self.device)
#             yield batch
