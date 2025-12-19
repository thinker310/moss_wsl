#!/usr/bin/env python3
"""
从 OSM 文件创建路网
"""

from mosstool.map.osm import RoadNet
import os

def main():
    print("=" * 70)
    print("从 OSM 创建路网")
    print("=" * 70)
    
    # ============================================
    # 1. 定义投影和范围
    # ============================================
    # 北京某区域（示例）
    projstr = "+proj=tmerc +lat_0=39.9 +lon_0=116.4"
    
    # 地理范围（经纬度）
    max_latitude = 39.92
    min_latitude = 39.88
    max_longitude = 116.42
    min_longitude = 116.38
    
    print(f"\n投影坐标系:  {projstr}")
    print(f"地理范围:")
    print(f"  纬度: {min_latitude}° ~ {max_latitude}°")
    print(f"  经度: {min_longitude}° ~ {max_longitude}°")
    
    # ============================================
    # 2. 创建 RoadNet 对象
    # ============================================
    print(f"\n创建 RoadNet 对象...")
    
    rn = RoadNet(
        proj_str=projstr,
        max_latitude=max_latitude,
        min_latitude=min_latitude,
        max_longitude=max_longitude,
        min_longitude=min_longitude,
    )
    
    print("✅ RoadNet 对象创建成功")
    
    # ============================================
    # 3. 从 GeoJSON 创建路网
    # ============================================
    # 注意：你需要先有一个 GeoJSON 文件
    # 可以从 OSM 文件手动转换，或使用其他工具
    
    geojson_file = "cache/topo.geojson"
    
    if not os.path.exists(geojson_file):
        print(f"\n❌ GeoJSON 文件不存在: {geojson_file}")
        print("\n你需要先准备 GeoJSON 文件:")
        print("  方法 1: 使用 mosstool 官方示例")
        print("         cd ~/mosstool/examples")
        print("         python map_osm2geojson.py")
        print("\n  方法 2: 使用 QGIS 或其他 GIS 工具转换")
        print("\n  方法 3: 使用在线工具（如 geojson.io）")
        return
    
    print(f"\n从 GeoJSON 创建路网:  {geojson_file}")
    roadnet = rn.create_road_net(geojson_file)
    
    print(f"✅ 路网创建成功！")
    
    # ============================================
    # 4. 导出为 GeoJSON（可选）
    # ============================================
    output_geojson = "output/roadnet.geojson"
    os.makedirs("output", exist_ok=True)
    
    rn.dump_as_geojson(output_geojson)
    print(f"✅ 路网已导出为 GeoJSON:  {output_geojson}")
    
    print(f"\n" + "=" * 70)
    print("完成！")
    print("=" * 70)

if __name__ == "__main__":
    main()
