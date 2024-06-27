"""Helpful functions to speed up dataset generation and plotting"""

import numpy as np
from beta_gen import *
from models import *
import scipy
from datetime import date
import tqdm.notebook


# ==============================================================================================================================================
# Data Gen --------------------------------------------------------------------------------------------------------
# ==============================================================================================================================================


def data_gen_pipeline(
    spectrum_parameters,
    model_type,
    use_case=False,
    parametrized=False,
    return_spec_df=False,
    only_train_val=False,
):
    """
    Generates and customizes training data for a specified model type.

    Args:
        spectrum_parameters (dict): Parameters for generating spectra.
        model_type (str): Type of model ("AE" for autoencoder or "MLP" for multilayer perceptron).
        use_case (bool, optional): Whether to use case-specific modifications. Defaults to False.
        parametrized (bool, optional): Whether to use parametrized training data, i.e. include an array of sterile mixing angle and sterile mass for each training spectrum. Defaults to False.

    Returns:
        tuple: Tuple containing training and validation data based on the specified model type.
            If model_type is "AE":
                For parametrized=True:
                    Returns a tuple (X_train_AE, y_train_AE, m_train_AE, s_train_AE,
                    X_test_AE, y_test_AE, m_test_AE, s_test_AE, X_val_sterile,
                    y, m_val_sterile, s_val_sterile, X_ref, y_ref, m_ref, s_ref).
                For parametrized=False:
                    Returns a tuple (X_train_AE, X_test_AE, y_train_AE, y_test_AE,
                    X_val_sterile, y, X_ref, y_ref).
            If model_type is "MLP":
                For parametrized=True:
                    Returns a tuple (X_train_mlp, y_train_mlp, m_train_mlp, s_train_mlp,
                    X_test_mlp, y_test_mlp, m_test_mlp, s_test_mlp, X_val_sterile_mlp,
                    y_val_sterile_mlp, m_val_sterile_mlp, s_val_sterile_mlp, X_val_ref_mlp,
                    y_val_ref_mlp, m_val_ref_mlp, s_val_ref_mlp).
                For parametrized=False:
                    Returns a tuple (X_train_mlp, y_train_mlp, X_test_mlp, y_test_mlp,
                    X_val_sterile_mlp, y_val_sterile_mlp, X_val_ref_mlp, y_val_ref_mlp).

    Examples:
        For examples of the spectrum_parameters dictionary, have a look at the jupyter notebooks (e.g. Cookbook.ipynb)
        For examples of the use of this function, have a look at the jupyter notebooks (e.g. Cookbook.ipynb)
    """

    # num ster spec
    num_ster_spec = int(
        spectrum_parameters["num_spec_it"] * spectrum_parameters["num_sterile_vals"]
    )
    # setting up inputs to the beta spectrum function
    ekin = np.linspace(
        spectrum_parameters["ekin_min"],
        spectrum_parameters["ekin_max"],
        spectrum_parameters["bins"],
    )

    if spectrum_parameters["smallterms"]:
        smallterms = np.ones(
            num_ster_spec,
            dtype=bool,
        )
    else:
        smallterms = np.zeros(
            num_ster_spec,
            dtype=bool,
        )

    m_neutrino = np.ones(num_ster_spec) * spectrum_parameters["m_n"]

    m_sterile_vals = np.linspace(
        spectrum_parameters["m_sterile_min"],
        spectrum_parameters["m_sterile_max"],
        spectrum_parameters["num_sterile_vals"],
    )
    m_sterile_arr = np.array([])
    sin2theta_arr = np.array([])

    for mass in m_sterile_vals:
        m_s = np.ones(int(spectrum_parameters["num_spec_it"])) * mass
        sin2theta = np.logspace(
            spectrum_parameters["sin2theta_log_max"],
            spectrum_parameters["sin2theta_log_min"],
            int(spectrum_parameters["num_spec_it"]),
        )
        m_sterile_arr = np.concatenate((m_sterile_arr, m_s))
        sin2theta_arr = np.concatenate((sin2theta_arr, sin2theta))

    # generating the spectra for training
    if (
        m_neutrino.shape
        == m_sterile_arr.shape
        == smallterms.shape
        == sin2theta_arr.shape
    ):
        # spectra_train = gen_spectra_fast(
        #     ekin,
        #     m_neutrino=m_neutrino,
        #     m_sterile=m_sterile_arr,
        #     sin2theta=sin2theta_arr,
        #     smallterms=smallterms,
        #     accurate_noise=True,
        # )
        # spectra_df = pd.DataFrame(spectra_train)

        Spectra_generator = Gen_Spec(
            ekin,
            m_neutrino=m_neutrino,
            m_sterile=m_sterile_arr,
            sin2theta=sin2theta_arr,
            smallterms=smallterms,
        )

        spectra_df = Spectra_generator.gen_fast(
            sterile=True, reference=True, sterile_noise=True, reference_noise=True
        )
        if return_spec_df:
            return spectra_df

    else:
        print(
            f"shapes dont match! {m_neutrino.shape == m_sterile_arr.shape == smallterms.shape == sin2theta_arr.shape}"
        )

    # Mod List
    mod_dict = spectrum_parameters["mod_dict"]

    if model_type == "AE":
        # Train spectra only containing reference spectra (i.e. no sterile)
        only_ref_train_dict = {
            "outputs": "xy",
            "num_ref_spec": num_ster_spec,
            "spectrum_type": "ref",
            "modifications": mod_dict,
        }
        if parametrized:
            only_ref_train_dict["outputs"] = "xyms"
            only_ref_train_data = Preprocessing(
                spectra_df, use_case=only_ref_train_dict
            )
            only_ref_train_data.modify()
            (
                X_train_AE,
                y_train_AE,
                m_train_AE,
                s_train_AE,
                X_test_AE,
                y_test_AE,
                m_test_AE,
                s_test_AE,
            ) = only_ref_train_data.create_train_test_dataset(validation_split=0.2)
        else:
            only_ref_train_data = Preprocessing(
                spectra_df, use_case=only_ref_train_dict
            )
            only_ref_train_data.modify()
            X_train_AE, y_train_AE, X_test_AE, y_test_AE = (
                only_ref_train_data.create_train_test_dataset(validation_split=0.2)
            )

        # Validation spectra for reconstruction loss only containing steriles
        only_ster_val_dict = {
            "outputs": "xy_no_split",
            "num_ref_spec": 0,
            "spectrum_type": "ster",
            "modifications": mod_dict,
        }
        if parametrized:
            only_ster_val_dict["outputs"] = "xyms_no_split"
            only_ster_val_data = Preprocessing(spectra_df, use_case=only_ster_val_dict)
            only_ster_val_data.modify()
            X_val_sterile, y, m_val_sterile, s_val_sterile = (
                only_ster_val_data.create_train_test_dataset(validation_split=0)
            )

        else:
            only_ster_val_data = Preprocessing(spectra_df, use_case=only_ster_val_dict)
            only_ster_val_data.modify()
            X_val_sterile, y = only_ster_val_data.create_train_test_dataset(
                validation_split=0
            )

        # Validation spectra for reference reconstruction loss only containing reference spectra (i.e. no sterile)
        ref_reco_loss_dict = {
            "outputs": "xy_no_split",
            "num_ref_spec": X_val_sterile.shape[0],
            "spectrum_type": "ref",
            "modifications": mod_dict,
        }
        if parametrized:
            ref_reco_loss_dict["outputs"] = "xyms_no_split"
            ref_reco_loss_data = Preprocessing(spectra_df, use_case=ref_reco_loss_dict)
            ref_reco_loss_data.modify()
            X_ref, y_ref, m_ref, s_ref = ref_reco_loss_data.create_train_test_dataset(
                validation_split=0
            )

        else:
            ref_reco_loss_data = Preprocessing(spectra_df, use_case=ref_reco_loss_dict)
            ref_reco_loss_data.modify()
            X_ref, y_ref = ref_reco_loss_data.create_train_test_dataset(
                validation_split=0
            )

        if parametrized:
            return (
                X_train_AE,
                y_train_AE,
                m_train_AE,
                s_train_AE,
                X_test_AE,
                y_test_AE,
                m_test_AE,
                s_test_AE,
                X_val_sterile,
                y,
                m_val_sterile,
                s_val_sterile,
                X_ref,
                y_ref,
                m_ref,
                s_ref,
            )

        return (
            X_train_AE,
            X_test_AE,
            y_train_AE,
            y_test_AE,
            X_val_sterile,
            y,
            X_ref,
            y_ref,
        )

    if model_type == "MLP":
        # Train spectra w/ Mix of Sterile and Reference Spectra
        mix_train_dict = {
            "outputs": "xy",
            "num_ref_spec": num_ster_spec,
            "spectrum_type": "both",
            "modifications": mod_dict,
        }

        if parametrized:
            mix_train_dict["outputs"] = "xyms"
            mix_train_data = Preprocessing(spectra_df, use_case=mix_train_dict)
            mix_train_data.modify()
            (
                X_train_mlp,
                y_train_mlp,
                m_train_mlp,
                s_train_mlp,
                X_test_mlp,
                y_test_mlp,
                m_test_mlp,
                s_test_mlp,
            ) = mix_train_data.create_train_test_dataset(validation_split=0.2)
            if only_train_val:
                return [
                    X_train_mlp,
                    y_train_mlp,
                    m_train_mlp,
                    s_train_mlp,
                    X_test_mlp,
                    y_test_mlp,
                    m_test_mlp,
                    s_test_mlp,
                ]

        else:
            mix_train_data = Preprocessing(spectra_df, use_case=mix_train_dict)
            mix_train_data.modify()
            X_train_mlp, y_train_mlp, X_test_mlp, y_test_mlp = (
                mix_train_data.create_train_test_dataset(validation_split=0.2)
            )
            if only_train_val:
                return [X_train_mlp, y_train_mlp, X_test_mlp, y_test_mlp]

        if mod_dict != None:
            if "shape_factor" in mod_dict:
                rng_idxs_reco_loss = np.random.choice(
                    np.arange(mod_dict["shape_factor"].shape[0]),
                    size=(spectra_df.sterile.shape[0]),
                )
                mod_dict["idxs"] = rng_idxs_reco_loss

        # Validation spectra for output distribution only containing steriles
        only_ster_val_output_dict = {
            "outputs": "xy_no_split",
            "num_ref_spec": 0,
            "spectrum_type": "ster",
            "modifications": mod_dict,
        }

        if parametrized:
            only_ster_val_output_dict["outputs"] = "xyms_no_split"
            only_ster_val_output_data = Preprocessing(
                spectra_df, use_case=only_ster_val_output_dict
            )

            only_ster_val_output_data.modify()

            (
                X_val_sterile_mlp,
                y_val_sterile_mlp,
                m_val_sterile_mlp,
                s_val_sterile_mlp,
            ) = only_ster_val_output_data.create_train_test_dataset(validation_split=0)
        else:
            only_ster_val_output_data = Preprocessing(
                spectra_df, use_case=only_ster_val_output_dict
            )

            only_ster_val_output_data.modify()

            X_val_sterile_mlp, y_val_sterile_mlp = (
                only_ster_val_output_data.create_train_test_dataset(validation_split=0)
            )

        # Validation spectra for reference output distribution only containing reference spectra (i.e. no sterile)
        if mod_dict != None:
            if "shape_factor" in mod_dict:
                rng_idxs_ref_loss = np.random.choice(
                    np.arange(mod_dict["shape_factor"].shape[0]),
                    size=(X_val_sterile_mlp.shape[0]),
                )
                mod_dict["idxs"] = rng_idxs_ref_loss

        only_ref_val_output_dict = {
            "outputs": "xy_no_split",
            "num_ref_spec": X_val_sterile_mlp.shape[0],
            "spectrum_type": "ref",
            "modifications": mod_dict,
        }
        if parametrized:
            only_ref_val_output_dict["outputs"] = "xyms_no_split"
            only_ref_val_output_data = Preprocessing(
                spectra_df, use_case=only_ref_val_output_dict
            )

            only_ref_val_output_data.modify()

            X_val_ref_mlp, y_val_ref_mlp, m_val_ref_mlp, s_val_ref_mlp = (
                only_ref_val_output_data.create_train_test_dataset(validation_split=0)
            )

        else:
            only_ref_val_output_data = Preprocessing(
                spectra_df, use_case=only_ref_val_output_dict
            )

            only_ref_val_output_data.modify()

            X_val_ref_mlp, y_val_ref_mlp = (
                only_ref_val_output_data.create_train_test_dataset(validation_split=0)
            )

        if parametrized:
            return (
                X_train_mlp,
                y_train_mlp,
                m_train_mlp,
                s_train_mlp,
                X_test_mlp,
                y_test_mlp,
                m_test_mlp,
                s_test_mlp,
                X_val_sterile_mlp,
                y_val_sterile_mlp,
                m_val_sterile_mlp,
                s_val_sterile_mlp,
                X_val_ref_mlp,
                y_val_ref_mlp,
                m_val_ref_mlp,
                s_val_ref_mlp,
            )

        return (
            X_train_mlp,
            y_train_mlp,
            X_test_mlp,
            y_test_mlp,
            X_val_sterile_mlp,
            y_val_sterile_mlp,
            X_val_ref_mlp,
            y_val_ref_mlp,
        )


# Template

# # The number of bins the Generated Spectra should contain
# bins = 186

# ekin_min, ekin_max = 0, 18600

# # The number of different sterile neutrino masses we generate spectra with
# num_sterile_vals = 20
# # The number of spectra per iteration
# num_spec_it = 1e4
# print(f"Number of spectra that will be generated: {num_spec_it*num_sterile_vals} \n approx time per dataset: {num_spec_it*num_sterile_vals * bins / 186 * (3*60 + 23) / 1e6} seconds")

# m_sterile_min, m_sterile_max = 1, 18e3

# sin2theta_log_min, sin2theta_log_max = -6, -1

# m_neutrino = 1
# smallterms = True

# spectrum_parameters = {"bins": bins,
#                        "ekin_min": ekin_min,
#                        "ekin_max": ekin_max,
#                        "num_sterile_vals": num_sterile_vals,
#                        "num_spec_it": num_spec_it,
#                        "m_sterile_min": m_sterile_min,
#                        "m_sterile_max": m_sterile_max,
#                        "sin2theta_log_min": sin2theta_log_min,
#                        "sin2theta_log_max": sin2theta_log_max,
#                        "m_n": m_neutrino,
#                        "smallterms": smallterms}


# ==============================================================================================================================================
# Grid scan functions (m_s, sin2theta) --------------------------------------------------------------------------------------------------------
# ==============================================================================================================================================


def scan_data_pipeline(scan_dict):
    """
    Generates validation data for parameter grid scan.

    Args:
        scan_dict (dict): Dictionary containing parameters for the parameter scan.

    Returns:
        pandas.DataFrame: DataFrame containing the generated validation spectra.

    Examples:
        For examples of the scan_dict dictionary, have a look at the jupyter notebooks (e.g. Deadlayer.ipynb)
    """

    ekin = np.linspace(scan_dict["ekin_min"], scan_dict["ekin_max"], scan_dict["bins"])

    scan_params = (
        np.linspace(
            scan_dict["m_sterile_min"],
            scan_dict["m_sterile_max"],
            scan_dict["num_sterile_vals"],
        ),
        np.logspace(
            scan_dict["sin2theta_log_max"],
            scan_dict["sin2theta_log_min"],
            scan_dict["num_sin2theta_scan"],
        ),
    )

    m_sterile_vals = scan_params[0]
    sin2theta_vals = scan_params[1]

    m_sterile_arr = np.array([])
    sin2theta_arr = np.array([])

    if scan_dict["smallterms"]:
        smallterms = np.ones(
            int(
                scan_dict["num_sterile_vals"]
                * scan_dict["num_sin2theta_scan"]
                * scan_dict["num_spec_scan"]
            ),
            dtype=bool,
        )
    else:
        smallterms = np.zeros(
            int(
                scan_dict["num_sterile_vals"]
                * scan_dict["num_sin2theta_scan"]
                * scan_dict["num_spec_scan"]
            ),
            dtype=bool,
        )

    m_neutrino = (
        np.ones(
            int(
                scan_dict["num_sterile_vals"]
                * scan_dict["num_sin2theta_scan"]
                * scan_dict["num_spec_scan"]
            )
        )
        * scan_dict["m_n"]
    )

    for mass in m_sterile_vals:
        m_s = np.ones(int(scan_dict["num_sin2theta_scan"])) * mass
        for i in range(scan_dict["num_spec_scan"]):
            m_sterile_arr = np.concatenate((m_sterile_arr, m_s))
            sin2theta_arr = np.concatenate((sin2theta_arr, sin2theta_vals))

    if (
        m_neutrino.shape
        == m_sterile_arr.shape
        == smallterms.shape
        == sin2theta_arr.shape
    ):
        Spectra_generator = Gen_Spec(
            ekin,
            m_neutrino=m_neutrino,
            m_sterile=m_sterile_arr,
            sin2theta=sin2theta_arr,
            smallterms=smallterms,
        )

        scan_spectra_df = Spectra_generator.gen_fast(
            sterile=True, reference=True, sterile_noise=True, reference_noise=True
        )

        # scan_spectra = gen_spectra_fast(
        #     ekin,
        #     m_neutrino=m_neutrino,
        #     m_sterile=m_sterile_arr,
        #     sin2theta=sin2theta_arr,
        #     smallterms=smallterms,
        #     accurate_noise=True,
        # )
        # scan_spectra_df = pd.DataFrame(scan_spectra)

        return scan_spectra_df

    else:
        print("shapes dont match!")


#   ChiSq --------------------------------------------------------------------------------------------------------


def chisq(y_ref, y_ster, V):

    # add epsilon to diagonal to ensure invertibility
    eps = np.diag(np.full((V.shape[0]), np.finfo(float).eps))
    V_inv = np.linalg.inv(V + eps)
    return (y_ster - y_ref).T @ V_inv @ (y_ster - y_ref)


def chisq_scan(scan_params, scan_df, V_syst=0, CL=0.95):  # OLD: use Gridsearch
    """Outdated, please use the Gridsearch class
    Computes the chi-square value of the data given reference data at different parameter gridpoints.
    It is possible to include systematics via the corresponding covariance matrices.

    Args:
        scan_params (tuple): Tuple containing arrays of parameter gridpoints for mass sterile neutrinos
            and sin^2(2*theta) values.
        scan_df (pd.DataFrame): DataFrame containing the data for the parameter scan.
        V_syst (bool, optional): Whether to include systematic uncertainties via covariance matrices. Defaults to False.
        CL (float, optional): Confidence level for the chi-square test. Defaults to 0.95.

    Returns:
        dict: A dictionary containing the chi-square values, contours, and confidence level.
            Keys:
                - "scan_matrix" (np.ndarray): Matrix of chi-square values for each grid point.
                - "contour_ms" (np.ndarray): Array of mass sterile neutrino values corresponding to the contour.
                - "contour_s2t" (np.ndarray): Array of sin^2(2*theta) values corresponding to the contour.
                - "perc" (float): Confidence level used for the chi-square test.
    """

    # Matrix to fill in chisq values for each grid point
    ChiSq_Vals = np.zeros((scan_params[0].shape[0], scan_params[1].shape[0]))
    s2t_scan_matrix = np.zeros_like(ChiSq_Vals)
    m_s_scan_matrix = np.zeros_like(ChiSq_Vals)

    # Calc z-value
    z_value_chisq = scipy.stats.chi2.ppf(CL, df=2)

    # Reference Spectrum
    y_ref = scan_df.reference_scaled[0]

    # Calc stat. cov. matrix
    V_stat = np.zeros((y_ref.shape[0] - 1, y_ref.shape[0] - 1))
    for count, i in enumerate(y_ref[:-1]):
        V_stat[count][count] = i

    V = V_stat + V_syst

    # run scan over grid
    for count_ms, test_ms in enumerate(scan_params[0]):
        for count_s2t, test_s2t in enumerate(scan_params[1]):
            y_mask1 = scan_df.m_sterile == test_ms
            s1 = scan_df[y_mask1]
            y_mask2 = s1.sin2theta == test_s2t
            s2 = s1[y_mask2]
            y_test = s2["sterile_scaled"].to_numpy()[0]

            chisq_it = chisq(y_ref[:-1], y_test[:-1], V)

            ChiSq_Vals[count_ms][count_s2t] = chisq_it
            s2t_scan_matrix[count_ms][count_s2t] = test_s2t
            m_s_scan_matrix[count_ms][count_s2t] = test_ms

    # get contours
    t = np.where(ChiSq_Vals <= z_value_chisq, s2t_scan_matrix, 0)
    s2t_ct_arr, m_s_ct_arr = ([], [])
    for row in range(t.shape[0]):
        idx = next((i for i, x in enumerate(t[row]) if x), None)
        m_s_ct = m_s_scan_matrix[row][idx]
        s2t_ct = t[row][idx]
        m_s_ct_arr.append(m_s_ct)
        s2t_ct_arr.append(s2t_ct)
    out_dict = {
        "scan_matrix": ChiSq_Vals,
        "contour_ms": np.array(m_s_ct_arr, dtype=np.float64),
        "contour_s2t": np.array(s2t_ct_arr, dtype=np.float64),
        "perc": z_value_chisq,
    }
    return out_dict


def percentile_uncertainty_gauss_approx(out, CL: int):
    perc = np.percentile(out, CL)
    alpha = CL / 100
    sigma = np.std(out)
    f = scipy.stats.norm.pdf(perc, loc=perc, scale=sigma)
    return 1 / f * np.sqrt(alpha * (1 - alpha) / out.shape[0])


class Gridsearch:
    def __init__(
        self,
        model,
        scan_spectra_df,
        scan_dict,
        CL,
        device="cpu",
        gen_data_on_the_fly=False,
    ):
        # if model != "chisq":
        #     if not gen_data_on_the_fly:
        #         assert (
        #             model.bins == scan_spectra_df["sterile_noise"][0].shape[0]
        #         ), "Model input shapes dont match data!"

        self.gen_data_on_the_fly = gen_data_on_the_fly

        self.scan_data = scan_spectra_df
        self.scan_dict = scan_dict
        self.CL = CL
        self.device = device
        self.model = model
        self.N_m_scan = scan_dict["num_sterile_vals"]
        self.N_sin2theta_scan = scan_dict["num_sin2theta_scan"]
        self.num_spec_scan = scan_dict["num_spec_scan"]
        self.model_type = scan_dict["model_type"]
        self.mod_dict = scan_dict["mod_dict"]

        if gen_data_on_the_fly:
            num_spec_tot = self.num_spec_scan * self.N_m_scan * self.N_sin2theta_scan
            self.only_ref_dict = {
                "outputs": "xy_no_split",
                "num_ref_spec": num_spec_tot,
                "spectrum_type": "ref",
                "modifications": self.mod_dict,
            }

        else:
            self.only_ref_dict = {
                "outputs": "xy_no_split",
                "num_ref_spec": self.scan_data.m_sterile.shape[0],
                "spectrum_type": "ref",
                "modifications": self.mod_dict,
            }

        self.only_ster_dict = {
            "outputs": "xy_no_split",
            "num_ref_spec": 0,
            "spectrum_type": "ster",
            "modifications": self.mod_dict,
        }

        self.scan_params = (
            np.linspace(
                self.scan_dict["m_sterile_min"],
                self.scan_dict["m_sterile_max"],
                self.N_m_scan,
            ),
            np.logspace(
                self.scan_dict["sin2theta_log_max"],
                self.scan_dict["sin2theta_log_min"],
                self.N_sin2theta_scan,
            ),
        )

        self.m_sterile_vals = self.scan_params[0]
        self.sin2theta_vals = self.scan_params[1]

        self.Out_scan = np.zeros((int(self.N_m_scan), int(self.N_sin2theta_scan)))
        self.s2t_scan_matrix = np.zeros_like(self.Out_scan)
        self.m_s_scan_matrix = np.zeros_like(self.Out_scan)
        self.scan_it_ster = []
        self.s2t_ct_arr, self.m_s_ct_arr = ([], [])

        self.Out_ref_perc_scan = np.zeros(
            (int(self.N_m_scan), int(self.N_sin2theta_scan))
        )

        for c_m, m in enumerate(self.m_sterile_vals):
            for c_s, s in enumerate(self.sin2theta_vals):
                self.s2t_scan_matrix[c_m][c_s] = s
                self.m_s_scan_matrix[c_m][c_s] = m

        # Variables that track the state of the gridsearch
        self.contour_flag = 0  # 0 -> no contour found so far
        self.current_pos = (0, 0)  # saves current position on the grid (m_s, s2t)
        self.search_results = np.zeros_like(
            self.Out_scan
        )  # here 0: area that has not been evaluated, 1: area that has been evaluted but no contour, 2: evaluated & contour

        # for errorbars on model prediction (in the gridsearch algorithm)
        self.contour_flag_pos = 0
        self.contour_flag_neg = 0

    def set_current_pos(self, value: tuple):
        self.current_pos = value

    def set_contour_flag(self, value: int, neg=False, pos=False):
        if neg:
            self.contour_flag_neg = value
        if pos:
            self.contour_flag_pos = value
        else:
            self.contour_flag = value

    def evaluate_gridpoint(self, gridpoint_data: pd.DataFrame, using_chisq=False):

        if using_chisq:  # for chisq scans with the covariance method

            self.only_ster_dict["outputs"] = "xy_no_split"
            only_ster_data = Preprocessing(
                gridpoint_data["dataframe"], use_case=self.only_ster_dict
            )
            only_ster_data.modify()
            X_after_cuts, y_after_cuts = only_ster_data.create_train_test_dataset(
                validation_split=0, scale=False, chisq=True
            )

            if isinstance(X_after_cuts, pd.Series):
                chisq_it = chisq(
                    gridpoint_data["ref_spec"].iloc[0],
                    X_after_cuts.iloc[0],
                    gridpoint_data["V"],
                )
            # if isinstance(X_after_cuts, pd.Series):
            #     chisq_it = chisq(
            #         gridpoint_data["ref_spec"].iloc[0][: gridpoint_data["idx_nonzero"]],
            #         X_after_cuts.iloc[0][: gridpoint_data["idx_nonzero"]],
            #         gridpoint_data["V"][
            #             : gridpoint_data["idx_nonzero"], : gridpoint_data["idx_nonzero"]
            #         ],
            #     )

            elif isinstance(gridpoint_data["ref_spec"], np.ndarray):
                chisq_it = chisq(
                    gridpoint_data["ref_spec"][0],
                    X_after_cuts[0],
                    gridpoint_data["V"],
                )
            # elif isinstance(gridpoint_data["ref_spec"], np.ndarray):
            #     chisq_it = chisq(
            #         gridpoint_data["ref_spec"][0][: gridpoint_data["idx_nonzero"]],
            #         X_after_cuts[0][: gridpoint_data["idx_nonzero"]],
            #         gridpoint_data["V"][
            #             : gridpoint_data["idx_nonzero"], : gridpoint_data["idx_nonzero"]
            #         ],
            #     )

            return chisq_it

        if self.model_type == "vanilla":

            self.only_ref_dict["outputs"] = "xy_no_split"
            self.only_ref_dict["num_ref_spec"] = gridpoint_data.m_sterile.shape[0]
            only_ref_data = Preprocessing(gridpoint_data, use_case=self.only_ref_dict)
            only_ref_data.modify()
            X_ref, y_ref = only_ref_data.create_train_test_dataset(validation_split=0)

            out_r = self.model.model_out(
                mode="ref",
                x_ref_test=X_ref,
                y_ref_test=y_ref,
                device=self.device,
            )

            # sterile output at gridpoint
            self.only_ster_dict["outputs"] = "xy_no_split"
            only_ster_data = Preprocessing(gridpoint_data, use_case=self.only_ster_dict)
            only_ster_data.modify()
            X_after_cuts, y_after_cuts = only_ster_data.create_train_test_dataset(
                validation_split=0
            )

            out_s = self.model.model_out(
                x_sterile_test=X_after_cuts,
                y_sterile_test=y_after_cuts,
                mode="ster",
                device=self.device,
            )

            return out_s, out_r

        if self.model_type == "parametrized":

            self.only_ref_dict["outputs"] = "xyms_no_split"
            self.only_ref_dict["num_ref_spec"] = gridpoint_data.m_sterile.shape[0]
            only_ref_data = Preprocessing(gridpoint_data, use_case=self.only_ref_dict)
            only_ref_data.modify()
            X_ref, y_ref, m_ref, s_ref = only_ref_data.create_train_test_dataset(
                validation_split=0
            )

            out_r = self.model.model_out(
                mode="ref",
                x_ref_test=X_ref,
                y_ref_test=y_ref,
                m_ref_test=m_ref,
                s_ref_test=s_ref,
                device=self.device,
            )

            # sterile output at gridpoint
            self.only_ster_dict["outputs"] = "xyms_no_split"
            only_ster_data = Preprocessing(gridpoint_data, use_case=self.only_ster_dict)
            only_ster_data.modify()
            X_after_cuts, y_after_cuts, m_after_cuts, s_after_cuts = (
                only_ster_data.create_train_test_dataset(validation_split=0)
            )

            out_s = self.model.model_out(
                x_sterile_test=X_after_cuts,
                y_sterile_test=y_after_cuts,
                m_sterile_test=m_after_cuts,
                s_sterile_test=s_after_cuts,
                mode="ster",
                device=self.device,
            )

            return out_s, out_r

    def generate_data(self, gridpoin_info, full_s2t_range=False, **spec_kwargs):

        m_s, s2t = gridpoin_info
        num_spec_scan = self.scan_dict["num_spec_scan"]

        if full_s2t_range:
            m_s_arr = np.ones(num_spec_scan * self.sin2theta_vals.shape[0]) * m_s
            s2t_arr = np.zeros((num_spec_scan, self.sin2theta_vals.shape[0]))
            for c, s2t in enumerate(self.sin2theta_vals):
                s2t_arr[c] = self.sin2theta_vals
            s2t_arr = s2t_arr.ravel()

            m_n_arr, smallterms_arr = (
                np.ones(num_spec_scan * self.sin2theta_vals.shape[0])
                * self.scan_dict["m_n"],
                np.ones(num_spec_scan * self.sin2theta_vals.shape[0])
                * self.scan_dict["smallterms"],
            )

        else:
            m_s_arr, s2t_arr = (
                np.ones(num_spec_scan) * m_s,
                np.ones(num_spec_scan) * s2t,
            )

            m_n_arr, smallterms_arr = (
                np.ones(num_spec_scan) * self.scan_dict["m_n"],
                np.ones(num_spec_scan) * self.scan_dict["smallterms"],
            )

        ekin = np.linspace(
            self.scan_dict["ekin_min"],
            self.scan_dict["ekin_max"],
            self.scan_dict["bins"],
        )

        Spectra_generator = Gen_Spec(
            ekin,
            m_neutrino=m_n_arr,
            m_sterile=m_s_arr,
            sin2theta=s2t_arr,
            smallterms=smallterms_arr,
        )
        scan_spectra_df = Spectra_generator.gen_fast(**spec_kwargs)

        # scan_spectra = gen_spectra_fast(
        #     ekin,
        #     m_neutrino=m_n_arr,
        #     m_sterile=m_s_arr,
        #     sin2theta=s2t_arr,
        #     smallterms=smallterms_arr,
        #     accurate_noise=True,
        # )
        # scan_spectra_df = pd.DataFrame(scan_spectra)

        return scan_spectra_df

    def searchplan_constructor(self):
        m_pos, s_pos = self.current_pos

        if s_pos == 0:
            plan = [i for i in range(self.N_sin2theta_scan)]

        if s_pos > 0:
            plan = [s_pos]
            for i in range(self.N_sin2theta_scan - 1):
                if i < s_pos:
                    if s_pos + i + 1 < self.N_sin2theta_scan:
                        plan.append(s_pos + i + 1)
                        plan.append(s_pos - i - 1)
                    if s_pos + i + 1 >= self.N_sin2theta_scan:
                        plan.append(s_pos - i - 1)

                if i >= s_pos:
                    plan.append(s_pos + i + 1)

        return plan[: self.N_sin2theta_scan]

    def check_for_contour(self):
        ms_atm = self.current_pos[0]

        row = self.search_results[ms_atm]

        for c_c, entry in enumerate(row):
            if entry == 1:
                if c_c + 1 < self.N_sin2theta_scan - 1:
                    if self.search_results[ms_atm][c_c + 1] == 2:
                        self.set_contour_flag(1)
                        self.s2t_ct_arr.append(self.sin2theta_vals[c_c])
                        self.m_s_ct_arr.append(self.m_sterile_vals[ms_atm])

            if entry == 2:
                if c_c == 0:
                    self.set_contour_flag(1)
                    self.s2t_ct_arr.append(self.sin2theta_vals[c_c])
                    self.m_s_ct_arr.append(self.m_sterile_vals[ms_atm])

    def perform_search(self, debug=True):

        for c_m, m_s in enumerate(self.m_sterile_vals):

            if debug:
                print(
                    f"Next sterile mass column: \n Current position: {self.current_pos}, (crosscheck with current m_s {m_s})"
                )

            self.set_contour_flag(0)

            if not self.gen_data_on_the_fly:
                m_s_mask = self.scan_data.m_sterile == m_s
                m_s_it_df = self.scan_data[m_s_mask]

            search_plan = self.searchplan_constructor()

            for s2t_idx in search_plan:
                if self.contour_flag == 0:

                    self.set_current_pos((c_m, s2t_idx))

                    if not self.gen_data_on_the_fly:
                        s2t_mask = m_s_it_df.sin2theta == self.sin2theta_vals[s2t_idx]
                        s2t_it_df = m_s_it_df[s2t_mask]
                    else:
                        s2t_it_df = self.generate_data(
                            gridpoin_info=(m_s, self.sin2theta_vals[s2t_idx])
                        )

                    out_s, out_r = self.evaluate_gridpoint(s2t_it_df)

                    o = out_s.mean()
                    perc_r = np.percentile(out_r, self.CL)

                    self.Out_scan[c_m][s2t_idx] = o
                    self.Out_ref_perc_scan[c_m][s2t_idx] = perc_r

                    if o <= perc_r:
                        self.search_results[c_m][s2t_idx] = 2
                    else:
                        self.search_results[c_m][s2t_idx] = 1

                    self.check_for_contour()

                    if self.contour_flag == 1:
                        self.set_current_pos((c_m + 1, s2t_idx))

        out_dict = {
            "scan_matrix": self.Out_scan,
            "model_out_ster_it": self.scan_it_ster,
            "contour_ms": np.array(self.m_s_ct_arr, dtype=np.float64),
            "contour_s2t": np.array(self.s2t_ct_arr, dtype=np.float64),
            "searched_positions": self.search_results,
            "perc": self.Out_ref_perc_scan,
        }

        return out_dict

    def get_errorbars(self):
        """Should only be called after a contour has been found.
        Construct error margin for the model prediction based on preexisting senistivity contour
        """
        s2t_ct_error_neg_arr, s2t_ct_error_pos_arr = ([], [])

        for c_m, m_s in enumerate(self.m_s_ct_arr):

            self.set_contour_flag(0, pos=True, neg=True)

            m_s_mask = self.scan_data.m_sterile == m_s
            m_s_it_df = self.scan_data[m_s_mask]

            idx_s2t_ct = np.where(self.scan_params[1] == self.s2t_ct_arr[c_m])[0][
                0
            ]  # get index of s2t array where contour is

            if idx_s2t_ct == 0:
                s2t_ct_error_neg_arr.append(self.scan_params[1][0])
                self.set_contour_flag(1, neg=True)

            search_plan_neg = np.flip(self.scan_params[1][: idx_s2t_ct + 1])
            search_plan_pos = self.scan_params[1][idx_s2t_ct:]

            for s2t in search_plan_pos:

                if self.contour_flag_pos == 0:

                    s2t_mask = m_s_it_df.sin2theta == s2t
                    s2t_it_df = m_s_it_df[s2t_mask]
                    out_s, out_r = self.evaluate_gridpoint(s2t_it_df)

                    o = out_s.mean()
                    sigma_out_s = np.std(out_s)
                    perc_r = np.percentile(out_r, self.CL)
                    sigma_perc = percentile_uncertainty_gauss_approx(out_r, self.CL)

                    if (
                        o - perc_r + sigma_out_s + sigma_perc <= 0
                    ):  # o <= perc_r - sigma_out_s - sigma_perc
                        s2t_ct_error_pos_arr.append(s2t)
                        self.set_contour_flag(1, pos=True)
                        # print("pos: ", c_m)

            for s2t in search_plan_neg:

                if self.contour_flag_neg == 0:

                    s2t_mask = m_s_it_df.sin2theta == s2t
                    s2t_it_df = m_s_it_df[s2t_mask]
                    out_s, out_r = self.evaluate_gridpoint(s2t_it_df)

                    o = out_s.mean()
                    sigma_out_s = np.std(out_s)
                    perc_r = np.percentile(out_r, self.CL)
                    sigma_perc = percentile_uncertainty_gauss_approx(out_r, self.CL)

                    if (
                        o >= perc_r + sigma_out_s + sigma_perc
                    ):  # o - perc_r - sigma_out_s - sigma_perc <= 0
                        s2t_ct_error_neg_arr.append(s2t)
                        self.set_contour_flag(1, neg=True)
                        # print("neg: ", c_m)

        return s2t_ct_error_neg_arr, s2t_ct_error_pos_arr

    def gridscan_full(self, errorbars=False, verbose=1):
        """Brute force gridscan, makes use of errorbars possible"""
        if errorbars:
            sigma_perc_tensor = np.zeros_like(self.Out_ref_perc_scan)

        only_ref_dict = {
            "outputs": "xy_no_split",
            "num_ref_spec": int(
                self.num_spec_scan * self.N_sin2theta_scan * self.N_m_scan
            ),
            "spectrum_type": "ref",
            "modifications": self.mod_dict,
        }

        # only_ref_dict = {
        #     "outputs": "xy_no_split",
        #     "num_ref_spec": self.scan_data.m_sterile.shape[0],
        #     "spectrum_type": "ref",
        #     "modifications": self.mod_dict,
        # }

        if self.model_type == "vanilla":
            if not self.gen_data_on_the_fly:
                only_ref_data = Preprocessing(self.scan_data, use_case=only_ref_dict)
                only_ref_data.modify()
                X_ref, y_ref = only_ref_data.create_train_test_dataset(
                    validation_split=0
                )
            else:
                scan_ref_df = self.generate_data(
                    gridpoin_info=(self.m_sterile_vals[0], self.sin2theta_vals[0]),
                    full_s2t_range=True,
                    reference=True,
                    reference_noise=True,
                )

                only_ref_data = Preprocessing(scan_ref_df, use_case=only_ref_dict)
                only_ref_data.modify()
                X_ref, y_ref = only_ref_data.create_train_test_dataset(
                    validation_split=0
                )

            # Distribution of model outputs for reference spectra
            out_r = self.model.model_out(
                mode="ref", x_ref_test=X_ref, y_ref_test=y_ref, device=self.device
            )
            perc = np.percentile(out_r, self.CL)
            self.Out_ref_perc_scan += perc

            if errorbars:
                sigma_perc = percentile_uncertainty_gauss_approx(out_r, self.CL)
                sigma_perc_tensor += 1
                sigma_perc_tensor *= sigma_perc

        with trange(len(self.m_sterile_vals), unit="m_s") as iterable:
            for count_i in iterable:
                m_s = self.m_sterile_vals[count_i]
                if verbose == 1:
                    iterable.set_description("Scanning")
                    iterable.set_postfix(
                        m_s=f"current sterile mass: {m_s}",
                    )

                if not self.gen_data_on_the_fly:
                    m_s_mask = self.scan_data.m_sterile == m_s
                    m_s_it_df = self.scan_data[m_s_mask]

                else:
                    m_s_it_df = self.generate_data(
                        gridpoin_info=(m_s, self.sin2theta_vals[0]),
                        full_s2t_range=True,
                        sterile=True,
                        reference=True,
                        sterile_noise=True,
                        reference_noise=True,
                    )

                for count_j, s2t in enumerate(self.sin2theta_vals):
                    s2t_mask = m_s_it_df.sin2theta == s2t
                    s2t_it_df = m_s_it_df[s2t_mask]

                    only_ster_dict = {
                        "outputs": "xy_no_split",
                        "num_ref_spec": 0,
                        "spectrum_type": "ster",
                        "modifications": self.mod_dict,
                    }

                    if self.model_type == "parametrized":
                        # Construct reference output for grid point
                        only_ref_dict["outputs"] = "xyms_no_split"
                        only_ref_dict["num_ref_spec"] = s2t_it_df.m_sterile.shape[0]
                        only_ref_data = Preprocessing(s2t_it_df, use_case=only_ref_dict)
                        only_ref_data.modify()
                        X_ref, y_ref, m_ref, s_ref = (
                            only_ref_data.create_train_test_dataset(validation_split=0)
                        )

                        out_r = self.model.model_out(
                            mode="ref",
                            x_ref_test=X_ref,
                            y_ref_test=y_ref,
                            m_ref_test=m_ref,
                            s_ref_test=s_ref,
                            device=self.device,
                        )

                        perc_r = np.percentile(out_r, self.CL)
                        self.Out_ref_perc_scan[count_i][count_j] = perc_r

                        only_ster_dict["outputs"] = "xyms_no_split"
                        only_ster_data = Preprocessing(
                            s2t_it_df, use_case=only_ster_dict
                        )
                        only_ster_data.modify()
                        X_after_cuts, y_after_cuts, m_after_cuts, s_after_cuts = (
                            only_ster_data.create_train_test_dataset(validation_split=0)
                        )

                        out_s = self.model.model_out(
                            x_sterile_test=X_after_cuts,
                            y_sterile_test=y_after_cuts,
                            m_sterile_test=m_after_cuts,
                            s_sterile_test=s_after_cuts,
                            mode="ster",
                            device=self.device,
                        )

                        if errorbars:
                            sigma_perc = percentile_uncertainty_gauss_approx(
                                out_r, self.CL
                            )
                            sigma_out_s = np.std(out_s)
                            sigma_perc_tensor[count_i][count_j] = sigma_out_s
                            # sigma_perc_tensor[count_i][count_j] = sigma_perc + sigma_out_s

                    else:
                        only_ster_data = Preprocessing(
                            s2t_it_df, use_case=only_ster_dict
                        )
                        only_ster_data.modify()
                        X_after_cuts, y_after_cuts = (
                            only_ster_data.create_train_test_dataset(validation_split=0)
                        )
                        out_s = self.model.model_out(
                            x_sterile_test=X_after_cuts,
                            y_sterile_test=y_after_cuts,
                            mode="ster",
                            device=self.device,
                        )

                        if errorbars:
                            sigma_out_s = np.std(out_s)
                            sigma_perc_tensor[count_i][count_j] += sigma_out_s

                    self.scan_it_ster.append(out_s)
                    self.Out_scan[count_i][count_j] = out_s.mean()
                    self.s2t_scan_matrix[count_i][count_j] = s2t
                    self.m_s_scan_matrix[count_i][count_j] = m_s

        if errorbars:
            s2t_ct_error_neg_arr, s2t_ct_error_pos_arr = ([], [])

        for r, row in enumerate(self.s2t_scan_matrix):
            flag = 0
            if errorbars:
                flag_neg = 0
                flag_pos = 0

            for c, column in enumerate(row):
                if flag == 0:
                    if self.Out_scan[r][c] <= self.Out_ref_perc_scan[r][c]:
                        self.m_s_ct_arr.append(self.m_s_scan_matrix[r][c])
                        self.s2t_ct_arr.append(self.s2t_scan_matrix[r][c])
                        flag = 1

                if errorbars:
                    if flag_neg == 0:
                        if (
                            self.Out_scan[r][c]
                            - self.Out_ref_perc_scan[r][c]
                            - sigma_perc_tensor[r][c]
                            <= 0
                        ):
                            s2t_ct_error_neg_arr.append(self.s2t_scan_matrix[r][c])
                            flag_neg = 1
                    if flag_pos == 0:
                        if (
                            self.Out_scan[r][c]
                            - self.Out_ref_perc_scan[r][c]
                            + sigma_perc_tensor[r][c]
                            <= 0
                        ):
                            s2t_ct_error_pos_arr.append(self.s2t_scan_matrix[r][c])
                            flag_pos = 1

        out_dict = {
            "scan_matrix": self.Out_scan,
            "model_out_ster_it": self.scan_it_ster,
            "model_out_ref_all": out_r,
            "contour_ms": np.array(self.m_s_ct_arr, dtype=np.float64),
            "contour_s2t": np.array(self.s2t_ct_arr, dtype=np.float64),
            "perc": self.Out_ref_perc_scan,
        }

        if errorbars:
            # out_dict["contour_ms_err"] = (m_s_ct_error_neg_arr, m_s_ct_error_pos_arr)
            out_dict["contour_s2t_err"] = (s2t_ct_error_neg_arr, s2t_ct_error_pos_arr)
            out_dict["error_tensor"] = sigma_perc_tensor

        return out_dict

    def gridscan_chisq_covariance(self, V_syst=0):
        """
        Computes the chi-square value of the data given reference data at different parameter gridpoints.
        It is possible to include systematics via the corresponding covariance matrices.

        Args:
            V_syst (bool, optional): Whether to include systematic uncertainties via covariance matrices. Defaults to False.

        Returns:
            dict: A dictionary containing the chi-square values, contours, and confidence level.
                Keys:
                    - "scan_matrix" (np.ndarray): Matrix of chi-square values for each grid point.
                    - "contour_ms" (np.ndarray): Array of mass sterile neutrino values corresponding to the contour.
                    - "contour_s2t" (np.ndarray): Array of sin^2(2*theta) values corresponding to the contour.
                    - "perc" (float): Confidence level used for the chi-square test.
        """
        # Only use spectra without noise
        self.only_ref_dict["no_noise"] = True
        self.only_ster_dict["no_noise"] = True

        # Calc z-value
        z_value_chisq = scipy.stats.chi2.ppf(self.CL / 100, df=2)

        # Get reference spectrum
        self.only_ref_dict["outputs"] = "xy_no_split"
        self.only_ref_dict["num_ref_spec"] = 1
        only_ref_data = Preprocessing(self.scan_data, use_case=self.only_ref_dict)
        only_ref_data.modify()
        X_ref, _ = only_ref_data.create_train_test_dataset(
            validation_split=0, scale=False
        )

        # Calc Stat. Cov. Matrix
        V_stat = np.zeros((X_ref[0].shape[0], X_ref[0].shape[0]))
        for count, i in enumerate(X_ref[0]):
            V_stat[count][count] = i

        # Add covariance matrices
        V = V_stat + V_syst

        # # Ensure invertibility by checking for zeros in diagonal    -> OLD, now added epsilon to diag
        # diag = np.diag(V)
        # idx_nonzero = np.nonzero(diag)[0][-1] + 1

        # run scan over grid
        for count_ms, test_ms in enumerate(self.scan_params[0]):
            for count_s2t, test_s2t in enumerate(self.scan_params[1]):
                mask_ms = self.scan_data.m_sterile == test_ms
                s1 = self.scan_data[mask_ms]

                mask_s2t = s1.sin2theta == test_s2t
                s2 = s1[mask_s2t]

                self.only_ster_dict["outputs"] = "xy_no_split"
                only_ster_data = Preprocessing(s2, use_case=self.only_ster_dict)
                only_ster_data.modify()
                X_after_cuts, y_after_cuts = only_ster_data.create_train_test_dataset(
                    validation_split=0, scale=False, chisq=True
                )

                if isinstance(X_after_cuts, pd.Series):
                    chisq_it = chisq(
                        X_ref.iloc[0],
                        X_after_cuts.iloc[0],
                        V,
                    )

                # if isinstance(X_after_cuts, pd.Series):
                #     chisq_it = chisq(
                #         X_ref.iloc[0][:idx_nonzero],
                #         X_after_cuts.iloc[0][:idx_nonzero],
                #         V[:idx_nonzero, :idx_nonzero],
                #     )

                elif isinstance(X_ref, np.ndarray):
                    chisq_it = chisq(
                        X_ref[0],
                        X_after_cuts[0],
                        V,
                    )
                # elif isinstance(X_ref, np.ndarray):
                #     chisq_it = chisq(
                #         X_ref[0][:idx_nonzero],
                #         X_after_cuts[0][:idx_nonzero],
                #         V[:idx_nonzero, :idx_nonzero],
                #     )

                self.Out_scan[count_ms][count_s2t] = chisq_it
                self.s2t_scan_matrix[count_ms][count_s2t] = test_s2t
                self.m_s_scan_matrix[count_ms][count_s2t] = test_ms

        # evaluate scan and extract contours
        for r, row in enumerate(self.s2t_scan_matrix):
            flag = 0
            for c, column in enumerate(row):
                if flag == 0:
                    if self.Out_scan[r][c] <= z_value_chisq:
                        self.m_s_ct_arr.append(self.m_s_scan_matrix[r][c])
                        self.s2t_ct_arr.append(self.s2t_scan_matrix[r][c])
                        flag = 1

        out_dict = {
            "chisq_matrix": self.Out_scan,
            "contour_ms": np.array(self.m_s_ct_arr, dtype=np.float64),
            "contour_s2t": np.array(self.s2t_ct_arr, dtype=np.float64),
            "perc": z_value_chisq,
        }

        return out_dict

    def gridsearch_chisq_covariance(self, V_syst=0, debug=True):
        # Only use spectra without noise
        self.only_ref_dict["no_noise"] = True
        self.only_ster_dict["no_noise"] = True

        # Calc z-value
        z_value_chisq = scipy.stats.chi2.ppf(self.CL / 100, df=2)

        # Get reference spectrum
        self.only_ref_dict["outputs"] = "xy_no_split"
        self.only_ref_dict["num_ref_spec"] = 1
        only_ref_data = Preprocessing(self.scan_data, use_case=self.only_ref_dict)
        only_ref_data.modify()
        X_ref, _ = only_ref_data.create_train_test_dataset(
            validation_split=0, scale=False
        )

        # Calc Stat. Cov. Matrix
        V_stat = np.zeros((X_ref[0].shape[0], X_ref[0].shape[0]))
        for count, i in enumerate(X_ref[0]):
            V_stat[count][count] = i

        # Add covariance matrices
        V = V_stat + V_syst

        # # Ensure invertibility by checking for zeros in diagonal  -> OLD, now adding epsilon to diag
        # diag = np.diag(V)
        # idx_nonzero = np.nonzero(diag)[0][-1] + 1

        # perform search
        for c_m, m_s in enumerate(self.m_sterile_vals):

            if debug:
                print(
                    f"Next sterile mass column: \n Current position: {self.current_pos}, (crosscheck with current m_s {m_s})"
                )

            self.set_contour_flag(0)

            m_s_mask = self.scan_data.m_sterile == m_s
            m_s_it_df = self.scan_data[m_s_mask]

            search_plan = self.searchplan_constructor()

            for s2t_idx in search_plan:
                if self.contour_flag == 0:

                    self.set_current_pos((c_m, s2t_idx))

                    s2t_mask = m_s_it_df.sin2theta == self.sin2theta_vals[s2t_idx]
                    s2t_it_df = m_s_it_df[s2t_mask]

                    gs_data = {
                        "dataframe": s2t_it_df,
                        "V": V,
                        "ref_spec": X_ref,
                    }

                    chisq_it = self.evaluate_gridpoint(
                        using_chisq=True, gridpoint_data=gs_data
                    )

                    self.Out_scan[c_m][s2t_idx] = chisq_it

                    if chisq_it <= z_value_chisq:
                        self.search_results[c_m][s2t_idx] = 2
                    else:
                        self.search_results[c_m][s2t_idx] = 1

                    self.check_for_contour()

                    if self.contour_flag == 1:
                        self.set_current_pos((c_m + 1, s2t_idx))

        out_dict = {
            "chisq_matrix": self.Out_scan,
            "contour_ms": np.array(self.m_s_ct_arr, dtype=np.float64),
            "contour_s2t": np.array(self.s2t_ct_arr, dtype=np.float64),
            "perc": z_value_chisq,
        }

        return out_dict


#   OLD ========================================================================================================
#   MLP --------------------------------------------------------------------------------------------------------


def model_scan_many(
    model_trained, scan_spectra_df, scan_dict, CL, plot=False, device="cpu"
):
    """
    Performs a scan over a grid of (m_sterile, sin2theta), calculating the Model Output at each point.
    Additionally, returns the percentile value of the Reference Model Output given a Confidence Level (CL).

    To calculate the Model Output, multiple spectra per grid point can (and should) be used, and the average Model Output will be returned.

    Args:
        model_trained (object): Trained model object capable of generating model outputs.
        scan_spectra_df (pd.DataFrame): DataFrame containing the spectra data for the parameter scan.
        scan_dict (dict): Dictionary containing parameters for the scan, including the number of grid points,
            model type, and modifications.
        CL (float): Confidence level for calculating the percentile value of the Reference Model Output.
        plot (bool, optional): Whether to plot the results. Defaults to False.
        device (str, optional): Device type for running the model (e.g., "cpu", "cuda"). Defaults to "cpu".

    Returns:
        dict: A dictionary containing the results of the scan and model outputs.
            Keys:
                - "scan_matrix" (np.ndarray): Matrix of Model Outputs for each grid point.
                - "model_out_ster_it" (list): List of model outputs for each grid point.
                - "model_out_ref_all" (float): Model output for reference spectra.
                - "contour_ms" (np.ndarray): Array of mass sterile neutrino values corresponding to the contour.
                - "contour_s2t" (np.ndarray): Array of sin^2(2*theta) values corresponding to the contour.
                - "perc" (float): Percentile value of the Reference Model Output given the Confidence Level.
    """

    # get params from scan_dict
    N_m_scan = scan_dict["num_sterile_vals"]
    N_sin2theta_scan = scan_dict["num_sin2theta_scan"]
    num_spec_scan = scan_dict["num_spec_scan"]
    model_type = scan_dict["model_type"]
    mod_dict = scan_dict["mod_dict"]

    scan_params = (
        np.linspace(scan_dict["m_sterile_min"], scan_dict["m_sterile_max"], N_m_scan),
        np.logspace(
            scan_dict["sin2theta_log_max"],
            scan_dict["sin2theta_log_min"],
            N_sin2theta_scan,
        ),
    )

    m_sterile_vals = scan_params[0]
    sin2theta_vals = scan_params[1]

    only_ref_dict = {
        "outputs": "xy_no_split",
        "num_ref_spec": scan_spectra_df.m_sterile.shape[0],
        "spectrum_type": "ref",
        "modifications": mod_dict,
    }

    if model_type == "vanilla":
        only_ref_data = Preprocessing(scan_spectra_df, use_case=only_ref_dict)
        only_ref_data.modify()
        X_ref, y_ref = only_ref_data.create_train_test_dataset(validation_split=0)

        # Distribution of model outputs for reference spectra
        out_r = model_trained.model_out(
            mode="ref", x_ref_test=X_ref, y_ref_test=y_ref, device=device
        )
        perc = np.percentile(out_r, CL)

    # create tensor that stores the mean Output for each configuration
    Out_scan = np.zeros((int(N_m_scan), int(N_sin2theta_scan)))
    s2t_scan_matrix = np.zeros_like(Out_scan)
    m_s_scan_matrix = np.zeros_like(Out_scan)

    scan_it_ster = []

    if model_type == "parametrized":
        Out_ref_perc_scan = np.zeros((int(N_m_scan), int(N_sin2theta_scan)))

    # run scan
    for count_i, m_s in enumerate(m_sterile_vals):
        m_s_mask = scan_spectra_df.m_sterile == m_s
        m_s_it_df = scan_spectra_df[m_s_mask]
        for count_j, s2t in enumerate(sin2theta_vals):
            s2t_mask = m_s_it_df.sin2theta == s2t
            s2t_it_df = m_s_it_df[s2t_mask]

            only_ster_dict = {
                "outputs": "xy_no_split",
                "num_ref_spec": 0,
                "spectrum_type": "ster",
                "modifications": mod_dict,
            }

            if model_type == "parametrized":
                # Construct reference output for grid point
                only_ref_dict["outputs"] = "xyms_no_split"
                only_ref_dict["num_ref_spec"] = s2t_it_df.m_sterile.shape[0]
                only_ref_data = Preprocessing(s2t_it_df, use_case=only_ref_dict)
                only_ref_data.modify()
                X_ref, y_ref, m_ref, s_ref = only_ref_data.create_train_test_dataset(
                    validation_split=0
                )

                out_r = model_trained.model_out(
                    mode="ref",
                    x_ref_test=X_ref,
                    y_ref_test=y_ref,
                    m_ref_test=m_ref,
                    s_ref_test=s_ref,
                    device=device,
                )

                perc_r = np.percentile(out_r, CL)
                Out_ref_perc_scan[count_i][count_j] = perc_r

                only_ster_dict["outputs"] = "xyms_no_split"
                only_ster_data = Preprocessing(s2t_it_df, use_case=only_ster_dict)
                only_ster_data.modify()
                X_after_cuts, y_after_cuts, m_after_cuts, s_after_cuts = (
                    only_ster_data.create_train_test_dataset(validation_split=0)
                )

                out_s = model_trained.model_out(
                    x_sterile_test=X_after_cuts,
                    y_sterile_test=y_after_cuts,
                    m_sterile_test=m_after_cuts,
                    s_sterile_test=s_after_cuts,
                    mode="ster",
                    device=device,
                )

            else:
                only_ster_data = Preprocessing(s2t_it_df, use_case=only_ster_dict)
                only_ster_data.modify()
                X_after_cuts, y_after_cuts = only_ster_data.create_train_test_dataset(
                    validation_split=0
                )
                out_s = model_trained.model_out(
                    x_sterile_test=X_after_cuts,
                    y_sterile_test=y_after_cuts,
                    mode="ster",
                    device=device,
                )

            scan_it_ster.append(out_s)
            Out_scan[count_i][count_j] = out_s.mean()
            s2t_scan_matrix[count_i][count_j] = s2t
            m_s_scan_matrix[count_i][count_j] = m_s

    # Creating the contour arrays
    s2t_ct_arr, m_s_ct_arr = ([], [])

    if model_type == "vanilla":
        t = np.where(Out_scan <= perc, s2t_scan_matrix, 0)
        for row in range(t.shape[0]):
            idx = next((i for i, x in enumerate(t[row]) if x), None)
            m_s_ct = m_s_scan_matrix[row][idx]
            s2t_ct = t[row][idx]
            if idx == None:
                idx = t[row].shape[0] - 1
                m_s_ct = m_s_scan_matrix[row][idx]
                s2t_ct = s2t_scan_matrix[row][idx]
            m_s_ct_arr.append(m_s_ct)
            s2t_ct_arr.append(s2t_ct)

    if model_type == "parametrized":
        for r, row in enumerate(s2t_scan_matrix):
            flag = 0
            for c, column in enumerate(row):
                if flag == 0:
                    if Out_scan[r][c] <= Out_ref_perc_scan[r][c]:
                        m_s_ct_arr.append(m_s_scan_matrix[r][c])
                        s2t_ct_arr.append(s2t_scan_matrix[r][c])
                        flag = 1

    if model_type == "parametrized":
        perc = Out_ref_perc_scan

    out_dict = {
        "scan_matrix": Out_scan,
        "model_out_ster_it": scan_it_ster,
        "model_out_ref_all": out_r,
        "contour_ms": np.array(m_s_ct_arr, dtype=np.float64),
        "contour_s2t": np.array(s2t_ct_arr, dtype=np.float64),
        "perc": perc,
    }

    return out_dict


#    AE --------------------------------------------------------------------------------------------------------
# TODO: Implement new way of creating the scans (see MLP)


def AE_scan_many(ae_trained, scan_spectra_df, scan_dict, CL, plot=False, device="cpu"):
    """Performes a scan over a grid (m_sterile, sin2theta), calculating the Reconstruction Loss (RL) at each point.
    Also returnes the percentile value of the Reference Reconstruction Loss given a Confidence Level (CL)

    To calculate the RL, many spectra per grid point can be used and the average RL will be returned
    """

    # get params from scan_dict
    N_m_scan = scan_dict["num_sterile_vals"]
    N_sin2theta_scan = scan_dict["num_sin2theta_scan"]
    num_spec_scan = scan_dict["num_spec_scan"]

    scan_params = (
        np.linspace(scan_dict["m_sterile_min"], scan_dict["m_sterile_max"], N_m_scan),
        np.logspace(
            scan_dict["sin2theta_log_max"],
            scan_dict["sin2theta_log_min"],
            N_sin2theta_scan,
        ),
    )

    m_sterile_vals = scan_params[0]
    sin2theta_vals = scan_params[1]

    X_ref, y_ref = create_train_test_dataset(
        spectra_df=scan_spectra_df,
        num_ref_spec=scan_spectra_df.m_sterile.shape[0],
        no_split_just_scale=True,
        only_ster=False,
        binary_class=False,
        random_state=42,
        shuffle=False,
        only_ref=True,
    )

    reco_l = reco_loss(
        ae_trained, mode="ref", x_ref_test=X_ref, y_ref_test=y_ref, device=device
    )

    perc = np.percentile(reco_l, CL)

    # create tensor that stores the mean Likelihood Ratio for each configuration
    LR_scan = np.zeros((int(N_m_scan), int(N_sin2theta_scan)))

    LR_scan_it = []

    # run scan
    for count_i, m_s in enumerate(m_sterile_vals):
        m_s_mask = scan_spectra_df.m_sterile == m_s
        m_s_it_df = scan_spectra_df[m_s_mask]
        for count_j, s2t in enumerate(sin2theta_vals):
            s2t_mask = m_s_it_df.sin2theta == s2t
            s2t_it_df = m_s_it_df[s2t_mask]

            X_after_cuts, y_after_cuts = create_train_test_dataset(
                s2t_it_df, no_split_just_scale=True, shuffle=False, num_ref_spec=0
            )

            reco_l = reco_loss(
                ae_trained, X_after_cuts, y_after_cuts, mode="ster", device=device
            )

            LR_scan_it.append(reco_l)
            LR_scan[count_i][count_j] = reco_l.mean()

    return LR_scan, LR_scan_it, perc


#   VAE --------------------------------------------------------------------------------------------------------
# TODO: Update this to use Preprocessing class instead of create_train_test_dataset


def VAE_scan_many(
    vae_trained, scan_spectra_df, scan_dict, CL, beta=1, plot=False, device="cpu"
):
    """Performes a scan over a grid (m_sterile, sin2theta), calculating the Reconstruction Loss (RL) at each point.
    Also returnes the percentile value of the Reference Reconstruction Loss given a Confidence Level (CL)

    To calculate the RL, many spectra per grid point can be used and the average RL will be returned
    """

    # get params from scan_dict
    N_m_scan = scan_dict["num_sterile_vals"]
    N_sin2theta_scan = scan_dict["num_sin2theta_scan"]
    num_spec_scan = scan_dict["num_spec_scan"]

    scan_params = (
        np.linspace(scan_dict["m_sterile_min"], scan_dict["m_sterile_max"], N_m_scan),
        np.logspace(
            scan_dict["sin2theta_log_max"],
            scan_dict["sin2theta_log_min"],
            N_sin2theta_scan,
        ),
    )

    m_sterile_vals = scan_params[0]
    sin2theta_vals = scan_params[1]

    X_ref, y_ref = create_train_test_dataset(
        spectra_df=scan_spectra_df,
        num_ref_spec=scan_spectra_df.m_sterile.shape[0],
        no_split_just_scale=True,
        only_ster=False,
        binary_class=False,
        random_state=42,
        shuffle=False,
        only_ref=True,
    )

    reco_l = vae_trained.reco_loss(
        mode="ref", x_ref_test=X_ref, y_ref_test=y_ref, device=device, beta=beta
    )

    perc = np.percentile(reco_l, CL)

    # create tensor that stores the mean Likelihood Ratio for each configuration
    LR_scan = np.zeros((int(N_m_scan), int(N_sin2theta_scan)))

    LR_scan_it = []

    # run scan
    for count_i, m_s in enumerate(m_sterile_vals):
        m_s_mask = scan_spectra_df.m_sterile == m_s
        m_s_it_df = scan_spectra_df[m_s_mask]
        for count_j, s2t in enumerate(sin2theta_vals):
            s2t_mask = m_s_it_df.sin2theta == s2t
            s2t_it_df = m_s_it_df[s2t_mask]

            X_after_cuts, y_after_cuts = create_train_test_dataset(
                s2t_it_df, no_split_just_scale=True, shuffle=False, num_ref_spec=0
            )

            reco_l = vae_trained.reco_loss(
                X_after_cuts, y_after_cuts, mode="ster", beta=beta, device=device
            )

            LR_scan_it.append(reco_l)
            LR_scan[count_i][count_j] = reco_l.mean()

    return LR_scan, LR_scan_it, perc


# ==============================================================================================================================================
# Plotting --------------------------------------------------------------------------------------------------------
# ==============================================================================================================================================


def plot_scan(
    list_of_scans,
    scan_titles_and_clrs,
    plot_range=((1e-9, 1e-1), (0, 18.6)),
    save=False,
    errorbars=False,
    title="Exclusion lines at 95% CL for $\mathbf{2*10^{15}}$ electrons",
):

    # plot
    fig, ax = plt.subplots(figsize=(11, 8))

    for count, scan in enumerate(list_of_scans):
        ax.plot(
            scan["contour_ms"] / 1000,
            scan["contour_s2t"],
            label=scan_titles_and_clrs[count][0],
            color=scan_titles_and_clrs[count][1],
        )
        if errorbars:
            for key in scan.keys():
                if key == "contour_s2t_err":
                    ax.fill_between(
                        scan["contour_ms"] / 1000,
                        scan["contour_s2t_err"][0],
                        scan["contour_s2t_err"][1],
                        color=scan_titles_and_clrs[count][2],
                        alpha=0.2,
                    )

    ax.grid(linestyle="--")

    ax.set_xlabel("m$_{\mathrm{s}}$ (keV)", fontsize=21)
    ax.set_xlim(plot_range[1][0], plot_range[1][1])
    ax.set_ylabel("sin$^{2}$ $\Theta$ ", fontsize=21)
    ax.set_ylim(plot_range[0][0], plot_range[0][1])
    ax.set_yscale("log")
    ax.tick_params(axis="x", labelsize=21)
    ax.tick_params(axis="y", labelsize=21)
    ax.legend()
    ax.set_title(title, weight="bold")


def load_contour(path_to_data, model_name, errors=True, appendix=None):
    """loads contour
    model_name w/ the 'model_weights/' part
    """
    scan_res = {}
    if appendix != None:
        scan_res["contour_ms"] = np.load(
            path_to_data + model_name + "_contour_ms_95CL" + appendix + ".npy",
            allow_pickle=True,
        )
        scan_res["contour_s2t"] = np.load(
            path_to_data + model_name + "_contour_s2t_95CL" + appendix + ".npy",
            allow_pickle=True,
        )
        if errors:
            scan_res["contour_s2t_err"] = np.load(
                path_to_data + model_name + "_contour_s2t_err_95CL" + appendix + ".npy",
                allow_pickle=True,
            )
    else:
        scan_res["contour_ms"] = np.load(
            path_to_data + model_name + "_contour_ms_95CL.npy", allow_pickle=True
        )
        scan_res["contour_s2t"] = np.load(
            path_to_data + model_name + "_contour_s2t_95CL.npy", allow_pickle=True
        )
        if errors:
            scan_res["contour_s2t_err"] = np.load(
                path_to_data + model_name + "_contour_s2t_err_95CL.npy",
                allow_pickle=True,
            )

    return scan_res


def model_name_constructor(
    test_number,
    spectrum_parameters,
    nhidden,
    epochs,
    bs,
    additional_info,
    model_type="MLP",
    parametrized=False,
):
    today = date.today()
    d = today.strftime("%d_%m")
    if parametrized:
        return (
            "model_weights/"
            + model_type
            + "_parametrized_test"
            + str(test_number)
            + d
            + "_b"
            + str(spectrum_parameters["bins"])
            + "_nh"
            + str(nhidden)
            + "_e"
            + str(epochs)
            + "_bs"
            + str(bs)
            + "_"
            + str(additional_info)
        )
    else:
        return (
            "model_weights/"
            + model_type
            + "_test"
            + str(test_number)
            + "_"
            + d
            + "_b"
            + str(spectrum_parameters["bins"])
            + "_nh"
            + str(nhidden)
            + "_e"
            + str(epochs)
            + "_bs"
            + str(bs)
            + "_"
            + str(additional_info)
        )
