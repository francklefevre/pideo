# AGENTS_METHODS

2025-07-13 15:07:17 - Initialized project structure for pideo: added pideo.py, configuration examples, videos directory, service template, and documentation.
2025-07-13 15:35:00 - Noted that Paho MQTT requires a background network loop (`client.loop_start()` / `client.loop_stop()`) for persistent connections. Added these calls in *pideo.py* and documented fallback when the library is absent.
