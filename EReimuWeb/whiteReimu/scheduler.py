from mahjong.record.reader import from_url

from .models import *
from .tenhou_record_check import *

class Process:
    status = False


def scheduler():
    if Process.status == False:
        # fetch from queue
        Process.status = True
        firstTask = Queue.objects.first()
        if firstTask == None:
            Process.status = False
            return
        try:
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
                loader=FileSystemLoader('templates'),
                autoescape=select_autoescape(['html', 'xml'])
            )
            template = env.get_template("record_checker_template.html")
            for player in planned_players:
                games = [GameAnalysis(str(game), game_reason_list(game, player, record)) for game in record.game_list]

                file_name = "Records/tenhou_record_%s_%s.html" % (log_id_from_url(log_url), player.name)
                with open(file_name, "w+", encoding='utf-8') as result_file:
                    result_file.write(template.render(
                        player=str(player),
                        record=str(record),
                        log_url=log_url,
                        games=games
                    ))

                print("report has been saved to", os.path.abspath(file_name))
        except Exception:
            # exception
            print("ERR")
        finally:
            firstTask.delete()
            Process.status = False
    else:
        pass
