import os
import re
import subprocess
import tempfile
import typing
from pathlib import Path

import librosa
import soundfile as sf

from . import model
from .yomi_to_voca import yomi_to_voca

re_alignment = re.compile(r"\[\s*(\d+)\s*(\d+)]  (-?\d+\.\d+)  (.+)")


def parse_julius_output(
    output: str,
) -> typing.List[typing.Tuple[int, int, str]]:
    results = []
    offset_align = 125_000  # 12.5 ms = 125 * 100 ns
    lines = output.split("\n")
    in_alignment = False
    for line in lines:
        if line == "=== begin forced alignment ===":
            in_alignment = True
        elif line == "=== end forced alignment ===":
            in_alignment = False

        if in_alignment:
            m = re_alignment.match(line)
            if m:
                begin_frame = int(m.group(1))
                end_frame = int(m.group(2))

                begin_time = int(begin_frame * 10e4)
                if begin_time != 0:
                    begin_time += offset_align
                end_time = int((end_frame + 1) * 10e4 + offset_align)

                text = m.group(4)

                results.append((begin_time, end_time, text))
    return results


def align(
    wav_path: str,
    text: str,
    model_path: typing.Optional[typing.Union[Path, str]] = None,
    julius_path: typing.Union[Path, str] = "/usr/bin/julius",
) -> typing.List[typing.Tuple[int, int, str]]:
    """Get the forced alignment from the given wav file and pronunciation.

    Args:
        wav_path: Path to the wav file.
        text: Pronunciation of the wav file written in hiragana or katakana.
        model_path: Path to hmmdefs_monof_mix16_gid.binhmm model file.
                    If None, fetch it via HTTPS and cache it to avoid further requests.
        julius_path: Path to julius binary.

    Returns:
        A list of tuples of (begin_time, end_time, phoneme).
        begin_time and end_time are in units of 100 nanoseconds.
    """

    # fetch model if not specified
    if model_path is None:
        model_path = model.retrieve()

    # convert audio
    convert_sr = 16000
    y, sr = sf.read(wav_path)
    resampled = librosa.resample(y, sr, convert_sr)

    # write to temp file
    fwav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(fwav, resampled, convert_sr, subtype="PCM_16")
    fwav.close()

    voca = yomi_to_voca(text)
    words = ["silB", voca, "silE"]

    # generate .dfa
    fdfa = tempfile.NamedTemporaryFile("wt", suffix=".dfa", delete=False)
    n = len(words)
    for i in range(n):
        fdfa.write(f"{i} {n-i-1} {i+1} 0 {1 if i == 0 else 0}\n")
    fdfa.write(f"{n} -1 -1 1 0\n")
    fdfa.close()

    # generate .dict
    fdict = tempfile.NamedTemporaryFile("wt", suffix=".dict", delete=False)
    for i in range(n):
        fdict.write(f"{i} [w_{i}] {words[i]}\n")
    fdict.close()

    # invoke julius
    input = (fwav.name + "\n").encode()
    proc = subprocess.run(
        [
            julius_path,
            "-input",
            "file",
            "-h",
            model_path,
            "-dfa",
            fdfa.name,
            "-v",
            fdict.name,
            "-palign",
        ],
        input=input,
        capture_output=True,
    )

    julius_output = proc.stdout.decode("utf-8")
    if proc.returncode != 0:
        raise RuntimeError(
            f"julius returned {proc.returncode}; {julius_output}"
        )

    results = parse_julius_output(julius_output)

    # remove temporary files
    os.unlink(fwav.name)
    os.unlink(fdfa.name)
    os.unlink(fdict.name)

    return results
