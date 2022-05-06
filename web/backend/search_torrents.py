import log
from pt.searcher import Searcher
from pt.torrent import Torrent
from utils.sqls import insert_search_results, delete_all_search_torrents


def search_medias_for_web(content):
    """
    WEB资源搜索
    :param content: 关键字文本，可以包括 类型、标题、季、集、年份等信息，使用 空格分隔，也支持种子的命名格式
    :return: 查询结果直接插入数据库中，进入WEB页面时查询展示
    """
    key_word, season_num, episode_num, year = Torrent.get_keyword_from_string(content)
    if not key_word:
        log.info("【WEB】检索关键字有误！" % content)
        return
    log.info("【WEB】开始检索 %s ..." % content)
    media_list = Searcher().search_medias(key_word=key_word,
                                          s_num=season_num,
                                          e_num=episode_num,
                                          year=year,
                                          mtype=None,
                                          whole_word=False)
    delete_all_search_torrents()
    if len(media_list) == 0:
        log.info("【WEB】%s 未检索到任何媒体资源" % content)
        return
    else:
        log.info("【WEB】共检索到 %s 个有效资源" % len(media_list))
        # 分组择优
        media_list = Torrent.get_torrents_group_item(media_list)
        log.info("【WEB】分组择优后剩余 %s 个有效资源" % len(media_list))
        # 插入数据库
        for media_item in media_list:
            insert_search_results(media_item)
