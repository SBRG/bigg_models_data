import os
from Bio import Entrez
Entrez.email = "aebrahim@ucsd.edu"

FOLDER_NAME = "genbank"
if not os.path.isdir(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)


def gen_filepath(accession):
    return os.path.join(FOLDER_NAME, accession + ".gb")


with open("model-genome.txt") as infile:
    for line in infile:
        split = line.split()
        if len(split) < 3:
            continue
        if line.startswith("#"):
            continue
        model = split[0].rsplit(".", 1)[0]
        ncbi_accessions = [i.split(":", 1)[1]
                           for i in split if i.startswith("ncbi_")]
        if len(ncbi_accessions) == 0:
            print("no genome found for " + model)
            continue
        accession = ncbi_accessions[0]
        if "," in accession:
            accession = accession.split(",")[-1]
        if accession.endswith(".gb"):
            accession = accession[:-3]
        if os.path.isfile(gen_filepath(accession)):
            print("already downloaded genome %s for %s" % (accession, model))
            continue
        search = Entrez.esearch(db="nucleotide", term=accession,
                                retmax=1)
        search_result = Entrez.read(search)
        search.close()
        try:
            genome_id = search_result["IdList"][0]
        except IndexError:
            print("no genome found with accession " + accession)
            continue
        print("downloading genome %s (id=%s) for %s" %
              (accession, genome_id, model))
        dl = Entrez.efetch(db="nuccore", id=genome_id, rettype="gbwithparts",
                           retmode="text")
        with open(gen_filepath(accession), "w") as outfile:
            outfile.write(dl.read())
        dl.close()
