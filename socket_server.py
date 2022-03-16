import socket
from tqdm import tqdm

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(ADDR)
	server.listen()
	print("[+] Listening...")

	conn, addr = server.accept()
	print(f"[+] Client connected from {addr[0]} : {addr[1]}")

	data = conn.recv(SIZE).decode(FORMAT)
	item = data.split("_")

	FILENAME = item[0]
	FILESIZE = int(item[1])

	print("[+] Filename and filesize recieved from client.")
	conn.send("Filename and filesize recieved".encode(FORMAT))

	bar = tqdm(range(FILESIZE), f"Receiving {FILENAME}", unit="B", unit_scale=True, unit_divisor=SIZE)

	with open(f"recv_{FILENAME}", "w") as f:
		while True:
			data = conn.recv(SIZE).decode(FORMAT)

			if not data:
				break

			f.write(data)
			conn.send("Data received.".encode(FORMAT))

			bar.update(len(data))

	
	conn.close()
	server.close()


if __name__ == "__main__":
	main()
