import glob
import os
import shutil
import time
import uuid
from abc import ABCMeta, abstractmethod
from pathlib import Path

import e2clab.tasks as t


class Optimization:

    __metaclass__ = ABCMeta

    def __init__(self, scenario_dir, artifacts_dir, duration, repeat):
        self.scenario_dir = scenario_dir
        self.artifacts_dir = artifacts_dir
        self.duration = duration
        self.repeat = repeat
        self.ray_dir = None
        self.optimization_dir = None
        self.experiment_dir = None
        self.optimization_id = None

    @abstractmethod
    def run(self):
        """(abstract) Setup your training: Implement the logic of your optimization."""
        pass

    def prepare(self):
        """
        Creates an optimization directory with all E2Clab config files (*.yaml files).
         The files are copied from "scenario_dir".
        """
        self.ray_dir = os.getcwd()
        self.optimization_id = uuid.uuid4().hex
        self.optimization_dir = (
            self.scenario_dir
            / f"{time.strftime('%Y%m%d-%H%M%S')}-{self.optimization_id}"
        )
        os.mkdir(self.optimization_dir)
        os.chdir(self.optimization_dir)
        files = glob.iglob(os.path.join(self.scenario_dir, "*.yaml"))
        for file in files:
            if os.path.isfile(file):
                shutil.copy2(file, self.optimization_dir)

    def launch(self, optimization_config=None):
        """
        Deploys the configurations defined by the search algorithm.
        It runs the following E2Clab commands:
        layers_services; network; workflow (prepare, launch, finalize); and finalize.
        """
        env = self.optimization_dir
        experiment_id = t.infra(
            self.optimization_dir,
            self.artifacts_dir,
            optimization_id=self.optimization_id,
            optimization_config=optimization_config,
            env=env,
        )
        self.experiment_dir = self.optimization_dir / experiment_id
        t.network(env=env)
        t.app("prepare", env=env)
        t.app("launch", env=env)
        time.sleep(int(self.duration))
        t.finalize(env=env)
        for exp in range(int(self.repeat)):
            current_repeat = exp + 1
            print(
                f"[{time.strftime('%Y%m%d-%H:%M:%S')}] "
                f"Repeating {Path(self.scenario_dir).stem}[{current_repeat} "
                f"out of {self.repeat}]"
            )
            experiment_id = t.infra_repeat(current_repeat, env=env)
            self.experiment_dir = self.optimization_dir / experiment_id
            t.network(env=env)
            t.app("launch", env=env)
            time.sleep(int(self.duration))
            t.finalize(env=env)

    def finalize(self):
        """
        Saves the optimization results.
        """
        shutil.copytree(self.ray_dir, f"{self.optimization_dir}/optimization-results")
