import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def check_upload_file_folder():
    return os.path.exists("./static/uploads")

def create_upload_file_folder(path):
    os.mkdir(path)
    print("path created")

def is_file_allowed(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS