import sys
import argparse
import re
from itertools import permutations

def main():
    # 创建参数解释器，输出描述和帮助信息
    parser = argparse.ArgumentParser(
        prog='stringsToConcat',
        description='字符串拆分和拼接',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
    1.基础用法（默认逗号拆分、空字符拼接）：
        python3 strConcat.py -s "aaa,bbb,ccc"
        输出:aaabbbccc

    2.自定义拆分符（按分号拆分）+空拼接：
        python3 strConcat.py -s "aaa;bbb;ccc" -d ";"
        输出:aaabbbccc
        python3 strConcat.py -s "aaa,bbb;ccc" -d ",;"
        输出:aaabbbccc


    3.自定义拼接符（逗号拆分、下划线拼接）：
        python3 strConcat.py -s "aaa,bbb,ccc" -j "_"
        输出:aaa_bbb_ccc

    4.混合自定义（竖线拆分、横线拼接）：
        python3 strConcat.py -s "aaa|bbb|ccc" -d "|" -j "-"
        输出:aaa-bbb-ccc 

    5.循环拼接:
        python3 strConcat.py -s "aa,bb" -r
        输出:1:aabb
             2:bbaa
"""
    )

    # 需要处理的字符串
    parser.add_argument(
        '-s', '--strings',
        required=True,
        type=str,
        help='指定需要处理的字符串'
    )

    # 指定分割符（默认“,”）
    parser.add_argument(
        '-d', '--delimiter',
        type=str,
        default=',',
        help='指定分割符'
    )

    # 指定连接符（默认空）
    parser.add_argument(
        '-j', '--joiner',
        type=str,
        default='',
        help='指定连接符'
    )

    parser.add_argument(
        '-r', '--range',
        action='store_true',
        help='循环排列'
    )

    args = parser.parse_args()

    try:
        # 转义特殊字符
        escaped_delimiters = re.escape(args.delimiter)
        str_list = re.split(r'[' + escaped_delimiters + ']', args.strings)

        # 过滤空
        str_list = [s for s in str_list if s.strip() != '']

        # 校验-r参数，大于等于2
        if args.range and len(str_list) < 2:
            print("循环排列需要字符串大于2(当前仅检测到一个)", file=sys.stderr)
            sys.exit(1)

        # -r的拼接逻辑
        if args.range:
            # 生成循环拼接字符串并遍历输出
            perm_list = permutations(str_list)
            print("[+]循环拼接结果:")
            for idx, perm in enumerate(perm_list, 1):
                result = args.joiner.join(perm)
                print(f"{result}")
        else:
            # 普通拼接
            result = args.joiner.join(str_list)
            print(f"[+]拼接结果:{result}")
    except Exception as e:
        print(f"处理失败{e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
