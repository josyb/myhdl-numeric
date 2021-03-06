from __future__ import absolute_import
from myhdl import enum, intbv, always_comb, Signal, instance, delay, \
    instances, StopSimulation, conversion

bitwise_op = enum('BW_AND', 'BW_ANDN', 'BW_OR', 'BW_XOR')


def bitwise(a, b, op):
    r = intbv(0)[8:]
    if op == bitwise_op.BW_AND:
        r[:] = a & b
    elif op == bitwise_op.BW_ANDN:
        r[:] = (~a) & b
    elif op == bitwise_op.BW_OR:
        r[:] = a | b
    elif op == bitwise_op.BW_XOR:
        r[:] = a ^ b
    return r


def LogicUnit(a, b, c, op):
    @always_comb
    def operate():
        c.next = bitwise(a, b, op)
    return operate


def bench_enum():
    clock = Signal(False)
    a, b, c = [Signal(intbv(0)[8:]) for _ in range(3)]
    op = Signal(bitwise_op.BW_AND)
    logic_unit = LogicUnit(a=a, b=b, c=c, op=op)

    @instance
    def clockgen():
        clock.next = 1
        while 1:
            yield delay(10)
            clock.next = not clock

    @instance
    def stimulus():
        a.next = 0xaa
        b.next = 0x55
        yield clock.posedge
        print('a=%s b=%s' % (int(a), int(b)))

        op.next = bitwise_op.BW_AND
        yield clock.posedge
        print(int(c))

        op.next = bitwise_op.BW_ANDN
        yield clock.posedge
        print(int(c))

        op.next = bitwise_op.BW_OR
        yield clock.posedge
        print(int(c))

        op.next = bitwise_op.BW_XOR
        yield clock.posedge
        print(int(c))

        raise StopSimulation

    return instances()


def test_enum():
    assert conversion.verify(bench_enum) == 0
