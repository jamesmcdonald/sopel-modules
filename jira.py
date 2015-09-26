from sopel import module
from sopel.formatting import color, bold
import requests
import pprint
from re import findall
import os

"""Snarf ticket information from Jira"""

@module.rule('.*[A-Z]+-[0-9]+.*')
def getticket(bot, trigger):
    """Look up tickets in Jira and display their information"""
    if not hasattr(bot.config, 'jira'):
        bot.say("I don't seem to have a 'jira' section in my config!")
        return
    user = bot.config.jira.user
    password = bot.config.jira.password
    url = bot.config.jira.url

    if user is None or password is None or url is None:
        bot.say('You need to set user, password and url in the jira section of the config')
        return

    for issue in findall('[A-Z]+-[0-9]+', trigger):
        r = requests.get(
            os.path.join(url, 'rest/api/2/issue', issue),
            auth=(user, password))
        if r.status_code != 200: return
        j = r.json()
        bot.say("({} {}) {} [ {} ] {} {}".format(
            j['fields']['issuetype']['name'],
            j['key'],
            j['fields']['summary'],
            color((j['fields']['assignee']['displayName'] if j['fields']['assignee'] else 'Unassigned'), 'BLUE'),
            bold(color(j['fields']['status']['name'], 'GREEN')),
            os.path.join(url, 'browse', j['key'])))
