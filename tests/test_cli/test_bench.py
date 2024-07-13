"""
bench
"""
import os
import shutil
import json
from lib import calculate_score
import pytest
from conf import conf

code_path = os.environ.get('GITHUB_WORKSPACE')
pdf_dev_path = conf.conf["pdf_dev_path"]
pdf_res_path = conf.conf["pdf_res_path"]

class TestBench():
    """
    test bench
    """
    def ci_ben(self):
        """
        ci benchmark
        """
        try:
            fr = open(os.path.join(pdf_dev_path, "result.json"), "r", encoding="utf-8")
            lines = fr.readlines()
            last_line = lines[-1].strip()
            last_score = json.loads(last_line)
            print ("last_score:", last_score)
            last_simscore = last_score["average_sim_score"]
            last_editdistance = last_score["average_edit_distance"]
            last_bleu = last_score["average_bleu_score"]
        except IOError:
            print ("result.json not exist")    
        os.system(f"python lib/pre_clean.py --tool_name mineru --download_dir {pdf_dev_path}")
        now_score = get_score()
        print ("now_score:", now_score)
        now_simscore = now_score["average_sim_score"]
        now_editdistance = now_score["average_edit_distance"]
        now_bleu = now_score["average_bleu_score"]
        assert last_simscore <= now_simscore
        assert last_editdistance <= now_editdistance
        assert last_bleu <= now_bleu


def get_score():
    """
    get score
    """
    data_path = os.path.join(pdf_dev_path, "ci")
    score = calculate_score.Scoring(os.path.join(data_path, "result.json"))
    score.calculate_similarity_total("mineru", data_path)
    res = score.summary_scores()
    return res


