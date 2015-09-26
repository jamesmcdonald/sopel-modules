from sopel import module
from datetime import datetime
import os
import codecs
"""Log work done in log files.

This provides a simple way to allow users on a channel to
log work in progress. The logs should be served by a
web server on the configured URL.

Log files are stored in directories like:
  <channel>/<year>

With filenames like:
  <channel>-<year>-<month>.log

The log entries are of the format:
  <timestamp> <nick>: <message>
"""

@module.require_chanmsg('Log your work in a channel!')
@module.rule('@wl.*')
@module.commands('wl')
@module.example('.wl I did some awesome stuff')
def worklog(bot, trigger):
    "Log work done to a log file, which will be served by a webserver"
    worklog_path = bot.config.worklog.worklog_path
    worklog_baseurl = bot.config.worklog.worklog_baseurl

    now = datetime.utcnow()
    logpath = os.path.join(worklog_path, trigger.sender, str(now.year))
    logfilename = '{}-{:04}-{:02}.log'.format(trigger.sender, now.year, now.month)
    logurl = os.path.join(worklog_baseurl, trigger.sender.replace('#', '%23'), str(now.year)) + '/'

    if trigger == '@wl' or trigger == '.wl':
        bot.reply('Worklog messages are logged to {}'.format(logurl))
        return
    msg = trigger.replace('@wl ', '')
    msg = trigger.replace('.wl ', '')
    if msg == '':
        bot.reply('You want me to log that you didn\'t do anything, lazybones?')
        return

    if not os.path.isdir(logpath):
        try:
            os.makedirs(logpath)
        except Exception as e:
            bot.say("Can't create worklog directory {}!".format(logpath))
            raise
            return
    logfile = codecs.open(os.path.join(logpath,logfilename), 'a', encoding='utf-8')
    logfile.write('{} {}: {}\n'.format(
        now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        trigger.nick,
        msg))
    logfile.close()
    bot.reply("Your glorious efforts are logged to {}".format(os.path.join(logurl,logfilename.replace('#', '%23'))))
