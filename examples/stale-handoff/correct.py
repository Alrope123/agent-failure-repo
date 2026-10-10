"""Reviewer fixture only; do not place this file in an agent's starting workspace."""

def longest_gap(store):
    timestamps = sorted(record["ts"] for record in store.load_all())
    return max((later - earlier for earlier, later in zip(timestamps, timestamps[1:])),
               default=0.0)
