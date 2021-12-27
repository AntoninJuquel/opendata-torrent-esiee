#!/usr/bin/env python3

def get_config():
    with open("config.txt","r") as file:
        text = file.read()
        text_lines = text.split("\n")
        text_values = {}
        for line in text_lines:
            if "=" in line:
                key_value = line.split("=")
                text_values[key_value[0]] = int(key_value[1])
    return text_values

