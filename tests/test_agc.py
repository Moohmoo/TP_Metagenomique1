"""Tests agc"""
import pytest
import os
import hashlib
from .context import agc
from agc import read_fasta
from agc import dereplication_fulllength
from agc import get_identity
from agc import abundance_greedy_clustering
from agc import write_OTU


def test_read_fasta():
    """Test fasta reading"""
    fasta_reader = read_fasta(os.path.abspath(os.path.join(os.path.dirname(__file__), "test_sequences.fasta.gz")), 200)
    assert(next(fasta_reader) == 'TGGGGAATATTGCACAATGGGCGCAAGCCTGATGCAGCCATGCCGCGTGTATGAAGAAGGCCTTCGGGTTGTAAAGTACTTTCAGCGGGGAGGAAGGTGTTGTGGTTAATAACCGCAGCAATTGACGTTACCCGCAGAAGAAGCACCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGGAAAGCGCA')
    # Short sequences should be skipped
    assert(next(fasta_reader) == 'TAGGGAATCTTCCGCAATGGGCGAAAGCCTGACGGAGCAACGCCGCGTGAGTGATGAAGGTCTTCGGATCGTAAAACTCTGTTATTAGGGAAGAACATATGTGTAAGTAACTGTGCACATCTTGACGGTACCTAATCAGAAAGCCACGGCTAACTACGTGCCAGCAGCCGCGGTAATACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTACAGCGCG')
    fasta_reader.close()

def test_dereplication_fulllength():
    """Test dereplication fulllength"""
    dereplication_reader =  dereplication_fulllength(os.path.abspath(os.path.join(os.path.dirname(__file__), "test_sequences.fasta.gz")), 200, 3)
    derep_1 = next(dereplication_reader)
    derep_2 = next(dereplication_reader)
    # Should be the most abundant sequence: seq4 counted 5 times
    assert(derep_1[0] == "ACTACGGGGCGCAGCAGTAGGGAATCTTCCGCAATGGACGAAAGTCTGACGGAGCAACGCCGCGTGTATGAAGAAGGTTTTCGGATCGTAAAGTACTGTTGTTAGAGAAGAACAAGGATAAGAGTAACTGCTTGTCCCTTGACGGTATCTAACCAGAAAGCCACGGCTAACTACGTGCCAGCAGCCGCGGTAATACGTAGGTGGCAAGCGTTGTCCGGAGTTAGTGGGCGTAAAGCGCGCGCAGGCGGTCTTTTAAGTCTGATGTCAAAGCCCCCGGCTTAACCGGGGAGGGTCATTGGAAACTGGAAGACTGGAGTGCAGAAGAGGAGAGTGGAATTCCACGTGTAGCGGTGAAATGCGTAGATATGTGGAGGAACACCAGTGGCGAAGGCGACTCTCTGGTCTGTAACTGACGCTGAGGCGCGAAAGCGTGGGGAGCAAA")
    assert(derep_1[1] == 5)
    # Should be the second most abundant sequence: seq3 counted 4 times
    assert(derep_2[0] == "TAGGGAATCTTCCGCAATGGGCGAAAGCCTGACGGAGCAACGCCGCGTGAGTGATGAAGGTCTTCGGATCGTAAAACTCTGTTATTAGGGAAGAACATATGTGTAAGTAACTGTGCACATCTTGACGGTACCTAATCAGAAAGCCACGGCTAACTACGTGCCAGCAGCCGCGGTAATACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTACAGCGCG")
    assert(derep_2[1] == 4)
    try:
        derep_3 = next(dereplication_reader)
        # derep_3 should be empty
        assert(len(derep_3) == 0)
    except StopIteration:
        # Congrats only two sequences to detect
        assert(True)

def test_get_identity():
    """
    """
    idres = get_identity(("TGGGGAATATTGCACAATGGGCGCAAGCCTGATGCAG", "TGGGGAATA--GCACAATGGGCGCAAGCCTCTAGCAG"))
    assert(round(idres,1) == 86.5)

def test_abundance_greedy_clustering():
    otu = abundance_greedy_clustering(os.path.abspath(os.path.join(os.path.dirname(__file__), "test_sequences.fasta.gz")),
        200, 3, 50, 8)
    assert(otu[0][0] == "ACTACGGGGCGCAGCAGTAGGGAATCTTCCGCAATGGACGAAAGTCTGACGGAGCAACGCCGCGTGTATGAAGAAGGTTTTCGGATCGTAAAGTACTGTTGTTAGAGAAGAACAAGGATAAGAGTAACTGCTTGTCCCTTGACGGTATCTAACCAGAAAGCCACGGCTAACTACGTGCCAGCAGCCGCGGTAATACGTAGGTGGCAAGCGTTGTCCGGAGTTAGTGGGCGTAAAGCGCGCGCAGGCGGTCTTTTAAGTCTGATGTCAAAGCCCCCGGCTTAACCGGGGAGGGTCATTGGAAACTGGAAGACTGGAGTGCAGAAGAGGAGAGTGGAATTCCACGTGTAGCGGTGAAATGCGTAGATATGTGGAGGAACACCAGTGGCGAAGGCGACTCTCTGGTCTGTAACTGACGCTGAGGCGCGAAAGCGTGGGGAGCAAA")
    assert(otu[1][0] == "TAGGGAATCTTCCGCAATGGGCGAAAGCCTGACGGAGCAACGCCGCGTGAGTGATGAAGGTCTTCGGATCGTAAAACTCTGTTATTAGGGAAGAACATATGTGTAAGTAACTGTGCACATCTTGACGGTACCTAATCAGAAAGCCACGGCTAACTACGTGCCAGCAGCCGCGGTAATACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTACAGCGCG")


def test_write_OTU():
    test_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.fna"))
    otu = [("TCAGCGAT", 8), ("TCAGCGAA",8), ("ACAGCGAT", 8), ("ACAGCGAA", 8)]
    write_OTU(otu, test_file)
    with open(test_file, 'rb') as otu_test:
        assert hashlib.md5(otu_test.read()).hexdigest() == "0a7caf3d43ba5f0c68bc05cb74782dbb"









