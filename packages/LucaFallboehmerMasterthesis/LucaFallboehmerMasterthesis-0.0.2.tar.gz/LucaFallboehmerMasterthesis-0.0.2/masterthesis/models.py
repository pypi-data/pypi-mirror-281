"""This script contains different model architectures

Functions
---------
init_weights
    initializes the weights of the linear layers in a model using the xavier initialization

Classes
---------
class_MLP
    a simple MLP used for binary classification

class_MLP_parametrized
    parametrized version of the classification MLP

Autoencoder_test
    autoencoder used for classification via the reconstruction loss

VAE
    Variational autoencoder
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from dataset import *
import numpy as np
import torch
from tqdm.notebook import trange
from .model_eval import *


def init_weights(m, bias=False):
    """
    Initializes the models weights for all linear layers using the xavier initialization
    """
    if isinstance(m, torch.nn.Linear):
        torch.nn.init.xavier_uniform(m.weight)
        if bias:
            torch.nn.init.zeros_(m.bias)


class class_MLP(torch.nn.Module):
    """
    Simple binary classification multilayer perceptron (MLP).

    Args:
        bins (int): Dimensionality of input features.
        hidden_dim (int): Number of dimensions used in the hidden layers.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for the adam optimizer.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.

    Attributes:
        bins (int): Dimensionality of input features.
        lin1 (torch.nn.Linear): First linear transformation layer.
        lin2 (torch.nn.Linear): Second linear transformation layer.
        out (torch.nn.Linear): Output layer.
        ReLU (torch.nn.ReLU): Rectified Linear Unit activation function.
        sigmoid (torch.nn.Sigmoid): Sigmoid activation function.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for optimization.
        random_state (int): Random seed for reproducibility.

    Methods:
        forward(x): Forward pass through the MLP.
        train_simple(epochs, X_train, y_train, X_validation, y_validation, gradient_flow=False, lr=1e-3, batch_size=32, device="cpu"): Trains the MLP model.
        eval_simple(losses_training, losses_validation, X_validation, y_validation, Nsamples=1000, threshold_pred=0.5, plot=True, device="cpu"): Evaluates the performance of the trained model.
        model_out(x_sterile_test=None, y_sterile_test=None, x_ref_test=None, y_ref_test=None, mode="Both", device="cpu", random_state=42): Computes the model output for given test data.
    """

    def __init__(self, bins, hidden_dim, batch_size, learning_rate, random_state=42):
        super(class_MLP, self).__init__()
        self.bins = bins
        self.lin1 = torch.nn.Linear(self.bins, hidden_dim)
        self.lin2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.out = torch.nn.Linear(hidden_dim, 1)
        self.ReLU = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()

        self.batch_size = batch_size
        self.learning_rate = learning_rate

        self.random_state = random_state

    def forward(self, x):
        h1 = self.ReLU(self.lin1(x))
        h2 = self.ReLU(self.lin2(h1))
        out = self.sigmoid(self.out(h2))
        return out

    def train_simple(
        self,
        X_train,
        y_train,
        X_validation,
        y_validation,
        epochs,
        gradient_flow=False,
        lr=1e-3,
        batch_size=32,
        device="cpu",
        verbose=1,
    ):
        """
        Trains the MLP model.

        Args:
            epochs (int): Number of training epochs.
            X_train (torch.Tensor): Training input data.
            y_train (torch.Tensor): Training target labels.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            gradient_flow (bool, optional): Whether to compute and return gradients. Defaults to False.
            lr (float, optional): Learning rate for optimization. Defaults to 1e-3.
            batch_size (int, optional): Size of batches for training. Defaults to 32.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            tuple: Tuple containing training losses, validation losses, and gradients if gradient_flow=True.
        """

        assert (
            self.bins == X_train[0].shape[0]
        ), f"Model input dimension ({self.bins}) doesnt match data ({X_train[0].shape[0]})!"

        optim = torch.optim.Adam(self.parameters(), lr)
        train_data = Dataset(X_train, y_train, seed=self.random_state)
        train_dl = DataLoader(train_data, batch_size=batch_size, device=device)
        val_data = Dataset(X_validation, y_validation, seed=self.random_state)
        val_dl = DataLoader(val_data, batch_size=batch_size, device=device)
        losses = []
        validation_losses = []
        gradients = {"lin1.weight": [], "lin2.weight": [], "out.weight": []}
        with trange(epochs, unit="epochs") as iterable:
            for count in iterable:
                if count > 0:
                    train_data.shuffle()
                    train_dl = DataLoader(
                        train_data, batch_size=batch_size, device=device
                    )
                for count_batch, (x_b, y_b) in enumerate(train_dl):
                    optim.zero_grad()
                    p = self(x_b)
                    loss = torch.nn.functional.binary_cross_entropy(p, y_b)
                    losses.append(loss.cpu().detach().numpy())
                    loss.backward()
                    if gradient_flow:
                        for n, p in self.named_parameters():
                            if (p.requires_grad) and ("bias" not in n):
                                avg_grad = p.grad.abs().mean()
                                gradients[n].append(avg_grad.cpu().detach().numpy())
                    optim.step()
                    if count_batch % 100 == 0:
                        x_b_val, y_b_val = iter(val_dl).__next__()
                        x_b_val = x_b_val.to(device)
                        y_b_val = y_b_val.to(device)
                        with torch.no_grad():
                            pred = self(x_b_val)  # reshape not really necessary anymore
                        loss_val = torch.nn.functional.binary_cross_entropy(
                            pred, y_b_val
                        )
                        validation_losses.append(loss_val.cpu().detach().numpy())
                        if verbose == 1:
                            iterable.set_description("Training")
                            iterable.set_postfix(
                                tr_loss=f"{float(losses[-1]):.4f}",
                                val_loss=f"{float(validation_losses[-1]):.4f}",
                            )

        if gradient_flow:
            return losses, validation_losses, pd.DataFrame(gradients)

        return losses, validation_losses

    def eval_simple(
        self,
        losses_training,
        losses_validation,
        X_validation,
        y_validation,
        threshold_pred=0.5,
        plot=("epochs", 100),
        device="cpu",
    ):
        self.eval()
        """
        Evaluates the performance of the trained model.

        Args:
            losses_training (list): Training losses.
            losses_validation (list): Validation losses.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            Nsamples (int, optional): Number of samples. Defaults to 1000.
            threshold_pred (float, optional): Prediction threshold. Defaults to 0.5.
            plot (tuple, optional): In which mode to plot the loss curve. Defaults to True.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            dict: Dictionary containing evaluation metrics.
        """

        val_data = Dataset(X_validation, y_validation, seed=self.random_state)
        val_dl = DataLoader(val_data, batch_size=len(val_data), device=device)
        x_val, y_val = iter(val_dl).__next__()
        y_val = y_val.cpu()
        with torch.no_grad():
            pred = self(x_val)
            pred = pred.cpu()
        sterile_pred = np.where(pred > threshold_pred, 1, 0)
        gt = y_val.detach().numpy()

        if plot is not False:
            if plot[0] == "epochs":
                r = int(len(losses_training) / len(losses_validation))
                e = int(len(losses_training) / plot[1])
                x_ax_val = []
                x_ax_epochs = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                    if i % e == 0:
                        x_ax_epochs.append(i)

                fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                if len(x_ax_val) == len(losses_validation):
                    ax.plot(
                        x_ax_val,
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                else:
                    ax.plot(
                        x_ax_val[:-1],
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                for c, epoch in enumerate(x_ax_epochs):
                    if c % 5 == 0:
                        ax.axvline(
                            epoch,
                            ymin=0,
                            ymax=1,
                            color="grey",
                            linestyle="--",
                            linewidth=0.5,
                        )

                ax.axvline(
                    x_ax_epochs[-1],
                    ymin=0,
                    ymax=1,
                    color="grey",
                    linestyle="--",
                    linewidth=0.5,
                    label="every fifth training epoch",
                )

                # ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

            if plot[0] == "grid":
                r = int(len(losses_training) / len(losses_validation))
                x_ax_val = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

        score_dict = {
            "accuracy": accuracy(gt, sterile_pred),
            "precision": precision(gt, sterile_pred),
            "recall": recall(gt, sterile_pred),
            "fall-out": fallout(gt, sterile_pred),
            "f1": f1(gt, sterile_pred),
            "threshold_roc": threshold_pred,
        }
        # accuracy(gt, sterile_pred), recall(gt, sterile_pred), precision(gt, sterile_pred), f1(gt, sterile_pred)
        return score_dict

    def model_out(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        mode="Both",
        device="cpu",
        random_state=42,
    ):
        self.eval()
        """
        Computes the model output for given test data.

        Args:
            x_sterile_test (numpy.ndarray, optional): Test input data for sterile class. Defaults to None.
            y_sterile_test (numpy.ndarray, optional): Test target labels for sterile class. Defaults to None.
            x_ref_test (numpy.ndarray, optional): Test input data for reference class. Defaults to None.
            y_ref_test (numpy.ndarray, optional): Test target labels for reference class. Defaults to None.
            mode (str, optional): Kind of spectra for which the output is calculated, possible modes: ("Both", "ref", or "ster"). Defaults to "Both".
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".
            random_state (int, optional): Random seed for reproducibility. Defaults to 42.

        Returns:
            numpy.ndarray: Model outputs for the specified mode.
        """

        if mode == "Both":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_s = self(x_s)
                out_r = self(x_r)

            return out_s.cpu().detach().numpy(), out_r.cpu().detach().numpy()

        if mode == "ref":
            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_r = self(x_r)

            return out_r.cpu().detach().numpy()

        if mode == "ster":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            with torch.no_grad():
                out_s = self(x_s)

            return out_s.cpu().detach().numpy()

    def integrated_gradients(
        self, x_data, y_data, baseline=None, steps=50, device="cpu"
    ):
        self.eval()
        if baseline is None:
            baseline = np.zeros_like(x_data)

        gradients = []

        y_arr = np.zeros(steps + 1) + y_data
        scaled_inputs = np.array(
            [
                baseline + (float(i) / steps) * (x_data - baseline)
                for i in range(steps + 1)
            ]
        )
        ds = Dataset(scaled_inputs, y_arr, 42)
        dl = DataLoader(ds, batch_size=1, device=device)

        for c, (scaled_input, y) in enumerate(dl):
            scaled_input.requires_grad_(True)
            output = self(scaled_input)
            loss = output
            loss.backward(retain_graph=True)
            gradients.append(scaled_input.grad.cpu().detach().clone())

        avg_gradients = torch.mean(torch.stack(gradients), dim=0)
        approx_int_grad = (
            torch.Tensor(x_data) - torch.Tensor(baseline)
        ) * avg_gradients

        return approx_int_grad.detach().numpy()

    def eval_full(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        losses_training=None,
        losses_validation=None,
        X_validation=None,
        y_validation=None,
        grads=None,
        threshold_pred=0.5,
        device="cpu",
        plot=("all", {"epochs": 100, "int_grad_spec": 100}),
    ):
        self.eval()
        score = self.eval_simple(
            losses_training,
            losses_validation,
            X_validation,
            y_validation,
            threshold_pred,
            plot=False,
            device=device,
        )
        out_s, out_r = self.model_out(
            x_sterile_test, y_sterile_test, x_ref_test, y_ref_test, device=device
        )
        int_grad_ster = self.integrated_gradients(
            x_sterile_test[plot[1]["int_grad_spec"]],
            y_sterile_test[plot[1]["int_grad_spec"]],
            device=device,
        )[0]
        int_grad_ref = self.integrated_gradients(
            x_ref_test[0], y_ref_test[0], device=device
        )[0]

        if plot[0] == "all":
            fig, (l_ax, g_ax, o_ax, i_g_ax) = plt.subplots(4, 1, figsize=(15, 30))

            # l_ax

            r = int(len(losses_training) / len(losses_validation))
            e = int(len(losses_training) / plot[1]["epochs"])
            x_ax_val = []
            x_ax_epochs = []
            for i in np.arange(len(losses_training)):
                if i % r == 0:
                    x_ax_val.append(i)
                if i % e == 0:
                    x_ax_epochs.append(i)

            l_ax.plot(
                np.arange(len(losses_training)),
                losses_training,
                label="training loss",
            )
            l_ax.set_yscale("log")
            l_ax.set_xlabel("training iterations")
            l_ax.set_ylabel("Loss value")
            l_ax.set_title("BCE Loss", weight="bold")
            l_ax.plot(x_ax_val, losses_validation, linewidth=3, label="validation loss")
            for c, epoch in enumerate(x_ax_epochs):
                if c % 5 == 0:
                    l_ax.axvline(
                        epoch,
                        ymin=0,
                        ymax=1,
                        color="grey",
                        linestyle="--",
                        linewidth=0.5,
                    )

            l_ax.axvline(
                x_ax_epochs[-1],
                ymin=0,
                ymax=1,
                color="grey",
                linestyle="--",
                linewidth=0.5,
                label="every fifth training epoch",
            )

            l_ax.legend()

            l_ax.table(
                cellText=[[k, v] for k, v in zip(score.keys(), score.values())],
                cellLoc="left",
                edges="open",
                bbox=[0.05, 0.05, 0.3, 0.3],
            )

            # g_ax
            g_ax.plot(list(grads.index.values), grads["lin1.weight"], label="lin1")
            g_ax.plot(list(grads.index.values), grads["lin2.weight"], label="lin2")
            g_ax.plot(list(grads.index.values), grads["out.weight"], label="out")
            g_ax.legend()
            g_ax.set_xlabel("training iterations")
            g_ax.set_ylabel("avg gradient")

            # o_ax
            ul = 1
            o_ax.hist(
                out_s,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="r",
                alpha=0.3,
                label="Model Output w/ sterile",
            )
            o_ax.hist(
                out_r,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="g",
                alpha=0.3,
                label="Reference",
            )
            o_ax.set_yscale("log")
            o_ax.set_xlabel("Model Output")
            o_ax.set_ylabel("Counts")
            o_ax.set_title("Histogram of Model Outputs", weight="bold")
            o_ax.legend()

            # i_g_ax
            i_g_ax.plot(
                int_grad_ster,
                marker="o",
                linestyle="-",
                color="b",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Sterile Spectrum",
            )
            i_g_ax.plot(
                int_grad_ref,
                marker="o",
                linestyle="-",
                color="g",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Reference Spectrum",
            )

            i_g_ax.set_title("Integrated Gradients Attributions", weight="bold")
            i_g_ax.set_xlabel("Energy Bin")
            i_g_ax.set_ylabel("Attribution Value")
            i_g_ax.grid(True, which="both", linestyle="--", linewidth=0.5)
            i_g_ax.axhline(0, color="grey", linewidth=0.8)

            i_g_ax.legend()

            fig.tight_layout()
            fig.show()


class class_MLP_parametrized(torch.nn.Module):
    """
    Parametrized multilayer perceptron (MLP) for binary classification.

    Args:
        bins (int): Dimensionality of input features.
        params (int): Number of additional parameters.
        hidden_dim (int): Number of units in the hidden layer.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for optimization.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.

    Attributes:
        bins (int): Dimensionality of input features.
        lin1 (torch.nn.Linear): First linear transformation layer.
        lin2 (torch.nn.Linear): Second linear transformation layer.
        out (torch.nn.Linear): Output layer.
        ReLU (torch.nn.ReLU): Rectified Linear Unit activation function.
        sigmoid (torch.nn.Sigmoid): Sigmoid activation function.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for optimization.
        random_state (int): Random seed for reproducibility.

    Methods:
        forward(x, m_s, sin2theta): Forward pass through the MLP.
        train_simple(epochs, X_train, y_train, m_train, s_train, X_validation, y_validation, m_validation, s_validation, lr=1e-3, batch_size=32, gradient_flow=False, device="cpu"): Trains the parametrized MLP model.
        eval_simple(losses_training, losses_validation, X_validation, y_validation, m_validation, s_validation, Nsamples=1000, threshold_pred=0.5, plot=True, device="cpu"): Evaluates the performance of the trained model.
        model_out(x_sterile_test=None, y_sterile_test=None, m_sterile_test=None, s_sterile_test=None, x_ref_test=None, y_ref_test=None, m_ref_test=None, s_ref_test=None, mode="Both", device="cpu"): Computes the model output for given test data.
    """

    def __init__(
        self, bins, params, hidden_dim, batch_size, learning_rate, random_state=42
    ):

        super(class_MLP_parametrized, self).__init__()
        self.bins = bins
        self.lin1 = torch.nn.Linear(bins + params, hidden_dim)
        self.lin2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.out = torch.nn.Linear(hidden_dim, 1)
        self.ReLU = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()

        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.random_state = random_state

    def forward(self, x, m_s, sin2theta):
        """
        Forward pass through the parametrized MLP.

        Args:
            x (torch.Tensor): Input data.
            m_s (torch.Tensor): Additional parameter.
            sin2theta (torch.Tensor): Additional parameter.

        Returns:
            torch.Tensor: Output predictions.
        """
        i = torch.cat((x, m_s, sin2theta), 1)
        h1 = self.ReLU(self.lin1(i))
        h2 = self.ReLU(self.lin2(h1))
        out = self.sigmoid(self.out(h2))
        return out

    def train_simple(
        self,
        X_train,
        y_train,
        m_train,
        s_train,
        X_validation,
        y_validation,
        m_validation,
        s_validation,
        epochs,
        lr=1e-3,
        batch_size=32,
        gradient_flow=False,
        device="cpu",
        verbose=1,
    ):
        """
        Trains the parametrized MLP model.

        Args:
            epochs (int): Number of training epochs.
            X_train (torch.Tensor): Training input data.
            y_train (torch.Tensor): Training target labels.
            m_train (torch.Tensor): Additional parameters for training data (sterile mass).
            s_train (torch.Tensor): Additional parameters for training data (mixing angle).
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            m_validation (torch.Tensor): Additional parameters for validation data (sterile mass).
            s_validation (torch.Tensor): Additional parameters for validation data (mixing angle).
            lr (float, optional): Learning rate for optimization. Defaults to 1e-3.
            batch_size (int, optional): Size of batches for training. Defaults to 32.
            gradient_flow (bool, optional): Whether to compute and return gradients. Defaults to False.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            tuple: Tuple containing training losses, validation losses, and gradients if gradient_flow=True.
        """

        optim = torch.optim.Adam(self.parameters(), lr)
        train_data = Dataset_Parametrized(
            X_train, y_train, m_train, s_train, seed=self.random_state
        )
        train_dl = DataLoader_Parametrized(
            train_data, batch_size=batch_size, device=device
        )
        val_data = Dataset_Parametrized(
            X_validation,
            y_validation,
            m_validation,
            s_validation,
            seed=self.random_state,
        )
        val_dl = DataLoader_Parametrized(val_data, batch_size=batch_size, device=device)
        losses = []
        validation_losses = []
        gradients = {"lin1.weight": [], "lin2.weight": [], "out.weight": []}
        with trange(epochs, unit="epochs") as iterable:
            for count in iterable:
                if count > 0:
                    train_data.shuffle()
                    train_dl = DataLoader_Parametrized(
                        train_data, batch_size=batch_size, device=device
                    )
                for count_batch, (x_b, y_b, m_b, s_b) in enumerate(train_dl):
                    optim.zero_grad()
                    p = self(x_b, m_b, s_b)
                    loss = torch.nn.functional.binary_cross_entropy(p, y_b)
                    losses.append(loss.cpu().detach().numpy())
                    loss.backward()
                    if gradient_flow:
                        for n, p in self.named_parameters():
                            if (p.requires_grad) and ("bias" not in n):
                                avg_grad = p.grad.abs().mean()
                                gradients[n].append(avg_grad.cpu().detach().numpy())
                    optim.step()
                    if count_batch % 100 == 0:
                        x_b_val, y_b_val, m_b_val, s_b_val = iter(val_dl).__next__()
                        x_b_val = x_b_val.to(device)
                        y_b_val = y_b_val.to(device)
                        m_b_val = m_b_val.to(device)
                        s_b_val = s_b_val.to(device)
                        with torch.no_grad():
                            pred = self(
                                x_b_val, m_b_val, s_b_val
                            )  # reshape not really necessary anymore
                        loss_val = torch.nn.functional.binary_cross_entropy(
                            pred, y_b_val
                        )
                        validation_losses.append(loss_val.cpu().detach().numpy())
                        if verbose == 1:
                            iterable.set_description("Training")
                            iterable.set_postfix(
                                tr_loss=f"{float(losses[-1]):.4f}",
                                val_loss=f"{float(validation_losses[-1]):.4f}",
                            )

        if gradient_flow:
            return losses, validation_losses, pd.DataFrame(gradients)

        return losses, validation_losses

    def eval_simple(
        self,
        losses_training,
        losses_validation,
        X_validation,
        y_validation,
        m_validation,
        s_validation,
        Nsamples=1000,
        threshold_pred=0.5,
        plot=True,
        device="cpu",
    ):
        """
        Evaluates the performance of the trained model.

        Args:
            losses_training (list): Training losses.
            losses_validation (list): Validation losses.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            m_validation (torch.Tensor): Additional parameters for validation data (sterile mass).
            s_validation (torch.Tensor): Additional parameters for validation data (mixing angle).
            Nsamples (int, optional): Number of samples. Defaults to 1000.
            threshold_pred (float, optional): Prediction threshold. Defaults to 0.5.
            plot (bool, optional): Whether to plot the loss curves. Defaults to True.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            dict: Dictionary containing evaluation metrics.
        """

        val_data = Dataset_Parametrized(
            X_validation,
            y_validation,
            m_validation,
            s_validation,
            seed=self.random_state,
        )
        val_dl = DataLoader_Parametrized(
            val_data, batch_size=len(val_data), device=device
        )
        x_val, y_val, m_val, s_val = iter(val_dl).__next__()
        y_val = y_val.cpu()
        with torch.no_grad():
            pred = self(x_val, m_val, s_val)
            pred = pred.cpu()
        sterile_pred = np.where(pred > threshold_pred, 1, 0)
        gt = y_val.detach().numpy()

        if plot is not False:
            if plot[0] == "epochs":
                r = int(len(losses_training) / len(losses_validation))
                e = int(len(losses_training) / plot[1])
                x_ax_val = []
                x_ax_epochs = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                    if i % e == 0:
                        x_ax_epochs.append(i)

                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                for c, epoch in enumerate(x_ax_epochs):
                    if c % 5 == 0:
                        ax.axvline(
                            epoch,
                            ymin=0,
                            ymax=1,
                            color="grey",
                            linestyle="--",
                            linewidth=0.5,
                        )

                ax.axvline(
                    x_ax_epochs[-1],
                    ymin=0,
                    ymax=1,
                    color="grey",
                    linestyle="--",
                    linewidth=0.5,
                    label="every fifth training epoch",
                )

                # ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

            if plot[0] == "grid":
                r = int(len(losses_training) / len(losses_validation))
                x_ax_val = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

        score_dict = {
            "accuracy": accuracy(gt, sterile_pred),
            "precision": precision(gt, sterile_pred),
            "recall": recall(gt, sterile_pred),
            "fall-out": fallout(gt, sterile_pred),
            "f1": f1(gt, sterile_pred),
            "threshold_roc": threshold_pred,
        }
        # accuracy(gt, sterile_pred), recall(gt, sterile_pred), precision(gt, sterile_pred), f1(gt, sterile_pred)
        return score_dict

    def model_out(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        m_sterile_test=None,
        s_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        m_ref_test=None,
        s_ref_test=None,
        mode="Both",
        device="cpu",
    ):
        """
        Computes the model output for given test data.

        Args:
            x_sterile_test (numpy.ndarray, optional): Test input data for sterile class. Defaults to None.
            y_sterile_test (numpy.ndarray, optional): Test target labels for sterile class. Defaults to None.
            m_sterile_test (numpy.ndarray, optional): Additional parameters for sterile test data (sterile mass). Defaults to None.
            s_sterile_test (numpy.ndarray, optional): Additional parameters for sterile test data (mixing angle). Defaults to None.
            x_ref_test (numpy.ndarray, optional): Test input data for reference class. Defaults to None.
            y_ref_test (numpy.ndarray, optional): Test target labels for reference class. Defaults to None.
            m_ref_test (numpy.ndarray, optional): Additional parameters for reference test data (sterile mass). Defaults to None.
            s_ref_test (numpy.ndarray, optional): Additional parameters for reference test data (mixing angle). Defaults to None.
            mode (str, optional): Kind of spectra for which the output is calculated, possible modes: ("Both", "ref", or "ster"). Defaults to "Both".
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            numpy.ndarray: Model outputs for the specified mode.
        """
        if mode == "Both":
            data_s = Dataset_Parametrized(
                x_sterile_test, y_sterile_test, m_sterile_test, s_sterile_test
            )
            x_s, y_s, m_s, s_s = data_s[:]
            x_s, y_s, m_s, s_s = (
                torch.FloatTensor(x_s.astype(np.float64)),
                torch.FloatTensor(y_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_s.astype(np.float64)).unsqueeze(-1),
            )
            x_s, y_s, m_s, s_s = (
                x_s.to(device),
                y_s.to(device),
                m_s.to(device),
                s_s.to(device),
            )

            data_r = Dataset_Parametrized(
                x_ref_test, y_ref_test, m_ref_test, s_ref_test
            )
            x_r, y_r, m_r, s_r = data_r[:]
            x_r, y_r, m_r, s_r = (
                torch.FloatTensor(x_r.astype(np.float64)),
                torch.FloatTensor(y_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_r.astype(np.float64)).unsqueeze(-1),
            )
            x_r, y_r, m_r, s_r = (
                x_r.to(device),
                y_r.to(device),
                m_r.to(device),
                s_r.to(device),
            )

            with torch.no_grad():
                out_s = self(x_s, m_s, s_s)
                out_r = self(x_r, m_r, s_r)

            return out_s.cpu().detach().numpy(), out_r.cpu().detach().numpy()

        if mode == "ref":
            data_r = Dataset_Parametrized(
                x_ref_test, y_ref_test, m_ref_test, s_ref_test
            )
            x_r, y_r, m_r, s_r = data_r[:]
            x_r, y_r, m_r, s_r = (
                torch.FloatTensor(x_r.astype(np.float64)),
                torch.FloatTensor(y_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_r.astype(np.float64)).unsqueeze(-1),
            )
            x_r, y_r, m_r, s_r = (
                x_r.to(device),
                y_r.to(device),
                m_r.to(device),
                s_r.to(device),
            )

            with torch.no_grad():
                out_r = self(x_r, m_r, s_r)

            return out_r.cpu().detach().numpy()

        if mode == "ster":
            data_s = Dataset_Parametrized(
                x_sterile_test, y_sterile_test, m_sterile_test, s_sterile_test
            )
            x_s, y_s, m_s, s_s = data_s[:]
            x_s, y_s, m_s, s_s = (
                torch.FloatTensor(x_s.astype(np.float64)),
                torch.FloatTensor(y_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_s.astype(np.float64)).unsqueeze(-1),
            )
            x_s, y_s, m_s, s_s = (
                x_s.to(device),
                y_s.to(device),
                m_s.to(device),
                s_s.to(device),
            )

            with torch.no_grad():
                out_s = self(x_s, m_s, s_s)

            return out_s.cpu().detach().numpy()

    def integrated_gradients(
        self, x_data, y_data, m_data, s_data, baseline=None, steps=50, device="cpu"
    ):
        self.eval()
        if baseline is None:
            baseline = np.zeros_like(x_data)

        gradients = []

        y_arr = np.zeros(steps + 1) + y_data
        scaled_inputs = np.array(
            [
                baseline + (float(i) / steps) * (x_data - baseline)
                for i in range(steps + 1)
            ]
        )
        ds = Dataset_Parametrized(scaled_inputs, y_arr, m_data, s_data, 42)
        dl = DataLoader_Parametrized(ds, batch_size=1, device=device)

        for c, (scaled_input, y, m, s) in enumerate(dl):
            scaled_input.requires_grad_(True)
            output = self(scaled_input, m, s)
            loss = output
            loss.backward(retain_graph=True)
            gradients.append(scaled_input.grad.cpu().detach().clone())

        avg_gradients = torch.mean(torch.stack(gradients), dim=0)
        approx_int_grad = (
            torch.Tensor(x_data) - torch.Tensor(baseline)
        ) * avg_gradients

        return approx_int_grad.detach().numpy()

    def eval_full(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        m_sterile_test=None,
        s_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        m_ref_test=None,
        s_ref_test=None,
        losses_training=None,
        losses_validation=None,
        X_validation=None,
        y_validation=None,
        m_validation=None,
        s_validation=None,
        grads=None,
        threshold_pred=0.5,
        device="cpu",
        plot=("all", {"epochs": 100, "int_grad_spec": 100}),
    ):
        self.eval()
        score = self.eval_simple(
            losses_training,
            losses_validation,
            X_validation,
            y_validation,
            m_validation,
            s_validation,
            threshold_pred,
            plot=False,
            device=device,
        )
        out_s, out_r = self.model_out(
            x_sterile_test,
            y_sterile_test,
            m_sterile_test,
            s_sterile_test,
            x_ref_test,
            y_ref_test,
            m_ref_test,
            s_ref_test,
            device=device,
        )
        int_grad_ster = self.integrated_gradients(
            x_sterile_test[plot[1]["int_grad_spec"]],
            y_sterile_test[plot[1]["int_grad_spec"]],
            m_sterile_test[plot[1]["int_grad_spec"]],
            s_sterile_test[plot[1]["int_grad_spec"]],
            device=device,
        )[0]
        int_grad_ref = self.integrated_gradients(
            x_ref_test[0], y_ref_test[0], m_ref_test[0], s_ref_test[0], device=device
        )[0]

        if plot[0] == "all":
            fig, (l_ax, g_ax, o_ax, i_g_ax) = plt.subplots(4, 1, figsize=(15, 30))

            # l_ax

            r = int(len(losses_training) / len(losses_validation))
            e = int(len(losses_training) / plot[1]["epochs"])
            x_ax_val = []
            x_ax_epochs = []
            for i in np.arange(len(losses_training)):
                if i % r == 0:
                    x_ax_val.append(i)
                if i % e == 0:
                    x_ax_epochs.append(i)

            l_ax.plot(
                np.arange(len(losses_training)),
                losses_training,
                label="training loss",
            )
            l_ax.set_yscale("log")
            l_ax.set_xlabel("training iterations")
            l_ax.set_ylabel("Loss value")
            l_ax.set_title("BCE Loss", weight="bold")
            l_ax.plot(x_ax_val, losses_validation, linewidth=3, label="validation loss")
            for c, epoch in enumerate(x_ax_epochs):
                if c % 5 == 0:
                    l_ax.axvline(
                        epoch,
                        ymin=0,
                        ymax=1,
                        color="grey",
                        linestyle="--",
                        linewidth=0.5,
                    )

            l_ax.axvline(
                x_ax_epochs[-1],
                ymin=0,
                ymax=1,
                color="grey",
                linestyle="--",
                linewidth=0.5,
                label="every fifth training epoch",
            )

            l_ax.legend()

            l_ax.table(
                cellText=[[k, v] for k, v in zip(score.keys(), score.values())],
                cellLoc="left",
                edges="open",
                bbox=[0.05, 0.05, 0.3, 0.3],
            )

            # g_ax
            g_ax.plot(list(grads.index.values), grads["lin1.weight"], label="lin1")
            g_ax.plot(list(grads.index.values), grads["lin2.weight"], label="lin2")
            g_ax.plot(list(grads.index.values), grads["out.weight"], label="out")
            g_ax.legend()
            g_ax.set_xlabel("training iterations")
            g_ax.set_ylabel("avg gradient")

            # o_ax
            ul = 1
            o_ax.hist(
                out_s,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="r",
                alpha=0.3,
                label="Model Output w/ sterile",
            )
            o_ax.hist(
                out_r,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="g",
                alpha=0.3,
                label="Reference",
            )
            o_ax.set_yscale("log")
            o_ax.set_xlabel("Model Output")
            o_ax.set_ylabel("Counts")
            o_ax.set_title("Histogram of Model Outputs", weight="bold")
            o_ax.legend()

            # i_g_ax
            i_g_ax.plot(
                int_grad_ster,
                marker="o",
                linestyle="-",
                color="b",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Sterile Spectrum",
            )
            i_g_ax.plot(
                int_grad_ref,
                marker="o",
                linestyle="-",
                color="g",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Reference Spectrum",
            )

            i_g_ax.set_title("Integrated Gradients Attributions", weight="bold")
            i_g_ax.set_xlabel("Energy Bin")
            i_g_ax.set_ylabel("Attribution Value")
            i_g_ax.grid(True, which="both", linestyle="--", linewidth=0.5)
            i_g_ax.axhline(0, color="grey", linewidth=0.8)

            i_g_ax.legend()

            fig.tight_layout()
            fig.show()


#
# Autoencoders (TODO need update)
#


class Autoencoder_test(torch.nn.Module):
    def __init__(self, bins, hidden_dim, latent_dim):
        super().__init__()
        self.bins = bins
        self.encoder = torch.nn.Sequential(
            # torch.nn.Flatten(),
            torch.nn.Linear(bins, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, latent_dim),
        )

        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(latent_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, bins),
        )

    def forward(self, x):
        code = self.encoder(x)
        reco = self.decoder(code)
        return code, reco

    def train(
        self,
        epochs,
        X_train,
        y_train,
        X_validation,
        y_validation,
        lr=1e-3,
        batch_size=32,
        device="cpu",
        random_state=1,
        plot_model=True,
    ):
        ekin = np.linspace(0, 18600, X_train[0].shape[0])
        train_data = Dataset(X_train, y_train)
        train_dl = DataLoader(train_data, batch_size=batch_size, device=device)
        val_data = Dataset(X_validation, y_validation)
        val_dl = DataLoader(val_data, batch_size=batch_size, device=device)
        optim = torch.optim.Adam(self.parameters(), lr)
        losses = []
        val_losses = []
        for count in range(epochs):
            if count > 0:
                X_train_shuffled, y_train_shuffled = shuffle(
                    X_train, y_train, random_state=random_state
                )
                train_data_shuffled = Dataset(X_train_shuffled, y_train_shuffled)
                train_dl = DataLoader(
                    train_data_shuffled, batch_size=batch_size, device=device
                )
                random_state += 1
            for count_batch, (x_b, y_b) in enumerate(train_dl):
                optim.zero_grad()
                code, reco = self(x_b)
                loss = torch.nn.functional.mse_loss(
                    x_b.squeeze(), reco
                )  # need squeeze?
                losses.append(loss.cpu().detach().numpy())
                loss.backward()
                optim.step()
                if count_batch % 100 == 0:
                    x_b_val, y_b_val = iter(val_dl).__next__()
                    x_b_val = x_b_val.to(device)
                    y_b_val = y_b_val.to(device)
                    with torch.no_grad():
                        code, reco = self(x_b_val)  # reshape ?
                    loss_val = torch.nn.functional.mse_loss(reco, x_b_val)
                    val_losses.append(loss_val.cpu().detach().numpy())
                    print(
                        f"Epoch: {count} | Batch: [{count_batch}/{len(train_data) / batch_size}] training loss: {float(loss):.10f}  validation loss: {float(loss_val):.10f}",
                    )
                    if plot_model:
                        f, axarr = plt.subplots(1, 3, figsize=(10, 10))
                        axarr[0].plot(ekin, x_b_val[0].cpu().detach().numpy())
                        axarr[1].plot(ekin, reco[0].cpu().detach().numpy())  # m[-1][0]
                        axarr[2].scatter(
                            code[:, 0].cpu().detach().numpy(),
                            code[:, 1].cpu().detach().numpy(),
                        )
                        f.set_tight_layout(True)

        return losses, val_losses

    def reco_loss(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        mode="Both",
        device="cpu",
    ):
        if mode == "Both":
            data_s = Dataset(x_sterile_test, y_sterile_test)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            data_r = Dataset(x_ref_test, y_ref_test)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                c_s, r_s = self(x_s)
                c_r, r_r = self(x_r)

            # r_s = r_s.cpu().detach().numpy()
            # r_r = r_r.cpu().detach().numpy()

            reco_losses = []
            ref_losses = []
            for count, reco_spec in enumerate(r_s):
                reco_loss = torch.nn.functional.mse_loss(
                    reco_spec, x_s.squeeze()[count]
                )
                reco_losses.append(reco_loss.cpu().detach().numpy())
            for count, value in enumerate(r_r):
                reco_ref_loss = torch.nn.functional.mse_loss(
                    value, x_r.squeeze()[count]
                )
                ref_losses.append(reco_ref_loss.cpu().detach().numpy())
            return np.array(reco_losses, dtype=np.float64), np.array(
                ref_losses, dtype=np.float64
            )

        if mode == "ref":
            data_r = Dataset(x_ref_test, y_ref_test)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                c_r, r_r = self(x_r)

            ref_losses = []
            for count, value in enumerate(r_r):
                reco_ref_loss = torch.nn.functional.mse_loss(
                    value, x_r.squeeze()[count]
                )
                ref_losses.append(reco_ref_loss.cpu().detach().numpy())

            return np.array(ref_losses, dtype=np.float64)

        if mode == "ster":
            data_s = Dataset(x_sterile_test, y_sterile_test)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            with torch.no_grad():
                c_s, r_s = self(x_s)

            reco_losses = []
            for count, reco_spec in enumerate(r_s):
                reco_loss = torch.nn.functional.mse_loss(
                    reco_spec, x_s.squeeze()[count]
                )
                reco_losses.append(reco_loss.cpu().detach().numpy())

            return np.array(reco_losses, dtype=np.float64)


# VAE


class VAE_Encoder(torch.nn.Module):
    def __init__(self, bins, hidden_dim, latent_dim, slope):
        super(VAE_Encoder, self).__init__()
        self.bins = bins
        self.slope = slope
        self.flatten_layer = torch.nn.Sequential(torch.nn.Flatten())
        self.lin1 = torch.nn.Linear(bins, hidden_dim)
        self.lin2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.lin_mean = torch.nn.Linear(hidden_dim, latent_dim)
        self.lin_var = torch.nn.Linear(hidden_dim, latent_dim)

        self.LeakyReLU = torch.nn.LeakyReLU(slope)

        self.training = True

    def forward(self, x):  # maybe need to use flatten here
        x_flat = self.flatten_layer(x)
        h_ = self.LeakyReLU(self.lin1(x_flat))
        h_ = self.LeakyReLU(self.lin2(h_))
        mean = self.lin_mean(h_)
        log_var = self.lin_var(h_)
        return mean, log_var


class VAE_Decoder(torch.nn.Module):
    def __init__(self, bins, hidden_dim, latent_dim, slope):
        super(VAE_Decoder, self).__init__()
        self.bins = bins
        self.slope = slope
        self.lin1 = torch.nn.Linear(latent_dim, hidden_dim)
        self.lin2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.out = torch.nn.Linear(hidden_dim, bins)

        self.LeakyReLU = torch.nn.LeakyReLU(slope)

    def forward(self, x):
        h = self.LeakyReLU(self.lin1(x))
        h = self.LeakyReLU(self.lin2(h))
        out = self.out(h)
        return out


class VAE(torch.nn.Module):
    def __init__(self, Encoder, Decoder):
        super(VAE, self).__init__()
        self.Encoder = Encoder
        self.Decoder = Decoder

    def reparametrization(self, mean, var):
        epsilon = torch.randn_like(var)
        z = mean + var * epsilon
        return z

    def forward(self, x):
        mean, log_var = self.Encoder(x)
        z = self.reparametrization(mean, torch.exp(0.5 * log_var))
        reco = self.Decoder(z)
        return mean, log_var, reco

    def loss_function(self, x, reco, code_mean, code_log_var, beta=1):
        reproduction_loss = torch.nn.functional.mse_loss(x, reco)
        KL_div = -0.5 * torch.sum(
            1 + code_log_var - code_mean.pow(2) - code_log_var.exp()
        )
        return reproduction_loss + beta * KL_div

    def train(
        self,
        epochs,
        X_train,
        y_train,
        X_validation,
        y_validation,
        lr=1e-3,
        batch_size=32,
        beta=1,
        device="cpu",
        random_state=1,
        plot_model=True,
    ):
        ekin = np.linspace(0, 18600, X_train[0].shape[0])
        train_data = Dataset(X_train, y_train)
        train_dl = DataLoader(train_data, batch_size=batch_size, device=device)
        val_data = Dataset(X_validation, y_validation)
        val_dl = DataLoader(val_data, batch_size=batch_size, device=device)
        optim = torch.optim.Adam(self.parameters(), lr)
        losses = []
        val_losses = []
        for count in range(epochs):
            if count > 0:
                X_train_shuffled, y_train_shuffled = shuffle(
                    X_train, y_train, random_state=random_state
                )
                train_data_shuffled = Dataset(X_train_shuffled, y_train_shuffled)
                train_dl = DataLoader(
                    train_data_shuffled, batch_size=batch_size, device=device
                )
                random_state += 1
            for count_batch, (x_b, y_b) in enumerate(train_dl):
                optim.zero_grad()
                code_mean, code_logvar, reco = self(x_b)
                loss = self.loss_function(
                    x_b.squeeze(), reco, code_mean, code_logvar, beta=beta
                )
                losses.append(loss.cpu().detach().numpy())
                loss.backward()
                optim.step()
                if count_batch % 100 == 0:
                    x_b_val, y_b_val = iter(val_dl).__next__()
                    x_b_val = x_b_val.to(device)
                    y_b_val = y_b_val.to(device)
                    with torch.no_grad():
                        code_mean, code_logvar, reco = self(x_b_val)  # reshape ?
                    loss_val = self.loss_function(
                        x_b_val.squeeze(), reco, code_mean, code_logvar, beta=beta
                    )
                    val_losses.append(loss_val.cpu().detach().numpy())
                    print(
                        f"Epoch: {count} | Batch: [{count_batch}/{len(train_data) / batch_size}] training loss: {float(loss):.10f}  validation loss: {float(loss_val):.10f}",
                    )
                    if plot_model:
                        f, axarr = plt.subplots(1, 3, figsize=(10, 10))
                        axarr[0].plot(ekin, x_b_val[0].cpu().detach().numpy())
                        axarr[1].plot(ekin, reco[0].cpu().detach().numpy())  # m[-1][0]
                        axarr[2].scatter(
                            code_mean[:, 0].cpu().detach().numpy(),
                            code_mean[:, 1].cpu().detach().numpy(),
                        )
                        f.set_tight_layout(True)

        return losses, val_losses

    def reco_loss(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        beta=1,
        mode="Both",
        device="cpu",
    ):
        if mode == "Both":
            data_s = Dataset(x_sterile_test, y_sterile_test)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            data_r = Dataset(x_ref_test, y_ref_test)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                c_m_s, c_l_s, r_s = self(x_s)
                c_m_r, c_l_r, r_r = self(x_r)

            # r_s = r_s.cpu().detach().numpy()
            # r_r = r_r.cpu().detach().numpy()

            reco_losses = []
            ref_losses = []
            for count, reco_spec in enumerate(r_s):
                reco_loss = self.loss_function(
                    x_s.squeeze()[count], reco_spec, c_m_s, c_l_s, beta=beta
                )
                reco_losses.append(reco_loss.cpu().detach().numpy())
            for count, reco_spec_ref in enumerate(r_r):
                reco_ref_loss = self.loss_function(
                    x_r.squeeze()[count], reco_spec_ref, c_m_r, c_l_r, beta=beta
                )
                ref_losses.append(reco_ref_loss.cpu().detach().numpy())
            return np.array(reco_losses, dtype=np.float64), np.array(
                ref_losses, dtype=np.float64
            )

        if mode == "ref":
            data_r = Dataset(x_ref_test, y_ref_test)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                c_m_r, c_l_r, r_r = self(x_r)

            ref_losses = []
            for count, reco_spec_ref in enumerate(r_r):
                reco_ref_loss = self.loss_function(
                    x_r.squeeze()[count], reco_spec_ref, c_m_r, c_l_r, beta=beta
                )
                ref_losses.append(reco_ref_loss.cpu().detach().numpy())

            return np.array(ref_losses, dtype=np.float64)

        if mode == "ster":
            data_s = Dataset(x_sterile_test, y_sterile_test)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            with torch.no_grad():
                c_m_s, c_l_s, r_s = self(x_s)

            reco_losses = []
            for count, reco_spec in enumerate(r_s):
                reco_loss = self.loss_function(
                    x_s.squeeze()[count], reco_spec, c_m_s, c_l_s, beta=beta
                )
                reco_losses.append(reco_loss.cpu().detach().numpy())

            return np.array(reco_losses, dtype=np.float64)


# Should implement this into model class: DONE


def reco_loss(
    ae,
    x_sterile_test=None,
    y_sterile_test=None,
    x_ref_test=None,
    y_ref_test=None,
    mode="Both",
    device="cpu",
):
    if mode == "Both":
        data_s = Dataset(x_sterile_test, y_sterile_test)
        x_s, y_s = data_s[:]
        x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
            y_s.astype(np.float64)
        ).unsqueeze(-1)
        x_s, y_s = x_s.to(device), y_s.to(device)

        data_r = Dataset(x_ref_test, y_ref_test)
        x_r, y_r = data_r[:]
        x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
            y_r.astype(np.float64)
        ).unsqueeze(-1)
        x_r, y_r = x_r.to(device), y_r.to(device)

        with torch.no_grad():
            c_s, r_s = ae(x_s)
            c_r, r_r = ae(x_r)

        # r_s = r_s.cpu().detach().numpy()
        # r_r = r_r.cpu().detach().numpy()

        reco_losses = []
        ref_losses = []
        for count, reco_spec in enumerate(r_s):
            reco_loss = torch.nn.functional.mse_loss(reco_spec, x_s.squeeze()[count])
            reco_losses.append(reco_loss.cpu().detach().numpy())
        for count, value in enumerate(r_r):
            reco_ref_loss = torch.nn.functional.mse_loss(value, x_r.squeeze()[count])
            ref_losses.append(reco_ref_loss.cpu().detach().numpy())
        return np.array(reco_losses, dtype=np.float64), np.array(
            ref_losses, dtype=np.float64
        )

    if mode == "ref":
        data_r = Dataset(x_ref_test, y_ref_test)
        x_r, y_r = data_r[:]
        x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
            y_r.astype(np.float64)
        ).unsqueeze(-1)
        x_r, y_r = x_r.to(device), y_r.to(device)

        with torch.no_grad():
            c_r, r_r = ae(x_r)

        ref_losses = []
        for count, value in enumerate(r_r):
            reco_ref_loss = torch.nn.functional.mse_loss(value, x_r.squeeze()[count])
            ref_losses.append(reco_ref_loss.cpu().detach().numpy())

        return np.array(ref_losses, dtype=np.float64)

    if mode == "ster":
        data_s = Dataset(x_sterile_test, y_sterile_test)
        x_s, y_s = data_s[:]
        x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
            y_s.astype(np.float64)
        ).unsqueeze(-1)
        x_s, y_s = x_s.to(device), y_s.to(device)

        with torch.no_grad():
            c_s, r_s = ae(x_s)

        reco_losses = []
        for count, reco_spec in enumerate(r_s):
            reco_loss = torch.nn.functional.mse_loss(reco_spec, x_s.squeeze()[count])
            reco_losses.append(reco_loss.cpu().detach().numpy())

        return np.array(reco_losses, dtype=np.float64)


# def plot_grad_flow(named_parameters):
#     """Plots the gradients flowing through different layers in the net during training.
#     Can be used for checking for possible gradient vanishing / exploding problems."""
#     ave_grads = []
#     max_grads = []
#     layers = []
#     for n, p in named_parameters:
#         if (p.requires_grad) and ("bias" not in n):
#             layers.append(n)
#             ave_grads.append(p.grad.abs().mean())
#             max_grads.append(p.grad.abs().max())
#     plt.bar(np.arange(len(max_grads)), max_grads, alpha=0.1, lw=1, color="c")
#     plt.bar(np.arange(len(max_grads)), ave_grads, alpha=0.1, lw=1, color="b")
#     plt.hlines(0, 0, len(ave_grads) + 1, lw=2, color="k")
#     plt.xticks(range(0, len(ave_grads), 1), layers, rotation="vertical")
#     plt.xlim(left=0, right=len(ave_grads))
#     plt.ylim(bottom=-0.001, top=0.02)  # zoom in on the lower gradient regions
#     plt.xlabel("Layers")
#     plt.ylabel("average gradient")
#     plt.title("Gradient flow")
#     plt.grid(True)
#     plt.legend(
#         [
#             Line2D([0], [0], color="c", lw=4),
#             Line2D([0], [0], color="b", lw=4),
#             Line2D([0], [0], color="k", lw=4),
#         ],
#         ["max-gradient", "mean-gradient", "zero-gradient"],
#     )
