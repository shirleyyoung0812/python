# -*- coding: utf-8 -*-

"""
Test suite for PEP 380 implementation

adapted from original tests written by Greg Ewing
see <http://www.cosc.canterbury.ac.nz/greg.ewing/python/yield-from/YieldFrom-Python3.1.2-rev5.zip>
"""

import unittest
import io
import sys
import inspect
import parser

from test.support import captured_stderr

class TestPEP380Operation(unittest.TestCase):
    """
    Test semantics.
    """

    def test_delegation_of_initial_next_to_subgenerator(self):
        """
        Test delegation of initial next() call to subgenerator
        """
        trace = []
        def g1():
            trace.append("Starting g1")
            yield from g2()
            trace.append("Finishing g1")
        def g2():
            trace.append("Starting g2")
            yield 42
            trace.append("Finishing g2")
        for x in g1():
            trace.append("Yielded %s" % (x,))
        self.assertEqual(trace,[
            "Starting g1",
            "Starting g2",
            "Yielded 42",
            "Finishing g2",
            "Finishing g1",
        ])

    def test_raising_exception_in_initial_next_call(self):
        """
        Test raising exception in initial next() call
        """
        trace = []
        def g1():
            try:
                trace.append("Starting g1")
                yield from g2()
            finally:
                trace.append("Finishing g1")
        def g2():
            try:
                trace.append("Starting g2")
                raise ValueError("spanish inquisition occurred")
            finally:
                trace.append("Finishing g2")
        try:
            for x in g1():
                trace.append("Yielded %s" % (x,))
        except ValueError as e:
            self.assertEqual(e.args[0], "spanish inquisition occurred")
        else:
            self.fail("subgenerator failed to raise ValueError")
        self.assertEqual(trace,[
            "Starting g1",
            "Starting g2",
            "Finishing g2",
            "Finishing g1",
        ])

    def test_delegation_of_next_call_to_subgenerator(self):
        """
        Test delegation of next() call to subgenerator
        """
        trace = []
        def g1():
            trace.append("Starting g1")
            yield "g1 ham"
            yield from g2()
            yield "g1 eggs"
            trace.append("Finishing g1")
        def g2():
            trace.append("Starting g2")
            yield "g2 spam"
            yield "g2 more spam"
            trace.append("Finishing g2")
        for x in g1():
            trace.append("Yielded %s" % (x,))
        self.assertEqual(trace,[
            "Starting g1",
            "Yielded g1 ham",
            "Starting g2",
            "Yielded g2 spam",
            "Yielded g2 more spam",
            "Finishing g2",
            "Yielded g1 eggs",
            "Finishing g1",
        ])

    def test_raising_exception_in_delegated_next_call(self):
        """
        Test raising exception in delegated next() call
        """
        trace = []
        def g1():
            try:
                trace.append("Starting g1")
                yield "g1 ham"
                yield from g2()
                yield "g1 eggs"
            finally:
                trace.append("Finishing g1")
        def g2():
            try:
                trace.append("Starting g2")
                yield "g2 spam"
                raise ValueError("hovercraft is full of eels")
                yield "g2 more spam"
            finally:
                trace.append("Finishing g2")
        try:
            for x in g1():
                trace.append("Yielded %s" % (x,))
        except ValueError as e:
            self.assertEqual(e.args[0], "hovercraft is full of eels")
        else:
            self.fail("subgenerator failed to raise ValueError")
        self.assertEqual(trace,[
            "Starting g1",
            "Yielded g1 ham",
            "Starting g2",
            "Yielded g2 spam",
            "Finishing g2",
            "Finishing g1",
        ])

    def test_delegation_of_send(self):
        """
        Test delegation of send()
        """
        trace = []
        def g1():
            trace.append("Starting g1")
            x = yield "g1 ham"
            trace.append("g1 received %s" % (x,))
            yield from g2()
            x = yield "g1 eggs"
            trace.append("g1 received %s" % (x,))
            trace.append("Finishing g1")
        def g2():
            trace.append("Starting g2")
            x = yield "g2 spam"
            trace.append("g2 received %s" % (x,))
            x = yield "g2 more spam"
            trace.append("g2 received %s" % (x,))
            trace.append("Finishing g2")
        g = g1()
        y = next(g)
        x = 1
        try:
            while 1:
                y = g.send(x)
                trace.append("Yielded %s" % (y,))
                x += 1
        except StopIteration:
            pass
        self.assertEqual(trace,[
            "Starting g1",
            "g1 received 1",
            "Starting g2",
            "Yielded g2 spam",
            "g2 received 2",
            "Yielded g2 more spam",
            "g2 received 3",
            "Finishing g2",
            "Yielded g1 eggs",
            "g1 received 4",
            "Finishing g1",
        ])

    def test_handling_exception_while_delegating_send(self):
        """
        Test handling exception while delegating 'send'
        """
        trace = []
        def g1():
            trace.append("Starting g1")
            x = yield "g1 ham"
            trace.append("g1 received %s" % (x,))
            yield from g2()
            x = yield "g1 eggs"
            trace.append("g1 received %s" % (x,))
            trace.append("Finishing g1")
        def g2():
            trace.append("Starting g2")
            x = yield "g2 spam"
            trace.append("g2 received %s" % (x,))
            raise ValueError("hovercraft is full of eels")
            x = yield "g2 more spam"
            trace.append("g2 received %s" % (x,))
            trace.append("Finishing g2")
        def run():
            g = g1()
            y = next(g)
            x = 1
            try:
                while 1:
                    y = g.send(x)
                    trace.append("Yielded %s" % (y,))
                    x += 1
            except StopIteration:
                trace.append("StopIteration")
        self.assertRaises(ValueError,run)
        self.assertEqual(trace,[
            "Starting g1",
            "g1 received 1",
            "Starting g2",
            "Yielded g2 spam",
            "g2 received 2",
        ])

    def test_delegating_close(self):
        """
        Test delegating 'close'
        """
        trace = []
        def g1():
            try:
                trace.append("Starting g1")
                yield "g1 ham"
                yield from g2()
                yield "g1 eggs"
            finally:
                trace.append("Finishing g1")
        def g2():
            try:
                trace.append("Starting g2")
                yield "g2 spam"
                yield "g2 more spam"
            finally:
                trace.append("Finishing g2")
        g = g1()
        for i in range(2):
            x = next(g)
            trace.append("Yielded %s" % (x,))
        g.close()
        self.assertEqual(trace,[
            "Starting g1",
            "Yielded g1 ham",
            "Starting g2",
            "Yielded g2 spam",
            "Finishing g2",
            "Finishing g1"
        ])

    def test_handing_exception_while_delegating_close(self):
        """
        Test handling exception while delegating 'close'
        """
        trace = []
        def g1():
            try:
                trace.append("Starting g1")
                yield "g1 ham"
                yield from g2()
                yield "g1 eggs"
            finally:
                trace.append("Finishing g1")
        def g2():
            try:
                trace.append("Starting g2")
                yield "g2 spam"
                yield "g2 more spam"
            finally:
                trace.append("Finishing g2")
                raise ValueError("nybbles have exploded with delight")
        try:
            g = g1()
            for i in range(2):
                x = next(g)
                trace.append("Yielded %s" % (x,))
            g.close()
        except ValueError as e:
            self.assertEqual(e.args[0], "nybbles have exploded with delight")
            self.assertIsInstance(e.__context__, GeneratorExit)
        else:
            self.fail("subgenerator failed to raise ValueError")
        self.assertEqual(trace,[
            "Starting g1",
            "Yielded g1 ham",
            "Starting g2",
            "Yielded g2 spam",
            "Finishing g2",
            "Finishing g1",
        ])

    def test_delegating_throw(self):
        """
        Test delegating 'throw'
        """
        trace = []
        def g1():
            try:
                trace.append("Starting g1")
                yield "g1 ham"
                yield from g2()
                yield "g1 eggs"
            finally:
                trace.append("Finishing g1")
        def g2():
            try:
                trace.append("Starting g2")
                yield "g2 spam"
                yield "g2 more spam"
            finally:
                trace.append("Finishing g2")
        try:
            g = g1()
            for i in range(2):
                x = next(g)
                trace.append("Yielded %s" % (x,))
            e = ValueError("tomato ejected")
            g.throw(e)
        except ValueError as e:
            self.assertEqual(e.args[0], "tomato ejected")
        else:
            self.fail("subgenerator failed to raise ValueError")
        self.assertEqual(trace,[
            "Starting g1",
            "Yielded g1 ham",
            "Starting g2",
            "Yielded g2 spam",
            "Finishing g2",
            "Finishing g1",
        ])

    def test_value_attribute_of_StopIteration_exception(self):
        """
        Test 'value' attribute of StopIteration exception
        """
        trace = []
        def pex(e):
            trace.append("%s: %s" % (e.__class__.__name__, e))
            trace.append("value = %s" % (e.value,))
        e = StopIteration()
        pex(e)
        e = StopIteration("spam")
        pex(e)
        e.value = "eggs"
        pex(e)
        self.assertEqual(trace,[
            "StopIteration: ",
            "value = None",
            "StopIteration: spam",
            "value = spam",
            "StopIteration: spam",
            "value = eggs",
        ])


    def test_exception_value_crash(self):
        # There used to be a refcount error when the return value
        # stored in the StopIteration has a refcount of 1.
        def g1():
            yield from g2()
        def g2():
            yield "g2"
            return [42]
        self.assertEqual(list(g1()), ["g2"])


    def test_generator_return_value(self):
        """
        Test generator return value
        """
        trace = []
        def g1():
            trace.append("Starting g1")
            yield "g1 ham"
            ret = yield from g2()
            trace.append("g2 returned %s" % (ret,))
            ret = yield from g2(42)
            trace.append("g2 returned %s" % (ret,))
            yield "g1 eggs"
            trace.append("Finishing g1")
        def g2(v = None):
            trace.append("Starting g2")
            yield "g2 spam"
            yield "g2 more spam"
            trace.append("Finishing g2")
            if v:
                return v
        for x in g1():
            trace.append("Yielded %s" % (x,))
        self.assertEqual(trace,[
            "Starting g1",
            "Yielded g1 ham",
            "Starting g2",
            "Yielded g2 spam",
            "Yielded g2 more spam",
            "Finishing g2",
            "g2 returned None",
            "Starting g2",
            "Yielded g2 spam",
            "Yielded g2 more spam",
            "Finishing g2",
            "g2 returned 42",
            "Yielded g1 eggs",
            "Finishing g1",
        ])

    def test_delegation_of_next_to_non_generator(self):
        """
        Test delegation of next() to non-generator
        """
        trace = []
        def g():
            yield from range(3)
        for x in g():
            trace.append("Yielded %s" % (x,))
        self.assertEqual(trace,[
            "Yielded 0",
            "Yielded 1",
            "Yielded 2",
        ])


    def test_conversion_of_sendNone_to_next(self):
        """
        Test conversion of send(None) to next()
        """
        trace = []
        def g():
            yield from range(3)
        gi = g()
        for x in range(3):
            y = gi.send(None)
            trace.append("Yielded: %s" % (y,))
        self.assertEqual(trace,[
            "Yielded: 0",
            "Yielded: 1",
            "Yielded: 2",
        ])

    def test_delegation_of_close_to_non_generator(self):
        """
        Test delegation of close() to non-generator
        """
        trace = []
        def g():
            try:
                trace.append("starting g")
                yield from range(3)
                trace.append("g should not be here")
            finally:
                trace.append("finishing g")
        gi = g()
        next(gi)
        with captured_stderr() as output:
            gi.close()
        self.assertEqual(output.getvalue(), '')
        self.assertEqual(trace,[
            "starting g",
            "finishing g",
        ])

    def test_delegating_throw_to_non_generator(self):
        """
        Test delegating 'throw' to non-generator
        """
        trace = []
        def g():
            try:
                trace.append("Starting g")
                yield from range(10)
            finally:
                trace.append("Finishing g")
        try:
            gi = g()
            for i in range(5):
                x = next(gi)
                trace.append("Yielded %s" % (x,))
            e = ValueError("tomato ejected")
            gi.throw(e)
        except ValueError as e:
            self.assertEqual(e.args[0],"tomato ejected")
        else:
            self.fail("subgenerator failed to raise ValueError")
        self.assertEqual(trace,[
            "Starting g",
            "Yielded 0",
            "Yielded 1",
            "Yielded 2",
            "Yielded 3",
            "Yielded 4",
            "Finishing g",
        ])

    def test_attempting_to_send_to_non_generator(self):
        """
        Test attempting to send to non-generator
        """
        trace = []
        def g():
            try:
                trace.append("starting g")
                yield from range(3)
                trace.append("g should not be here")
            finally:
                trace.append("finishing g")
        try:
            gi = g()
            next(gi)
            for x in range(3):
                y = gi.send(42)
                trace.append("Should not have yielded:", y)
        except AttributeError as e:
            self.assertIn("send", e.args[0])
        else:
            self.fail("was able to send into non-generator")
        self.assertEqual(trace,[
            "starting g",
            "finishing g",
        ])

    def test_broken_getattr_handling(self):
        """
        Test subiterator with a broken getattr implementation
        """
        class Broken:
            def __iter__(self):
                return self
            def __next__(self):
                return 1
            def __getattr__(self, attr):
                1/0

        def g():
            yield from Broken()

        with self.assertRaises(ZeroDivisionError):
            gi = g()
            self.assertEqual(next(gi), 1)
            gi.send(1)

        with self.assertRaises(ZeroDivisionError):
            gi = g()
            self.assertEqual(next(gi), 1)
            gi.throw(AttributeError)

        with captured_stderr() as output:
            gi = g()
            self.assertEqual(next(gi), 1)
            gi.close()
        self.assertIn('ZeroDivisionError', output.getvalue())

    def test_exception_in_initial_next_call(self):
        """
        Test exception in initial next() call
        """
        trace = []
        def g1():
            trace.append("g1 about to yield from g2")
            yield from g2()
            trace.append("g1 should not be here")
        def g2():
            yield 1/0
        def run():
            gi = g1()
            next(gi)
        self.assertRaises(ZeroDivisionError,run)
        self.assertEqual(trace,[
            "g1 about to yield from g2"
        ])

    def test_attempted_yield_from_loop(self):
        """
        Test attempted yield-from loop
        """
        trace = []
        def g1():
            trace.append("g1: starting")
            yield "y1"
            trace.append("g1: about to yield from g2")
            yield from g2()
            trace.append("g1 should not be here")

        def g2():
            trace.append("g2: starting")
            yield "y2"
            trace.append("g2: about to yield from g1")
            yield from gi
            trace.append("g2 should not be here")
        try:
            gi = g1()
            for y in gi:
                trace.append("Yielded: %s" % (y,))
        except ValueError as e:
            self.assertEqual(e.args[0],"generator already executing")
        else:
            self.fail("subgenerator didn't raise ValueError")
        self.assertEqual(trace,[
            "g1: starting",
            "Yielded: y1",
            "g1: about to yield from g2",
            "g2: starting",
            "Yielded: y2",
            "g2: about to yield from g1",
        ])

    def test_returning_value_from_delegated_throw(self):
        """
        Test returning value from delegated 'throw'
        """
        trace = []
        def g1():
            try:
                trace.append("Starting g1")
                yield "g1 ham"
                yield from g2()
                yield "g1 eggs"
            finally:
                trace.append("Finishing g1")
        def g2():
            try:
                trace.append("Starting g2")
                yield "g2 spam"
                yield "g2 more spam"
            except LunchError:
                trace.append("Caught LunchError in g2")
                yield "g2 lunch saved"
                yield "g2 yet more spam"
        class LunchError(Exception):
            pass
        g = g1()
        for i in range(2):
            x = next(g)
            trace.append("Yielded %s" % (x,))
        e = LunchError("tomato ejected")
        g.throw(e)
        for x in g:
            trace.append("Yielded %s" % (x,))
        self.assertEqual(trace,[
            "Starting g1",
            "Yielded g1 ham",
            "Starting g2",
            "Yielded g2 spam",
            "Caught LunchError in g2",
            "Yielded g2 yet more spam",
            "Yielded g1 eggs",
            "Finishing g1",
        ])

    def test_next_and_return_with_value(self):
        """
        Test next and return with value
        """
        trace = []
        def f(r):
            gi = g(r)
            next(gi)
            try:
                trace.append("f resuming g")
                next(gi)
                trace.append("f SHOULD NOT BE HERE")
            except StopIteration as e:
                trace.append("f caught %s" % (repr(e),))
        def g(r):
            trace.append("g starting")
            yield
            trace.append("g returning %s" % (r,))
            return r
        f(None)
        f(42)
        self.assertEqual(trace,[
            "g starting",
            "f resuming g",
            "g returning None",
            "f caught StopIteration()",
            "g starting",
            "f resuming g",
            "g returning 42",
            "f caught StopIteration(42,)",
        ])

    def test_send_and_return_with_value(self):
        """
        Test send and return with value
        """
        trace = []
        def f(r):
            gi = g(r)
            next(gi)
            try:
                trace.append("f sending spam to g")
                gi.send("spam")
                trace.append("f SHOULD NOT BE HERE")
            except StopIteration as e:
                trace.append("f caught %r" % (e,))
        def g(r):
            trace.append("g starting")
            x = yield
            trace.append("g received %s" % (x,))
            trace.append("g returning %s" % (r,))
            return r
        f(None)
        f(42)
        self.assertEqual(trace,[
            "g starting",
            "f sending spam to g",
            "g received spam",
            "g returning None",
            "f caught StopIteration()",
            "g starting",
            "f sending spam to g",
            "g received spam",
            "g returning 42",
            "f caught StopIteration(42,)",
        ])

    def test_catching_exception_from_subgen_and_returning(self):
        """
        Test catching an exception thrown into a
        subgenerator and returning a value
        """
        trace = []
        def inner():
            try:
                yield 1
            except ValueError:
                trace.append("inner caught ValueError")
            return 2

        def outer():
            v = yield from inner()
            trace.append("inner returned %r to outer" % v)
            yield v
        g = outer()
        trace.append(next(g))
        trace.append(g.throw(ValueError))
        self.assertEqual(trace,[
            1,
            "inner caught ValueError",
            "inner returned 2 to outer",
            2,
        ])

    def test_throwing_GeneratorExit_into_subgen_that_returns(self):
        """
        Test throwing GeneratorExit into a subgenerator that
        catches it and returns normally.
        """
        trace = []
        def f():
            try:
                trace.append("Enter f")
                yield
                trace.append("Exit f")
            except GeneratorExit:
                return
        def g():
            trace.append("Enter g")
            yield from f()
            trace.append("Exit g")
        try:
            gi = g()
            next(gi)
            gi.throw(GeneratorExit)
        except GeneratorExit:
            pass
        else:
            self.fail("subgenerator failed to raise GeneratorExit")
        self.assertEqual(trace,[
            "Enter g",
            "Enter f",
        ])

    def test_throwing_GeneratorExit_into_subgenerator_that_yields(self):
        """
        Test throwing GeneratorExit into a subgenerator that
        catches it and yields.
        """
        trace = []
        def f():
            try:
                trace.append("Enter f")
                yield
                trace.append("Exit f")
            except GeneratorExit:
                yield
        def g():
            trace.append("Enter g")
            yield from f()
            trace.append("Exit g")
        try:
            gi = g()
            next(gi)
            gi.throw(GeneratorExit)
        except RuntimeError as e:
            self.assertEqual(e.args[0], "generator ignored GeneratorExit")
        else:
            self.fail("subgenerator failed to raise GeneratorExit")
        self.assertEqual(trace,[
            "Enter g",
            "Enter f",
        ])

    def test_throwing_GeneratorExit_into_subgen_that_raises(self):
        """
        Test throwing GeneratorExit into a subgenerator that
        catches it and raises a different exception.
        """
        trace = []
        def f():
            try:
                trace.append("Enter f")
                yield
                trace.append("Exit f")
            except GeneratorExit:
                raise ValueError("Vorpal bunny encountered")
        def g():
            trace.append("Enter g")
            yield from f()
            trace.append("Exit g")
        try:
            gi = g()
            next(gi)
            gi.throw(GeneratorExit)
        except ValueError as e:
            self.assertEqual(e.args[0], "Vorpal bunny encountered")
            self.assertIsInstance(e.__context__, GeneratorExit)
        else:
            self.fail("subgenerator failed to raise ValueError")
        self.assertEqual(trace,[
            "Enter g",
            "Enter f",
        ])

    def test_yield_from_empty(self):
        def g():
            yield from ()
        self.assertRaises(StopIteration, next, g())

    def test_delegating_generators_claim_to_be_running(self):
        # Check with basic iteration
        def one():
            yield 0
            yield from two()
            yield 3
        def two():
            yield 1
            try:
                yield from g1
            except ValueError:
                pass
            yield 2
        g1 = one()
        self.assertEqual(list(g1), [0, 1, 2, 3])
        # Check with send
        g1 = one()
        res = [next(g1)]
        try:
            while True:
                res.append(g1.send(42))
        except StopIteration:
            pass
        self.assertEqual(res, [0, 1, 2, 3])
        # Check with throw
        class MyErr(Exception):
            pass
        def one():
            try:
                yield 0
            except MyErr:
                pass
            yield from two()
            try:
                yield 3
            except MyErr:
                pass
        def two():
            try:
                yield 1
            except MyErr:
                pass
            try:
                yield from g1
            except ValueError:
                pass
            try:
                yield 2
            except MyErr:
                pass
        g1 = one()
        res = [next(g1)]
        try:
            while True:
                res.append(g1.throw(MyErr))
        except StopIteration:
            pass
        # Check with close
        class MyIt(object):
            def __iter__(self):
                return self
            def __next__(self):
                return 42
            def close(self_):
                self.assertTrue(g1.gi_running)
                self.assertRaises(ValueError, next, g1)
        def one():
            yield from MyIt()
        g1 = one()
        next(g1)
        g1.close()

    def test_delegator_is_visible_to_debugger(self):
        def call_stack():
            return [f[3] for f in inspect.stack()]

        def gen():
            yield call_stack()
            yield call_stack()
            yield call_stack()

        def spam(g):
            yield from g

        def eggs(g):
            yield from g

        for stack in spam(gen()):
            self.assertTrue('spam' in stack)

        for stack in spam(eggs(gen())):
            self.assertTrue('spam' in stack and 'eggs' in stack)

    def test_custom_iterator_return(self):
        # See issue #15568
        class MyIter:
            def __iter__(self):
                return self
            def __next__(self):
                raise StopIteration(42)
        def gen():
            nonlocal ret
            ret = yield from MyIter()
        ret = None
        list(gen())
        self.assertEqual(ret, 42)


def test_main():
    from test import support
    test_classes = [TestPEP380Operation]
    support.run_unittest(*test_classes)


if __name__ == '__main__':
    test_main()
