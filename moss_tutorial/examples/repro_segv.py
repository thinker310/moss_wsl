import os
from moss import Engine, Verbosity

print("LD_LIBRARY_PATH=", os.environ.get("LD_LIBRARY_PATH"))
print("CUDA_VISIBLE_DEVICES=", os.environ.get("CUDA_VISIBLE_DEVICES"))

e = Engine(
    name="repro",
    map_file="data/map.pb",
    person_file="data/person_routed_sanitized.pb",
    output_dir="output/repro",
    verbose_level=Verbosity.NO_OUTPUT,   # 先关掉噪声
    device=0,
)

print("init ok. road:", e.road_count, "lane:", e.lane_count, "junc:", e.junction_count, "person:", e.person_count)

# 只跑 1 步
e.next_step()
print("step ok")
