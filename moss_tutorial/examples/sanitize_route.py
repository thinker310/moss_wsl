import math
from mosstool.type import Persons

IN_FILE = "data/person_routed.pb"
OUT_FILE = "data/person_routed_sanitized.pb"

pb = Persons()
pb.ParseFromString(open(IN_FILE, "rb").read())

patched_trip_dt = 0
patched_sched_dt = 0
patched_fallback = 0

def set_if_field_exists(msg, name, value):
    if hasattr(msg, name):
        try:
            setattr(msg, name, float(value))
            return True
        except Exception:
            return False
    return False

for new_id, p in enumerate(pb.persons):
    # 1) 统一重排 id，避免引擎按索引报错时产生歧义
    if hasattr(p, "id"):
        p.id = int(new_id)

    # 2) 遍历 schedule/trip，强制“写回 departure_time”
    for s in getattr(p, "schedules", []):
        # 若 schedule 层存在 departure_time/start_time，也写一下（不同版本字段名可能不同）
        sched_time_written = False

        for t in getattr(s, "trips", []):
            if not hasattr(t, "departure_time"):
                continue

            dt = getattr(t, "departure_time", 0.0) or 0.0
            dt = float(dt)

            # 兜底：如果 dt 非法，给一个正数
            if (not math.isfinite(dt)) or dt <= 0.0:
                dt = 1.0
                patched_fallback += 1

            # 关键：无条件写回一次，触发 presence / 重新序列化
            t.departure_time = dt
            patched_trip_dt += 1

            # 同步写 schedule 层（如果存在字段）
            if not sched_time_written:
                for fname in ("departure_time", "start_time", "begin_time"):
                    if set_if_field_exists(s, fname, dt):
                        patched_sched_dt += 1
                        sched_time_written = True
                        break

open(OUT_FILE, "wb").write(pb.SerializeToString())
print("rewrote trip.departure_time for trips:", patched_trip_dt)
print("wrote schedule time fields:", patched_sched_dt)
print("fallback-fixed dt:", patched_fallback)
print("wrote:", OUT_FILE)
