# Copyright (C) 2001,2002 Python Software Foundation
# Author: barry@zope.com (Barry Warsaw)

"""Class representing image/* type MIME documents.
"""

import imghdr

# Intrapackage imports
import MIMEBase
import Errors
import Encoders



class MIMEImage(MIMEBase.MIMEBase):
    """Class for generating image/* type MIME documents."""

    def __init__(self, _imagedata, _subtype=None,
                 _encoder=Encoders.encode_base64, **_params):
        """Create an image/* type MIME document.

        _imagedata is a string containing the raw image data.  If this data
        can be decoded by the standard Python `imghdr' module, then the
        subtype will be automatically included in the Content-Type: header.
        Otherwise, you can specify the specific image subtype via the _subtype
        parameter.

        _encoder is a function which will perform the actual encoding for
        transport of the image data.  It takes one argument, which is this
        Image instance.  It should use get_payload() and set_payload() to
        change the payload to the encoded form.  It should also add any
        Content-Transfer-Encoding: or other headers to the message as
        necessary.  The default encoding is Base64.

        Any additional keyword arguments are passed to the base class
        constructor, which turns them into parameters on the Content-Type:
        header.
        """
        if _subtype is None:
            _subtype = imghdr.what(None, _imagedata)
        if _subtype is None:
            raise TypeError, 'Could not guess image MIME subtype'
        MIMEBase.MIMEBase.__init__(self, 'image', _subtype, **_params)
        self.set_payload(_imagedata)
        _encoder(self)
