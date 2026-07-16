from sklearn.cluster import KMeans

from .config import RANDOM_STATE


def build_model(k):

    model = KMeans(

        n_clusters=k,

        random_state=RANDOM_STATE,

        n_init=20,

        init="k-means++",

        max_iter=500

    )

    return model

