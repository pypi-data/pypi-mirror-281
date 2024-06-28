import base64
import logging
logger = logging.getLogger(__name__)


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}
def is_image_file(abs_fname):
    """
    Check if the given file name has an image file extension.

    :param file_name: The name of the file to check.
    :return: True if the file is an image, False otherwise.
    """
    abs_fname = str(abs_fname)  # Convert file_name to string
    return any(abs_fname.endswith(ext) for ext in IMAGE_EXTENSIONS)

def read_image(abs_fname):
    try:
        with open(str(abs_fname), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode("utf-8")
    except FileNotFoundError:
        logger.error(f"{abs_fname}: file not found error")
        return
    except IsADirectoryError:
        logger.error(f"{abs_fname}: is a directory")
        return
    except Exception as e:
        logger.error(f"{abs_fname}: {e}")
        return

def read_text(abs_fname, encoding="utf-8"):
    if is_image_file(abs_fname):
        return read_image(abs_fname)

    try:
        with open(str(abs_fname), "r", encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"{abs_fname}: file not found error")
        return
    except IsADirectoryError:
        logger.error(f"{abs_fname}: is a directory")
        return
    except UnicodeError as e:
        logger.error(f"{abs_fname}: {e}")
        return
