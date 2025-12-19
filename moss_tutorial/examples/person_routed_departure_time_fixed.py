from mosstool.type import Persons

IN_ORIG = "data/person.pb"
IN_ROUTED = "data/person_routed.pb"
OUT_FIXED = "data/person_routed_fixed.pb"

# 读取原始与 routed
orig = Persons(); orig.ParseFromString(open(IN_ORIG, "rb").read())
routed = Persons(); routed.ParseFromString(open(IN_ROUTED, "rb").read())

# 建索引：person_id -> schedules/trips departure_time
dt_map = {}
for p in orig.persons:
    pid = getattr(p, "id", None)
    if pid is None:
        continue
    for si, s in enumerate(p.schedules):
        for ti, t in enumerate(s.trips):
            if hasattr(t, "departure_time"):
                dt_map[(pid, si, ti)] = t.departure_time

patched = 0
for p in routed.persons:
    pid = getattr(p, "id", None)
    for si, s in enumerate(p.schedules):
        for ti, t in enumerate(s.trips):
            if not hasattr(t, "departure_time"):
                continue

            # 判断 presence（proto3 optional 才能 HasField）
            try:
                has = t.HasField("departure_time")
            except Exception:
                # 没有 presence 语义就不处理
                has = True

            if not has:
                # 优先用原始文件中的 departure_time
                key = (pid, si, ti)
                if key in dt_map:
                    t.departure_time = dt_map[key]  # 关键：显式赋值触发 presence
                else:
                    t.departure_time = 0.0
                patched += 1

open(OUT_FIXED, "wb").write(routed.SerializeToString())
print(f"patched departure_time: {patched}")
print(f"wrote: {OUT_FIXED}")
