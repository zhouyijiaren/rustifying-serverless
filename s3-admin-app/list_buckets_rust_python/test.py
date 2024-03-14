import sys
from typing import List, Tuple
import functools

from line_profiler import LineProfiler

def func_line_time(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        func_return = f(*args, **kwargs)
        lp = LineProfiler()
        lp_wrap = lp(f)
        lp_wrap(*args, **kwargs)
        lp.print_stats()
        return func_return
    return decorator
        

async def get_buckets_region(buckets: List[str]) -> List[Tuple[str, str]]:
    from aiobotocore.config import AioConfig
    from aiobotocore.session import get_session
    import asyncio
    session = get_session()
    bucket_info_list = []
    
    async with session.create_client("s3", config=AioConfig(retries={"max_attempts": 0}) ) as s3_client:
        tasks = [
            get_bucket_info(s3_client, bucket["Name"]) for bucket in buckets
        ]

        # Run the batch of tasks and collect results
        results = await asyncio.gather(*tasks)

    # Add results to bucket_info_list
    bucket_info_list.extend(results)

    return bucket_info_list


async def get_bucket_info(s3_client, bucket_name: str):
    bucket_location = await s3_client.get_bucket_location(Bucket=bucket_name)
    region = bucket_location["LocationConstraint"] or "us-east-1"
    return {"name": bucket_name, "region": region}


@func_line_time
def run_1():
    import s3_ops_rust
    s3_client = s3_ops_rust.S3OpsRust()
    l = s3_client.list_buckets()
    print(l)

@func_line_time
def run_2():
    import asyncio
    import boto3
    import uvloop
    s3_client = boto3.client("s3")
    s3_buckets = s3_client.list_buckets()
    bucket_info_list = []

    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        bucket_info_list = runner.run(get_buckets_region(s3_buckets["Buckets"]))
        print(bucket_info_list)

# main
if __name__ == "__main__":
    # arg parse
    f = sys.argv
    run_rust = False
    if len(f) == 2 and int(f[1]) == 1:
        run_rust = True
    if run_rust:
        run_1()
    else:
        run_2()
        
