"""Reviewer fixture showing the missing-sort behavior; not an agent run."""

def longest_gap(store):
    timestamps = [record["ts"] for record in store.load_all()]
    return max((later - earlier for earlier, later in zip(timestamps, timestamps[1:])),
               default=0.0)
