import ckanext.pygments.utils as pygment_utils


def is_format_supported(fmt: str) -> bool:
    """Check if we are supporting a specified resource format"""
    for formats in pygment_utils.LEXERS:
        if fmt in formats:
            return True

    return False
