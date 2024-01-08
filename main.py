from tasks.task import task

if __name__ == "__main__":
    task(channel="tv_globo", headless=False)
    task(channel="g1", headless=True)
