# %%

import torch
from torch.nn.functional import one_hot
from bayesian_network.common.torch_settings import TorchSettings
import torchvision
from torchvision.transforms import transforms
from bayesian_network.bayesian_network import BayesianNetwork, Node
from bayesian_network.inference_machines.torch_sum_product_algorithm_inference_machine import (
    TorchSumProductAlgorithmInferenceMachine,
)
from bayesian_network.interfaces import IInferenceMachine
from bayesian_network.optimizers.em_optimizer import EmOptimizer

# %%


def preprocess(
    torch_settings: TorchSettings, gamma, selected_num_observations
):
    mnist = torchvision.datasets.MNIST(
        "./mnist", train=True, transform=transforms.ToTensor(), download=True
    )
    data = mnist.train_data.to(torch_settings.device)

    # Make smaller selection
    if selected_num_observations:
        data = data[0:selected_num_observations, :, :]

    data = data.ge(128).long()

    height, width = data.shape[1:3]
    num_features = height * width
    num_observations = data.shape[0]

    # Morph into evidence structure
    data = data.reshape([num_observations, num_features])

    # evidence: List[num_observed_nodes x torch.Tensor[num_observations x num_states]], one-hot encoded
    evidence = [
        node_evidence * (1 - gamma) + gamma / 2
        for node_evidence in one_hot(data.T, 2).to(torch_settings.dtype)
    ]

    return evidence


# %%


def fit(torch_settings, evidence):
    num_observations = evidence[0].shape[0]
    height = 28
    width = 28
    num_classes = 10

    # Create network
    Q = Node(
        torch.ones(
            (num_classes),
            device=torch_settings.device,
            dtype=torch_settings.dtype,
        )
        / num_classes,
        name="Q",
    )
    mu = (
        torch.rand(
            (height, width, num_classes),
            device=torch_settings.device,
            dtype=torch_settings.dtype,
        )
        * 0.2
        + 0.4
    )
    mu = torch.stack([1 - mu, mu], dim=3)
    Ys = [
        Node(mu[iy, ix], name=f"Y_{iy}x{ix}")
        for iy in range(height)
        for ix in range(width)
    ]

    nodes = [Q] + Ys
    parents = {Y: [Q] for Y in Ys}
    parents[Q] = []

    network = BayesianNetwork(nodes, parents)

    # Fit network
    num_iterations = 2
    num_sp_iterations = 3

    def inference_machine_factory(
        bayesian_network: BayesianNetwork,
    ) -> IInferenceMachine:
        return TorchSumProductAlgorithmInferenceMachine(
            bayesian_network=bayesian_network,
            observed_nodes=Ys,
            torch_settings=torch_settings,
            num_iterations=num_sp_iterations,
            num_observations=num_observations,
            callback=lambda *args: None,
        )

    def callback(ll, iteration, duration):
        print(
            f"Finished iteration {iteration}/{num_iterations} - ll: {ll} - it took: {duration} s"
        )

    em_optimizer = EmOptimizer(network, inference_machine_factory)
    em_optimizer.optimize(evidence, num_iterations, callback)

    return network


# %%

torch_settings = TorchSettings(torch.device("cpu"), torch.float64)
selected_num_observations = 100
gamma = 0.00001

evidence = preprocess(torch_settings, gamma, selected_num_observations)
network = fit(torch_settings, evidence)

# %%

import matplotlib.pyplot as plt

Ys = network.nodes[1:]
w = torch.stack([y.cpt.cpu() for y in Ys])

plt.figure()
for i in range(0, 10):
    plt.subplot(4, 3, i + 1)
    plt.imshow(w[:, i, 1].reshape(28, 28))
    plt.colorbar()
    plt.clim(0, 1)
