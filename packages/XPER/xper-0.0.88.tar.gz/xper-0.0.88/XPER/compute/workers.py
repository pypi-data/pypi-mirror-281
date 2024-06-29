import multiprocessing

def get_max_workers():
    max_workers = multiprocessing.cpu_count()
    return max_workers

if __name__ == "__main__":
    max_workers = get_max_workers()
    print(f"Maximum number of workers (logical processors) available: {max_workers}")