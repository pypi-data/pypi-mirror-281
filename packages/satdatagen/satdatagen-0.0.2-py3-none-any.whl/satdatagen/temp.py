import json
import time

start = time.time()
f = open("object_sizes.json")
end = time.time()

print(f'total time: {end - start}')
file = f.read()


# print(file)
words = file.split(" ")
for w in range(len(words)):
	if 'null' in words[w]:
		words[w] = words[w].replace('null', '\"null\"')
		# print(words[w])

new_file = " ".join(words)
# print(new_file)

rso_dict = json.loads(file)
# print(rso_dict)