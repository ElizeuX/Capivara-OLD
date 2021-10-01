# -*- coding: utf-8 -*-


class CapivaraEmptyError(Exception):
    def __init__(self, error_code, *args, **kwargs):
        super(CapivaraEmptyError, self).__init__(*args, **kwargs)
        self.error_code = error_code


class WritingRecordError(Exception):
    def __init__(self, error_code, *args, **kwargs):
        super(WritingRecordError, self).__init__(*args, **kwargs)
        self.error_code = error_code


class CapivaraDoesNotExistError(Exception):
    def __init__(self, error_code, *args, **kwargs):
        super(CapivaraDoesNotExistError, self).__init__(*args, **kwargs)
        self.error_code = error_code


class CapivaraDecodeFailError(Exception):
    def __init__(self, error_code, *args, **kwargs):
        super(CapivaraDoesNotExistError, self).__init__(*args, **kwargs)
        self.error_code = error_code
