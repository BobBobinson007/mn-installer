# Install with: git clone https://github.com/BobBobinson007/mn-installer.git && cd micro-notes && python3 installer.py

import random
import time

a = 0

print()

print("╔═══════Micro-Notes═══════╗")

while a <= 100:
    print(f"\r╠═ Paket_1/4         {a:>3}% ║", end="", flush=True)
    a += 1
    time.sleep(random.uniform(0.005, 0.05))
    

a = 0
print()

while a <= 100:
    print(f"\r╠═ Paket_2/4         {a:>3}% ║", end="", flush=True)
    a += 1
    time.sleep(random.uniform(0.005, 0.05))

a = 0
print()

while a <= 100:
    print(f"\r╠═ Paket_3/4         {a:>3}% ║", end="", flush=True)
    a += 1
    time.sleep(random.uniform(0.005, 0.05))

a = 0
print()

while a <= 100:
    print(f"\r╠═ Paket_4/4         {a:>3}% ║", end="", flush=True)
    a += 1
    time.sleep(random.uniform(0.0005, 0.005))

print("\n╠═════════════════════════╣")
print("║                         ║")
print("║      You installed!     ║")
print("║       Micro-Notes       ║")
print("║                         ║")
print("╚═════════════════════════╝")
print()
