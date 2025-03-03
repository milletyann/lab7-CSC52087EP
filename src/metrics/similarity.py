import torch
from torchmetrics import Metric
from torchmetrics.utilities import dim_zero_cat
from torchtyping import TensorType

num_samples, num_feats = None, None


class SimilarityScore(Metric):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_state("feats_1", default=[], dist_reduce_fx="cat")
        self.add_state("feats_2", default=[], dist_reduce_fx="cat")

    def update(
        self,
        feats_1: TensorType["num_samples", "num_feats"],
        feats_2: TensorType["num_samples", "num_feats"],
    ) -> float:
        """Update state with new features."""
        # ----------------------------------------------------------------------------- #
        # Complete this part for `Code 11`
        normed_feats_1 = feats_1 / feats_1.norm(dim=-1, keepdim=True)
        self.feats_1.append(normed_feats_1)
        normed_feats_2 = feats_2 / feats_2.norm(dim=-1, keepdim=True)
        self.feats_2.append(normed_feats_2)
        # ----------------------------------------------------------------------------- #

    def compute(self) -> float:
        """Compute cosine similarity between features."""
        feats_1 = dim_zero_cat(self.feats_1)
        feats_2 = dim_zero_cat(self.feats_2)

        # ----------------------------------------------------------------------------- #
        # Complete this part for `Code 11`
        score = torch.cosine_similarity(feats_1, feats_2, dim=-1)
        # ----------------------------------------------------------------------------- #

        return torch.max(score, torch.zeros_like(score))
