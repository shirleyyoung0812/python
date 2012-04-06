#!/usr/bin/env python3

import unittest
from test import support

import contextlib
import socket
import urllib.request
import sys
import os
import email.message
import time


class URLTimeoutTest(unittest.TestCase):
    # XXX this test doesn't seem to test anything useful.

    TIMEOUT = 30.0

    def setUp(self):
        socket.setdefaulttimeout(self.TIMEOUT)

    def tearDown(self):
        socket.setdefaulttimeout(None)

    def testURLread(self):
        with support.transient_internet("www.python.org"):
            f = urllib.request.urlopen("http://www.python.org/")
            x = f.read()


class urlopenNetworkTests(unittest.TestCase):
    """Tests urllib.reqest.urlopen using the network.

    These tests are not exhaustive.  Assuming that testing using files does a
    good job overall of some of the basic interface features.  There are no
    tests exercising the optional 'data' and 'proxies' arguments.  No tests
    for transparent redirection have been written.

    setUp is not used for always constructing a connection to
    http://www.python.org/ since there a few tests that don't use that address
    and making a connection is expensive enough to warrant minimizing unneeded
    connections.

    """

    @contextlib.contextmanager
    def urlopen(self, *args, **kwargs):
        resource = args[0]
        with support.transient_internet(resource):
            r = urllib.request.urlopen(*args, **kwargs)
            try:
                yield r
            finally:
                r.close()

    def test_basic(self):
        # Simple test expected to pass.
        with self.urlopen("http://www.python.org/") as open_url:
            for attr in ("read", "readline", "readlines", "fileno", "close",
                         "info", "geturl"):
                self.assertTrue(hasattr(open_url, attr), "object returned from "
                                "urlopen lacks the %s attribute" % attr)
            self.assertTrue(open_url.read(), "calling 'read' failed")

    def test_readlines(self):
        # Test both readline and readlines.
        with self.urlopen("http://www.python.org/") as open_url:
            self.assertIsInstance(open_url.readline(), bytes,
                                  "readline did not return a string")
            self.assertIsInstance(open_url.readlines(), list,
                                  "readlines did not return a list")

    def test_info(self):
        # Test 'info'.
        with self.urlopen("http://www.python.org/") as open_url:
            info_obj = open_url.info()
            self.assertIsInstance(info_obj, email.message.Message,
                                  "object returned by 'info' is not an "
                                  "instance of email.message.Message")
            self.assertEqual(info_obj.get_content_subtype(), "html")

    def test_geturl(self):
        # Make sure same URL as opened is returned by geturl.
        URL = "http://www.python.org/"
        with self.urlopen(URL) as open_url:
            gotten_url = open_url.geturl()
            self.assertEqual(gotten_url, URL)

    def test_getcode(self):
        # test getcode() with the fancy opener to get 404 error codes
        URL = "http://www.python.org/XXXinvalidXXX"
        with support.transient_internet(URL):
            open_url = urllib.request.FancyURLopener().open(URL)
            try:
                code = open_url.getcode()
            finally:
                open_url.close()
            self.assertEqual(code, 404)

    def test_fileno(self):
        if sys.platform in ('win32',):
            # On Windows, socket handles are not file descriptors; this
            # test can't pass on Windows.
            return
        # Make sure fd returned by fileno is valid.
        with self.urlopen("http://www.python.org/", timeout=None) as open_url:
            fd = open_url.fileno()
            with os.fdopen(fd, encoding='utf-8') as f:
                self.assertTrue(f.read(), "reading from file created using fd "
                                          "returned by fileno failed")

    def test_bad_address(self):
        # Make sure proper exception is raised when connecting to a bogus
        # address.
        bogus_domain = "sadflkjsasf.i.nvali.d"
        try:
            socket.gethostbyname(bogus_domain)
        except socket.gaierror:
            pass
        else:
            # This happens with some overzealous DNS providers such as OpenDNS
            self.skipTest("%r should not resolve for test to work" % bogus_domain)
        self.assertRaises(IOError,
                          # SF patch 809915:  In Sep 2003, VeriSign started
                          # highjacking invalid .com and .net addresses to
                          # boost traffic to their own site.  This test
                          # started failing then.  One hopes the .invalid
                          # domain will be spared to serve its defined
                          # purpose.
                          # urllib.urlopen, "http://www.sadflkjsasadf.com/")
                          urllib.request.urlopen,
                          "http://sadflkjsasf.i.nvali.d/")


class urlretrieveNetworkTests(unittest.TestCase):
    """Tests urllib.request.urlretrieve using the network."""

    @contextlib.contextmanager
    def urlretrieve(self, *args):
        resource = args[0]
        with support.transient_internet(resource):
            file_location, info = urllib.request.urlretrieve(*args)
            try:
                yield file_location, info
            finally:
                support.unlink(file_location)

    def test_basic(self):
        # Test basic functionality.
        with self.urlretrieve("http://www.python.org/") as (file_location, info):
            self.assertTrue(os.path.exists(file_location), "file location returned by"
                            " urlretrieve is not a valid path")
            with open(file_location, encoding='utf-8') as f:
                self.assertTrue(f.read(), "reading from the file location returned"
                                " by urlretrieve failed")

    def test_specified_path(self):
        # Make sure that specifying the location of the file to write to works.
        with self.urlretrieve("http://www.python.org/",
                              support.TESTFN) as (file_location, info):
            self.assertEqual(file_location, support.TESTFN)
            self.assertTrue(os.path.exists(file_location))
            with open(file_location, encoding='utf-8') as f:
                self.assertTrue(f.read(), "reading from temporary file failed")

    def test_header(self):
        # Make sure header returned as 2nd value from urlretrieve is good.
        with self.urlretrieve("http://www.python.org/") as (file_location, info):
            self.assertIsInstance(info, email.message.Message,
                                  "info is not an instance of email.message.Message")

    def test_data_header(self):
        logo = "http://www.python.org/community/logos/python-logo-master-v3-TM.png"
        with self.urlretrieve(logo) as (file_location, fileheaders):
            datevalue = fileheaders.get('Date')
            dateformat = '%a, %d %b %Y %H:%M:%S GMT'
            try:
                time.strptime(datevalue, dateformat)
            except ValueError:
                self.fail('Date value not in %r format', dateformat)


def test_main():
    support.requires('network')
    support.run_unittest(URLTimeoutTest,
                         urlopenNetworkTests,
                         urlretrieveNetworkTests)

if __name__ == "__main__":
    test_main()
