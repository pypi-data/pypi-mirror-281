import os

import yaml
from ray import tune
from ray.tune.schedulers import AsyncHyperBandScheduler

# from ray.tune.suggest import ConcurrencyLimiter
from ray.tune.search import ConcurrencyLimiter

# from ray.tune.suggest.skopt import SkOptSearch
from ray.tune.search.bayesopt import BayesOptSearch

from e2clab.optimizer import Optimization


class UserDefinedOptimization(Optimization):

    def run(self):
        # algo = SkOptSearch()
        algo = BayesOptSearch()
        algo = ConcurrencyLimiter(algo, max_concurrent=3)
        scheduler = AsyncHyperBandScheduler()
        objective = tune.run(
            self.run_objective,
            metric="user_response_time",
            mode="min",
            name="my_application",
            search_alg=algo,
            scheduler=scheduler,
            num_samples=9,
            config={
                "http_pool": tune.randint(20, 60),
                "simsearch_pool": tune.randint(20, 60),
                "extrac_pool": tune.randint(1, 3),
            },
            fail_fast=True,
        )

        print("Hyperparameters found: ", objective.best_config)

    def run_objective(self, _config):
        print("*" * 10 + " Configuration to deploy = ", _config)
        print("*" * 10 + " os.getcwd() = ", os.getcwd())
        # create an optimization directory using "self.prepare()"
        self.prepare()
        print("*" * 10 + " os.getcwd() = ", os.getcwd())
        # update the parameters of your configuration file(s) (located in "self.optimization_dir") according to
        # "_config" (defined by the search algorithm)
        config_yaml = None
        with open(f"{self.optimization_dir}/layers_services.yaml") as f:
            config_yaml = yaml.load(f, Loader=yaml.FullLoader)
        for layer in config_yaml["layers"]:
            for service in layer["services"]:
                if service["name"] in ["myapplication"]:
                    service["quantity"] = _config["extrac_pool"]
        with open(f"{self.optimization_dir}/layers_services.yaml", "w") as f:
            yaml.dump(config_yaml, f)
        print("*" * 10 + " BEFORE DEPLOY")
        # deploy the configurations (defined by the search algorithm) using "self.launch()".
        # "self.launch()" runs: layers_services; network; workflow (prepare, launch, finalize); and finalize;
        self.launch(optimization_config=_config)
        print("*" * 10 + " AFTER DEPLOY")
        # save the optimization results using "self.finalize()"
        self.finalize()
        # get the metric value that you generated in "self.experiment_dir"
        user_response_time: int = 0
        with open(f"{self.experiment_dir}/results/results.txt") as file:
            for line in file:
                user_response_time = int(line.rstrip().split(",")[1])
        print("*" * 10 + f" user_response_time = {user_response_time}")
        # report the metric value to Ray Tune as follows: "tune.report(my_metric=my_metric)"
        tune.report(
            user_response_time=user_response_time
        )  # tune.track.log(user_response_time=user_response_time)
