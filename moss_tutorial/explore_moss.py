#!/usr/bin/env python3
"""
MOSS API 探索脚本
帮助了解 MOSS 的使用方法
"""

import moss
from moss import Engine, TlPolicy, Verbosity, DBRecorder
import inspect

def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def explore_class(cls, name):
    """探索一个类的详细信息"""
    print_section(f"{name} 类详细信息")
    
    # 1. 文档字符串
    if cls.__doc__:
        print(f"\n📖 说明:\n{cls.__doc__}\n")
    else:
        print("\n📖 说明:  无文档字符串\n")
    
    # 2. 初始化参数
    try:
        sig = inspect.signature(cls.__init__)
        print("🔧 初始化参数:")
        for param_name, param in sig.parameters.items():
            if param_name != 'self':
                annotation = param.annotation if param.annotation != inspect.Parameter. empty else "未指定类型"
                default = f" = {param.default}" if param. default != inspect.Parameter.empty else " (必需)"
                print(f"  • {param_name}:  {annotation}{default}")
    except Exception as e:
        print(f"⚠️ 无法获取初始化参数: {e}")
    
    # 3. 方法列表
    print("\n⚙️ 可用方法:")
    methods = []
    for attr_name in dir(cls):
        if not attr_name.startswith('_'):
            attr = getattr(cls, attr_name)
            if callable(attr):
                methods.append(attr_name)
                # 尝试获取方法签名
                try:
                    sig = inspect.signature(attr)
                    print(f"  • {attr_name}{sig}")
                    # 如果有文档字符串，也打印出来
                    if attr.__doc__:
                        doc_lines = attr.__doc__.strip().split('\n')
                        print(f"      → {doc_lines[0]}")
                except: 
                    print(f"  • {attr_name}()")
    
    # 4. 属性
    print("\n📊 属性:")
    for attr_name in dir(cls):
        if not attr_name. startswith('_'):
            attr = getattr(cls, attr_name, None)
            if not callable(attr):
                print(f"  • {attr_name}: {type(attr).__name__}")

def main():
    print_section("MOSS 城市交通仿真工具 - API 探索")
    
    # 探索主要组件
    print("\n📦 MOSS 包含的主要组件:")
    components = {}
    for name in dir(moss):
        if not name.startswith('_'):
            obj = getattr(moss, name)
            components[name] = type(obj).__name__
            # 修复：去掉格式化中的空格
            name_padded = name.ljust(20)
            type_name = type(obj).__name__
            print(f"  • {name_padded} - {type_name}")
    
    # 详细探索主要类
    print_section("详细探索主要类")
    
    # Engine
    explore_class(Engine, "Engine")
    
    # TlPolicy
    if hasattr(moss, 'TlPolicy'):
        print_section("TlPolicy 枚举值")
        print("\n可用的交通灯策略:")
        for attr in dir(TlPolicy):
            if not attr.startswith('_'):
                value = getattr(TlPolicy, attr)
                print(f"  • TlPolicy.{attr} = {value}")
    
    # Verbosity
    if hasattr(moss, 'Verbosity'):
        print_section("Verbosity 枚举值")
        print("\n可用的日志级别:")
        for attr in dir(Verbosity):
            if not attr.startswith('_'):
                value = getattr(Verbosity, attr)
                print(f"  • Verbosity.{attr} = {value}")
    
    # DBRecorder
    if hasattr(moss, 'DBRecorder'):
        explore_class(DBRecorder, "DBRecorder")
    
    print_section("探索完成")
    print("\n💡 提示:")
    print("  1. 查看上面的参数要求")
    print("  2. 准备必需的输入文件（地图、配置等）")
    print("  3. 根据参数创建 Engine 实例")
    print("  4. 调用方法运行仿真")
    print("\n🔗 建议查看 MOSS 的 GitHub 仓库获取官方示例")

if __name__ == "__main__":
    main()
