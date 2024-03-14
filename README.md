# from https://github.com/fun-with-serverless/rustifying-serverless.git

1. 下面是简单的测试，感觉rust内核的反而网络请求会更慢。所以就不尝试了。很奇怪
2. 其他修改是在mac的适应

xiangzhou@XiangZhou list_buckets_rust_python % python3 test.py  
[{'name': 'dfdfdf', 'region': 'us-east-1'}]
[{'name': 'dfdfdf', 'region': 'us-east-1'}]
Timer unit: 1e-09 s

Total time: 2.43846 s
File: /Users/xiangzhou/github/rustifying-serverless/s3-admin-app/list_buckets_rust_python/test.py
Function: run_2 at line 53

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    53                                           @func_line_time
    54                                           def run_2():
    55         1       3000.0   3000.0      0.0      import asyncio
    56         1       1000.0   1000.0      0.0      import boto3
    57         1       1000.0   1000.0      0.0      import uvloop
    58         1   18589000.0    2e+07      0.8      s3_client = boto3.client("s3")
    59         1 1137499000.0    1e+09     46.6      s3_buckets = s3_client.list_buckets()
    60         1       1000.0   1000.0      0.0      bucket_info_list = []
    62         2     944000.0 472000.0      0.0      with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
    63         1 1281362000.0    1e+09     52.5          bucket_info_list = runner.run(get_buckets_region(s3_buckets["Buckets"]))
    64         1      61000.0  61000.0      0.0          print(bucket_info_list)

xiangzhou@XiangZhou list_buckets_rust_python % python3 test.py 1
[('dfdfdf', '')]
[('dfdfdf', '')]
Timer unit: 1e-09 s

Total time: 2.35182 s
File: /Users/xiangzhou/github/rustifying-serverless/s3-admin-app/list_buckets_rust_python/test.py
Function: run_1 at line 46

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    46                                           @func_line_time
    47                                           def run_1():
    48         1       5000.0   5000.0      0.0      import s3_ops_rust
    49         1   10357000.0    1e+07      0.4      s3_client = s3_ops_rust.S3OpsRust()
    50         1 2341323000.0    2e+09     99.6      l = s3_client.list_buckets()
    51         1     134000.0 134000.0      0.0      print(l)

