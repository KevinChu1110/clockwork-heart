import subprocess

res = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                      "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0",
                      "proofs/combat_feel/rabbit_combat.mp4"], capture_output=True, text=True)
print("Packet count:", res.stdout.strip())
