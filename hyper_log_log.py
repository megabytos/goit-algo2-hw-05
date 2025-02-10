import json
import time
from datasketch import HyperLogLog
import gzip

file_path = 'lms-stage-access.tar.gz'


def ip_generator(path):
    with gzip.open(path, "rt", encoding="utf-8") as file:
        for line in file:
            try:
                log_entry = json.loads(line.strip())
                remote_addr = log_entry.get("remote_addr")
                if remote_addr:
                    yield remote_addr
            except json.JSONDecodeError:
                continue


def count_unique_ip_set(ip_arr):
    unique_ip_set = set(ip_arr)
    return len(unique_ip_set)


def count_unique_ip_hll(ip_arr):
    hll = HyperLogLog(p=14)
    for ip in ip_arr:
        hll.update(ip.encode('utf-8'))
    return hll.count()


if __name__ == "__main__":
    data = ip_generator(file_path)

    start = time.time()
    exact_count = count_unique_ip_set(data)
    exact_time = time.time() - start

    data = ip_generator(file_path)
    start = time.time()
    approx_count = count_unique_ip_hll(data)
    approx_time = time.time() - start

    print("Comparison results:")
    print(f"{'':<25}{'Exact count':<20}{'HyperLogLog count':<20}")
    print(f"{'Unique elements':<25}{exact_count:<20}{approx_count:<20}")
    print(f"{'Execution time (sec)':<25}{exact_time:<20.5f}{approx_time:<20.5f}")
