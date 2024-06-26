import numpy as np
import pandas as pd

from ema import EmbeddingHandler

DATA_DIR = "examples/HCN1-variants/"
FP_METADATA = DATA_DIR + "metadata.csv"
FP_EMB_ESM1b = DATA_DIR + "esm1b_t33_650M_UR50S-embeddings.npy"
FP_EMB_ESM2 = DATA_DIR + "esm2_t33_650M_UR50D-embeddings.npy"

# load metadata and embeddings

metadata = pd.read_csv(FP_METADATA)
emb_esm1b = np.load(FP_EMB_ESM1b)
emb_esm2 = np.load(FP_EMB_ESM2)

if DATA_DIR == "examples/ion-channel-proteins/":
    FP_EMB_ESM1v = DATA_DIR + "esm1v_t33_650M_UR90S_1-embeddings.npy"
    emb_esm1v = np.load(FP_EMB_ESM1v)

if DATA_DIR == "examples/HCN1-variants/":
    # find wt sequence index in the metadata by the variant_id which contains "WT"
    wt_idx = metadata["variant_id"].str.contains("WT").idxmax()

    # delete the wt sequence from the metadata and embeddings
    metadata = metadata.drop(wt_idx)
    emb_esm1b = np.delete(emb_esm1b, wt_idx, axis=0)
    emb_esm2 = np.delete(emb_esm2, wt_idx, axis=0)

    print(emb_esm1b.shape, emb_esm2.shape)

# initialize embedding handler
emb_handler = EmbeddingHandler(metadata)

# add embeddings to the handler
emb_handler.add_emb_space(embeddings=emb_esm1b, emb_space_name="ESM-1b")
emb_handler.add_emb_space(embeddings=emb_esm2, emb_space_name="ESM-2")

if DATA_DIR == "examples/ion-channel-proteins/":
    emb_handler.add_emb_space(embeddings=emb_esm1v, emb_space_name="ESM-1v")

import plotly.express as px
import scipy.stats as stats
from scipy.stats import wilcoxon


# mann-whitney u test
distances_per_group = emb_handler.get_distances_per_group(
    emb_space_name="ESM-1b",
    distance_metric="euclidean",
    group="('uniprot', 'Region')",
)

print(
    "Disordered - Disordered:",
    "Len: ",
    len(distances_per_group["Disordered - Disordered"]),
    "Median: ",
    np.median(distances_per_group["Disordered - Disordered"]),
    "MAD: ",
    stats.median_abs_deviation(
        distances_per_group["Non-disordered - Disordered"]
    ),
)
print(
    "Non-disordered - Disordered:",
    "Len: ",
    len(distances_per_group["Non-disordered - Disordered"]),
    "Median: ",
    np.median(distances_per_group["Non-disordered - Disordered"]),
    "MAD: ",
    stats.median_abs_deviation(distances_per_group["Disordered - Disordered"]),
)

# plot histogram of distances
fig_1 = px.histogram(
    x=distances_per_group["Disordered - Disordered"],
    nbins=100,
    title="Disordered - Disordered",
)

fig_2 = px.histogram(
    x=distances_per_group["Non-disordered - Disordered"],
    nbins=100,
    title="Non-disordered - Disordered",
)

U1, p = stats.mannwhitneyu(
    np.array(distances_per_group["Disordered - Disordered"]),
    np.array(distances_per_group["Non-disordered - Disordered"]),
    alternative="less",
    method="auto",
)

n1 = len(distances_per_group["Disordered - Disordered"])
n2 = len(distances_per_group["Non-disordered - Disordered"])
U2 = n1 * n2 - U1
U = min(U1, U2)
effect_size = 1 - (2 * U) / (n1 * n2)

print("effect size: ", effect_size)
print("p: ", p)
# n1 = len(go_term_count_brain_go_terms_brain_proteins)
# n2 = len(go_term_count_brain_go_terms_non_brain_proteins)
# U2 = n1*n2 - U1
# U = min(U1, U2)
# effect_size = 1 - 2*U / (n1 * n1)

# t-test

t_test_results = stats.ttest_ind(
    distances_per_group["Disordered - Disordered"],
    distances_per_group["Non-disordered - Disordered"],
    equal_var=False,
)


fig = emb_handler.plot_emb_dis_dif_dis_per_group(
    emb_space_name="ESM-1b",
    distance_metric="euclidean",
    group="('uniprot', 'Region')",
    plot_type="box",
    # log_scale=True
)

fig = emb_handler.plot_emb_dis_dif_dis_per_group(
    emb_space_name="ESM-1b",
    distance_metric="euclidean",
    group="('uniprot', 'Region')",
    plot_type="box",
    # log_scale=True
)
