import concurrent.futures
import argparse
import sys
from random import randint
import requests

DANGO_ENPOINT = 'https://emoji.getdango.com/api/emoji'

def get_relevant_emojis(x):
	return requests.get(DANGO_ENPOINT, params={'q':x}).json()['results']

def emojify(x):
	relevant = get_relevant_emojis(x)
	if relevant[0]['score'] < 0.012:
		return x
	if x.endswith('.'):
		return x[:len(x)-1] + " " + ' '.join(list(map(lambda x: x['text'], relevant[:randint(args.min_emojis, args.max_emojis)]))) + '. '
	else:
		return x + " " + ' '.join(list(map(lambda x: x['text'], relevant[:randint(args.min_emojis, args.max_emojis)]))) + ' '

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
parser.add_argument('-mwi', '--min-words', default=1, type=int, help='minimum amount of words to be split by.')
parser.add_argument('-mwa', '--max-words', default=3, type=int, help='maximum amount of words to be split by.')
args = parser.parse_args() 

base = ' '.join(args.text)
if not base:
	print('no input found.')
	exit(1)

if args.min_words < 1:
	print('min words invalid range! valid: [1:]')
	exit(1)

if args.max_words < 1:
	print('max words invalid range! valid [1:]')
	exit(1)

if args.min_emojis < 1 or args.min_emojis > 10:
	print('min emojis invalid range! valid: [1-10]')
	exit(1)

if args.max_emojis > 10 or args.max_emojis < 1:
	print('max emojis invalid range! valid: [1-10].')
	exit(1)

split_base = split_by_random(base, ' ', args.min_words, args.max_words)
executor = concurrent.futures.ProcessPoolExecutor(len(split_base))
futures = [executor.submit(emojify, section) for section in split_base]
concurrent.futures.wait(futures)
print(' '.join(list(map(lambda x: x.result(), futures))))
