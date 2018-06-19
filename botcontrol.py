
import discord
import random

client = discord.Client()

badWords = []
badWordsFile = open("badWordDict.txt", "r")
lines = badWordsFile.read()
for line in lines.split('\n'):
	#print(line)
	badWords.append(line)


@client.event
async def on_message(message):

	#picking the random num for guessing game
	rnum = random.randint(1, 10)

	#list of all the members in the server
	x = message.server.members
	
#this if statement so bot doen't respon to itself
	if message.author == client.user:
		return

#greeting
	if message.content.startswith('!hello'):
		msg = 'Hello {0.author.mention}'.format(message)
		await client.send_message(message.channel, msg)
	
#gets everyone's attention
	elif message.content.startswith('!attention'):
		msg = '@everyone'
		await client.send_message(message.channel, msg)

#returns all the members in the server
	elif message.content.startswith('!members'):
		msg = ''
		for member in x:
			msg += member.name
			msg += "\n"
		await client.send_message(message.channel, msg)

#returns all the commands 
	elif message.content.startswith('!commands') or message.content.startswith('!help'):
		msg = '!hello says hi to me, type !members and I will tell you everyone in the server. Type !guessgame for a fun game. Type !attention to get everyones attention. Also, watch your language or you will be hearing from me.'
		await client.send_message(message.channel, msg)

#guessing game ----------------------------------------------------------------------
	elif message.content.startswith('!guessgame'):
		await client.send_message(message.channel, 'Guess a number between 1 and 10')
		
		def guess_check(m):
			return m.content.isdigit()
		
		guess = await client.wait_for_message(timeout=20.0, author=message.author, check=guess_check)
		answer = random.randint(1, 10)
		if guess is None:
			fmt = 'sorry you took too long. It was '+str(answer)
			await client.send_message(message.channel, fmt)
			return
		if int(guess.content)==answer:
			await client.send_message(message.channel, 'You are right!')
		else:
			await client.send_message(message.channel, 'Sorry it was actually {}'.format(answer))
#end guessing game ---------------------------------------------------------------------

#finding all the bad words ---------------------------------------------------------------------
	for word in message.content.split(' '):
		#print(word + ' ')
		for badword in badWords:
			message.content = message.content.lower()
			if word == badword:
				await client.delete_message(message)
				msg = 'Now now, {0.author.mention}'.format(message)+' you said ' + word + ' and that is not nice'
				await client.send_message(message.channel, msg)
#end finding bad words -------------------------------------------------------------------------

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('Ready to do your bidding')
	print('------')

client.run('your token here')
