from moss import Engine, Verbosity

print("初始化 MOSS 引擎...")
e = Engine(
    name="my_first_simulation",
    map_file="data/map.pb",
    person_file="data/person_routed_sanitized.pb",
    start_step=0,
    step_interval=1,
    output_dir="output",
    verbose_level=Verbosity.ALL,
    device=0,                               # 显式指定 CUDA 设备号
)
def _call_first(engine, candidates):
    """
    Try call engine.<name>() for the first existing callable in candidates.
    Return None if none exists.
    """
    for name in candidates:
        fn = getattr(engine, name, None)
        if callable(fn):
            return fn()
    return None

def print_map_stats(engine):
    # 尝试常见命名：count / size / ids
    road_count = _call_first(engine, ["get_road_count", "road_count", "roads_count", "num_roads"])
    junc_count = _call_first(engine, ["get_junction_count", "junction_count", "junctions_count", "num_junctions"])
    lane_count = _call_first(engine, ["get_lane_count", "lane_count", "lanes_count", "num_lanes"])

    # 如果没有 count 方法，用 ids 列表长度兜底
    if road_count is None:
        road_ids = _call_first(engine, ["get_road_ids"])
        road_count = len(road_ids) if road_ids is not None else None

    if junc_count is None:
        junc_ids = _call_first(engine, ["get_junction_ids"])
        junc_count = len(junc_ids) if junc_ids is not None else None

    if lane_count is None:
        # 你日志里有 fetch_lanes，通常会返回 lanes 或 lane ids
        lanes = _call_first(engine, ["fetch_lanes", "get_lanes"])
        lane_count = len(lanes) if lanes is not None else None

    print("地图信息:")
    print(f"  道路数: {road_count}")
    print(f"  路口数: {junc_count}")
    print(f"  车道数: {lane_count}")
print_map_stats(e)
print("\nEngine public methods:")
print([n for n in dir(e) if not n.startswith("_")])
print("\n开始仿真（模拟1小时）...")
for step in range(3600):
    e.next_step(1)
    if step % 600 == 0:  # 每10分钟打印一次
        print(f"  步骤 {step}:  仿真时间 {step//60} 分钟")

print("\n✅ 仿真完成！")
print("输出文件保存在 output/ 目录")
