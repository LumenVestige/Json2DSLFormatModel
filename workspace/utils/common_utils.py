import time


def get_cost_time(time_flag):
    total_seconds = (time.time() - time_flag)
    # 计算分钟、秒和毫秒
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)  # 计算毫秒

    # 格式化为 m:s:ms
    return f"{minutes}:{seconds:02d}:{milliseconds:03d}"
