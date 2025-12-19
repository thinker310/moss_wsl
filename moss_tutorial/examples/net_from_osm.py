import geojson  # 关键导入
from mosstool.map.builder import Builder
from mosstool.util.format_converter import dict2pb
from mosstool.type import Map
import os

# 配置
ROADNET_FILE = "cache/net.geojson"
OUTPUT_FILE = "data/map.pb"
PROJ_STR = "+proj=tmerc +lat_0=39.90 +lon_0=116.40"

# 使用 geojson. load() 加载（不是 json.load()）
print("加载 GeoJSON 文件...")
with open(ROADNET_FILE, "r", encoding="utf-8") as f:
    net = geojson.load(f)  # 关键：使用 geojson.load()

# 创建空 AOI
aois = geojson.FeatureCollection([])

# 构建
print("构建地图...")
builder = Builder(net=net, aois=aois, proj_str=PROJ_STR)
m = builder.build("my_map")

# 保存
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
pb = dict2pb(m, Map())
with open(OUTPUT_FILE, "wb") as f:
    f.write(pb.SerializeToString())

print(f"✅ 地图创建成功!")
print(f"   道路: {len(m['roads'])} 条")
print(f"   路口: {len(m['junctions'])} 个")
