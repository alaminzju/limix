import os

import limix
from limix._cli.pipeline import Pipeline
from limix._cli.preprocess import normalize, where


def test_pipeline_where_filter():

    filenames = [
        "chrom22_subsample20_maf0.10.bed",
        "chrom22_subsample20_maf0.10.fam",
        "chrom22_subsample20_maf0.10.bim",
    ]
    shapes = [
        (274, 5647),
        (274, 0),
        (274, 49008),
        (274, 49008),
        (4, 49008),
        (274, 5647),
        (274, 0),
        (274, 49008),
    ]
    specs = [
        "genotype:(16050612 <= pos) & (pos < 21050612)",
        "genotype:(16050612 <= pos) & (pos < 16050612)",
        "genotype",
        "genotype:",
        "genotype:sample.isin(['HG00111', 'HG00112', 'NA20775', 'NA20804'])",
        "genotype:(chrom == '22') & (16050612 <= pos) & (pos < 21050612)",
        "genotype: a0 == a1",
        "genotype: sample != None",
    ]
    with limix.file_example(filenames) as filepaths:
        folder = os.path.dirname(filepaths[0])
        filepath = os.path.join(folder, "chrom22_subsample20_maf0.10")

        for shape, spec in zip(shapes, specs):
            G = limix.io.fetch("genotype", f"{filepath}", verbose=False)
            data = {"G": G}
            pipeline = Pipeline(data)
            pipeline.append(where, spec=spec)
            data = pipeline.run(verbose=False)
            assert data["G"].shape == shape
            assert data["G"].dims == ("sample", "candidate")


def test_pipeline_normalize():

    with limix.file_example("expr.csv") as filepath:
        folder = os.path.dirname(filepath)
        filepath = os.path.join(folder, "expr.csv")

        y = limix.io.fetch("trait", f"{filepath}::row=trait", verbose=False)
        data = {"y": y}
        pipeline = Pipeline(data)
        pipeline.append(normalize, spec="trait:trait:gaussianize")
        data = pipeline.run(verbose=False)
