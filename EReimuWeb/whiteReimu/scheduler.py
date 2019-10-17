import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from .models import *
from .tenhou_record_check import *


class stat:
    averageTime = 90
    qNum = 10


logging.basicConfig(filename='info.log', level=logging.WARNING, format='%(asctime)s %(message)s')
scheduler1 = BackgroundScheduler()
scheduler1.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler1, "interval", seconds=10)
def scheduler():
    firstTask = Queue.objects.first()
    if firstTask == None:
        return
    try:
        startTime = time.time()
        log_url = firstTask.log_url
        name = firstTask.player_name
        record = from_url(log_url, 10)
        planned_players = record.players.copy()
        if name.strip():
            player = next((x for x in record.players if x.name == name), None)
            if player is None:
                raise ValueError("Player '%s' not found in record %s." % (name, record))
            planned_players = [player]
        env = Environment(
            loader=FileSystemLoader('whiteReimu/templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template("record_checker_template.html")
        for player in planned_players:
            games = [GameAnalysis(str(game), game_reason_list(game, player, record)) for game in record.game_list]

            file_name = "whiteReimu/Records/tenhou_record_%s_%s.html" % (log_id_from_url(log_url), player.name)
            with open(file_name, "w+", encoding='utf-8') as result_file:
                result_file.write(template.render(
                    player=str(player),
                    record=str(record),
                    log_url=log_url,
                    games=games
                ))
            a = MahjongRecord(log_url=log_url, player_name=name,
                              save_url="tenhou_record_%s_%s.html" % (log_id_from_url(log_url), player.name))
            a.save()
            logging.warning("Report of record %s username %s generated.", log_url, name)

    except Exception as e:
        # exception
        a = Fails(log_url=log_url, player_name=name)
        a.save()
        logging.error("Report of record %s username %s failed.%s", log_url, name,str(e))
    finally:
        firstTask.delete()
        processTime = time.time() - startTime
        stat.averageTime = (stat.averageTime * stat.qNum + processTime) / (stat.qNum + 1)


register_events(scheduler1)

scheduler1.start()
