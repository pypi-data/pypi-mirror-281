# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="DeleteResult.py">
#   Copyright (c) 2003-2023 Aspose Pty Ltd
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

import pprint
import re  # noqa: F401

import six

class DeleteResult(object):
    """
    Delete result information
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'file_info': 'FileInfo',
        'size': 'int',
        'succeeded': 'list[Signature]',
        'failed': 'list[Signature]'
    }

    attribute_map = {
        'file_info': 'FileInfo',
        'size': 'Size',
        'succeeded': 'Succeeded',
        'failed': 'Failed'
    }

    def __init__(self, file_info=None, size=None, succeeded=None, failed=None, **kwargs):  # noqa: E501
        """Initializes new instance of DeleteResult"""  # noqa: E501

        self._file_info = None
        self._size = None
        self._succeeded = None
        self._failed = None

        if file_info is not None:
            self.file_info = file_info
        if size is not None:
            self.size = size
        if succeeded is not None:
            self.succeeded = succeeded
        if failed is not None:
            self.failed = failed
    
    @property
    def file_info(self):
        """
        Gets the file_info.  # noqa: E501

        Source document file info  # noqa: E501

        :return: The file_info.  # noqa: E501
        :rtype: FileInfo
        """
        return self._file_info

    @file_info.setter
    def file_info(self, file_info):
        """
        Sets the file_info.

        Source document file info  # noqa: E501

        :param file_info: The file_info.  # noqa: E501
        :type: FileInfo
        """
        self._file_info = file_info
    
    @property
    def size(self):
        """
        Gets the size.  # noqa: E501

        Source document size in bytes  # noqa: E501

        :return: The size.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size.

        Source document size in bytes  # noqa: E501

        :param size: The size.  # noqa: E501
        :type: int
        """
        if size is None:
            raise ValueError("Invalid value for `size`, must not be `None`")  # noqa: E501
        self._size = size
    
    @property
    def succeeded(self):
        """
        Gets the succeeded.  # noqa: E501

        List of successfully deleted signatures  # noqa: E501

        :return: The succeeded.  # noqa: E501
        :rtype: list[Signature]
        """
        return self._succeeded

    @succeeded.setter
    def succeeded(self, succeeded):
        """
        Sets the succeeded.

        List of successfully deleted signatures  # noqa: E501

        :param succeeded: The succeeded.  # noqa: E501
        :type: list[Signature]
        """
        self._succeeded = succeeded
    
    @property
    def failed(self):
        """
        Gets the failed.  # noqa: E501

        List of signatures that were not deleted  # noqa: E501

        :return: The failed.  # noqa: E501
        :rtype: list[Signature]
        """
        return self._failed

    @failed.setter
    def failed(self, failed):
        """
        Sets the failed.

        List of signatures that were not deleted  # noqa: E501

        :param failed: The failed.  # noqa: E501
        :type: list[Signature]
        """
        self._failed = failed

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DeleteResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
