from __future__ import annotations

import logging
from typing import Optional

from heudiconv.utils import SeqInfo

lgr = logging.getLogger("heudiconv")


def create_key(
    template: Optional[str],
    outtype: tuple[str, ...] = ("nii.gz",),
    annotation_classes: None = None,
) -> tuple[str, tuple[str, ...], None]:
    if template is None or not template:
        raise ValueError("Template must be a valid format string")
    return (template, outtype, annotation_classes)


def infotodict(
    seqinfo: list[SeqInfo],
) -> dict[tuple[str, tuple[str, ...], None], list[str]]:
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
    t2w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T2w')
    rest= create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_dir-lr_bold')
    fmap_rest_lr = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-lr_epi')
    fmap_rest_rl = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-rl_epi')
    
    info = {t1w: [], t2w: [], rest: [], fmap_rest_lr: [], fmap_rest_rl: []}
    for s in seqinfo:
        if "LOC" in str(s.image_type).upper():
            print(f"Skipping localizer sequence: {s.protocol_name}")
            # skip localizer sequences
            continue
        elif "NORM" in s.image_type:
            print(f"Skipping normalized sequence: {s.protocol_name}")
            # skip normalization sequences
            continue
        elif s.dim3 == 256:
            if "T1" in s.protocol_name or "MPR" in s.protocol_name:
                print(f"Found T1 sequence: {s.protocol_name}")
                info[t1w] = [s.series_id]
            elif "T2" in s.protocol_name:
                print(f"Found T2 sequence: {s.protocol_name}")
                info[t2w] = [s.series_id]
        elif s.dim1 == 64:
            print(f"Found resting state sequence: {s.protocol_name}")
            info[rest] = [s.series_id]
        elif s.dim1 == 74:
            if "LR" in str(s.protocol_name).upper():
                print(f"Found field map sequence: {s.protocol_name}")
                info[fmap_rest_lr] = [s.series_id]
            elif "RL" in str(s.protocol_name).upper():
                print(f"Found field map sequence: {s.protocol_name}")
                info[fmap_rest_rl] = [s.series_id]
        else:
            print(f"Unknown sequence: {s.protocol_name}, dim1={s.dim1}, dim3={s.dim3}")
    return info
