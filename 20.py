# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import deque
import math


input_value = open("input.txt", "r").read()
lines = input_value.split("\n")


class Conjunction:
    def __init__(self, name, registry, outputs):
        self.name = name
        self.registry = registry
        self.outputs = outputs
        self.state = {}
        self.counter_low = 0
        self.counter_high = 0

    def pulse(self, source, type):
        if type == "low":
            self.counter_low += 1
        else:
            self.counter_high += 1
        self.state[source] = type
        output_type = "low"
        for source in self.state:
            if self.state[source] == "low":
                output_type = "high"
                break
        specs = []
        for output in self.outputs:
            if output not in self.registry:
                module = self.registry[output] = Untyped(output, self.registry, [])
            else:
                module = self.registry[output]
            specs.append((module, self.name, output_type))
        return specs


class FlipFlop:
    def __init__(self, name, registry, outputs):
        self.name = name
        self.registry = registry
        self.outputs = outputs
        self.state = "off"
        self.counter_low = 0
        self.counter_high = 0

    def pulse(self, _, type):
        if type == "low":
            self.counter_low += 1
        else:
            self.counter_high += 1
        if type == "high":
            return []
        output_type = "high" if self.state == "off" else "low"
        self.state = "on" if self.state == "off" else "off"
        specs = []
        for output in self.outputs:
            if output not in self.registry:
                module = self.registry[output] = Untyped(output, self.registry, [])
            else:
                module = self.registry[output]
            specs.append((module, self.name, output_type))
        return specs


class Broadcaster:
    def __init__(self, name, registry, outputs):
        self.name = name
        self.registry = registry
        self.outputs = outputs
        self.state = None
        self.counter_low = 0
        self.counter_high = 0

    def pulse(self, _, type):
        if type == "low":
            self.counter_low += 1
        else:
            self.counter_high += 1
        output_type = type
        specs = []
        for output in self.outputs:
            if output not in self.registry:
                module = self.registry[output] = Untyped(output, self.registry, [])
            else:
                module = self.registry[output]
            specs.append((module, self.name, output_type))
        return specs


class Untyped:
    def __init__(self, name, registry, outputs):
        self.name = name
        self.registry = registry
        self.outputs = outputs
        self.state = None
        self.counter_low = 0
        self.counter_high = 0

    def pulse(self, _, type):
        if self.name == "rx" and type == "low":
            print(type)
        if type == "low":
            self.counter_low += 1
        else:
            self.counter_high += 1
        return []


registry = {}
for line in lines:
    [source, destinations] = line.split(" -> ")
    destinations = destinations.split(", ")
    if source == "broadcaster":
        registry["broadcaster"] = Broadcaster("broadcaster", registry, destinations)
        continue

    source_type = source[0]
    name = source[1:]
    if source_type == "%":
        registry[name] = FlipFlop(name, registry, destinations)
    else:  # Type is conjunction.
        registry[name] = Conjunction(name, registry, destinations)


# Initialize Conjunction state to low for all inputs.
for module in registry.values():
    for output in module.outputs:
        if output in registry and isinstance(registry[output], Conjunction):
            registry[output].state[module.name] = "low"


def push_button():
    queue = deque()
    queue.append((registry["broadcaster"], "button", "low"))
    got_desired = False
    while queue:
        (module, source, pulse_type) = queue.popleft()
        if module.name == "hf" and pulse_type == "low":
            got_desired = True
        for new_spec in module.pulse(source, pulse_type):
            queue.append(new_spec)
    return got_desired


# for _ in range(1000):
#     push_button()

# print(
#     sum(module.counter_low for module in registry.values())
#     * sum(module.counter_high for module in registry.values())
# )

# i = 0
# while True:
#     i += 1
#     if push_button():
#         print(i)
#         input()

# Analysis
# - low to rx
# - all high to vf
# - any low to pm + any low to mk + any low to pk + any low to hf
print(math.lcm(3881, 3889, 4021, 4013))
