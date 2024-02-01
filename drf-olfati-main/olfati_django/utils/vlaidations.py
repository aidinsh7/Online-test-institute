from django.core.exceptions import ValidationError

size = 5


def validate_image_size(value):
    # Set the maximum allowed size (in bytes), for example, 2 MB
    max_size = size * 1024 * 1024

    if value.size > max_size:
        raise ValidationError(f'محدودیت سایز تا حداکثر {size} مگابایت')
