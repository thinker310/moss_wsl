import random
from mosstool.type import Map, Persons, Person, Schedule, Trip, Position, LanePosition

# 加载地图
print("加载地图...")
with open("data/map.pb", "rb") as f:
    m = Map()
    m.ParseFromString(f.read())

print(f"地图信息: {len(m.roads)} 条道路, {len(m.lanes)} 条车道")

# 收集 road lane ids（只拿“道路上的车道”，排除 junction/connector lanes）
road_lane_ids = set()
for r in m.roads:
    if hasattr(r, "lane_ids") and len(r.lane_ids) > 0:
        road_lane_ids.update(list(r.lane_ids))
    elif hasattr(r, "lanes") and len(r.lanes) > 0:
        for l in r.lanes:
            road_lane_ids.add(l.id if hasattr(l, "id") else l)

# 在 road lanes 中再筛选“可驾驶”
drivable_lanes = [
    lane.id
    for lane in m.lanes
    if (lane.id in road_lane_ids) and (lane.type == 1)  # LANE_TYPE_DRIVING = 1
]

print(f"road lanes: {len(road_lane_ids)} 条；可驾驶 road lanes: {len(drivable_lanes)} 条")
if not drivable_lanes:
    raise SystemExit("❌ 没有找到可驾驶的 road lane（routing 需要 road lane）")

# 生成人员
persons = []
num_persons = 100
print(f"生成 {num_persons} 个人员...")

for i in range(num_persons):
    start_lane = random.choice(drivable_lanes)
    end_lane = random.choice(drivable_lanes)
    while end_lane == start_lane:
        end_lane = random.choice(drivable_lanes)

    person = Person(
        id=i,
        home=Position(lane_position=LanePosition(lane_id=start_lane, s=1.0)),
        schedules=[
            Schedule(
                trips=[
                    Trip(
                        mode=2,
                        end=Position(lane_position=LanePosition(lane_id=end_lane, s=1.0)),
                        departure_time=random.uniform(0, 3600),
                    )
                ],
                loop_count=1,
            )
        ],
    )
    # 1) 尽量把 person.type 设成 “车辆/机动车”
    type_enum = Person.DESCRIPTOR.fields_by_name["type"].enum_type
    name2num = {v.name: v.number for v in type_enum.values}

    # 兼容不同版本的枚举命名
    for k in ("VEHICLE", "CAR", "TYPE_VEHICLE", "PERSON_TYPE_VEHICLE"):
        if k in name2num:
            person.type = name2num[k]
            break
    # 关键：补齐 vehicle_attribute（不要用 VehicleAttribute(...)）
    va = person.vehicle_attribute
    va.lane_change_length = 10.0
    va.min_gap = 1.0
    va.headway = 1.5
    va.length = 5.0
    va.width = 2.0
    va.max_speed = 33.33  # 约 120 km/h
    va.max_acceleration = 3.0
    va.max_braking_acceleration = -10.0
    va.usual_acceleration = 2.0
    va.usual_braking_acceleration = -4.5
    va.model = "normal"
    va.lane_max_speed_recognition_deviation = 1.0
    # 3) pedestrian_attribute：关键是“触发 presence”
    pa = person.pedestrian_attribute
    if pa.ByteSize() == 0:
        # 先尝试常见字段名；不同版本字段名可能不同，所以做 hasattr 保护
        if hasattr(pa, "max_speed"):
            pa.max_speed = 1.5
        elif hasattr(pa, "speed"):
            pa.speed = 1.5
        elif hasattr(pa, "desired_speed"):
            pa.desired_speed = 1.5
        else:
            # 实在不知道字段名，就给第一个数值字段赋个值，确保 presence
            for f in pa.DESCRIPTOR.fields:
                if f.cpp_type in (f.CPPTYPE_INT32, f.CPPTYPE_INT64, f.CPPTYPE_UINT32, f.CPPTYPE_UINT64, f.CPPTYPE_DOUBLE, f.CPPTYPE_FLOAT):
                    setattr(pa, f.name, 1)
                    break
    persons.append(person)

# 保存人员文件
print("保存人员文件...")
pb = Persons(persons=persons)
with open("data/person.pb", "wb") as f:
    f.write(pb.SerializeToString())

print(f"已生成 {len(persons)} 个人员，保存到 data/person.pb")
print("下一步: 运行仿真: python run_simulation.py")
