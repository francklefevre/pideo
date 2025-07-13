#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This software is free software: you can do whatever you want with it.
# Developed by Franck LEFEVRE for K1 (https://k1info.com), aided by his team of friendly robots.

import os
import sys
import json
import logging
import random
import subprocess
import socket

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None


def setup_logging(err_file_path):
    # Clear existing error log
    open(err_file_path, 'w').close()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # File handler for errors
    err_handler = logging.FileHandler(err_file_path, mode='a')
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(err_handler)
    # Console output for info and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(console_handler)


def load_json_file(path, default=None):
    if os.path.isfile(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error("Failed to parse JSON file %s: %s", path, e)
    return default if default is not None else {}


def get_video_duration(path):
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries',
            'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(result.stdout.strip())
    except Exception as e:
        logging.error("Could not determine duration for %s: %s", path, e)
        return None


def notify_mqtt(client, topic, video, duration):
    payload = json.dumps({'video': video, 'duration': duration})
    try:
        client.publish(topic, payload)
    except Exception as e:
        logging.error("Failed to publish MQTT message: %s", e)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    err_file = os.path.basename(__file__) + '.err.txt'
    setup_logging(os.path.join(script_dir, err_file))

    # Load configurations
    cfg = load_json_file(os.path.join(script_dir, 'param.json'), {})
    secrets = load_json_file(os.path.join(script_dir, 'secret.json'), {})

    mqtt_server = cfg.get('mqtt_server')
    mqtt_port = cfg.get('mqtt_port', 1883)
    mqtt_topic = cfg.get('mqtt_topic')
    mqtt_username = secrets.get('mqtt_username')
    mqtt_password = secrets.get('mqtt_password')
    # Command template for video playback; {video_path} will be expanded.
    player_cmd = cfg.get('player_cmd', "ffmpeg -re -i '{video_path}' -f null -")

    # Determine videos directory
    videos_dir = os.path.join(script_dir, cfg.get('videos_dir', 'videos'))
    if not os.path.isdir(videos_dir):
        logging.error("Videos directory does not exist: %s", videos_dir)
        return

    # MQTT setup if available and configured
    use_mqtt = bool(mqtt and mqtt_server and mqtt_topic)

    if mqtt is None and (mqtt_server or mqtt_topic):
        logging.warning(
            "python-paho-mqtt package not found – MQTT notifications disabled. "
            "Install it with 'pip3 install --break-system-packages paho-mqtt' or run inside a virtualenv.")

    if use_mqtt:
        try:
            # Simple connectivity check before instantiating the client
            sock = socket.create_connection((mqtt_server, mqtt_port), timeout=5)
            sock.close()

            client = mqtt.Client()
            if mqtt_username:
                client.username_pw_set(mqtt_username, mqtt_password)

            # Establish connection (60 s keep-alive by default)
            client.connect(mqtt_server, mqtt_port)

            # Start a background thread to handle network I/O (keep-alive, reconnect…)
            client.loop_start()
        except Exception as exc:
            logging.warning("Cannot reach MQTT %s:%s (%s). MQTT notifications disabled.", mqtt_server, mqtt_port, exc)
            use_mqtt = False

    # Load playlist if defined
    playlist_path = os.path.join(videos_dir, 'playlist.json')
    playlist = []
    loop = False
    index = 0
    if os.path.isfile(playlist_path):
        data = load_json_file(playlist_path, {})
        playlist = data.get('videos', []) or []
        loop = bool(data.get('loop', False))
        if playlist:
            logging.info("Loaded playlist with %d video(s), loop=%s", len(playlist), loop)

    # Gather available video files
    supported = ('.mp4', '.avi', '.mkv', '.mov')
    all_videos = [f for f in os.listdir(videos_dir)
                  if os.path.isfile(os.path.join(videos_dir, f)) and f.lower().endswith(supported)]
    if not all_videos:
        logging.error("No video files found in %s", videos_dir)
        return

    # Playback loop
    while True:
        if playlist:
            video = playlist[index]
            index += 1
            if index >= len(playlist):
                if loop:
                    index = 0
                else:
                    logging.info("Playlist finished, exiting.")
                    break
        else:
            video = random.choice(all_videos)

        video_path = os.path.join(videos_dir, video)
        if not os.path.isfile(video_path):
            logging.error("Video not found: %s", video_path)
            continue

        duration = get_video_duration(video_path)
        if use_mqtt:
            notify_mqtt(client, mqtt_topic, video, duration)

        logging.info("Playing video: %s", video)
        try:
            cmd = player_cmd.format(video_path=video_path)
            logging.info("Running playback command: %s", cmd)
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error("Playback failed for %s: %s", video, e)

    # Cleanup MQTT
    if use_mqtt:
        try:
            client.disconnect()
            client.loop_stop()
        except Exception:
            pass


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logging.exception("Unhandled exception in main")
        sys.exit(1)
