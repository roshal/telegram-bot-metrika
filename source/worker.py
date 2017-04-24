def run():
	import asyncio
	import json
	import os
	import requests
	import telepot
	import telepot.loop
	def pre(string):
		return '```\n' + string + '```'
	def dumps(obj, **keywords):
		return json.dumps(**{
			**{
				'obj': obj,
				'indent': 2,
			},
			**keywords,
		})
	def commands():
		class metrika:
			def __init__(self, config):
				self.url = 'https://api-metrika.yandex.ru/stat/v1/data'
				self.params = {
					'oauth_token': config['oauth-token'],
					'direct_client_logins': ','.join(config['direct-client-logins']),
					'ids': ','.join(config['ids']),
					'dimensions': (
						# 'ym:ad:currency',
						# 'ym:ad:directBanner',
						# 'ym:ad:directBannerGroup',
						# 'ym:ad:directConditionType',
						'ym:ad:directOrder',
						'ym:ad:directPhraseOrCond',
						'ym:ad:directPlatform',
						'ym:ad:directPlatformType',
						'ym:ad:directSearchPhrase',
						# 'ym:ad:displayCampaign',
						# 'ym:ad:<attribution>DirectBanner',
						# 'ym:ad:<attribution>DirectOrder',
						# 'ym:ad:<attribution>DirectPhraseOrCond',
						# 'ym:ad:<attribution>DirectSearchPhrase',
						# 'ym:ad:currencyName',
						# 'ym:ad:directBannerName',
						# 'ym:ad:directBannerGroupName',
						# 'ym:ad:directConditionTypeName',
						# 'ym:ad:directOrderName',
						# 'ym:ad:directPhraseOrCondName',
						# 'ym:ad:directPlatformName',
						# 'ym:ad:directPlatformTypeName',
					),
					'metrics': (
						'ym:ad:<currency>AdCost',
						# 'ym:ad:<currency>AdCostPerVisit',
						'ym:ad:clicks',
						# 'ym:ad:goal<goal_id><currency>AdCostPerVisi',
						# 'ym:ad:goal<goal_id><currency>CPA',
						'ym:ad:visits',
						'ym:ad:avgVisitDurationSeconds',
						'ym:ad:bounceRate',
						'ym:ad:pageDepth',
						'ym:ad:users',
					),
					# 'attribution': 'last',
					'currency': 'RUB',
					'date1': 'today',
					'pretty': 1,
				}
			def __call__(self, message, send):
				mapping = json.loads(requests.get(self.url, self.params).text)
				print(dumps(mapping))
				if 'data' in mapping and mapping['data']:
					if 'query' in mapping and 'metrics' in mapping['query']:
						string = ''
						lengths = dict(zip(
							[
								'dimensions',
								'metrics',
							],
							[
								2 + max(len(key) for key in mapping['query']['dimensions']),
								3 + max(len(key) for key in mapping['query']['metrics']),
							],
						))
						for item in mapping['data']:
							for key, value in zip(mapping['query']['dimensions'], item['dimensions']):
								if value:
									string += '{:-<{length}.{length}} {}\n'.format(str(key) + ' ', value['name'], **{
										'length': lengths['dimensions'],
									})
							for key, value in zip(mapping['query']['metrics'], item['metrics']):
								if value:
									string += '- {:-<{length}.{length}}{:->6}.{:8}\n'.format(str(key) + ' ', *(' ' + str(value)).split('.'), **{
										'length': lengths['metrics'],
									})
						for name in [
							'min',
							'max',
							'totals',
						]:
							string += name + '\n'
							for key, value in zip(mapping['query']['metrics'], mapping['totals']):
								if value:
									string += '- {:-<{length}.{length}}{:->6}.{:8}\n'.format(str(key) + ' ', *(' ' + str(value)).split('.'), **{
										'length': lengths['metrics'],
									})
						send(pre(string))
					else:
						send(pre('query is empty'))
				else:
					send(pre('data is empty'))
		class commands:
			def __init__(self):
				self.metrika = metrika({
					'oauth-token': os.environ.get('metrika-token'),
					'direct-client-logins': [
						os.environ.get('metrika-login')
					],
					'ids': [
						os.environ.get('metrika-counter-id'),
					],
				})
			def start(self, message, send):
				send(pre('hello'))
		return commands()
	class sender:
		def __init__(self, bot, *arguments, **keywords):
			self.bot = bot
			self.arguments = arguments
			self.keywords = keywords
		def __call__(self, *arguments, **keywords):
			self.bot.sendMessage(*(self.arguments + arguments), **{
				**self.keywords,
				**keywords,
			})
	class handler:
		def __init__(self, bot, *arguments, **keywords):
			self.bot = bot
			self.arguments = arguments
			self.keywords = keywords
		def __call__(self, message):
			print(dumps(message))
			send = sender(self.bot, message['chat']['id'], **{
				'parse_mode': 'Markdown',
				'reply_to_message_id': message['message_id'],
			})
			if 'text' in message:
				if message['text']:
					if message['text'][0] == '/':
						key = message['text'][1:]
						if key in self.keywords['commands']:
							self.keywords['commands'][key](message, send)
						else:
							send(pre('command not found'))
					else:
						send(''.join(reversed(message['text'])))
			else:
				send(pre(dumps(message)))
	bot = telepot.Bot(os.environ.get('telegram-token'))
	commands = commands()
	loop = asyncio.get_event_loop()
	loop.create_task(telepot.loop.MessageLoop(bot, handler(bot, **{
		'commands': {
			'start': commands.start,
			'metrika': commands.metrika,
		},
	})).run_forever())
	loop.run_forever()
if __name__ == '__main__':
	run()
