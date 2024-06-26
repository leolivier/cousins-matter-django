def validate_zipfile_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    # valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    # if not ext.lower() in valid_extensions:
    if ext.lower() != ".zip":
        raise ValidationError('File must be a zip file')
