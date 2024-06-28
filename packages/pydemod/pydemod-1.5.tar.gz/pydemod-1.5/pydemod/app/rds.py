# This file is part of Pydemod
# Copyright Christophe Jacquet (F8FTK), 2014
# Licence: GNU GPL v3
# See: https://github.com/ChristopheJacquet/Pydemod

import numpy as np

import pydemod.coding.polynomial as poly
import pydemod.filters.shaping as shaping

def generate_basic_wordstream(pi: int, psName: str):
    """
    Generates a basic RDS stream composed of 0B groups for a given PI code
    and station name.

    Please use LibRDS to encode RDS
    """
    print("PyDemod: generate_basic_wordstream usage, switch to LibRDS for non-testing purposes")

    if pi < 0 or pi > 0xFFFF:
        raise Exception("PI code must be between 0x0000 and 0xFFFF")

    if len(psName) > 8:
        raise Exception("PS name must not be more than 8 characters long")

    psName = psName.ljust(8)

    while True:
        for i in range(4):
            yield ('A', pi & 0xFFFF)

            yield ('B', 0x0800 | i) #0x800 has the 5th starting bit enabled which is the AB switch for RDS Groups (http://www.interactive-radio-system.com/docs/EN50067_RDS_Standard.pdf, page 13)

            yield ("C'", pi & 0xFFFF) #B group, these dont have a C group so they have a pi code here instead (http://www.interactive-radio-system.com/docs/EN50067_RDS_Standard.pdf, page 15-16)

            yield ('D', (ord(psName[i*2])<<8) + ord(psName[i*2+1])) # PS Characters, please don't use this profesionally, RDS has a special charset which is similiar to UTF-8 but not completly



def bitstream(gen, seconds) -> np.ndarray:
    wordstream = [next(gen) for _ in range(int(seconds * 1187.5 / 26))]
    return poly.rds_code.wordstream_to_bitstream(wordstream)

def bitstream_one_group(gen) -> np.ndarray:
    wordstream = [next(gen) for _ in range(int((0.0876) * 1187.5 / 26))]
    return poly.rds_code.wordstream_to_bitstream(wordstream)


def pulse_shaping_filter(length, sample_rate):
    return shaping.rrcosfilter(length, 1, 1/(2*1187.5), sample_rate+1) [1]


def unmodulated_signal(bitstream, sample_rate = 228000):
    samples_per_bit = int(sample_rate / 1187.5)

    # Differentially encode
    diffbs = np.zeros(len(bitstream), dtype=int)
    for i in range(1, len(bitstream)):
        if diffbs[i-1] != bitstream[i]:
            diffbs[i] = 1

    # Positive symbol pattern
    symbol = np.zeros(samples_per_bit)
    symbol[0] = 1
    symbol[samples_per_bit//2-1] = -1

    # Generate the sample array
    samples = np.tile(symbol, len(diffbs))
    for i in range(len(diffbs)):
        if diffbs[i] == 0:
            samples[i * samples_per_bit : (i+1)*samples_per_bit] *= -1

    # Apply the data-shaping filter
    shapedSamples = np.convolve(samples, pulse_shaping_filter(samples_per_bit*2, sample_rate))

    return shapedSamples