import datetime
import glob
import os
import pathlib
from html import escape
from itertools import chain
from json import dumps
import re
import inspect

from jinja2 import Environment, FileSystemLoader

from . import stats as stats_module
from .runners import STATE_STOPPED, STATE_STOPPING, MasterRunner
from .stats import sort_stats, update_stats_history
from .user.inspectuser import get_ratio

PERCENTILES_FOR_HTML_REPORT = [0.50, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0]
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
BUILD_PATH = os.path.join(ROOT_PATH, "webui", "dist")
STATIC_PATH = os.path.join(BUILD_PATH, "assets")
descriptions = {}
split_str = 'api-'

def render_template(file, **kwargs):
    env = Environment(loader=FileSystemLoader(BUILD_PATH), extensions=["jinja2.ext.do"])
    template = env.get_template(file)
    return template.render(**kwargs)

def get_description(environment,stats):
    """
    legth = len(environment.runner.user_classes)
    classes = environment.runner.user_classes
    for class_ in classes:
        methods = [method for method in dir(class_) if callable(getattr(class_, method))]
        for method in methods:
            if method in ['on_start','on_stop','start','stop','wait','wait_time','__init__','__le__', '__lt__',
                          '__ne__', '__new__', '__reduce__', '__str__', '__sizeof__', '__subclasshook__', '__setattr__',
                          '__repr__','__reduce_ex__','context']:
                continue
            description = getattr(class_, method).__doc__ # 直接访问方法的 __doc__ 属性
            if description:
                desc_api  = description.split('/api-')
                if len(desc_api) <=1:
                    continue
                descriptions[desc_api[1]] = desc_api[0]
    """
    for stat in stats:
        api = stat.name.split(split_str)
        if len(api) <= 1:
            continue
        stat.description =descriptions.get(api[1],'')

    return stats

def get_html_report(
    environment,
    show_download_link=True,
    theme="",
):
    stats = environment.runner.stats

    start_ts = stats.start_time
    start_time = datetime.datetime.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M:%S")

    if end_ts := stats.last_request_timestamp:
        end_time = datetime.datetime.fromtimestamp(end_ts).strftime("%Y-%m-%d %H:%M:%S")
    else:
        end_time = start_time

    host = None
    if environment.host:
        host = environment.host
    elif environment.runner.user_classes:
        all_hosts = {l.host for l in environment.runner.user_classes}
        if len(all_hosts) == 1:
            host = list(all_hosts)[0]

    requests_statistics = list(chain(sort_stats(stats.entries), [stats.total]))

    failures_statistics = sort_stats(stats.errors)
    exceptions_statistics = [
        {**exc, "nodes": ", ".join(exc["nodes"])} for exc in environment.runner.exceptions.values()
    ]

    update_stats_history(environment.runner)
    history = stats.history

    static_js = []
    js_files = [os.path.basename(filepath) for filepath in glob.glob(os.path.join(STATIC_PATH, "*.js"))]

    for js_file in js_files:
        path = os.path.join(STATIC_PATH, js_file)
        static_js.append("// " + js_file + "\n")
        with open(path, encoding="utf8") as f:
            static_js.append(f.read())
        static_js.extend(["", ""])

    is_distributed = isinstance(environment.runner, MasterRunner)
    user_spawned = (
        environment.runner.reported_user_classes_count if is_distributed else environment.runner.user_classes_count
    )

    if environment.runner.state in [STATE_STOPPED, STATE_STOPPING]:
        user_spawned = environment.runner.final_user_classes_count

    task_data = {
        "per_class": get_ratio(environment.user_classes, user_spawned, False),
        "total": get_ratio(environment.user_classes, user_spawned, True),
    }

    requests_statistics = get_description(environment, requests_statistics)



    return render_template(
        "report.html",
        template_args={
            "is_report": True,

            "requests_statistics": [stat.to_dict(escape_string_values=True) for stat in requests_statistics],
            "failures_statistics": [stat.to_dict() for stat in failures_statistics],
            "exceptions_statistics": [stat for stat in exceptions_statistics],
            "response_time_statistics": [
                {
                    "name": escape(stat.name),
                    "method": escape(stat.method or ""),
                    "description": escape(stat.description or ""),
                    **{
                        str(percentile): stat.get_response_time_percentile(percentile)
                        for percentile in PERCENTILES_FOR_HTML_REPORT
                    },
                }
                for stat in requests_statistics
            ],
            "start_time": start_time,
            "end_time": end_time,
            "host": escape(str(host)),
            "history": history,
            "show_download_link": show_download_link,
            "locustfile": escape(str(environment.locustfile)),
            "tasks": task_data,
            "percentiles_to_chart": stats_module.PERCENTILES_TO_CHART,
        },
        theme=theme,
        static_js="\n".join(static_js),
    )
