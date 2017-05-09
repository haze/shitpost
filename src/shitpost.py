import sys
from random import randint
import requests

DANGO_ENPOINT = 'https://emoji.getdango.com/api/emoji'

def get_relevant_emojis(x):
	r = requests.get(DANGO_ENPOINT, params={'q':x})
	return r.json()['results']

def emojify(x):
	relevant = get_relevant_emojis(x)
	if relevant[0]['score'] < 0.012:
		return x
	if x.endswith('.'):
		return x[:len(x)-1] + " " + ' '.join(list(map(lambda x: x['text'], get_relevant_emojis(x)[:randint(1, 3)]))) + '. '
	else:
		return x + " " + ' '.join(list(map(lambda x: x['text'], get_relevant_emojis(x)[:randint(1, 3)]))) + ' '

def split_by_random(base, char, a, e):
	buff = []
	b = base.split(char)
	while not len(b) == 0:
		to = randint(a, e)
		section = b[0:to]
		buff.append(' '.join(section))
		b = b[to:]
	return buff

base = ' '.join(sys.argv[1:])
if not base:
	print('no input found.')
	exit(1)

split_base = split_by_random(base, ' ', 1, 3)
print(' '.join(list(map(emojify, split_base))))
