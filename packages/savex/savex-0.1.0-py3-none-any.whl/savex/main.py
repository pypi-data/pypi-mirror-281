import os
import re
import base64


def file_filter(file):
    try:
        filename = file.name
        return sanitize_file_name(filename, file)
    except Exception as e:
        print("An error occurred:", e)
        return False


def sanitize_file_name(filename, file):
    # Restrict allowed characters
    filename = re.sub(r'[^a-zA-Z0-9\s\.\-_]', '', filename)

    # Remove multiple consecutive dots or spaces
    filename = re.sub(r'\.{2,}', '.', filename)
    filename = re.sub(r'\s{2,}', ' ', filename)

    # Prevent path traversal attempts
    filename = filename.replace('/', '').replace('\\', '')

    # Check for remaining invalid characters
    if re.search(r'[^a-zA-Z0-9\s\.\-_]', filename):
        return False  # Invalid file name

    # Restrict allowed extensions (adjust as needed)
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
    extension = os.path.splitext(filename)[1][1:].lower()
    if extension not in allowed_extensions:
        return False  # Invalid extension

    # Prevent potential backdoor files (e.g., image.jpg.php)
    parts = filename.split('.')
    extension_count = len(parts) - 1  # Number of extensions
    if extension_count > 1:
        return False  # Too many extensions

    # Basic content checks (adjust patterns as needed)
    suspicious_patterns = [
        '<?php',       # PHP opening tag
        '<script>',   # JavaScript opening tag
        '<%',          # JSP opening tag
        '<@',          # ASP opening tag
        '@Echo',       # VBScript Echo statement
        '%--',         # XML comment opening sequence
        'data:application/'  # base64
    ]

    with open(file.name, 'rb') as f:
        file_content = f.read()
        for pattern in suspicious_patterns:
            if pattern.encode() in file_content:
                return False  # Suspicious content found
            elif b'data:image/' in file_content:
                return detect_backdoor(file_content)
            else:
                return filename

    return filename


def detect_backdoor(base64_image):
    # Convert the base64 image to a binary string
    binary_image = base64.b64decode(base64_image)

    # Check the size of the image
    if len(binary_image) < 1000:
        # The image is probably too small to contain a backdoor
        return True  # Not a backdoor

    # Check the format of the image
    magic_number = binary_image[:4].hex().upper()
    known_magic_numbers = {
        "FFD8FF": "JPEG",
        "89504E47": "PNG",
        "47494638": "GIF"
    }
    if magic_number not in known_magic_numbers:
        # The image is not in a known format
        return True

    # Check for the presence of known backdoor signatures
    known_backdoor_signatures = [
        # PHP web shell backdoor
        b'eval(base64_decode(\'...\'));'
    ]
    for signature in known_backdoor_signatures:
        if signature in binary_image:
            # The image contains a backdoor
            return False

    # The image is not a backdoor
    return True
