import os
import subprocess


class FeatureBrewStore:

    def __init__(self, provider, feature_brew_estimator, dataset_name, initialize=True, registry="local", final_features=[]):
        self.provider = provider
        self.feature_brew_estimator = feature_brew_estimator
        self.dataset_name = dataset_name
        self.registry = registry
        self.initialize = initialize
        self.final_features = final_features


    def deploy(self):
        cwd = os.getcwd()
        # initialize store
        if self.initialize:
            subprocess.run(["feast", "init", "feast_store"])

        os.chdir(os.path.join(cwd, "feast_store", "feature_repo"))
        print (os.getcwd())
        # initialize store
        subprocess.run(["feast", "apply"])
        # subprocess.run(["feast", "ui", "--port", "8000"])
