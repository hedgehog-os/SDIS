import pytest
from Post_Machine import PostMachine
from Commands import Mark, Clear, Right, Left, Jump, Stop
from parser import parse

def test_mark_and_clear():
    tape = "000"
    commands = [Mark(1), Clear(2), Stop()]
    machine = PostMachine(tape, commands)
    machine.run()
    assert machine.tape == {0: 0, 1: 0, 2: 0}
    assert machine.stopped

def test_right_and_left():
    tape = "0"
    commands = [Right(1), Mark(2), Left(3), Stop()]
    machine = PostMachine(tape, commands)
    machine.run()
    assert machine.tape == {0: 0, 1: 1}
    assert machine.head == 0

def test_jump_zero_and_one():
    tape = "01"
    commands = [Jump(1, 2), Mark(3), Clear(3), Stop()]
    machine = PostMachine(tape, commands)
    machine.run()
    # head = 0 → tape[0] = 0 → jump to 1 → Mark → tape[0] = 1
    assert machine.tape[0] == 1
    assert machine.stopped

def test_jump_to_clear():
    tape = "0"
    commands = [Jump(1, 2), Clear(3), Mark(4), Stop()]
    machine = PostMachine(tape, commands)
    machine.run()
    assert machine.tape[0] == 0
    assert machine.stopped


def test_parse_commands():
    raw = [
        "? 1; 3",
        "V 2",
        "→ 4",
        "X 5",
        "!",
        "← 4"
    ]
    parsed = parse(raw)
    assert isinstance(parsed[0], Jump)
    assert isinstance(parsed[1], Mark)
    assert isinstance(parsed[2], Right)
    assert isinstance(parsed[3], Clear)
    assert isinstance(parsed[4], Stop)
    assert isinstance(parsed[5], Left)

def test_full_execution():
    tape = "01001"
    program = [
        "? 1; 3",   # tape[0] = 0 → jump to 1
        "V 2",      # tape[0] = 1 → jump to 2
        "→ 4",      # head = 1 → jump to 4
        "X 5",      # tape[0] = 0 → jump to 5
        "!",        # stop
        "← 4"       # head = 0 → jump to 4
    ]
    machine = PostMachine(tape, parse(program))
    machine.run()
    assert machine.stopped
    assert machine.tape[0] == 1
    assert machine.head == 1