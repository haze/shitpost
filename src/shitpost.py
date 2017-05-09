import argparse
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

# main
parser = argparse.ArgumentParser()
parser.add_argument('text', nargs='*',type=str, help='text to intersperse.')
parser.add_argument('-mi', '--min-emojis', default=2, type=int, help='minimum amount of emojis to be interspersed.')
parser.add_argument('-ma', '--max-emojis', default=3, type=int, help='maximum amount of emojis to be interspersed.')
args = parser.parse_args() 

base = ' '.join(args.text)
if not base:
	print('no input found.')
	exit(1)

if args.min_emojis < 1 or args.min_emojis > 10:
	print('min emojis valid range [1-10]')
	exit(1)

if args.max_emojis > 10 or args.max_emojis < 1:
	print('max emojis valid range [1-10].')
	exit(1)



split_base = split_by_random(base, ' ', args.min_emojis, args.max_emojis)
print(' '.join(list(map(emojify, split_base))))
