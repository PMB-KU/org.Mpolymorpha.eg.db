import argparse
import json
from typing import Dict, List, Optional

import pandas as pd

import api


def load_annotaions(path: Optional[str] = None, all_gene_ids: Optional[List[str]] = None) -> Dict:
    if path is None:
        annotations_api = "https://marchantia.info/api/annotations/"
        print("annotation api:", annotations_api)
        annotations = api.get_annotations(annotations_api, all_gene_ids)
        with open("annotation.json", "w") as w:
            json.dump(annotations, w)

        return annotations
    else:
        with open(path) as f:
            annotations = json.load(f)

        return annotations


def load_nomenclatures(path: Optional[str] = None) -> List:
    if path is None:
        nomenclatures_api = "https://marchantia.info/api/nomenclatures/"
        print("nomenclatures api:", nomenclatures_api)
        nomenclatures = api.get_nomenclature(nomenclatures_api)
        with open("nomenclatures.json", "w") as w:
            json.dump(nomenclatures, w)

        return nomenclatures
    else:
        with open(path) as f:
            nomenclatures = json.load(f)
        return nomenclatures


def make_gene2go(all_gene_ids: List[str], annotations: Dict):
    gene2go = []
    for gene_id in all_gene_ids:
        annotation = annotations.get(gene_id)

        if annotation is None:
            continue

        for go in annotation["GO"]:
            gene2go.append([gene_id, go["id"], "ISO"])

    gene2go = pd.DataFrame(gene2go, columns=["GID", "GO", "EVIDENCE"])
    gene2go.to_csv("gene2go.csv", index=None)

def make_gene2ko(all_gene_ids: List[str], annotations: Dict):
    gene2ko = []
    for gene_id in all_gene_ids:
        annotation = annotations.get(gene_id)

        if annotation is None:
            continue
        
        for kegg in annotation["KEGG"]:
            gene2ko.append([gene_id, kegg["id"]])
        gene2ko = pd.DataFrame(gene2ko, columns=["GID", "KO"])
        

def make_geneinfo(all_gene_ids: List[str], nomenclatures: List):
    gene_info = {}

    for gene_id in all_gene_ids:
        gene_info.setdefault(gene_id, {
            "SYMBOL": gene_id,
            "PRODUCT": "No Information",
            "REFERENCE": "No Reference"
        })

    for nomenclature in nomenclatures:
        gene_id = nomenclature[0]
        symbol = nomenclature[2]
        product = nomenclature[3]
        ref = nomenclature[4]
        gene_info[gene_id] = {
            "SYMBOL": symbol,
            "PRODUCT": product,
            "REFERENCE": ref
        }

    df = pd.DataFrame.from_dict(gene_info, orient="index")
    df.index.name = "GID"
    df["ENTREZID"] = df.index
    df.to_csv("gene_info.csv")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-api", action="store_true")
    parser.add_argument("--annotation", default="annotation.json", type=str)
    parser.add_argument(
        "--nomenclature", default="nomenclatures.json", type=str)
    args = parser.parse_args()

    # annotations = load_annotaions("annotation.json")
    # nomenclatures = load_nomenclatures("nomenclatures.json")
    all_gene_ids = api.get_all_gene_ids()

    if args.use_api:
        annotations = load_annotaions(all_gene_ids=all_gene_ids)
        nomenclatures = load_nomenclatures()
    else:
        annotations = load_annotaions(args.annotation)
        nomenclatures = load_nomenclatures(args.nomenclature)

    make_gene2go(all_gene_ids, annotations)
    make_geneinfo(all_gene_ids, nomenclatures)


if __name__ == "__main__":
    main()
