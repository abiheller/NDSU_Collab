from os.path import join as opj


def create_key(template, outtype=("nii.gz",), annotation_classes=None):
    if template is None or not template:
        raise ValueError("Template must be a valid format string")
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    t1w = create_key(
        opj("sub-{subject}", "{session}", "anat", "sub-{subject}_{session}_T1w")
    )
    t2w = create_key(
        opj(
            "sub-{subject}",
            "{session}",
            "anat",
            "sub-{subject}_{session}_T2w",
        )
     )
    rest = create_key(
        opj(
            "sub-{subject}",
            "{session}",
            "func",
            "sub-{subject}_{session}_task-rest_dir-lr_bold",
        )

    )
    fmap_rest_lr = create_key(
        opj(
            "sub-{subject}",
            "{session}",
            "fmap",
            "sub-{subject}_{session}_dir-lr_epi",
        )
    )
    fmap_rest_rl = create_key(
        opj(
            "sub-{subject}",
            "{session}",
            "fmap",
            "sub-{subject}_{session}_dir-rl_epi",
        )
  
    )
    info = {
        t1w: [],
        t2w: [],
        rest: [],
        fmap_rest_lr: [],
        fmap_rest_rl: []
    }
    for s in seqinfo:
        if "LOC" in str(s.protocol_name).upper():
            print(f"Skipping localizer sequence: {s.protocol_name}, {s.image_type}")
            # skip localizer sequences
            continue
        elif "T1" in s.protocol_name or "MPR" in s.protocol_name:
            print(f"Found T1 sequence: {s.protocol_name}, {s.image_type}, dim3={s.dim3}")
            info[t1w] = [s.series_id]
        elif "T2" in s.protocol_name:
            print(f"Found T2 sequence: {s.protocol_name}, {s.image_type}, dim3={s.dim3}")
            info[t2w] = [s.series_id]
        elif "GRE" in str(s.protocol_name).upper():
            if "LR" in str(s.protocol_name).upper():
                print(f"Found field map sequence: {s.protocol_name}, {s.image_type}, dim1={s.dim1}")
                info[fmap_rest_lr] = [s.series_id]
            elif "RL" in str(s.protocol_name).upper():
                print(f"Found field map sequence: {s.protocol_name}, {s.image_type}, dim1={s.dim1}")
                info[fmap_rest_rl] = [s.series_id]
        elif s.dim1 == 64:
            print(f"Found resting state sequence: {s.protocol_name}, {s.image_type}, dim1={s.dim1}")
            info[rest] = [s.series_id]
        else:
            print(f"Unknown sequence: "
                  f"protocol_name={s.protocol_name}, "
                  f"image_type={s.image_type}, "
                  f"dim1={s.dim1}, "
                  f"dim3={s.dim3}")
    return info
