# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

seeds = lines[0].split(": ")[1].split(" ")
seeds = {(int(seeds[i]), int(seeds[i + 1])) for i in range(0, len(seeds), 2)}

maps = ("\n".join(lines[2:])).split("\n\n")
maps_list = []
for item_string in maps:
    item = item_string.split("\n")
    maps_list.append([tuple(int(r) for r in x.split(" ")) for x in item[1:]])

for item in maps_list:
    new_seeds = set()
    for seed, seed_range in seeds:
        for dst, src, count in item:
            if src <= seed < src + count:
                new_seeds.add(
                    (dst + (seed - src), min(seed_range, (src + count) - seed))
                )
            elif seed < src < seed + seed_range:
                new_seeds.add((dst, min(count, seed_range - (src - seed))))
    seeds = new_seeds

print(min(seeds)[0])
