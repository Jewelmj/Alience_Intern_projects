def is_allowed_extension(filename, allowed_extensions):
    return filename.lower().endswith(
        tuple(allowed_extensions)
    )