from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import torch
from gpytorch.functions import add_diag
from gpytorch.likelihoods import Likelihood
from gpytorch.random_variables import GaussianRandomVariable


class GaussianLikelihood(Likelihood):
    """
    """

    def __init__(self, log_noise_prior=None):
        super(GaussianLikelihood, self).__init__()
        self.register_parameter(name="log_noise", parameter=torch.nn.Parameter(torch.tensor([0.])), prior=log_noise_prior)

    def forward(self, input):
        assert isinstance(input, GaussianRandomVariable)
        mean, covar = input.representation()
        noise = add_diag(covar, self.log_noise.exp())
        return input.__class__(mean, noise)

    def log_probability(self, input, target):
        res = -0.5 * ((target - input.mean()) ** 2 + input.var()) / self.log_noise.exp()
        res += -0.5 * self.log_noise - 0.5 * math.log(2 * math.pi)
        return res.sum(0)
