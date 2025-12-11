import re
from collections import Counter
import logging

log = logging.getLogger(__name__)
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.CRITICAL) #  DEBUG INFO WARNING CRITICAL

class Excel:
	def __init__(self, word):
		self.original_word = word
		self.word = list()
		self.correct = list()
		self.distance = 0
		self.initial_distance = 0
		self.offset = None


	def compare(self, correct):
		if self.original_word.lower() == correct.lower():
			return True, [] # distance, word

		if fail := self.pre_check(correct):
			return fail

		if fail := self.letter_by_letter(correct):
			return fail

		self.case_correction()
		return self.distance, self.word


	def pre_check(self, correct): # gets missing and different
		c = Counter(correct.lower())
		w = Counter(self.original_word.lower())
		c.subtract(w)
		missing = sum(map(abs, c.values()))
		self.offset = len(correct) - len(self.original_word)
		self.initial_distance = int(round((missing - abs(self.offset))/2,0)) + abs(self.offset)
		if self.initial_distance > 2:
			return False, [] # call exit method


	def letter_by_letter(self, correct, reverse=False):
		self.distance = 0
		self.word = list(self.original_word.ljust(len(correct), '_'))
		self.correct = list(correct.ljust(len(self.original_word), '_'))

		i = 0
		while i < len(self.word):
			if self.word[i].lower() != self.correct[i].lower():
				self.distance += 1
				if self.distance > 2:
					self.original_word, correct = self.original_word[::-1], correct[::-1]
					if not reverse: # recursive call to check reverse order
						return self.letter_by_letter(correct, reverse=True)
					return False, []
				
				def calculate_lookaheads(start_id):
					la_insert = la_delete = default = 0
					for j in range(start_id, len(self.word)):
						if (j == len(self.word) - 1 and self.word[j] != '_') or \
						(j < len(self.word) - 1 and self.word[j].lower() != self.correct[j + 1].lower()):
							la_insert += 1
						if (j == len(self.word) - 1 and self.correct[j] != '_') or \
						(j < len(self.word) - 1 and self.word[j + 1].lower() != self.correct[j].lower()):
							la_delete += 1
						if self.word[j].lower() != self.correct[j].lower():
							default += 1
					return la_insert, la_delete, default
				la_insert, la_delete, default = calculate_lookaheads(i)
				
				# Strategy pattern - based on self.offset, self.initial_distance and lookaheads
				if self.offset == -2 or la_delete == 0 and self.offset < 0:
					operations = ['delete', 'swap', 'insert', 'replace']
				elif self.offset == 2 or la_insert == 0 and (self.offset > 0 or self.correct[-1::] == ['_']):
					operations = ['insert', 'swap', 'delete', 'replace']
				elif self.offset == 0 and len(self.word) <= 3:
					operations = ['swap', 'replace', 'insert', 'delete']
				else:
					operations = ['swap', 'insert', 'delete', 'replace']
				log.info(f'{"".join(self.word)} vs {correct}: d{self.initial_distance} o{self.offset} i{la_insert} d{la_delete} ~{default}', end=' ')
				log.info(operations)
				
				for operation in operations:
					method = getattr(self, f'do_{operation}')
					if method(i, la_insert=la_insert, la_delete=la_delete, default=default):
						if operation == 'delete':
							i -= 1
						break

			# for all letters: if not in the correct position, correct case
			if i >= len(self.original_word) or self.original_word[i] != self.word[i]:
				if i < len(self.original_word) and self.original_word[i].lower() == self.word[i].lower():
					self.word[i] = self.word[i].upper() if self.original_word[i].isupper() else self.word[i].lower()
				else: # letters not in the correct position, correct case to lower
					self.word[i] = self.word[i].lower()
				
			i += 1
			# end of loop
		if reverse: self.original_word, self.word = self.original_word[::-1], self.word[::-1] # we don't need correct here

	# --- OPERATIONS BEGIN ---
	def do_swap(self, i, **kwargs): # swap, swap -> insert in the middle and double swap
		if (i < len(self.word) - 1 and (self.word[i + 1].lower(), self.word[i].lower()) == (self.correct[i], self.correct[i + 1])) or \
		(self.offset == 1 and self.distance == 1 and i < len(self.word) - 2 and \
		(self.word[i].lower(), self.word[i + 1].lower()) == (self.correct[i + 2], self.correct[i])) or \
		(self.offset == 0 and self.distance == 1 and self.initial_distance == 0 and i < len(self.word) - 2 and \
		(self.word[i].lower(), self.word[i + 1].lower(), self.word[i + 2].lower()) == (self.correct[i + 2], self.correct[i], self.correct[i + 1])): 
			log.warning(f'Swapped {self.word[i], self.word[i + 1]} @ {self.word}')
			self.word[i], self.word[i + 1] = self.correct[i], self.correct[i + 1]
			return True

	def do_insert(self, i, la_insert, default, **kwargs):
		if self.offset == 2 or self.correct[-1:] != ['_'] and not (i == len(self.word) - 1 and self.word[-1:] != ['_']) and \
		(la_insert == 0 or (la_insert <= 2 and self.distance < 2 and la_insert < default)):
			log.warning(f'Inserted {i} @ {self.word}')
			self.word.insert(i, self.correct[i])
			if self.word[-1:] == ['_']: # word was shorter
				self.word.pop() # removes 1x '_' rpadding
			else: # equal
				self.correct.append('_')
			return True

	def do_delete(self, i, la_delete, default, **kwargs):
		if self.offset == -1 and self.initial_distance == 1 and self.distance == 1 and i < len(self.word) - 2 and \
		(self.word[i].lower(), self.word[i + 2].lower()) == (self.correct[i + 1], self.correct[i]):
			log.warning(f'Delete-swap {i + 1} @ {self.word}')
			del self.word[i + 1]
			if self.correct[-1:] == ['_']: # correct was shorter
				self.correct.pop() # removes 1x '_' rpadding
			else: # equal
				self.word.append('_')
			return True
		if self.offset == -2 or self.word[-1:] != ['_'] and not (i == len(self.word) - 1 and self.correct[-1:] != ['_']) and \
		(la_delete == 0 or (la_delete <= 2 and self.distance < 2 and la_delete < default)):
			log.warning(f'Deleted {i} @ {self.word}')
			del self.word[i]
			if self.correct[-1:] == ['_']: # correct was shorter
				self.correct.pop() # removes 1x '_' rpadding
			else: # equal
				self.word.append('_')
			return True

	def do_replace(self, i, **kwargs):
		log.warning(f'Replaced @ {i} with {self.correct[i]}')
		self.word[i] = self.correct[i]
		return True
	# --- OPERATIONS END ---


	def case_correction(self):
		self.word = ''.join(self.word).rstrip('_')
		if self.original_word.isupper():
			if len(self.original_word) > 1:
				self.word = self.word.upper()
			else:
				self.word = self.word.capitalize()
		self.correct = ''.join(self.correct).rstrip('_')

		log.warning(f'{self.word} -> {self.correct}: Distance {self.distance} , true')




# ---------------------------------------------------------------------------- #

def spellchecker(text, word_list):
	words = []
	if re.search(r'[a-zA-Z]', text):
		words = filter(bool, [re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', w) for w in text.split()])

	# build dictionary
	result = {}
	for word in words:
		suggestions = {1: [], 2: []}
		current_word = Excel(word) # PowerPoint
		for correct in word_list:
			distance, corrected = current_word.compare(correct)
			if distance is True:
				suggestions = {1: None, 2: None}
				break
			if distance and len(corrected):
				suggestions[distance].append(corrected)
		if suggestions[1]:
			result[word] = sorted(set(suggestions[1]))
		elif suggestions[2] is not None:
			result[word] = sorted(set(suggestions[2]))
	print(f'Final: {result}')
	return result



# spellchecker("slPell", ['spell'])
spellchecker("Ye", ["eye", "me", "ereht", "rieht"]) 

# test = Excel('nEwnt')
# distance, corrected = test.compare('went') # Expected: ['wEnt']
# print(distance, corrected)