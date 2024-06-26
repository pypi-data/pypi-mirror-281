# Intro
> This project is a file downloader, supporting dynamic download according to the size of the file to choose the download mode, for the connection that supports breakpoint continuation will automatically break the connection, for the unsupported link will overwrite the previous content, the project includes retry mechanism, etc., currently supports: streaming download, large file fragment download.

# Give an example
```python
from yundownload import YunDownloader


download = YunDownloader(
    url='https://dldir1.qq.com/qqfile/qq/PCQQ9.7.17/QQ9.7.17.29225.exe',
    limit=1, # concurrency
    timeout=1000, # You are advised to set a longer timeout period for large file fragments because large file fragments exert pressure on the peer server
    dynamic_concurrency=True,
    save_path='QQ9.7.17.29225.exe'
)
# Files larger than this size are downloaded in fragments
download.DISTINGUISH_SIZE = 100 * 1024 * 1024
# The size of each shard at download time
download.CHUNK_SIZE = 100 * 1024 * 1024
# Heartbeat status detection time
download.HEARTBEAT_SLEEP = 1
# Run task. error_retry: Number of retries when an error occurs
download.run(error_retry=3)
```

# Update log
- V 0.1.13
  - Troubleshooting Heartbeat detection 
- V 0.1.12
  - This version throws an exception after a retry failure
- V 0.1.10
  - Optimized breakpoint continuation
  - Optimized concurrent downloads
  - Optimized heartbeat detection
  - Optimized error retry
  - This version still does not throw an exception after a retry failure