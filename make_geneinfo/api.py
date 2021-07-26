import io
import json
import requests
import pandas as pd

from typing import List, Dict

HEADERS = {"Content-type": "application/json"}

def get_gene_corresponding_table() -> pd.DataFrame:
    url = (
        "https://marchantia.info/download/MpTak_v6.1/gene_correspondence_MpTak_v6.1.tsv"
    )
    r = requests.get(url)
    df: pd.DataFrame = pd.read_csv(io.BytesIO(r.content), sep="\t").dropna()

    return df

def get_all_gene_ids() -> List:
    df = get_gene_corresponding_table()
    df = df[(df["locus_type"] == "mRNA") & (df["MpTak_v6.1"] != "-")]

    return list(df["MpTak_v6.1"].drop_duplicates())

def get_annotations(
    url: str, all_gene_ids: List[str], genome_version: str = "MpTak_v6.1"
) -> Dict:

    query = json.dumps(
        {
            "genome": genome_version,
            "dbtypes": ["KOG", "KEGG", "Pfam", "GO"],
            "query": all_gene_ids,
        }
    )

    req = requests.post(url, query, headers=HEADERS)

    return req.json()


def get_nomenclature(url: str) -> List:
    req = requests.post(url, headers=HEADERS)
    return req.json()